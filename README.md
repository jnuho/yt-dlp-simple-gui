
# yt-dlp on Windows

- [install uv](#install-uv)
- [install ffmpeg using chocolatey](#install-ffmpeg-using-chocolatey)
- [powersehll]
    - [Activate virtual environment when opening powershell](#activate-virtual-environment-when-opening-powershell)
    - [install requirements.txt](#install-requirements.txt)
    - [Create executable](#create-executable)


## install uv

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
cd C:\Users\user\Downloads
uv venv .venv --python 3.10
```

## install ffmpeg using chocolatey

```bash
# First install Chocolatey if you haven't already
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install FFmpeg
choco install ffmpeg
```

## powershell

### Activate virtual environment when opening powershell
    - https://serverfault.com/a/31202
    - https://www.hanselman.com/blog/signing-powershell-scripts
    - https://learn.microsoft.com/ko-kr/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5


- Set ExecutionPolicy for profile
    - to allow Profile script on powershell startup

```bash
Set-ExecutionPolicy Unrestricted
```

- Edit profile

```bash
echo $PROFILE
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }; notepad $PROFILE
```

```bash
# Activate virtual environment safely
$venvPath = "C:\Users\$env:USERNAME\Downloads\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found: $venvPath" -ForegroundColor Red
}

function venv { & $venvPath }

function run { & python "C:\Users\$env:USERNAME\Downloads\yt-dlp-simple-gui\pyqt.py" }
```

 ### install requirements.txt

```bash
# uv pip install yt-dlp --upgrade
# uv pip install PyQt6 --upgrade
uv pip install -r requirements.txt
```

- requirements.txt

```
pyqt6>=6.8.1
pyqt6-qt6>=6.8.2
pyqt6-sip>=13.10.0
yt-dlp>=2025.3.27
```

- Write pyqt gui

- Create executable

```bash
```
