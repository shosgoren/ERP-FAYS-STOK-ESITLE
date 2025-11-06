"""
Şifreli Konfigürasyon Yönetimi
Bağlantı bilgilerini şifreli olarak saklar
"""
import os
import json
import base64
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None
    PBKDF2HMAC = None
    hashes = None
    default_backend = None

class SecureConfig:
    """Şifreli konfigürasyon yöneticisi"""
    
    CONFIG_FILE = "connection.dat"  # Şifreli dosya
    
    # Sabit salt (gerçek uygulamada bu da şifrelenmiş olmalı)
    _SALT = b'StokEsitleme2025_SecureConfig_Salt_V1'
    
    @staticmethod
    def _get_key():
        """Şifreleme anahtarı oluştur"""
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ImportError("cryptography kütüphanesi yüklü değil!")
        
        # Makine bazlı benzersiz anahtar oluştur
        machine_id = os.environ.get('COMPUTERNAME', 'DEFAULT') + os.environ.get('USERNAME', 'USER')
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SecureConfig._SALT,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        return key
    
    @staticmethod
    def save_config(config_data):
        """
        Konfigürasyonu şifreli olarak kaydet
        
        Args:
            config_data (dict): {
                'DB_SERVER': '...',
                'DB_LOGO': '...',
                'DB_FAYS': '...',
                'DB_USER': '...',
                'DB_PASSWORD': '...',
                'DB_DRIVER': '...',
                'DEFAULT_WAREHOUSE': '...'
            }
        """
        try:
            if not CRYPTOGRAPHY_AVAILABLE:
                return False, "cryptography kütüphanesi yüklü değil!"
            
            # JSON'a dönüştür
            json_data = json.dumps(config_data)
            
            # Şifrele
            key = SecureConfig._get_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(json_data.encode())
            
            # Dosyaya kaydet
            config_path = Path(SecureConfig.CONFIG_FILE)
            config_path.write_bytes(encrypted_data)
            
            return True, "Bağlantı bilgileri güvenli olarak kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"
    
    @staticmethod
    def load_config():
        """
        Şifreli konfigürasyonu yükle
        
        Returns:
            tuple: (success, data_or_error_message)
        """
        try:
            if not CRYPTOGRAPHY_AVAILABLE:
                return False, "cryptography kütüphanesi yüklü değil!"
            
            config_path = Path(SecureConfig.CONFIG_FILE)
            
            if not config_path.exists():
                return False, "Kaydedilmiş bağlantı bilgisi bulunamadı."
            
            # Dosyadan oku
            encrypted_data = config_path.read_bytes()
            
            # Şifre çöz
            key = SecureConfig._get_key()
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # JSON'dan dönüştür
            config_data = json.loads(decrypted_data.decode())
            
            return True, config_data
        except Exception as e:
            return False, f"Yükleme hatası: {str(e)}"
    
    @staticmethod
    def config_exists():
        """Kaydedilmiş konfigürasyon var mı?"""
        return Path(SecureConfig.CONFIG_FILE).exists()
    
    @staticmethod
    def delete_config():
        """Kaydedilmiş konfigürasyonu sil"""
        try:
            config_path = Path(SecureConfig.CONFIG_FILE)
            if config_path.exists():
                config_path.unlink()
            return True, "Kaydedilmiş bağlantı bilgileri silindi."
        except Exception as e:
            return False, f"Silme hatası: {str(e)}"

