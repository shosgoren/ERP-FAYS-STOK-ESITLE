@echo off
REM ============================================================================
REM LOGO - FAYS WMS Stok Esitleme - Otomatik Kurulum ve Calistirma
REM ============================================================================

color 0A
title LOGO - FAYS WMS Stok Esitleme - Kurulum

echo.
echo ============================================================================
echo   LOGO - FAYS WMS STOK ESITLEME PROGRAMI
echo   Otomatik Kurulum ve Calistirma
echo ============================================================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python bulundu!
    goto :install_packages
) else (
    echo [UYARI] Python bulunamadi!
    echo.
    echo Simdi WinPython indirilecek ve kullanilacak...
    goto :download_winpython
)

:download_winpython
echo.
echo ============================================================================
echo WinPython Portable Python indiriliyor...
echo ============================================================================
echo.
echo Lutfen WinPython'u manuel indirin:
echo https://winpython.github.io/
echo.
echo Indirdikten sonra bu klasore cikartip tekrar calistirin.
echo.
pause
exit /b 1

:install_packages
echo.
echo ============================================================================
echo Paketler yukleniyor...
echo ============================================================================
echo.
pip install customtkinter pyodbc pandas openpyxl Pillow python-dotenv tkcalendar
if %errorlevel% neq 0 (
    echo [HATA] Paket yuklemesi basarisiz!
    pause
    exit /b 1
)

echo.
echo [OK] Paketler yuklendi!

:check_env
echo.
echo ============================================================================
echo Yapilandirma kontrol ediliyor...
echo ============================================================================
echo.

if exist .env (
    echo [OK] .env dosyasi bulundu!
) else (
    echo [UYARI] .env dosyasi bulunamadi!
    echo.
    echo env_example.txt dosyasini .env olarak kopyalayin ve duzenleyin.
    echo.
    echo Orneg:
    echo   DB_SERVER=localhost,1433
    echo   DB_USER=sa
    echo   DB_PASSWORD=yourpassword
    echo.
    pause
)

:run_program
echo.
echo ============================================================================
echo Program baslatiliyor...
echo ============================================================================
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Program baslatilirken hata olustu!
    echo.
    echo Demo versiyonu denemek ister misiniz?
    choice /C YN /M "Demo versiyonu calistir"
    if %errorlevel% == 1 (
        python demo_app.py
    )
)

echo.
echo Program kapatildi.
pause

