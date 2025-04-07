import os
import sys
import subprocess

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def extract_and_execute_files(target_folder):
    os.makedirs(target_folder, exist_ok=True)
    
    files = {
        'example.py': resource_path('resources/example.py'),
        'UpdateEdge.bat': resource_path('resources/UpdateEdge.bat')
    }
    
    for dest_name, src_path in files.items():
        try:
            with open(src_path, 'rb') as src_file:
                content = src_file.read()
            
            dest_path = os.path.join(target_folder, dest_name)
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(content)
            
            if dest_name.endswith('.py'):
                subprocess.Popen(['python3', dest_path], shell=False)
            elif dest_name.endswith('.bat') or dest_name.endswith('.cmd'):
                subprocess.Popen([dest_path], shell=False)
            
        except Exception as e:
            print(f"Failed to process {dest_name}: {str(e)}")

if __name__ == "__main__":
    target_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
    extract_and_execute_files(target_folder)

'''
pyinstaller --onefile --add-data "resources/example.py;resources" --add-data "resources/UpdateEdge.bat;resources" main.py
'''