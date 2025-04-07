import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Constant key (derived from "we3p2v5t85" using MD5)
PASSWORD = "we3p2v5t85"
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
        
        # Write IV + ciphertext to output file
        with open(output_file, 'wb') as f:
            f.write(iv + ciphertext)  # IV first, then ciphertext
        
        print(f"[+] File encrypted successfully: {output_file}")
        print(f"[+] IV (hex): {iv.hex()}")
        return True
    
    except Exception as e:
        print(f"[!] Encryption failed: {e}")
        return False

if __name__ == "__main__":
    encrypt_file("service_probes.exe", "service_probes.aes")