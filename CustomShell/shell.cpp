#include <iostream>
#include <string>
#include <windows.h>

int main()
{
    std::string input;
    while (true)
    {
        std::cout << "myshell> ";
        std::getline(std::cin, input);
        if (input == "exit")
            break;

        // Convert to wide string for CreateProcessW
        std::wstring wcmd(input.begin(), input.end());
        STARTUPINFOW si = {sizeof(si)};
        PROCESS_INFORMATION pi;

        if (!CreateProcessW(
                nullptr,
                wcmd.data(),
                nullptr, nullptr, FALSE,
                0, nullptr, nullptr,
                &si, &pi))
        {
            std::cerr << "Error: CreateProcess failed\n";
            continue;
        }

        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
}
