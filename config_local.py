"""
Local Test Configuration
Docker SQL Server için özel ayarlar
"""
import os

# .env yerine doğrudan ayarlar (test için)
os.environ['DB_SERVER'] = 'localhost,1433'
os.environ['DB_LOGO'] = 'GOLD'
os.environ['DB_FAYS'] = 'FaysWMSAkturk'
os.environ['DB_USER'] = 'sa'
os.environ['DB_PASSWORD'] = 'E123456.'
os.environ['DB_DRIVER'] = 'ODBC Driver 17 for SQL Server'
os.environ['APP_TITLE'] = 'LOGO - FAYS WMS Stok Eşitleme (TEST)'
os.environ['DEFAULT_WAREHOUSE'] = 'MERKEZ'
os.environ['LOG_LEVEL'] = 'INFO'

print("✅ Test konfigürasyonu yüklendi - Docker SQL Server (localhost:1433)")

