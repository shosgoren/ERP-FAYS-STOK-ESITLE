"""
LOGO - FAYS WMS Stok Eşitleme Programı
Ana Uygulama
"""
import customtkinter as ctk
from tkinter import messagebox
import logging

# Test için config_local'ı yükle (varsa)
try:
    import config_local
except ImportError:
    pass

from config import Config
from database import DatabaseManager
from stock_sync_engine import StockSyncEngine
from ui_components import (
    ConnectionFrame,
    ComparisonFrame,
    SyncFrame,
    QueryEditorFrame,
    SettingsFrame
)

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stok_esitleme.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StockSyncApp(ctk.CTk):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        
        # Tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Pencere ayarları
        self.title(Config.APP_TITLE)
        self.geometry("1400x900")
        
        # Veritabanı yöneticisi
        self.db_manager = DatabaseManager()
        self.sync_engine = StockSyncEngine(self.db_manager)
        
        # UI bileşenlerini oluştur
        self.create_ui()
        
        logger.info("Uygulama başlatıldı")
    
    def create_ui(self):
        """UI bileşenlerini oluştur"""
        
        # Ana container
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Üst başlık çubuğu - FAYS Veritabanı adı
        self.title_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.title_frame.grid_columnconfigure(0, weight=1)
        
        self.db_title_label = ctk.CTkLabel(
            self.title_frame,
            text="FAYS Veritabanı: Bağlantı Yok",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        self.db_title_label.pack(side="left", padx=20, pady=15)
        
        # Ana içerik alanı - Tab View
        self.tabview = ctk.CTkTabview(self, width=1000)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Tab'leri oluştur
        self.tab_connection = self.tabview.add("Bağlantı")
        self.tab_comparison = self.tabview.add("Stok Karşılaştırma")
        self.tab_sync = self.tabview.add("Stok Eşitleme")
        self.tab_query = self.tabview.add("SQL Sorguları")
        self.tab_settings = self.tabview.add("Ayarlar")
        
        # Tab içeriklerini oluştur
        self.connection_frame = ConnectionFrame(
            self.tab_connection, 
            self.db_manager,
            self.on_connection_changed
        )
        
        self.comparison_frame = ComparisonFrame(
            self.tab_comparison,
            self.sync_engine
        )
        
        self.sync_frame = SyncFrame(
            self.tab_sync,
            self.sync_engine
        )
        
        self.query_editor_frame = QueryEditorFrame(
            self.tab_query,
            self.db_manager
        )
        
        self.settings_frame = SettingsFrame(
            self.tab_settings
        )
        
        # Program başladığında otomatik bağlantı yükle
        self.connection_frame.auto_load_connection()
    
    def on_connection_changed(self, connected, db_name=None):
        """Bağlantı durumu değiştiğinde çağrılır"""
        if connected:
            db_display = db_name if db_name else "Bağlı"
            self.db_title_label.configure(
                text=f"FAYS Veritabanı: {db_display}",
                text_color="green"
            )
            logger.info(f"Veritabanı bağlantısı başarılı: {db_display}")
        else:
            self.db_title_label.configure(
                text="FAYS Veritabanı: Bağlantı Yok",
                text_color="gray"
            )
            logger.warning("Veritabanı bağlantısı kesildi")
    
    
    def on_closing(self):
        """Uygulama kapanırken"""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
            self.db_manager.disconnect()
            logger.info("Uygulama kapatıldı")
            self.destroy()


def main():
    """Ana fonksiyon"""
    try:
        app = StockSyncApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        logger.error(f"Uygulama hatası: {e}", exc_info=True)
        messagebox.showerror("Hata", f"Uygulama başlatılamadı:\n{str(e)}")


if __name__ == "__main__":
    main()

