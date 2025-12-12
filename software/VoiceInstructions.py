import platform
import subprocess

# Only import win32com on Windows
if platform.system() == "Windows":
    from win32com.client import Dispatch

def speak(text):
    """
    Cross-platform TTS function:
    - Windows: SAPI.SpVoice
    - macOS: 'say' command
    """
    system_platform = platform.system()

    if system_platform == "Windows":
        try:
            voice = Dispatch("SAPI.SpVoice")
            voice.Speak(text)
        except Exception as e:
            print(f"TTS error on Windows: {e}")

    elif system_platform == "Darwin":  # macOS
        try:
            subprocess.call(["say", text])
        except Exception as e:
            print(f"TTS error on macOS: {e}")

    else:
        # Fallback for Linux or unsupported systems
        print(f"TTS not supported on {system_platform}. Message: {text}")

