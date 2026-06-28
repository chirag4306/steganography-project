import tkinter as tk
from tkinter import filedialog, messagebox
import stego_engine
import crypto_utils

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-256 Steganography Engine")
        self.root.geometry("500x450")
        self.root.configure(padx=20, pady=20)

        self.selected_image_path = None

        # --- UI Elements ---
        # 1. Image Selection
        tk.Label(root, text="Step 1: Select Cover Image (PNG/BMP)", font=("Helvetica", 10, "bold")).pack(anchor="w")
        
        self.btn_select = tk.Button(root, text="Browse Image", command=self.select_image)
        self.btn_select.pack(fill="x", pady=5)
        
        self.lbl_image = tk.Label(root, text="No image selected", fg="gray")
        self.lbl_image.pack(anchor="w", pady=10)

        # 2. Secret Message Input
        tk.Label(root, text="Step 2: Secret Message", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.txt_message = tk.Text(root, height=5, width=50)
        self.txt_message.pack(pady=5)

        # 3. Password Input
        tk.Label(root, text="Step 3: AES Encryption Password", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.ent_password = tk.Entry(root, show="*", width=30) # show="*" hides the password typing
        self.ent_password.pack(anchor="w", pady=5)

        # 4. Action Buttons
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(fill="x", pady=20)

        self.btn_hide = tk.Button(frame_buttons, text="Encrypt & Hide", bg="lightblue", command=self.hide_process)
        self.btn_hide.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_extract = tk.Button(frame_buttons, text="Extract & Decrypt", bg="lightgreen", command=self.extract_process)
        self.btn_extract.pack(side="right", expand=True, fill="x", padx=5)

    def select_image(self):
        # Only allow lossless formats
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp")])
        if filepath:
            self.selected_image_path = filepath
            self.lbl_image.config(text=filepath, fg="black")

    def hide_process(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        password = self.ent_password.get()
        message = self.txt_message.get("1.0", tk.END).strip()
        
        if not password or not message:
            messagebox.showerror("Error", "Password and Message cannot be empty!")
            return

        try:
            # Ask user where to save the new image
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if not save_path: return # User cancelled save

            # Execute the engine
            encrypted_bytes = crypto_utils.encrypt_payload(password, message)
            stego_engine.hide_data(self.selected_image_path, encrypted_bytes, save_path)
            
            messagebox.showinfo("Success", f"Data encrypted and hidden successfully!\nSaved to: {save_path}")
            self.txt_message.delete("1.0", tk.END) # Clear text box for security
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def extract_process(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select the image containing the hidden data!")
            return
            
        password = self.ent_password.get()
        if not password:
            messagebox.showerror("Error", "Password is required for decryption!")
            return

        try:
            # Execute the extraction
            extracted_bytes = stego_engine.extract_data(self.selected_image_path)
            decrypted_message = crypto_utils.decrypt_payload(password, extracted_bytes)
            
            # Show the secret message in the text box
            self.txt_message.delete("1.0", tk.END)
            self.txt_message.insert(tk.END, decrypted_message)
            messagebox.showinfo("Success", "Message successfully extracted and decrypted!")
            
        except Exception as e:
            # If the password is wrong, cryptography throws an InvalidTag error
            messagebox.showerror("Decryption Failed", "Failed to decrypt! Incorrect password or corrupted image/data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
