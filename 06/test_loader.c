#include <windows.h>
#include <stdio.h>

int main() {
    HMODULE hDll = LoadLibraryA("python311.dll");
    if (!hDll) {
        printf("Failed to load DLL\n");
        return 1;
    }

    // Get the function pointer
    void (*DecryptAndExecute)() = (void(*)())GetProcAddress(hDll, "DecryptAndExecute");
    if (!DecryptAndExecute) {
        printf("Failed to get function\n");
        FreeLibrary(hDll);
        return 1;
    }

    // Call the function
    DecryptAndExecute();

    FreeLibrary(hDll);
    return 0;
}
// gcc test_loader.c -o test_loader.exe