Set "VIRTUAL_ENV=aact_venv"

If Not Exist "%VIRTUAL_ENV%\Scripts\activate.bat" (
    python3.11 -m venv %VIRTUAL_ENV%
    Call "%VIRTUAL_ENV%\Scripts\activate.bat"
    pip.exe install -r requirements.txt
) else (Call "%VIRTUAL_ENV%\Scripts\activate.bat")

python3.11 "code\aact.py"

Pause
