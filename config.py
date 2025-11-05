"""
Konfigürasyon Yönetimi
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Config:
    """Uygulama konfigürasyon sınıfı"""
    
    # Veritabanı Bağlantı Bilgileri
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_LOGO = os.getenv('DB_LOGO', 'GOLD')
    DB_FAYS = os.getenv('DB_FAYS', 'FaysWMSAkturk')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    # Uygulama Ayarları
    APP_TITLE = os.getenv('APP_TITLE', 'LOGO - FAYS WMS Stok Eşitleme')
    DEFAULT_WAREHOUSE = os.getenv('DEFAULT_WAREHOUSE', 'MERKEZ')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Fiş Türleri
    FIS_SAYIM_FAZLASI = 50  # Sayım Fazlası (GirisCikis=1)
    FIS_SAYIM_EKSIGI = 51   # Sayım Eksiği (GirisCikis=2)
    
    # yr_BilgiLines Link Numarası
    FISNO_LINK_NUMARASI = 99102
    
    @staticmethod
    def get_connection_string(database='FAYS'):
        """Veritabanı bağlantı string'i oluştur"""
        db_name = Config.DB_FAYS if database == 'FAYS' else Config.DB_LOGO
        
        conn_str = (
            f"DRIVER={{{Config.DB_DRIVER}}};"
            f"SERVER={Config.DB_SERVER};"
            f"DATABASE={db_name};"
            f"UID={Config.DB_USER};"
            f"PWD={Config.DB_PASSWORD};"
            "TrustServerCertificate=yes;"
        )
        return conn_str
    
    @staticmethod
    def save_to_env(key, value):
        """Ayarları .env dosyasına kaydet"""
        env_path = '.env'
        
        # Mevcut .env dosyasını oku
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Key'i bul ve güncelle veya ekle
        found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                found = True
                break
        
        if not found:
            lines.append(f"{key}={value}\n")
        
        # Dosyaya yaz
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

