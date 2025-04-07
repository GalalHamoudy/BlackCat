import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Constant key (derived from "tiqny2q2je" using MD5)
PASSWORD = "tiqny2q2je"
KEY = hashlib.md5(PASSWORD.encode()).digest()  # 16-byte AES-128 key

def encrypt_file(input_file, output_file):
    # Generate random IV (16 bytes)
    iv = os.urandom(16)
    
    # Create AES cipher
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    
    try:
        # Read plaintext file
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        # Pad and encrypt data
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        # Combine IV and ciphertext, then encode in Base64
        iv_ciphertext = iv + ciphertext
        base64_data = base64.b64encode(iv_ciphertext).decode('utf-8')
        
        # Write Base64 data to output file
        with open(output_file, 'w') as f:
            f.write(base64_data)
        
        print(f"[+] File encrypted successfully: {output_file}")
        print(f"[+] IV (hex): {iv.hex()}")
        return True
    
    except Exception as e:
        print(f"[!] Encryption failed: {e}")
        return False

if __name__ == "__main__":
    encrypt_file("shell4.py", "shell4.txt")