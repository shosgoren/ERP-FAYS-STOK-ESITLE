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
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sol menü paneli
        self.create_sidebar()
        
        # Ana içerik alanı - Tab View
        self.tabview = ctk.CTkTabview(self, width=1000)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
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
    
    def create_sidebar(self):
        """Sol menü panelini oluştur"""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Başlık
        title_label = ctk.CTkLabel(
            sidebar,
            text="STOK EŞİTLEME\nSİSTEMİ",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Versiyon
        version_label = ctk.CTkLabel(
            sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=12)
        )
        version_label.grid(row=1, column=0, padx=20, pady=(0, 30))
        
        # Durum göstergesi
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="● Bağlantı Yok",
            text_color="red",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=10)
        
        # Hızlı erişim butonları
        ctk.CTkLabel(
            sidebar,
            text="Hızlı İşlemler",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=3, column=0, padx=20, pady=(20, 10))
        
        connect_btn = ctk.CTkButton(
            sidebar,
            text="🔌 Bağlan",
            command=self.quick_connect,
            width=160
        )
        connect_btn.grid(row=4, column=0, padx=20, pady=5)
        
        compare_btn = ctk.CTkButton(
            sidebar,
            text="📊 Karşılaştır",
            command=self.quick_compare,
            width=160
        )
        compare_btn.grid(row=5, column=0, padx=20, pady=5)
        
        sync_btn = ctk.CTkButton(
            sidebar,
            text="🔄 Eşitle",
            command=self.quick_sync,
            width=160,
            fg_color="green",
            hover_color="darkgreen"
        )
        sync_btn.grid(row=6, column=0, padx=20, pady=5)
        
        # Alt bilgi
        info_label = ctk.CTkLabel(
            sidebar,
            text="LOGO ERP ↔ FAYS WMS\nStok Senkronizasyonu",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        info_label.grid(row=9, column=0, padx=20, pady=(0, 20))
    
    def on_connection_changed(self, connected):
        """Bağlantı durumu değiştiğinde çağrılır"""
        if connected:
            self.status_label.configure(
                text="● Bağlı",
                text_color="green"
            )
            logger.info("Veritabanı bağlantısı başarılı")
        else:
            self.status_label.configure(
                text="● Bağlantı Yok",
                text_color="red"
            )
            logger.warning("Veritabanı bağlantısı kesildi")
    
    def quick_connect(self):
        """Hızlı bağlantı"""
        self.tabview.set("Bağlantı")
        self.connection_frame.connect()
    
    def quick_compare(self):
        """Hızlı karşılaştırma"""
        if not self.db_manager.conn_fays or not self.db_manager.conn_logo:
            messagebox.showwarning(
                "Uyarı",
                "Önce veritabanına bağlanmalısınız!"
            )
            self.tabview.set("Bağlantı")
            return
        
        self.tabview.set("Stok Karşılaştırma")
        self.comparison_frame.compare()
    
    def quick_sync(self):
        """Hızlı eşitleme"""
        if not self.db_manager.conn_fays or not self.db_manager.conn_logo:
            messagebox.showwarning(
                "Uyarı",
                "Önce veritabanına bağlanmalısınız!"
            )
            self.tabview.set("Bağlantı")
            return
        
        self.tabview.set("Stok Eşitleme")
    
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

