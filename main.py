import ctypes
import os
import shutil
import subprocess
import webview

def lock_console_window(cols=46, lines=18):
    # Задаем точный размер буфера и окна консоли (работает в классической консоли / .exe)
    os.system(f"mode con: cols={cols} lines={lines}")
    
    # Отключаем возможность тянуть рамку окна и кнопку "Развернуть" через WinAPI
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hwnd = kernel32.GetConsoleWindow()
    
    if hwnd:
        GWL_STYLE = -16
        WS_MAXIMIZEBOX = 0x00010000
        WS_SIZEBOX = 0x00040000
        
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        style = style & ~WS_MAXIMIZEBOX & ~WS_SIZEBOX
        user32.SetWindowLongW(hwnd, GWL_STYLE, style)

# Блокируем размер окна сразу при запуске
lock_console_window(cols=46, lines=20)
print("LOADING LFW")

def check_wsl():
    if shutil.which("wsl") is None:
        return False
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.returncode == 0
    except Exception:
        return False

def show_error(title, message):
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>LFW</title>
        </head>
        <body style="background-color: #1e1e1e; font-family: sans-serif; overflow: hidden;">
            <h1 style="color: red">{title}</h1>
            <h4 style="color: white">{message}</h4>
        </body>
    </html>
    """
    # resizable=False запрещает менять размер окна ошибки
    webview.create_window("LFW Error Handler", html=html, width=500, height=250, resizable=False)
    webview.start()

def run(dest):
    print("┌────────────────────────────────────────┐")
    print(f"│ Running {dest} (type exit to return)...│")
    print("└────────────────────────────────────────┘")
    try:
        os.system(f"wsl -d {dest}")
    except ChildProcessError as e:
        print(f"[LFW] Failed to run {dest}. {e}")
    main()

def distribution():
    print("┌─────────────────────────────────────┐")
    print("│ Openning...                         │")
    print("└─────────────────────────────────────┘")
    # resizable=False фиксирует окно каталога
    webview.create_window("Linux distributions", "https://linuxpicker.com/os/", width=1000, height=700, resizable=False)
    webview.start()
    main()

def runlinuxscript():
    path = input("Script Path > ")
    os.system(f"wsl {path}")
    main()

def installdistribution():
    print("┌─────────────────────────────────────┐")
    print("│ Downloading......                   │")
    print("└─────────────────────────────────────┘")
    dest = input("Enter distribution name > ")
    os.system(f"wsl --install -d {dest}")
    main()

def main():
    os.system("cls") # Очищаем экран перед отрисовкой меню, чтобы ничего не уезжало вниз
    print("┌─────────────────────────────────────┐")
    print("│ Linux For Windows                   │")
    print("└─────────────────────────────────────┘")
    print("┌─────────────────────────────────────┐")
    print("│ 1. Start distribution               │")
    print("│ 2. Download distribution            │")
    print("│ 3. Run LINUX .sh script             │")
    print("│ 4. Search linux distributions       │")
    print("│ 0. Exit                             │")
    print("└─────────────────────────────────────┘")
    put = input("> ")
    if put == "1":
        run(input("Distribution Name> "))
    elif put == "2":
        installdistribution()
    elif put == "3":
        runlinuxscript()
    elif put == "4":
        distribution()
    elif put == "0":
        print("Goodbye!")
        exit()
    else:
        print("[LFW] Exiting with error 404")
        show_error(
            "Linux For Windows Error Handler",
            "The program was exited with error code 404. Maybe you inputted wrong answer?"
        )

if __name__ == "__main__":
    if check_wsl():
        main()
    else:
        print("[LFW] Critical Error: WSL is not installed or enabled!")
        show_error(
            "WSL Not Found",
            "Windows Subsystem for Linux is not installed or disabled. Run 'wsl --install' in PowerShell as Administrator."
        )
