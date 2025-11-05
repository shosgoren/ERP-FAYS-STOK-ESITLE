"""
Standalone EXE Oluşturma Script'i
PyInstaller ile tek dosya .exe oluşturur
"""
import os
import sys

print("""
╔══════════════════════════════════════════════════════════════╗
║  LOGO - FAYS WMS Stok Eşitleme - EXE Builder                ║
╚══════════════════════════════════════════════════════════════╝

Bu script, programı standalone .exe dosyasına dönüştürür.
Windows Server'da Python kurulumu gerekmeden çalışır!

ADIMLAR:
1. PyInstaller kurulumu (macOS'ta veya Windows'ta)
2. EXE oluşturma
3. Windows Server'a kopyalama

""")

# PyInstaller spec dosyası oluştur
spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'customtkinter',
        'pyodbc',
        'pandas',
        'openpyxl',
        'PIL',
        'dotenv',
        'tkcalendar',
        'babel.numbers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StokEsitleme',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI modu
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)
"""

with open('StokEsitleme.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)

print("✅ StokEsitleme.spec dosyası oluşturuldu")
print("\nŞimdi EXE oluşturmak için:")
print("\n1. Windows bilgisayarda (veya Wine ile):")
print("   pip install pyinstaller")
print("   pyinstaller StokEsitleme.spec")
print("\n2. dist/StokEsitleme.exe dosyası oluşacak")
print("3. Bu dosyayı Windows Server'a kopyalayın")
print("\n4. .env dosyasını da StokEsitleme.exe ile aynı klasöre koyun")
print("\n5. Çift tıklayarak çalıştırın!")

