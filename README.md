## Automatic WiFi AP connection changer

This script was created due to the Windows can't connect to the WiFi AP with stronger signal.

# How to use
1. Download the latest version of this package from GitHub

        git clone https://github.com/google/android 
2. Create venv (optionally)

        python -m venv venv
        ./venv/Scripts/activate.ps1 
2. Install requirements:

        pip install -r requirements.txt
3. Change configuration in settings.py to your own settings
4. Make executable file via pyinstaller

        pyinstall --path $FULL_PATH_TO_SERVICE_PY_FILE main.py --onefile
5. Install it as service
        ./build/main.exe