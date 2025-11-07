"""
UI Bileşenleri
CustomTkinter ile modern arayüz bileşenleri
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import ttk
import pandas as pd
import logging
from datetime import datetime
from config import Config
from config_secure import SecureConfig
from sql_templates import SQLTemplates
from ui_theme import ModernTheme

logger = logging.getLogger(__name__)


class ConnectionFrame(ctk.CTkFrame):
    """Veritabanı bağlantı ekranı"""
    
    def __init__(self, parent, db_manager, on_connection_changed):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        self.db_manager = db_manager
        self.on_connection_changed = on_connection_changed
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur - Modern tasarım"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="Veritabanı Bağlantısı",
            font=ModernTheme.get_font('h2'),
            text_color=ModernTheme.COLORS['text_primary']
        )
        title.pack(pady=(0, ModernTheme.SPACING['xl']))
        
        # Form container - Modern kart
        form_card = ModernTheme.create_card(self)
        form_card.pack(fill="both", expand=True, padx=0, pady=0)
        
        form_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        # Form alanları - Modern tasarım
        fields = [
            ("Server", "server_entry", "örn: server.database.windows.net", Config.DB_SERVER),
            ("Kullanıcı Adı", "username_entry", "Kullanıcı adı", Config.DB_USER),
            ("Şifre", "password_entry", "Şifre", Config.DB_PASSWORD, True),  # Password field
            ("LOGO Veritabanı", "logo_db_entry", "GOLD", Config.DB_LOGO),
            ("FAYS Veritabanı", "fays_db_entry", "FaysWMSAkturk", Config.DB_FAYS),
        ]
        
        for idx, field_info in enumerate(fields):
            label_text = field_info[0]
            attr_name = field_info[1]
            placeholder = field_info[2]
            default_value = field_info[3]
            is_password = len(field_info) > 4 and field_info[4]
            
            # Label
            label = ModernTheme.create_label(
                form_frame,
                label_text,
                size='body',
                color='text_primary'
            )
            label.grid(row=idx, column=0, padx=ModernTheme.SPACING['md'], 
                      pady=ModernTheme.SPACING['md'], sticky="w")
            
            # Entry
            entry = ModernTheme.create_modern_entry(
                form_frame,
                placeholder=placeholder,
                width=500
            )
            if is_password:
                entry.configure(show="*")
            entry.grid(row=idx, column=1, padx=ModernTheme.SPACING['md'], 
                      pady=ModernTheme.SPACING['md'], sticky="ew")
            entry.insert(0, default_value)
            
            setattr(self, attr_name, entry)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Butonlar - Modern tasarım
        button_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_container.grid(row=len(fields), column=0, columnspan=2, 
                             pady=(ModernTheme.SPACING['xl'], ModernTheme.SPACING['md']))
        
        # Ana butonlar
        primary_buttons = ctk.CTkFrame(button_container, fg_color="transparent")
        primary_buttons.pack(fill="x", pady=ModernTheme.SPACING['md'])
        
        self.connect_btn = ModernTheme.create_success_button(
            primary_buttons,
            text="Bağlan",
            command=self.connect,
            width=200
        )
        self.connect_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        self.test_btn = ModernTheme.create_secondary_button(
            primary_buttons,
            text="Test Et",
            command=self.test_connection,
            width=200
        )
        self.test_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        # İkincil butonlar
        secondary_buttons = ctk.CTkFrame(button_container, fg_color="transparent")
        secondary_buttons.pack(fill="x", pady=ModernTheme.SPACING['sm'])
        
        self.save_btn = ModernTheme.create_secondary_button(
            secondary_buttons,
            text="Kaydet",
            command=self.save_secure_config,
            width=200
        )
        self.save_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        self.delete_btn = ModernTheme.create_danger_button(
            secondary_buttons,
            text="Kaydı Sil",
            command=self.delete_secure_config,
            width=200
        )
        self.delete_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        # Durum mesajı - Modern kart (light tema için açık gri)
        self.status_card = ModernTheme.create_card(self)
        self.status_card.pack(fill="x", pady=ModernTheme.SPACING['md'])
        self.status_card.configure(fg_color='#E5E7EB', border_width=0)  # Light tema - açık gri
        
        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="",
            font=ModernTheme.get_font('body'),
            text_color=ModernTheme.COLORS['text_primary']
        )
        self.status_label.pack(padx=ModernTheme.SPACING['lg'], pady=ModernTheme.SPACING['md'])
    
    def connect(self, silent=False):
        """Veritabanına bağlan"""
        try:
            if not silent:
                self.status_label.configure(
                    text="Bağlanıyor...",
                    text_color=ModernTheme.COLORS['loading']
                )
                self.status_card.configure(fg_color='#E5E7EB')  # Light tema için açık gri
                self.update()
            
            # Ayarları güncelle
            Config.DB_SERVER = self.server_entry.get()
            Config.DB_USER = self.username_entry.get()
            Config.DB_PASSWORD = self.password_entry.get()
            Config.DB_LOGO = self.logo_db_entry.get()
            Config.DB_FAYS = self.fays_db_entry.get()
            
            # Bağlan
            success = self.db_manager.connect()
            
            if success:
                # Veritabanı adını al
                db_name = Config.DB_FAYS
                if not silent:
                    self.status_label.configure(
                        text="✓ Bağlantı başarılı!",
                        text_color=ModernTheme.COLORS['success']
                    )
                    self.status_card.configure(fg_color='#E5E7EB')  # Light tema
                self.on_connection_changed(True, db_name)
                if not silent:
                    messagebox.showinfo("Başarılı", "Veritabanı bağlantısı başarıyla kuruldu!")
            else:
                if not silent:
                    self.status_label.configure(
                        text="✗ Bağlantı başarısız!",
                        text_color=ModernTheme.COLORS['danger']
                    )
                    self.status_card.configure(fg_color='#E5E7EB')  # Light tema
                self.on_connection_changed(False)
                if not silent:
                    messagebox.showerror("Hata", "Veritabanına bağlanılamadı!")
                
        except Exception as e:
            if not silent:
                self.status_label.configure(
                    text=f"✗ Hata: {str(e)}",
                    text_color=ModernTheme.COLORS['danger']
                )
                self.status_card.configure(fg_color='#E5E7EB')  # Light tema
            self.on_connection_changed(False)
            if not silent:
                messagebox.showerror("Hata", f"Bağlantı hatası:\n{str(e)}")
    
    def test_connection(self):
        """Bağlantıyı test et"""
        if not self.db_manager.conn_fays or not self.db_manager.conn_logo:
            messagebox.showwarning("Uyarı", "Önce bağlantı kurmalısınız!")
            return
        
        try:
            if self.db_manager.test_connection():
                messagebox.showinfo("Başarılı", "Bağlantı testi başarılı!")
            else:
                messagebox.showerror("Hata", "Bağlantı testi başarısız!")
        except Exception as e:
            messagebox.showerror("Hata", f"Test hatası:\n{str(e)}")
    
    def save_secure_config(self):
        """Bağlantı bilgilerini şifreli olarak kaydet"""
        try:
            config_data = {
                'DB_SERVER': self.server_entry.get(),
                'DB_USER': self.username_entry.get(),
                'DB_PASSWORD': self.password_entry.get(),
                'DB_LOGO': self.logo_db_entry.get(),
                'DB_FAYS': self.fays_db_entry.get(),
            }
            
            success, message = SecureConfig.save_config(config_data)
            
            if success:
                messagebox.showinfo("Başarılı", "Bağlantı bilgileri şifreli olarak kaydedildi!\n\n"
                                               "Bir sonraki açılışta '📂 Kayıtlı Bağlantıyı Yükle' "
                                               "butonuna tıklayarak yükleyebilirsiniz.")
            else:
                messagebox.showerror("Hata", message)
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{str(e)}")
    
    def load_secure_config(self, auto_connect=False):
        """Kaydedilmiş bağlantı bilgilerini yükle"""
        try:
            if not SecureConfig.config_exists():
                if not auto_connect:
                    messagebox.showwarning("Uyarı", "Kaydedilmiş bağlantı bilgisi bulunamadı!")
                return False
            
            success, result = SecureConfig.load_config()
            
            if success:
                # Form alanlarını doldur
                self.server_entry.delete(0, tk.END)
                self.server_entry.insert(0, result.get('DB_SERVER', ''))
                
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, result.get('DB_USER', ''))
                
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, result.get('DB_PASSWORD', ''))
                
                self.logo_db_entry.delete(0, tk.END)
                self.logo_db_entry.insert(0, result.get('DB_LOGO', 'GOLD'))
                
                self.fays_db_entry.delete(0, tk.END)
                self.fays_db_entry.insert(0, result.get('DB_FAYS', 'FaysWMSAkturk'))
                
                if auto_connect:
                    # Otomatik bağlan (sessiz mod - mesaj gösterme)
                    # connect çağrısı auto_load_connection içinde yapılacak
                    return True
                else:
                    messagebox.showinfo("Başarılı", "Bağlantı bilgileri yüklendi!\n"
                                                   "Şimdi 'Bağlan' butonuna tıklayabilirsiniz.")
                    return True
            else:
                if not auto_connect:
                    messagebox.showerror("Hata", result)
                return False
        except Exception as e:
            if not auto_connect:
                messagebox.showerror("Hata", f"Yükleme hatası:\n{str(e)}")
            return False
    
    def auto_load_connection(self):
        """Program başladığında otomatik olarak kayıtlı bağlantıyı yükle ve bağlan"""
        try:
            if SecureConfig.config_exists():
                # Bağlantı bilgilerini yükle
                if self.load_secure_config(auto_connect=True):
                    # Sessiz modda bağlan (mesaj gösterme)
                    self.connect(silent=True)
        except Exception as e:
            logger.warning(f"Otomatik bağlantı yükleme hatası: {e}")
    
    def delete_secure_config(self):
        """Kaydedilmiş bağlantı bilgilerini sil"""
        try:
            if not SecureConfig.config_exists():
                messagebox.showwarning("Uyarı", "Silinecek kayıt bulunamadı!")
                return
            
            response = messagebox.askyesno(
                "Onay",
                "Kaydedilmiş bağlantı bilgilerini silmek istediğinize emin misiniz?"
            )
            
            if response:
                success, message = SecureConfig.delete_config()
                if success:
                    messagebox.showinfo("Başarılı", message)
                else:
                    messagebox.showerror("Hata", message)
        except Exception as e:
            messagebox.showerror("Hata", f"Silme hatası:\n{str(e)}")


class ComparisonFrame(ctk.CTkFrame):
    """Stok karşılaştırma ekranı"""
    
    def __init__(self, parent, sync_engine):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.sync_engine = sync_engine
        self.df_result = None
        self.tree_data = []  # Filtreleme için tüm veriler
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        
        # Üst panel - Filtreler ve butonlar
        top_panel = ctk.CTkFrame(self)
        top_panel.pack(fill="x", padx=10, pady=10)
        
        # Depo seçimi
        ctk.CTkLabel(
            top_panel,
            text="Depo:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.warehouse_combo = ctk.CTkComboBox(
            top_panel,
            values=["Tümü"],
            width=200
        )
        self.warehouse_combo.pack(side="left", padx=10)
        self.warehouse_combo.set("Tümü")
        
        # Karşılaştır butonu
        self.compare_btn = ctk.CTkButton(
            top_panel,
            text="📊 Karşılaştır",
            command=self.compare,
            width=150,
            fg_color="blue",
            hover_color="darkblue"
        )
        self.compare_btn.pack(side="left", padx=20)
        
        # Excel'e aktar butonu
        self.export_btn = ctk.CTkButton(
            top_panel,
            text="📥 Excel'e Aktar",
            command=self.export_to_excel,
            width=150
        )
        self.export_btn.pack(side="left", padx=10)
        
        # Filtreleme paneli
        filter_panel = ctk.CTkFrame(self)
        filter_panel.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            filter_panel,
            text="🔍 Filtrele:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.filter_entry = ctk.CTkEntry(
            filter_panel,
            placeholder_text="Ürün kodu, adı veya diğer alanlarda ara...",
            width=400,
            font=ctk.CTkFont(size=12)
        )
        self.filter_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.filter_entry.bind('<KeyRelease>', self.on_filter_change)
        
        # Filtreyi temizle butonu
        clear_filter_btn = ctk.CTkButton(
            filter_panel,
            text="✖ Temizle",
            command=self.clear_filter,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        clear_filter_btn.pack(side="left", padx=10, pady=10)
        
        # İstatistik paneli
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Henüz karşılaştırma yapılmadı",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack(pady=10)
        
        # Treeview için frame
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar'lar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="extended"
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Grid yerleşimi
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview stilini ayarla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       rowheight=25)
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#1f538d')])
    
    def load_warehouses(self, silent=False):
        """Depoları yükle"""
        try:
            # Bağlantı kontrolü
            if not self.sync_engine.db.conn_fays or not self.sync_engine.db.conn_logo:
                if not silent:
                    messagebox.showwarning("Uyarı", "Önce veritabanına bağlanmalısınız!")
                return
            
            warehouses = self.sync_engine.get_warehouses()
            if warehouses:
                # Mevcut değeri koru
                current_value = self.warehouse_combo.get()
                self.warehouse_combo.configure(values=["Tümü"] + warehouses)
                
                # Eğer mevcut değer listede varsa koru
                if current_value in ["Tümü"] + warehouses:
                    self.warehouse_combo.set(current_value)
                else:
                    self.warehouse_combo.set("Tümü")
                
                if not silent:
                    messagebox.showinfo("Başarılı", f"{len(warehouses)} depo yüklendi")
                logger.info(f"{len(warehouses)} depo yüklendi: {warehouses}")
            else:
                if not silent:
                    messagebox.showwarning("Uyarı", "Depo bulunamadı!")
                logger.warning("Depo listesi boş")
        except Exception as e:
            if not silent:
                messagebox.showerror("Hata", f"Depo listesi yüklenemedi:\n{str(e)}")
            logger.warning(f"Depo listesi yüklenemedi: {e}", exc_info=True)
    
    def compare(self):
        """Stokları karşılaştır"""
        try:
            warehouse = self.warehouse_combo.get()
            if warehouse == "Tümü":
                warehouse = None
            
            self.stats_label.configure(text="Karşılaştırma yapılıyor...")
            self.update()
            
            # Karşılaştırma yap
            self.df_result = self.sync_engine.compare_stocks(warehouse)
            
            # Treeview'i temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if len(self.df_result) == 0:
                self.stats_label.configure(
                    text="✓ Stoklar eşit - Fark yok",
                    text_color="green"
                )
                return
            
            # Sütunları ayarla
            columns = list(self.df_result.columns)
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'
            
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor='center')
            
            # Verileri ekle ve filtreleme için sakla
            self.tree_data = []  # Tüm verileri sakla (filtreleme için)
            for _, row in self.df_result.iterrows():
                values = [row[col] for col in columns]
                self.tree_data.append((values, row))
                
                # Fark durumuna göre renklendirme için tag
                if row['FARK'] > 0:
                    tag = 'fazla'
                else:
                    tag = 'eksik'
                
                self.tree.insert('', 'end', values=values, tags=(tag,))
            
            # Tag renkleri
            self.tree.tag_configure('fazla', background='#4a0000')  # Kırmızımsı
            self.tree.tag_configure('eksik', background='#004a00')  # Yeşilimsi
            
            # İstatistikleri göster
            total_diff = len(self.df_result)
            fays_fazla = len(self.df_result[self.df_result['FARK'] > 0])
            fays_eksik = len(self.df_result[self.df_result['FARK'] < 0])
            
            stats_text = (
                f"Toplam Fark: {total_diff} | "
                f"🔴 FAYS Fazla: {fays_fazla} | "
                f"🟢 FAYS Eksik: {fays_eksik}"
            )
            self.stats_label.configure(text=stats_text, text_color="white")
            
            logger.info(f"Karşılaştırma tamamlandı: {total_diff} fark bulundu")
            
        except Exception as e:
            self.stats_label.configure(text="Hata oluştu!", text_color="red")
            messagebox.showerror("Hata", f"Karşılaştırma hatası:\n{str(e)}")
            logger.error(f"Karşılaştırma hatası: {e}", exc_info=True)
    
    def on_filter_change(self, event=None):
        """Filtre değiştiğinde treeview'i güncelle"""
        if not hasattr(self, 'tree_data') or len(self.tree_data) == 0:
            return
        
        filter_text = self.filter_entry.get().lower().strip()
        
        # Treeview'i temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtreleme yap
        filtered_count = 0
        for values, row in self.tree_data:
            # Tüm değerlerde ara (case-insensitive)
            match = False
            for val in values:
                if filter_text in str(val).lower():
                    match = True
                    break
            
            if match or filter_text == "":
                # Fark durumuna göre renklendirme için tag
                if row['FARK'] > 0:
                    tag = 'fazla'
                else:
                    tag = 'eksik'
                
                self.tree.insert('', 'end', values=values, tags=(tag,))
                filtered_count += 1
        
        # İstatistikleri güncelle
        if filter_text:
            total_diff = len(self.df_result)
            fays_fazla = len(self.df_result[self.df_result['FARK'] > 0])
            fays_eksik = len(self.df_result[self.df_result['FARK'] < 0])
            
            stats_text = (
                f"Toplam Fark: {total_diff} | "
                f"🔴 FAYS Fazla: {fays_fazla} | "
                f"🟢 FAYS Eksik: {fays_eksik} | "
                f"🔍 Filtrelenmiş: {filtered_count}"
            )
        else:
            total_diff = len(self.df_result)
            fays_fazla = len(self.df_result[self.df_result['FARK'] > 0])
            fays_eksik = len(self.df_result[self.df_result['FARK'] < 0])
            
            stats_text = (
                f"Toplam Fark: {total_diff} | "
                f"🔴 FAYS Fazla: {fays_fazla} | "
                f"🟢 FAYS Eksik: {fays_eksik}"
            )
        
        self.stats_label.configure(text=stats_text, text_color="white")
    
    def clear_filter(self):
        """Filtreyi temizle"""
        self.filter_entry.delete(0, 'end')
        self.on_filter_change()
    
    def export_to_excel(self):
        """Sonuçları Excel'e aktar"""
        if self.df_result is None or len(self.df_result) == 0:
            messagebox.showwarning("Uyarı", "Aktarılacak veri yok!")
            return
        
        try:
            # Dosya adı sor
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"Stok_Karsilastirma_{timestamp}.xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                self.sync_engine.export_to_excel(self.df_result, filename)
                messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Excel export hatası:\n{str(e)}")


class SyncFrame(ctk.CTkFrame):
    """Stok eşitleme ekranı"""
    
    def __init__(self, parent, sync_engine):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        self.sync_engine = sync_engine
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur - Modern tasarım"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="Stok Eşitleme",
            font=ModernTheme.get_font('h2'),
            text_color=ModernTheme.COLORS['text_primary']
        )
        title.pack(pady=(0, ModernTheme.SPACING['lg']))
        
        # Uyarı paneli - Modern tasarım
        warning_card = ctk.CTkFrame(
            self,
            fg_color=ModernTheme.COLORS['warning'],
            corner_radius=ModernTheme.RADIUS['md']
        )
        warning_card.pack(fill="x", pady=(0, ModernTheme.SPACING['lg']))
        
        warning_label = ctk.CTkLabel(
            warning_card,
            text="⚠️ DİKKAT: Bu işlem FAYS WMS stoklarını LOGO ERP'ye göre eşitleyecektir!\n"
                 "İşlem geri alınamaz! Devam etmeden önce yedek aldığınızdan emin olun.",
            font=ModernTheme.get_font('body'),
            text_color="white",
            justify="left"
        )
        warning_label.pack(padx=ModernTheme.SPACING['lg'], pady=ModernTheme.SPACING['md'])
        
        # Ayarlar paneli - Modern kart
        settings_card = ModernTheme.create_card(self)
        settings_card.pack(fill="x", pady=(0, ModernTheme.SPACING['lg']))
        
        settings_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        settings_frame.pack(fill="x", padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        # Depo seçimi
        depo_label = ModernTheme.create_section_title(settings_frame, "Eşitlenecek Depo")
        depo_label.pack(anchor="w", pady=(0, ModernTheme.SPACING['sm']))
        
        self.warehouse_combo = ctk.CTkComboBox(
            settings_frame,
            values=[Config.DEFAULT_WAREHOUSE],
            width=400,
            height=40,
            font=ModernTheme.get_font('body'),
            corner_radius=ModernTheme.RADIUS['md'],
            command=self.on_warehouse_changed
        )
        self.warehouse_combo.pack(fill="x", pady=(0, ModernTheme.SPACING['lg']))
        self.warehouse_combo.set(Config.DEFAULT_WAREHOUSE)
        
        # Depoları otomatik yükle
        self.auto_load_warehouses()
        
        # Raf seçimi (Sayım Fazlası için)
        raf_label = ModernTheme.create_section_title(settings_frame, "Sayım Fazlası Rafı (LOGO stokları için)")
        raf_label.pack(anchor="w", pady=(0, ModernTheme.SPACING['sm']))
        
        self.raf_combo = ctk.CTkComboBox(
            settings_frame,
            values=["Raf seçmek için depo seçin..."],
            width=400,
            height=40,
            font=ModernTheme.get_font('body'),
            corner_radius=ModernTheme.RADIUS['md'],
            state="disabled",
            command=self.on_raf_changed
        )
        self.raf_combo.pack(fill="x", pady=(0, ModernTheme.SPACING['xl']))
        
        self.selected_raf_ref_no = None
        
        # Depo seçildiğinde rafları otomatik yükle
        if self.warehouse_combo.get() and self.warehouse_combo.get() != "Tümü":
            self.on_warehouse_changed(self.warehouse_combo.get())
        
        # Butonlar
        button_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        button_container.pack(fill="x", pady=ModernTheme.SPACING['md'])
        
        preview_btn = ModernTheme.create_warning_button(
            button_container,
            text="Önizleme Yap",
            command=self.preview_sync,
            width=200
        )
        preview_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        self.sync_btn = ModernTheme.create_danger_button(
            button_container,
            text="EŞİTLEMEYİ BAŞLAT",
            command=self.start_sync,
            width=300,
            height=50,
            font=ModernTheme.get_font('h4')
        )
        self.sync_btn.pack(side="left", padx=ModernTheme.SPACING['sm'])
        
        # Sonuç paneli - Modern kart
        result_card = ModernTheme.create_card(self)
        result_card.pack(fill="both", expand=True, pady=(0, 0))
        
        result_label = ModernTheme.create_section_title(result_card, "İşlem Sonuçları")
        result_label.pack(anchor="w", padx=ModernTheme.SPACING['lg'], pady=(ModernTheme.SPACING['lg'], ModernTheme.SPACING['sm']))
        
        self.result_text = ctk.CTkTextbox(
            result_card,
            font=ModernTheme.get_font('code'),
            wrap="word",
            corner_radius=ModernTheme.RADIUS['md'],
            fg_color='#FFFFFF',  # Beyaz arka plan (light tema)
            text_color=ModernTheme.COLORS['text_primary']
        )
        self.result_text.pack(fill="both", expand=True, padx=ModernTheme.SPACING['lg'], pady=(0, ModernTheme.SPACING['lg']))
        
        self.result_text.insert("1.0", "Eşitleme işlemi henüz başlatılmadı.\n\n"
                                      "İşlem Adımları:\n"
                                      "1. Depo seçin\n"
                                      "2. Önizleme yapın\n"
                                      "3. Eşitlemeyi başlatın\n")
    
    def auto_load_warehouses(self):
        """Depoları otomatik yükle"""
        try:
            # Bağlantı kontrolü
            if not self.sync_engine.db.conn_fays or not self.sync_engine.db.conn_logo:
                logger.debug("Bağlantı yok, depolar yüklenemedi")
                return
            
            warehouses = self.sync_engine.get_warehouses()
            if warehouses and len(warehouses) > 0:
                # Mevcut değeri koru
                current_value = self.warehouse_combo.get()
                self.warehouse_combo.configure(values=warehouses)
                
                # Eğer mevcut değer listede varsa koru, yoksa ilkini seç
                if current_value in warehouses:
                    self.warehouse_combo.set(current_value)
                elif warehouses:
                    self.warehouse_combo.set(warehouses[0])
                    # Depo seçildiğinde rafları da yükle
                    self.on_warehouse_changed(warehouses[0])
                
                logger.info(f"{len(warehouses)} depo otomatik yüklendi: {warehouses}")
            else:
                logger.warning("Depo listesi boş")
        except Exception as e:
            logger.warning(f"Depo listesi otomatik yüklenemedi: {e}", exc_info=True)
    
    def on_warehouse_changed(self, warehouse):
        """Depo değiştiğinde rafları otomatik yükle"""
        if warehouse and warehouse != "Tümü":
            self.raf_combo.configure(state="normal")
            self.load_rafs(silent=True)  # Otomatik yükleme, mesaj gösterme
        else:
            self.raf_combo.configure(state="disabled")
            self.raf_combo.configure(values=["Raf seçmek için depo seçin..."])
            self.selected_raf_ref_no = None
    
    def load_rafs(self, silent=False):
        """Seçilen depoya göre rafları otomatik yükle"""
        try:
            warehouse = self.warehouse_combo.get()
            if not warehouse or warehouse == "Tümü":
                if not silent:
                    messagebox.showwarning("Uyarı", "Önce bir depo seçmelisiniz!")
                return
            
            raflar = self.sync_engine.db.get_raflar(warehouse)
            
            if raflar:
                # ComboBox için format: "RafAdi (idNo)"
                raf_values = [f"{raf['RafAdi']} ({raf['idNo']})" for raf in raflar]
                self.raf_combo.configure(values=raf_values)
                
                # İlk rafı seç
                if raf_values:
                    self.raf_combo.set(raf_values[0])
                    self.selected_raf_ref_no = raflar[0]['idNo']
                
                logger.info(f"{len(raflar)} adet raf otomatik yüklendi - Depo: {warehouse}")
            else:
                self.raf_combo.configure(values=["Bu depoda raf bulunamadı"])
                self.selected_raf_ref_no = None
                if not silent:
                    messagebox.showwarning("Uyarı", "Bu depoda raf bulunamadı!")
        except Exception as e:
            logger.warning(f"Raf listesi yüklenemedi: {e}")
            if not silent:
                messagebox.showerror("Hata", f"Raf listesi yüklenemedi:\n{str(e)}")
    
    def on_raf_changed(self, raf_text):
        """Raf seçildiğinde RafRefNo'yu kaydet"""
        if raf_text and "(" in raf_text and ")" in raf_text:
            try:
                # "RafAdi (idNo)" formatından idNo'yu çıkar
                idno_str = raf_text.split("(")[1].split(")")[0]
                self.selected_raf_ref_no = int(idno_str)
            except:
                self.selected_raf_ref_no = None
    
    def preview_sync(self):
        """Eşitleme önizlemesi yap"""
        try:
            warehouse = self.warehouse_combo.get()
            
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"Önizleme yapılıyor - Depo: {warehouse}\n\n")
            self.update()
            
            # Karşılaştırma yap
            df_diff = self.sync_engine.compare_stocks(warehouse)
            
            if len(df_diff) == 0:
                self.result_text.insert("end", "✓ Stoklar zaten eşit!\n")
                return
            
            # Özet bilgi
            fays_fazla = df_diff[df_diff['FARK'] > 0]
            fays_eksik = df_diff[df_diff['FARK'] < 0]
            
            self.result_text.insert("end", f"ÖNIZLEME RAPORU\n")
            self.result_text.insert("end", f"=" * 80 + "\n\n")
            self.result_text.insert("end", f"Toplam Fark: {len(df_diff)} kalem\n\n")
            
            if len(fays_fazla) > 0:
                self.result_text.insert("end", f"🔴 FAYS FAZLA (Sayım Eksiği Fişi Oluşturulacak): {len(fays_fazla)} kalem\n")
                self.result_text.insert("end", f"   Toplam Miktar: {abs(fays_fazla['FARK'].sum()):.2f}\n\n")
            
            if len(fays_eksik) > 0:
                self.result_text.insert("end", f"🟢 FAYS EKSİK (Sayım Fazlası Fişi Oluşturulacak): {len(fays_eksik)} kalem\n")
                self.result_text.insert("end", f"   Toplam Miktar: {abs(fays_eksik['FARK'].sum()):.2f}\n\n")
            
            self.result_text.insert("end", "\nDetaylı Liste:\n")
            self.result_text.insert("end", "-" * 80 + "\n")
            
            for _, row in df_diff.head(20).iterrows():
                durum = "FAZLA" if row['FARK'] > 0 else "EKSİK"
                self.result_text.insert(
                    "end",
                    f"{row['MALZEME KODU']:<15} | {row['MALZEME ADI']:<30} | "
                    f"FARK: {row['FARK']:>8.2f} | {durum}\n"
                )
            
            if len(df_diff) > 20:
                self.result_text.insert("end", f"\n... ve {len(df_diff) - 20} kayıt daha\n")
            
        except Exception as e:
            self.result_text.insert("end", f"\nHATA: {str(e)}\n")
            messagebox.showerror("Hata", f"Önizleme hatası:\n{str(e)}")
    
    def start_sync(self):
        """Eşitlemeyi başlat"""
        warehouse = self.warehouse_combo.get()
        
        # Onay iste
        confirm = messagebox.askyesno(
            "Eşitleme Onayı",
            f"'{warehouse}' deposundaki FAYS WMS stokları LOGO ERP'ye göre eşitlenecek!\n\n"
            "Bu işlem geri alınamaz!\n\n"
            "Devam etmek istiyor musunuz?",
            icon='warning'
        )
        
        if not confirm:
            return
        
        try:
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"Eşitleme başlatıldı - Depo: {warehouse}\n")
            self.result_text.insert("end", f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            self.update()
            
            # Raf seçimi kontrolü
            if not self.selected_raf_ref_no:
                response = messagebox.askyesno(
                    "Raf Seçimi",
                    "Sayım fazlası için raf seçilmedi!\n\n"
                    "Varsayılan raf kullanılacak. Devam etmek istiyor musunuz?"
                )
                if not response:
                    return
                raf_ref_no = None
            else:
                raf_ref_no = self.selected_raf_ref_no
            
            # Eşitleme yap
            result = self.sync_engine.synchronize_stocks(warehouse, default_raf_ref_no=raf_ref_no)
            
            if result['success']:
                self.result_text.insert("end", f"\n✓ EŞİTLEME BAŞARILI!\n\n")
                self.result_text.insert("end", f"Oluşturulan Fiş Sayısı: {len(result['created_fis'])}\n")
                self.result_text.insert("end", f"İşlenen Kalem Sayısı: {result['total_items']}\n\n")
                
                self.result_text.insert("end", "Oluşturulan Fişler:\n")
                self.result_text.insert("end", "-" * 80 + "\n")
                
                for fis in result['created_fis']:
                    self.result_text.insert(
                        "end",
                        f"FişNo: {fis['fisno']} | "
                        f"Tür: {fis['fis_turu_adi']} | "
                        f"Satır: {fis['lines_count']}\n"
                        f"  → {fis['aciklama']}\n\n"
                    )
                
                self.result_text.insert("end", f"\nBitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                messagebox.showinfo("Başarılı", "Stok eşitleme tamamlandı!")
                
            else:
                self.result_text.insert("end", f"\n✗ EŞİTLEME BAŞARISIZ!\n\n")
                self.result_text.insert("end", f"Hata: {result['message']}\n")
                
                messagebox.showerror("Hata", result['message'])
                
        except Exception as e:
            self.result_text.insert("end", f"\n✗ HATA!\n{str(e)}\n")
            messagebox.showerror("Hata", f"Eşitleme hatası:\n{str(e)}")
            logger.error(f"Eşitleme hatası: {e}", exc_info=True)


class QueryEditorFrame(ctk.CTkFrame):
    """SQL sorgu düzenleyici ekranı"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.db_manager = db_manager
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="SQL Sorgu Düzenleyici",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=10)
        
        # Üst panel - Butonlar
        top_panel = ctk.CTkFrame(self, fg_color="transparent")
        top_panel.pack(fill="x", padx=10, pady=10)
        
        # Sorgu türü seçimi
        ctk.CTkLabel(
            top_panel,
            text="Sorgu Şablonu:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.query_type_combo = ctk.CTkComboBox(
            top_panel,
            values=[
                "Stok Karşılaştırma (Varsayılan)",
                "FAYS Stok Raporu",
                "LOGO Stok Raporu",
                "Boş Sorgu"
            ],
            width=250,
            command=self.load_query_template
        )
        self.query_type_combo.pack(side="left", padx=10)
        self.query_type_combo.set("Stok Karşılaştırma (Varsayılan)")
        
        # Çalıştır butonu
        run_btn = ctk.CTkButton(
            top_panel,
            text="▶️ Çalıştır",
            command=self.run_query,
            width=120,
            fg_color="green",
            hover_color="darkgreen"
        )
        run_btn.pack(side="left", padx=10)
        
        # Temizle butonu
        clear_btn = ctk.CTkButton(
            top_panel,
            text="🗑️ Temizle",
            command=self.clear_results,
            width=120
        )
        clear_btn.pack(side="left", padx=10)
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(
            top_panel,
            text="💾 Sorguyu Kaydet",
            command=self.save_query,
            width=140
        )
        save_btn.pack(side="left", padx=10)
        
        # Ana içerik - TabView (SQL Sorgusu ve INSERT Şablonları)
        main_tabview = ctk.CTkTabview(self)
        main_tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # SQL Sorgusu sekmesi
        sql_tab = main_tabview.add("SQL Sorgusu")
        
        # Sorgu editörü
        editor_frame = ctk.CTkFrame(sql_tab)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            editor_frame,
            text="SQL Sorgusu:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.query_text = ctk.CTkTextbox(
            editor_frame,
            font=ctk.CTkFont(family="Courier", size=11),
            wrap="none"
        )
        self.query_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Varsayılan sorguyu yükle
        self.load_query_template("Stok Karşılaştırma (Varsayılan)")
        
        # Sonuç alanı
        result_label = ctk.CTkLabel(
            sql_tab,
            text="Sorgu Sonucu:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_label.pack(anchor="w", padx=20, pady=5)
        
        self.result_text = ctk.CTkTextbox(
            sql_tab,
            font=ctk.CTkFont(family="Courier", size=11),
            height=200
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # INSERT Şablonları sekmesi
        templates_tab = main_tabview.add("INSERT Şablonları")
        
        # Açıklama
        info = ctk.CTkLabel(
            templates_tab,
            text="Bu şablonlar stok eşitleme sırasında kullanılır. {Değişken} formatındaki alanlar otomatik doldurulur.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info.pack(pady=10)
        
        # Şablonları yükle
        templates = SQLTemplates.load_templates()
        
        # Notebook (tabs) for templates
        template_notebook = ctk.CTkTabview(templates_tab)
        template_notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # stk_Fis INSERT şablonu
        tab1 = template_notebook.add("stk_Fis INSERT")
        ctk.CTkLabel(
            tab1,
            text="stk_Fis Tablosu INSERT Şablonu:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.fis_text = ctk.CTkTextbox(
            tab1,
            font=ctk.CTkFont(family="Courier", size=11),
            wrap="none"
        )
        self.fis_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.fis_text.insert("1.0", templates.get("stk_Fis_INSERT", ""))
        
        # stk_FisLines INSERT şablonu
        tab2 = template_notebook.add("stk_FisLines INSERT")
        ctk.CTkLabel(
            tab2,
            text="stk_FisLines Tablosu INSERT Şablonu:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.fislines_text = ctk.CTkTextbox(
            tab2,
            font=ctk.CTkFont(family="Courier", size=11),
            wrap="none"
        )
        self.fislines_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.fislines_text.insert("1.0", templates.get("stk_FisLines_INSERT", ""))
        
        # Açıklamalar sekmesi
        tab3 = template_notebook.add("Fiş Açıklamaları")
        ctk.CTkLabel(
            tab3,
            text="Sayım Eksiği (FisTuru=51) Açıklaması:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.eksik_entry = ctk.CTkEntry(tab3, width=600)
        self.eksik_entry.pack(padx=10, pady=5)
        self.eksik_entry.insert(0, templates.get("Sayim_Eksigi_Aciklama", ""))
        
        ctk.CTkLabel(
            tab3,
            text="Sayım Fazlası (FisTuru=50) Açıklaması:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(20, 5))
        
        self.fazla_entry = ctk.CTkEntry(tab3, width=600)
        self.fazla_entry.pack(padx=10, pady=5)
        self.fazla_entry.insert(0, templates.get("Sayim_Fazlasi_Aciklama", ""))
        
        # Kaydet butonu
        save_templates_btn = ctk.CTkButton(
            templates_tab,
            text="💾 Şablonları Kaydet",
            command=self.save_templates,
            width=200,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_templates_btn.pack(pady=15)
    
    def load_query_template(self, choice):
        """Sorgu şablonunu yükle"""
        self.query_text.delete("1.0", "end")
        
        if choice == "Stok Karşılaştırma (Varsayılan)":
            query = self.db_manager._get_default_comparison_query()
        elif choice == "FAYS Stok Raporu":
            query = """
            SELECT 
                RTRIM(LTRIM(ln.depo)) AS [Depo Adı],
                RTRIM(LTRIM(LN.StokKodu)) AS [Ürün Kodu],
                RTRIM(LTRIM(LN.barkodno)) AS [Standart Barkod No],
                RTRIM(LTRIM(LN.urungrup1)) AS [Ürün Adı],
                I.STGRPCODE AS [Grup Kodu],
                RTRIM(LTRIM(LN.miktarbirimi)) AS [Birimi],
                RTRIM(LTRIM(LN.urungrup5)) AS [Raf Adı],
                SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) as NetMiktar
            FROM dbo.stk_Fis AS FS WITH (NOLOCK) 
            LEFT OUTER JOIN dbo.stk_FisLines AS LN WITH (NOLOCK) ON LN.Link_FisNo = FS.FisNo
            LEFT JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=LN.StokKodu COLLATE Turkish_CI_AS
            GROUP BY 
                ln.depo, LN.StokKodu, LN.barkodno, LN.urungrup1,
                I.STGRPCODE, LN.miktarbirimi, LN.urungrup5
            HAVING SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) <> 0.00
            """
        elif choice == "LOGO Stok Raporu":
            query = """
            SELECT     
                [AMBAR ADI] = AMBARLAR.NAME, 
                ITEMS.CODE AS [MALZEME KODU], 
                RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
                ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
                ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
                ROUND((SUM(ST.ONHAND) - SUM(ST.RESERVED) + SUM(ST.TEMPOUT) - SUM(ST.TEMPIN)),2) AS [GERÇEK STOK],
                ROUND(SUM(ST.ONHAND)-SUM(ST.RESERVED),2) AS [SEVKEDİLEBİLİR STOK]
            FROM         
                GOLD..LG_013_ITEMS AS ITEMS WITH (NOLOCK)		 
                INNER JOIN GOLD..LV_013_01_STINVTOT AS ST WITH (NOLOCK) ON ST.STOCKREF = ITEMS.LOGICALREF 
                LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR WITH (NOLOCK) ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013' 
            WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
            GROUP BY  
                ITEMS.CODE, ITEMS.NAME, ITEMS.STGRPCODE, ST.INVENNO, AMBARLAR.NAME
            ORDER BY ITEMS.CODE
            """
        else:
            query = "-- Sorgunuzu buraya yazın\nSELECT "
        
        self.query_text.insert("1.0", query)
    
    def run_query(self):
        """Sorguyu çalıştır"""
        try:
            query = self.query_text.get("1.0", "end-1c").strip()
            
            if not query:
                messagebox.showwarning("Uyarı", "Sorgu boş!")
                return
            
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", "Sorgu çalıştırılıyor...\n")
            self.update()
            
            # Sorguyu çalıştır
            df = self.db_manager.execute_query(query, database='FAYS')
            
            # Sonucu göster
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"Sorgu başarıyla çalıştırıldı!\n")
            self.result_text.insert("end", f"Dönen kayıt sayısı: {len(df)}\n\n")
            
            if len(df) > 0:
                # İlk 100 satırı göster
                result_str = df.head(100).to_string()
                self.result_text.insert("end", result_str)
                
                if len(df) > 100:
                    self.result_text.insert("end", f"\n\n... ve {len(df) - 100} kayıt daha")
            else:
                self.result_text.insert("end", "Sonuç yok.")
            
        except Exception as e:
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"HATA!\n\n{str(e)}")
            messagebox.showerror("Hata", f"Sorgu hatası:\n{str(e)}")
            logger.error(f"Sorgu hatası: {e}", exc_info=True)
    
    def clear_results(self):
        """Sonuçları temizle"""
        self.result_text.delete("1.0", "end")
    
    def save_query(self):
        """Sorguyu dosyaya kaydet"""
        try:
            query = self.query_text.get("1.0", "end-1c")
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".sql",
                filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(query)
                messagebox.showinfo("Başarılı", f"Sorgu kaydedildi:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası:\n{str(e)}")
    
    def save_templates(self):
        """INSERT şablonlarını kaydet"""
        try:
            new_templates = {
                "stk_Fis_INSERT": self.fis_text.get("1.0", "end-1c"),
                "stk_FisLines_INSERT": self.fislines_text.get("1.0", "end-1c"),
                "Sayim_Eksigi_Aciklama": self.eksik_entry.get(),
                "Sayim_Fazlasi_Aciklama": self.fazla_entry.get()
            }
            
            success, message = SQLTemplates.save_templates(new_templates)
            
            if success:
                messagebox.showinfo("Başarılı", "Şablonlar kaydedildi!")
            else:
                messagebox.showerror("Hata", message)
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{str(e)}")


class SettingsFrame(ctk.CTkFrame):
    """Ayarlar ekranı"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur - Modern tasarım"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="Uygulama Ayarları",
            font=ModernTheme.get_font('h2'),
            text_color=ModernTheme.COLORS['text_primary']
        )
        title.pack(pady=(0, ModernTheme.SPACING['lg']))
        
        # Ayarlar formu - Modern kart
        form_card = ModernTheme.create_card(self)
        form_card.pack(fill="both", expand=True, padx=0, pady=0)
        
        form_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACING['xl'], pady=ModernTheme.SPACING['xl'])
        
        # Tema
        theme_label = ModernTheme.create_label(
            form_frame,
            "Tema:",
            size='body',
            color='text_primary'
        )
        theme_label.grid(row=0, column=0, padx=ModernTheme.SPACING['md'], 
                        pady=ModernTheme.SPACING['md'], sticky="w")
        
        self.theme_combo = ctk.CTkComboBox(
            form_frame,
            values=["light", "dark"],
            width=400,
            height=40,
            font=ModernTheme.get_font('body'),
            corner_radius=ModernTheme.RADIUS['md']
        )
        self.theme_combo.grid(row=0, column=1, padx=ModernTheme.SPACING['md'], 
                              pady=ModernTheme.SPACING['md'], sticky="ew")
        self.theme_combo.set("light")  # Varsayılan light tema
        self.theme_combo.configure(command=self.change_theme)
        
        # Varsayılan Depo
        depo_label = ModernTheme.create_label(
            form_frame,
            "Varsayılan Depo:",
            size='body',
            color='text_primary'
        )
        depo_label.grid(row=1, column=0, padx=ModernTheme.SPACING['md'], 
                       pady=ModernTheme.SPACING['md'], sticky="w")
        
        self.default_warehouse_entry = ModernTheme.create_modern_entry(
            form_frame,
            placeholder="MERKEZ",
            width=400
        )
        self.default_warehouse_entry.grid(row=1, column=1, padx=ModernTheme.SPACING['md'], 
                                          pady=ModernTheme.SPACING['md'], sticky="ew")
        self.default_warehouse_entry.insert(0, Config.DEFAULT_WAREHOUSE)
        
        # Log Seviyesi
        log_label = ModernTheme.create_label(
            form_frame,
            "Log Seviyesi:",
            size='body',
            color='text_primary'
        )
        log_label.grid(row=2, column=0, padx=ModernTheme.SPACING['md'], 
                      pady=ModernTheme.SPACING['md'], sticky="w")
        
        self.log_level_combo = ctk.CTkComboBox(
            form_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=400,
            height=40,
            font=ModernTheme.get_font('body'),
            corner_radius=ModernTheme.RADIUS['md']
        )
        self.log_level_combo.grid(row=2, column=1, padx=ModernTheme.SPACING['md'], 
                                  pady=ModernTheme.SPACING['md'], sticky="ew")
        self.log_level_combo.set(Config.LOG_LEVEL)
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Kaydet butonu
        save_btn = ModernTheme.create_primary_button(
            form_frame,
            text="Ayarları Kaydet",
            command=self.save_settings,
            width=200
        )
        save_btn.grid(row=3, column=0, columnspan=2, pady=ModernTheme.SPACING['xl'])
        
        # Bilgi paneli - Modern kart
        info_card = ModernTheme.create_card(self)
        info_card.pack(fill="x", pady=(ModernTheme.SPACING['lg'], 0))
        
        info_text = (
            "📌 LOGO - FAYS WMS Stok Eşitleme Programı\n"
            "📅 Versiyon: 1.0.0\n"
            "👨‍💻 2025\n\n"
            "Bu program LOGO ERP ve FAYS WMS veritabanları arasındaki\n"
            "stok farklılıklarını tespit eder ve eşitler."
        )
        
        ctk.CTkLabel(
            info_card,
            text=info_text,
            font=ModernTheme.get_font('body_small'),
            text_color=ModernTheme.COLORS['text_primary'],
            justify="left"
        ).pack(padx=ModernTheme.SPACING['lg'], pady=ModernTheme.SPACING['lg'])
    
    def change_theme(self, choice):
        """Temayı değiştir"""
        ctk.set_appearance_mode(choice)
    
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            Config.save_to_env('DEFAULT_WAREHOUSE', self.default_warehouse_entry.get())
            Config.save_to_env('LOG_LEVEL', self.log_level_combo.get())
            
            Config.DEFAULT_WAREHOUSE = self.default_warehouse_entry.get()
            Config.LOG_LEVEL = self.log_level_combo.get()
            
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi:\n{str(e)}")

