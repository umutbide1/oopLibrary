import os
import platform

def clear_screen():
    """İşletim sistemine göre terminal ekranını temizler."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')