import streamlit as st
import crypto_utils
import stego_engine
import os

# Web App Header
st.set_page_config(page_title="Steganography Engine", page_icon="🔒")
st.title("AES-256 Steganography Engine 🔒🖼️")
st.markdown("Hide encrypted messages inside images securely.")

tab1, tab2 = st.tabs(["Encrypt & Hide", "Extract & Decrypt"])

# --- TAB 1: HIDE DATA ---
with tab1:
    st.header("Hide a Secret Message")
    cover_image = st.file_uploader("Upload Cover Image (PNG/BMP)", type=['png', 'bmp'], key="cover")
    secret_msg = st.text_area("Secret Message (Payload)")
    password_hide = st.text_input("AES Encryption Password", type="password", key="pass_hide")

    if st.button("Encrypt & Hide"):
        if cover_image and secret_msg and password_hide:
            temp_input = "temp_cover.png"
            temp_output = "temp_secret.png"
            with open(temp_input, "wb") as f:
                f.write(cover_image.getbuffer())

            try:
                encrypted_bytes = crypto_utils.encrypt_payload(password_hide, secret_msg)
                stego_engine.hide_data(temp_input, encrypted_bytes, temp_output)

                with open(temp_output, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Secret Image",
                        data=f,
                        file_name="secret_image.png",
                        mime="image/png"
                    )
                st.success("Data encrypted and hidden successfully! Click the button above to download.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                if os.path.exists(temp_input): os.remove(temp_input)
                if os.path.exists(temp_output): os.remove(temp_output)
        else:
            st.warning("Please fill all fields and upload an image.")

# --- TAB 2: EXTRACT DATA ---
with tab2:
    st.header("Extract a Secret Message")
    stego_image = st.file_uploader("Upload Secret Image (PNG/BMP)", type=['png', 'bmp'], key="stego")
    password_extract = st.text_input("AES Decryption Password", type="password", key="pass_extract")

    if st.button("Extract & Decrypt"):
        if stego_image and password_extract:
            temp_stego = "temp_stego.png"
            with open(temp_stego, "wb") as f:
                f.write(stego_image.getbuffer())

            try:
                extracted_bytes = stego_engine.extract_data(temp_stego)
                decrypted_message = crypto_utils.decrypt_payload(password_extract, extracted_bytes)
                
                st.success("Message Successfully Extracted and Decrypted!")
                st.info(decrypted_message)
            except Exception:
                st.error("Decryption Failed! Incorrect password or corrupted image.")
            finally:
                if os.path.exists(temp_stego): os.remove(temp_stego)
        else:
            st.warning("Please upload the image and enter the password.")
                  
