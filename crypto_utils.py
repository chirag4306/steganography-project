import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a 256-bit (32-byte) key from the user's password.
    Uses PBKDF2 with SHA-256 and 100,000 iterations to prevent brute-force attacks.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_payload(password: str, plaintext: str) -> bytes:
    """
    Encrypts a string using AES-256-GCM.
    Returns a single byte string containing: [Salt (16)] + [IV (12)] + [Ciphertext + Auth Tag]
    """
    # 1. Generate a random 16-byte salt for key derivation
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    # 2. Generate a random 12-byte Initialization Vector (IV) recommended for GCM
    iv = os.urandom(12)
    
    # 3. Initialize the AES-GCM cipher
    aesgcm = AESGCM(key)
    
    # 4. Encrypt the data. GCM automatically appends a 16-byte authentication tag to the end.
    ciphertext = aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)
    
    # 5. Concatenate everything so the decryptor has all the public info it needs
    return salt + iv + ciphertext

def decrypt_payload(password: str, encrypted_data: bytes) -> str:
    """
    Parses the byte string, re-derives the key, and decrypts the payload.
    Will raise an InvalidTag exception if the password is wrong or data was tampered with.
    """
    # 1. Extract the components based on their known byte lengths
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    ciphertext = encrypted_data[28:]
    
    # 2. Re-derive the exact same 32-byte key using the extracted salt
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    
    # 3. Decrypt the data. If the tag fails validation, this throws an error.
    plaintext_bytes = aesgcm.decrypt(iv, ciphertext, None)
    
    return plaintext_bytes.decode('utf-8')

# --- Quick Test Block ---
# This block only runs if you execute this file directly. 
# It won't run when we import these functions into the main steganography engine later.
if __name__ == "__main__":
    print("--- Cryptography Engine Test ---")
    my_password = "SuperSecretPassword123!"
    my_secret_message = "This is a highly confidential payload."
    
    print(f"Original Message: {my_secret_message}")
    
    # Encrypt
    encrypted_bytes = encrypt_payload(my_password, my_secret_message)
    print(f"\nEncrypted (Raw Bytes): {encrypted_bytes}")
    print(f"Total Byte Length to Hide: {len(encrypted_bytes)} bytes")
    
    # Decrypt
    decrypted_message = decrypt_payload(my_password, encrypted_bytes)
    print(f"\nDecrypted Message: {decrypted_message}")
