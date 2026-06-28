from PIL import Image
import crypto_utils
import os

# A unique delimiter to tell the extraction loop where the message ends
DELIMITER = "===END_OF_PAYLOAD==="
DELIMITER_BIN = ''.join(format(ord(char), '08b') for char in DELIMITER)

def bytes_to_binary(data_bytes: bytes) -> str:
    """Converts raw bytes into a continuous string of 0s and 1s."""
    return ''.join(format(byte, '08b') for byte in data_bytes)

def binary_to_bytes(binary_str: str) -> bytes:
    """Converts a string of 0s and 1s back into raw bytes."""
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_segment = binary_str[i:i+8]
        if len(byte_segment) == 8:
            byte_array.append(int(byte_segment, 2))
    return bytes(byte_array)

def hide_data(image_path: str, payload_bytes: bytes, output_path: str):
    """Hides encrypted bytes into the LSB of an image."""
    # 1. Convert payload to binary and add the delimiter
    binary_payload = bytes_to_binary(payload_bytes) + DELIMITER_BIN
    payload_len = len(binary_payload)
    
    # 2. Open image and prepare for pixel manipulation
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    # 3. Check capacity (3 bits per pixel: R, G, B)
    if payload_len > len(pixels) * 3:
        raise ValueError("Image is too small to hold this payload!")
        
    # 4. Inject data into pixels
    new_pixels = []
    bit_idx = 0
    
    for pixel in pixels:
        r, g, b = pixel
        
        # Modify R, G, B channels if we still have bits to hide
        # bitwise AND with 254 (11111110) clears the last bit
        # bitwise OR injects our message bit
        if bit_idx < payload_len:
            r = (r & 254) | int(binary_payload[bit_idx])
            bit_idx += 1
        if bit_idx < payload_len:
            g = (g & 254) | int(binary_payload[bit_idx])
            bit_idx += 1
        if bit_idx < payload_len:
            b = (b & 254) | int(binary_payload[bit_idx])
            bit_idx += 1
            
        new_pixels.append((r, g, b))
        
    # 5. Save the new image (must be PNG to avoid compression loss)
    img.putdata(new_pixels)
    img.save(output_path, "PNG")
    print(f"[+] Success! Encrypted payload hidden in {output_path}")

def extract_data(image_path: str) -> bytes:
    """Extracts hidden binary data from an image's LSB."""
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    binary_extracted = ""
    
    for pixel in pixels:
        r, g, b = pixel
        # Extract the last bit using bitwise AND with 1
        binary_extracted += str(r & 1)
        binary_extracted += str(g & 1)
        binary_extracted += str(b & 1)
        
        # Check if we've found our delimiter yet
        if DELIMITER_BIN in binary_extracted:
            # Stop extracting and cut off the delimiter
            clean_binary = binary_extracted.split(DELIMITER_BIN)[0]
            return binary_to_bytes(clean_binary)
            
    raise ValueError("No hidden data found or delimiter missing!")

# --- Quick Test Block ---
if __name__ == "__main__":
    print("--- Steganography Engine Test ---")
    
    # 1. Create a dummy image for testing (a simple 100x100 red square)
    test_img_path = "test_cover.png"
    output_img_path = "test_secret.png"
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(test_img_path)
    
    # 2. Setup our secret
    password = "StegoPassword321!"
    secret = "Zero-Trust Covert Channel Established."
    print(f"Original text: {secret}")
    
    # 3. Encrypt it using our crypto_utils module
    print("[*] Encrypting payload...")
    encrypted_bytes = crypto_utils.encrypt_payload(password, secret)
    
    # 4. Hide it in the image
    print("[*] Hiding payload in image...")
    hide_data(test_img_path, encrypted_bytes, output_img_path)
    
    # 5. Extract it from the new image
    print("[*] Extracting payload from image...")
    extracted_bytes = extract_data(output_img_path)
    
    # 6. Decrypt it
    print("[*] Decrypting payload...")
    decrypted_text = crypto_utils.decrypt_payload(password, extracted_bytes)
    print(f"\n[+] Extracted and Decrypted text: {decrypted_text}")
    
    # Clean up test files
    if os.path.exists(test_img_path): os.remove(test_img_path)
    if os.path.exists(output_img_path): os.remove(output_img_path)
