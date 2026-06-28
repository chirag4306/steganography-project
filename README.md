# Cryptographically Secured Steganography Engine 🔒🖼️

A Zero-Trust covert communication tool built in Python. This project combines **Advanced Encryption Standard (AES-256-GCM)** with **Least Significant Bit (LSB) Image Steganography** to hide encrypted payloads inside standard PNG/BMP images without perceptually altering the original file.

## ✨ Features
* **Military-Grade Cryptography:** Secures the secret payload using AES-256-GCM and derives keys using PBKDF2 (100,000 iterations of SHA-256) to thwart brute-force attacks.
* **Authenticated Encryption:** The GCM mode generates an authentication tag, ensuring that any tampering with the image or data is instantly detected.
* **LSB Pixel Manipulation:** Modifies only the Least Significant Bits of the RGB color channels, making the hidden data mathematically retrievable but completely invisible to the human eye.
* **Lightweight GUI:** A clean, user-friendly desktop interface built with Python's native Tkinter.

## 🛠️ Technologies Used
* **Language:** Python 3.x
* **Cryptography:** `cryptography` library (hazmat primitives)
* **Image Processing:** `Pillow` (PIL)
* **UI:** `Tkinter`

## 🚀 How to Run the Project

**1. Clone the repository:**
```bash
git clone [https://github.com/chirag4306/steganography-project.git](https://github.com/chirag4306/steganography-project.git)
cd steganography-project

2. Create a virtual environment (Recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt


4. Launch the application:

python3 main_gui.py
