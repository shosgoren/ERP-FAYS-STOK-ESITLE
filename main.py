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
from ui_theme import ModernTheme

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
        
        # Modern tema ayarları
        ModernTheme.apply_theme()
        
        # Pencere ayarları
        self.title(Config.APP_TITLE)
        # Tam ekran açılsın
        self.state("zoomed")  # Windows'ta tam ekran
        # Light tema için arka plan rengi
        self.configure(fg_color=ModernTheme.COLORS['bg_primary'])
        
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
        
        # Üst başlık çubuğu - Modern tasarım (koyu mavi)
        self.title_frame = ModernTheme.create_card(
            self,
            height=70,
            corner_radius=0
        )
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.configure(
            fg_color=ModernTheme.COLORS['header_bg'],
            border_width=0
        )
        
        # Sol tarafta logo/başlık
        header_left = ctk.CTkFrame(self.title_frame, fg_color="transparent")
        header_left.pack(side="left", padx=ModernTheme.SPACING['lg'], pady=ModernTheme.SPACING['md'])
        
        app_title = ctk.CTkLabel(
            header_left,
            text="📦 Stok Eşitleme",
            font=ModernTheme.get_font('h3'),
            text_color=ModernTheme.COLORS['header_text']
        )
        app_title.pack(side="left", padx=(0, ModernTheme.SPACING['lg']))
        
        # Sağ tarafta veritabanı durumu
        header_right = ctk.CTkFrame(self.title_frame, fg_color="transparent")
        header_right.pack(side="right", padx=ModernTheme.SPACING['lg'], pady=ModernTheme.SPACING['md'])
        
        self.status_indicator = ctk.CTkFrame(
            header_right,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=ModernTheme.COLORS['disconnected']
        )
        self.status_indicator.pack(side="left", padx=(0, ModernTheme.SPACING['sm']))
        
        self.db_title_label = ctk.CTkLabel(
            header_right,
            text="Bağlantı Yok",
            font=ModernTheme.get_font('body'),
            text_color=ModernTheme.COLORS['header_text']
        )
        self.db_title_label.pack(side="left")
        
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
                text=f"{db_display}",
                text_color=ModernTheme.COLORS['header_text']
            )
            self.status_indicator.configure(fg_color=ModernTheme.COLORS['connected'])
            logger.info(f"Veritabanı bağlantısı başarılı: {db_display}")
            
            # Bağlantı kurulduğunda depoları otomatik yükle
            try:
                self.sync_frame.auto_load_warehouses()
                self.comparison_frame.load_warehouses(silent=True)  # Sessiz mod - mesaj gösterme
            except Exception as e:
                logger.warning(f"Depolar otomatik yüklenirken hata: {e}", exc_info=True)
        else:
            self.db_title_label.configure(
                text="Bağlantı Yok",
                text_color=ModernTheme.COLORS['header_text']
            )
            self.status_indicator.configure(fg_color=ModernTheme.COLORS['disconnected'])
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

