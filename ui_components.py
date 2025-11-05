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

logger = logging.getLogger(__name__)


class ConnectionFrame(ctk.CTkFrame):
    """Veritabanı bağlantı ekranı"""
    
    def __init__(self, parent, db_manager, on_connection_changed):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.db_manager = db_manager
        self.on_connection_changed = on_connection_changed
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="Veritabanı Bağlantı Ayarları",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Form container
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=100, pady=20)
        
        # Server
        ctk.CTkLabel(
            form_frame,
            text="Server:",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.server_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="örn: server.database.windows.net"
        )
        self.server_entry.grid(row=0, column=1, padx=20, pady=15)
        self.server_entry.insert(0, Config.DB_SERVER)
        
        # Username
        ctk.CTkLabel(
            form_frame,
            text="Kullanıcı Adı:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Kullanıcı adı"
        )
        self.username_entry.grid(row=1, column=1, padx=20, pady=15)
        self.username_entry.insert(0, Config.DB_USER)
        
        # Password
        ctk.CTkLabel(
            form_frame,
            text="Şifre:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=0, padx=20, pady=15, sticky="w")
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            show="*",
            placeholder_text="Şifre"
        )
        self.password_entry.grid(row=2, column=1, padx=20, pady=15)
        self.password_entry.insert(0, Config.DB_PASSWORD)
        
        # LOGO Database
        ctk.CTkLabel(
            form_frame,
            text="LOGO Veritabanı:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=0, padx=20, pady=15, sticky="w")
        
        self.logo_db_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="GOLD"
        )
        self.logo_db_entry.grid(row=3, column=1, padx=20, pady=15)
        self.logo_db_entry.insert(0, Config.DB_LOGO)
        
        # FAYS Database
        ctk.CTkLabel(
            form_frame,
            text="FAYS Veritabanı:",
            font=ctk.CTkFont(size=14)
        ).grid(row=4, column=0, padx=20, pady=15, sticky="w")
        
        self.fays_db_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="FaysWMSAkturk"
        )
        self.fays_db_entry.grid(row=4, column=1, padx=20, pady=15)
        self.fays_db_entry.insert(0, Config.DB_FAYS)
        
        # Butonlar
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=30)
        
        self.connect_btn = ctk.CTkButton(
            button_frame,
            text="🔌 Bağlan",
            command=self.connect,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.connect_btn.pack(side="left", padx=10)
        
        self.test_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Bağlantıyı Test Et",
            command=self.test_connection,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.test_btn.pack(side="left", padx=10)
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Ayarları Kaydet",
            command=self.save_settings,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.save_btn.pack(side="left", padx=10)
        
        # Durum mesajı
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
    
    def connect(self):
        """Veritabanına bağlan"""
        try:
            self.status_label.configure(text="Bağlanıyor...", text_color="yellow")
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
                self.status_label.configure(
                    text="✓ Bağlantı başarılı!",
                    text_color="green"
                )
                self.on_connection_changed(True)
                messagebox.showinfo("Başarılı", "Veritabanı bağlantısı başarıyla kuruldu!")
            else:
                self.status_label.configure(
                    text="✗ Bağlantı başarısız!",
                    text_color="red"
                )
                self.on_connection_changed(False)
                messagebox.showerror("Hata", "Veritabanına bağlanılamadı!")
                
        except Exception as e:
            self.status_label.configure(
                text=f"✗ Hata: {str(e)}",
                text_color="red"
            )
            self.on_connection_changed(False)
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
    
    def save_settings(self):
        """Ayarları .env dosyasına kaydet"""
        try:
            Config.save_to_env('DB_SERVER', self.server_entry.get())
            Config.save_to_env('DB_USER', self.username_entry.get())
            Config.save_to_env('DB_PASSWORD', self.password_entry.get())
            Config.save_to_env('DB_LOGO', self.logo_db_entry.get())
            Config.save_to_env('DB_FAYS', self.fays_db_entry.get())
            
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi:\n{str(e)}")


class ComparisonFrame(ctk.CTkFrame):
    """Stok karşılaştırma ekranı"""
    
    def __init__(self, parent, sync_engine):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.sync_engine = sync_engine
        self.df_result = None
        
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
        
        # Depoları yükle butonu
        refresh_warehouses_btn = ctk.CTkButton(
            top_panel,
            text="🔄",
            width=40,
            command=self.load_warehouses
        )
        refresh_warehouses_btn.pack(side="left", padx=5)
        
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
    
    def load_warehouses(self):
        """Depoları yükle"""
        try:
            warehouses = self.sync_engine.get_warehouses()
            if warehouses:
                self.warehouse_combo.configure(values=["Tümü"] + warehouses)
                messagebox.showinfo("Başarılı", f"{len(warehouses)} depo yüklendi")
        except Exception as e:
            messagebox.showerror("Hata", f"Depo listesi yüklenemedi:\n{str(e)}")
    
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
            
            # Verileri ekle
            for _, row in self.df_result.iterrows():
                values = [row[col] for col in columns]
                
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
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.sync_engine = sync_engine
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        
        # Uyarı paneli
        warning_frame = ctk.CTkFrame(self, fg_color="#8B0000")
        warning_frame.pack(fill="x", padx=10, pady=10)
        
        warning_label = ctk.CTkLabel(
            warning_frame,
            text="⚠️ DİKKAT: Bu işlem FAYS WMS stokla rını LOGO ERP'ye göre eşitleyecektir!\n"
                 "İşlem geri alınamaz! Devam etmeden önce yedek aldığınızdan emin olun.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        warning_label.pack(pady=15)
        
        # Ayarlar paneli
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=10, pady=20)
        
        # Depo seçimi
        ctk.CTkLabel(
            settings_frame,
            text="Eşitlenecek Depo:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.warehouse_combo = ctk.CTkComboBox(
            settings_frame,
            values=[Config.DEFAULT_WAREHOUSE],
            width=300,
            font=ctk.CTkFont(size=14)
        )
        self.warehouse_combo.pack(pady=10)
        self.warehouse_combo.set(Config.DEFAULT_WAREHOUSE)
        
        # Depoları yükle butonu
        refresh_btn = ctk.CTkButton(
            settings_frame,
            text="🔄 Depoları Yükle",
            command=self.load_warehouses,
            width=200
        )
        refresh_btn.pack(pady=10)
        
        # Önizleme butonu
        preview_btn = ctk.CTkButton(
            settings_frame,
            text="👁️ Önizleme Yap",
            command=self.preview_sync,
            width=200,
            fg_color="orange",
            hover_color="darkorange"
        )
        preview_btn.pack(pady=10)
        
        # Eşitleme butonu
        self.sync_btn = ctk.CTkButton(
            settings_frame,
            text="🔄 EŞİTLEMEYİ BAŞLAT",
            command=self.start_sync,
            width=300,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="red",
            hover_color="darkred"
        )
        self.sync_btn.pack(pady=20)
        
        # Sonuç paneli
        result_frame = ctk.CTkFrame(self)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.result_text = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.result_text.insert("1.0", "Eşitleme işlemi henüz başlatılmadı.\n\n"
                                      "İşlem Adımları:\n"
                                      "1. Depo seçin\n"
                                      "2. Önizleme yapın\n"
                                      "3. Eşitlemeyi başlatın\n")
    
    def load_warehouses(self):
        """Depoları yükle"""
        try:
            warehouses = self.sync_engine.get_warehouses()
            if warehouses:
                self.warehouse_combo.configure(values=warehouses)
                messagebox.showinfo("Başarılı", f"{len(warehouses)} depo yüklendi")
        except Exception as e:
            messagebox.showerror("Hata", f"Depo listesi yüklenemedi:\n{str(e)}")
    
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
            
            # Eşitleme yap
            result = self.sync_engine.synchronize_stocks(warehouse)
            
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
        
        # Sorgu editörü
        editor_frame = ctk.CTkFrame(self)
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
            self,
            text="Sorgu Sonucu:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_label.pack(anchor="w", padx=20, pady=5)
        
        self.result_text = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Courier", size=11),
            height=200
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
    
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


class SettingsFrame(ctk.CTkFrame):
    """Ayarlar ekranı"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="Uygulama Ayarları",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Ayarlar formu
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Tema
        ctk.CTkLabel(
            form_frame,
            text="Tema:",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.theme_combo = ctk.CTkComboBox(
            form_frame,
            values=["dark", "light"],
            width=300
        )
        self.theme_combo.grid(row=0, column=1, padx=20, pady=15)
        self.theme_combo.set("dark")
        self.theme_combo.configure(command=self.change_theme)
        
        # Varsayılan Depo
        ctk.CTkLabel(
            form_frame,
            text="Varsayılan Depo:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")
        
        self.default_warehouse_entry = ctk.CTkEntry(
            form_frame,
            width=300
        )
        self.default_warehouse_entry.grid(row=1, column=1, padx=20, pady=15)
        self.default_warehouse_entry.insert(0, Config.DEFAULT_WAREHOUSE)
        
        # Log Seviyesi
        ctk.CTkLabel(
            form_frame,
            text="Log Seviyesi:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=0, padx=20, pady=15, sticky="w")
        
        self.log_level_combo = ctk.CTkComboBox(
            form_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=300
        )
        self.log_level_combo.grid(row=2, column=1, padx=20, pady=15)
        self.log_level_combo.set(Config.LOG_LEVEL)
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(
            form_frame,
            text="💾 Ayarları Kaydet",
            command=self.save_settings,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        save_btn.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Bilgi paneli
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=50, pady=20)
        
        info_text = (
            "📌 LOGO - FAYS WMS Stok Eşitleme Programı\n"
            "📅 Versiyon: 1.0.0\n"
            "👨‍💻 2025\n\n"
            "Bu program LOGO ERP ve FAYS WMS veritabanları arasındaki\n"
            "stok farklılıklarını tespit eder ve eşitler."
        )
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=20, pady=20)
    
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

