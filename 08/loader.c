// gcc loader.c -o loader.exe
#include <windows.h>
#include <stdio.h>

int main() {
    HMODULE hDll = LoadLibraryA("python311x.dll");
    if (!hDll) {
        printf("Error loading DLL: %d\n", GetLastError());
        return 1;
    }

    void (*ExecuteInOrder)() = (void(*)())GetProcAddress(hDll, "ExecuteInOrder");
    if (!ExecuteInOrder) {
        printf("Error getting function: %d\n", GetLastError());
        FreeLibrary(hDll);
        return 1;
    }

    printf("Starting batch execution...\n");
    ExecuteInOrder();
    printf("All batches completed!\n");

    FreeLibrary(hDll);
    return 0;
}