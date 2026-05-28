@echo off
cd /d "%~dp0\.."

echo Setting up Wedding Invitation Generator...
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist config.yaml (
  copy config.example.yaml config.yaml
  echo Created config.yaml from the example — please edit it with your details.
)

echo.
echo Setup complete. Double-click scripts\generate.bat or run it from Command Prompt.
