@echo off
REM LOGO - FAYS WMS Stok Eşitleme Programı Başlatıcı
REM Bu dosyayı çift tıklayarak programı başlatabilirsiniz

echo ========================================
echo LOGO - FAYS WMS Stok Esitleme
echo ========================================
echo.
echo Program baslatiliyor...
echo.

REM Mevcut dizine git
cd /d "%~dp0"

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.8 veya uzeri yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Gerekli paketlerin yüklü olup olmadığını kontrol et
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Gerekli paketler yukleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo HATA: Paketler yuklenemedi!
        pause
        exit /b 1
    )
)

REM Programı başlat
python main.py

REM Hata durumunda pencereyi açık tut
if errorlevel 1 (
    echo.
    echo Program hata ile kapandi.
    pause
)

