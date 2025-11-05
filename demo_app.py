"""
LOGO - FAYS WMS Stok Eşitleme - DEMO Sürümü
macOS'ta arayüzü görmek için - ODBC gerektirmez
Mock (örnek) verilerle çalışır
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime

# Tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DemoApp(ctk.CTk):
    """Demo Uygulama - Arayüz Önizlemesi"""
    
    def __init__(self):
        super().__init__()
        
        # Pencere ayarları
        self.title("LOGO - FAYS WMS Stok Eşitleme (DEMO)")
        self.geometry("1400x900")
        
        # Mock veriler
        self.mock_data = self.create_mock_data()
        self.connected = False
        
        # UI oluştur
        self.create_ui()
    
    def create_mock_data(self):
        """Örnek stok verileri"""
        return pd.DataFrame({
            'MALZEME KODU': ['61007030', '343403022', 'TEST001', 'TEST002'],
            'MALZEME ADI': ['BULAŞIK MAKİNESİ DETERJAN', 'TEMİZLİK MALZEMESİ', 'TEST ÜRÜN 1', 'TEST ÜRÜN 2'],
            'GRUP KODU': ['GRUP-A', 'GRUP-A', 'GRUP-C', 'GRUP-C'],
            'AMBAR ADI': ['MERKEZ', 'MERKEZ', 'MERKEZ', 'MERKEZ'],
            'LOGO FİİLİ STOK': [100.0, 75.0, 200.0, 0.0],
            'FAYS STOK': [120.0, 60.0, 180.0, 30.0],
            'FARK': [20.0, -15.0, -20.0, 30.0],
            'DURUM': ['FAYS FAZLA', 'FAYS EKSİK', 'FAYS EKSİK', 'FAYS FAZLA']
        })
    
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
        self.create_connection_tab()
        self.create_comparison_tab()
        self.create_sync_tab()
        self.create_query_tab()
        self.create_settings_tab()
    
    def create_sidebar(self):
        """Sol menü paneli"""
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Başlık
        title_label = ctk.CTkLabel(
            sidebar,
            text="STOK EŞİTLEME\nSİSTEMİ\n(DEMO)",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Versiyon
        version_label = ctk.CTkLabel(
            sidebar,
            text="v1.0.0 - Preview",
            font=ctk.CTkFont(size=12)
        )
        version_label.grid(row=1, column=0, padx=20, pady=(0, 30))
        
        # Durum göstergesi
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="● Demo Modu",
            text_color="orange",
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
            text="🔌 Bağlan (Demo)",
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
        
        # Alt bilgi
        info_label = ctk.CTkLabel(
            sidebar,
            text="⚠️ DEMO SÜRÜMÜ\nmacOS Önizleme\n\nGerçek versiyon için\nWindows Server gerekli",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        info_label.grid(row=9, column=0, padx=20, pady=(0, 20))
    
    def create_connection_tab(self):
        """Bağlantı sekmesi"""
        frame = ctk.CTkFrame(self.tab_connection)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="Veritabanı Bağlantı Ayarları (DEMO)",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Demo bilgi
        demo_info = ctk.CTkTextbox(frame, height=150)
        demo_info.pack(fill="x", padx=100, pady=20)
        demo_info.insert("1.0", 
            "🎯 DEMO MOD AKTİF\n\n"
            "Bu macOS önizleme sürümüdür. Gerçek veritabanına bağlanmaz.\n"
            "Örnek verilerle arayüzü test edebilirsiniz.\n\n"
            "✅ Görebilirsiniz:\n"
            "  • Modern arayüz tasarımı\n"
            "  • Tüm sekme ve butonlar\n"
            "  • Örnek stok karşılaştırma verileri\n"
            "  • Tablo ve rapor görünümleri\n\n"
            "❌ Çalışmaz:\n"
            "  • Gerçek veritabanı bağlantısı (ODBC gerekli)\n"
            "  • Fiş oluşturma (Windows'ta çalışır)\n\n"
            "💻 Windows Server'da tam sürüm tüm özelliklerle çalışır!"
        )
        demo_info.configure(state="disabled")
        
        # Demo bağlan butonu
        connect_btn = ctk.CTkButton(
            frame,
            text="🔌 Demo Bağlantısını Aç",
            command=self.demo_connect,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="orange",
            hover_color="darkorange"
        )
        connect_btn.pack(pady=30)
    
    def create_comparison_tab(self):
        """Karşılaştırma sekmesi"""
        # Üst panel
        top_panel = ctk.CTkFrame(self.tab_comparison)
        top_panel.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            top_panel,
            text="Depo:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        warehouse_combo = ctk.CTkComboBox(
            top_panel,
            values=["MERKEZ", "ŞUBE-1", "ŞUBE-2"],
            width=200
        )
        warehouse_combo.pack(side="left", padx=10)
        warehouse_combo.set("MERKEZ")
        
        compare_btn = ctk.CTkButton(
            top_panel,
            text="📊 Karşılaştır",
            command=self.show_comparison,
            width=150,
            fg_color="blue"
        )
        compare_btn.pack(side="left", padx=20)
        
        export_btn = ctk.CTkButton(
            top_panel,
            text="📥 Excel'e Aktar (Demo)",
            command=lambda: messagebox.showinfo("Demo", "Windows'ta Excel dosyası oluşturulur"),
            width=150
        )
        export_btn.pack(side="left", padx=10)
        
        # İstatistik
        self.stats_label = ctk.CTkLabel(
            self.tab_comparison,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack(pady=10)
        
        # Treeview
        tree_frame = ctk.CTkFrame(self.tab_comparison)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="extended"
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Stil
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
    
    def create_sync_tab(self):
        """Eşitleme sekmesi"""
        # Uyarı
        warning = ctk.CTkFrame(self.tab_sync, fg_color="#8B0000")
        warning.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            warning,
            text="⚠️ DEMO MOD - Eşitleme yapılamaz\n"
                 "Windows Server'da gerçek veritabanı ile çalışır",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Ayarlar
        settings = ctk.CTkFrame(self.tab_sync)
        settings.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            settings,
            text="Eşitlenecek Depo:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        warehouse = ctk.CTkComboBox(
            settings,
            values=["MERKEZ", "ŞUBE-1", "ŞUBE-2"],
            width=300
        )
        warehouse.pack(pady=10)
        warehouse.set("MERKEZ")
        
        preview_btn = ctk.CTkButton(
            settings,
            text="👁️ Önizleme Yap (Demo)",
            command=self.show_sync_preview,
            width=200,
            fg_color="orange"
        )
        preview_btn.pack(pady=10)
        
        # Sonuç
        self.sync_result = ctk.CTkTextbox(self.tab_sync, font=ctk.CTkFont(size=12))
        self.sync_result.pack(fill="both", expand=True, padx=10, pady=10)
        self.sync_result.insert("1.0", 
            "Demo önizleme:\n\n"
            "Windows'ta eşitleme yapıldığında:\n"
            "• 2 adet fiş oluşturulur\n"
            "• stk_Fis ve stk_FisLines tablolarına kayıt eklenir\n"
            "• FAYS stokları LOGO'ya göre düzeltilir\n"
            "• İşlem logları kaydedilir\n\n"
            "Test için 'Önizleme Yap' butonunu kullanabilirsiniz."
        )
    
    def create_query_tab(self):
        """SQL sorgu sekmesi"""
        top = ctk.CTkFrame(self.tab_query, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            top,
            text="SQL Sorgu Düzenleyici (Demo)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10)
        
        run_btn = ctk.CTkButton(
            top,
            text="▶️ Çalıştır (Demo)",
            command=lambda: messagebox.showinfo("Demo", "Windows'ta gerçek sorgu çalışır"),
            width=120,
            fg_color="green"
        )
        run_btn.pack(side="left", padx=10)
        
        # Editor
        self.query_text = ctk.CTkTextbox(
            self.tab_query,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.query_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        sample_query = """-- Örnek Karşılaştırma Sorgusu
SELECT
    X.[MALZEME KODU],
    X.[MALZEME ADI],
    X.[GRUP KODU],
    X.[AMBAR ADI],
    ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [LOGO FİİLİ STOK],
    ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2) AS [FAYS STOK],
    ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [FARK]
FROM
(
    -- LOGO Stokları
    SELECT     
        [AMBAR ADI] = AMBARLAR.NAME, 
        ITEMS.CODE AS [MALZEME KODU], 
        RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
        ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
        ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
        0 AS [FAYS STOK]
    FROM GOLD..LG_013_ITEMS AS ITEMS
    INNER JOIN GOLD..LV_013_01_STINVTOT AS ST ON ST.STOCKREF = ITEMS.LOGICALREF 
    LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR ON AMBARLAR.NR = ST.INVENNO
    WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
    GROUP BY ITEMS.CODE, ITEMS.NAME, ITEMS.STGRPCODE, ST.INVENNO, AMBARLAR.NAME
    
    UNION ALL
    
    -- FAYS Stokları
    SELECT ...
) X
GROUP BY X.[MALZEME KODU], X.[MALZEME ADI], X.[GRUP KODU], X.[AMBAR ADI]

-- Bu sorgu Windows'ta düzenlenebilir ve çalıştırılabilir
"""
        self.query_text.insert("1.0", sample_query)
    
    def create_settings_tab(self):
        """Ayarlar sekmesi"""
        frame = ctk.CTkFrame(self.tab_settings)
        frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="Uygulama Ayarları (Demo)",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Tema
        theme_frame = ctk.CTkFrame(frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="Tema:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=["dark", "light"],
            width=300,
            command=self.change_theme
        )
        theme_combo.pack(side="left", padx=20)
        theme_combo.set("dark")
        
        # Bilgi
        info = ctk.CTkTextbox(frame, height=300)
        info.pack(fill="both", expand=True, padx=20, pady=20)
        info.insert("1.0",
            "📌 LOGO - FAYS WMS Stok Eşitleme Programı\n"
            "📅 Versiyon: 1.0.0 DEMO\n"
            "💻 Platform: macOS Preview / Windows Production\n\n"
            "🎯 ÖZELLİKLER:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ Modern CustomTkinter Arayüzü\n"
            "✅ Dark/Light Tema Desteği\n"
            "✅ 5 Tab Yapısı (Bağlantı, Karşılaştırma, Eşitleme, SQL, Ayarlar)\n"
            "✅ Gerçek Zamanlı Stok Karşılaştırma\n"
            "✅ Otomatik Fiş Oluşturma (Sayım Fazlası/Eksiği)\n"
            "✅ SQL Sorgu Editörü\n"
            "✅ Excel Export\n"
            "✅ Detaylı Loglama\n"
            "✅ Güvenli Onay Mekanizması\n\n"
            "🖥️ SİSTEM GEREKSİNİMLERİ:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• Windows Server 2012+ veya Windows 10+\n"
            "• Python 3.8+\n"
            "• ODBC Driver 17 for SQL Server\n"
            "• SQL Server 2012+ (Azure SQL destekli)\n"
            "• GOLD ve FaysWMSAkturk veritabanları\n\n"
            "⚠️ macOS'ta sadece arayüz önizlemesi gösterilir.\n"
            "   Tam işlevsellik için Windows Server gereklidir.\n\n"
            "📖 Detaylı bilgi: README.md, KURULUM.md, KULLANIM.md"
        )
        info.configure(state="disabled")
    
    def quick_connect(self):
        """Hızlı bağlan (demo)"""
        self.demo_connect()
    
    def quick_compare(self):
        """Hızlı karşılaştır"""
        self.tabview.set("Stok Karşılaştırma")
        self.show_comparison()
    
    def demo_connect(self):
        """Demo bağlantı"""
        self.connected = True
        self.status_label.configure(text="● Demo Bağlı", text_color="green")
        messagebox.showinfo(
            "Demo Bağlantı",
            "✅ Demo bağlantı başarılı!\n\n"
            "Örnek verilerle çalışıyorsunuz.\n"
            "Windows'ta gerçek veritabanına bağlanır."
        )
    
    def show_comparison(self):
        """Karşılaştırma göster"""
        if not self.connected:
            messagebox.showwarning("Uyarı", "Önce demo bağlantısını açın!")
            self.tabview.set("Bağlantı")
            return
        
        # Treeview'i temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sütunları ayarla
        columns = list(self.mock_data.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        for col in columns:
            self.tree.heading(col, text=col)
            width = 150 if col == 'MALZEME ADI' else 120
            self.tree.column(col, width=width, anchor='center')
        
        # Verileri ekle
        for _, row in self.mock_data.iterrows():
            values = [row[col] for col in columns]
            tag = 'fazla' if row['FARK'] > 0 else 'eksik'
            self.tree.insert('', 'end', values=values, tags=(tag,))
        
        # Renkler
        self.tree.tag_configure('fazla', background='#4a0000')
        self.tree.tag_configure('eksik', background='#004a00')
        
        # İstatistik
        fazla = len(self.mock_data[self.mock_data['FARK'] > 0])
        eksik = len(self.mock_data[self.mock_data['FARK'] < 0])
        
        self.stats_label.configure(
            text=f"Toplam Fark: {len(self.mock_data)} | 🔴 FAYS Fazla: {fazla} | 🟢 FAYS Eksik: {eksik}",
            text_color="white"
        )
    
    def show_sync_preview(self):
        """Eşitleme önizleme"""
        self.sync_result.delete("1.0", "end")
        
        preview_text = f"""
ÖNIZLEME RAPORU (DEMO)
{'='*70}

Depo: MERKEZ
Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TOPLAM FARK: 4 kalem

🔴 FAYS FAZLA (Sayım Eksiği Fişi Oluşturulacak): 2 kalem
   Toplam Miktar: 50.00
   
   Detay:
   • 61007030 - BULAŞIK MAKİNESİ DETERJAN
     LOGO: 100.00, FAYS: 120.00, Fark: +20.00
   
   • TEST002 - TEST ÜRÜN 2
     LOGO: 0.00, FAYS: 30.00, Fark: +30.00

🟢 FAYS EKSİK (Sayım Fazlası Fişi Oluşturulacak): 2 kalem
   Toplam Miktar: 35.00
   
   Detay:
   • 343403022 - TEMİZLİK MALZEMESİ
     LOGO: 75.00, FAYS: 60.00, Fark: -15.00
   
   • TEST001 - TEST ÜRÜN 1
     LOGO: 200.00, FAYS: 180.00, Fark: -20.00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OLUŞTURULACAK FİŞLER:

Fiş 1: Sayım Eksiği (FisTuru=51, GirisCikis=2)
  → FisNo: 1067969
  → Satır Sayısı: 2
  → Açıklama: 0.KAT:SAYILMAYAN VE STOKTA FAZLA OLAN STOKLAR
  → İşlem: FAYS'dan çıkış yapılacak (stok azalacak)

Fiş 2: Sayım Fazlası (FisTuru=50, GirisCikis=1)
  → FisNo: 1067970
  → Satır Sayısı: 2
  → Açıklama: 0.KAT:SAYIM YAPILAN VE SAYIM FAZLASI VEREN STOKLAR
  → İşlem: FAYS'a giriş yapılacak (stok artacak)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ DİKKAT: Bu bir DEMO önizlemedir!

Windows'ta gerçek eşitleme yapıldığında:
✓ yr_BilgiLines tablosundan FisNo alınır
✓ stk_Fis tablosuna kayıt eklenir
✓ stk_FisLines tablosuna satırlar eklenir
✓ FAYS stokları otomatik eşitlenir
✓ İşlem logları kaydedilir

EŞİTLEME SONRASI:
→ Tekrar karşılaştırma yapıldığında 0 fark bulunur
→ Tüm stoklar LOGO ERP ile uyumlu hale gelir

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.sync_result.insert("1.0", preview_text)
        
        messagebox.showinfo(
            "Demo Önizleme",
            "Eşitleme önizlemesi gösterildi!\n\n"
            "Windows'ta 'EŞİTLEMEYİ BAŞLAT' butonu\n"
            "ile gerçek eşitleme yapılır."
        )
    
    def change_theme(self, choice):
        """Tema değiştir"""
        ctk.set_appearance_mode(choice)
        messagebox.showinfo("Tema", f"Tema '{choice}' olarak değiştirildi!")


def main():
    """Ana fonksiyon"""
    print("\n" + "="*70)
    print("🎯 LOGO - FAYS WMS Stok Eşitleme DEMO")
    print("="*70)
    print("\n📱 macOS Arayüz Önizlemesi Başlatılıyor...")
    print("\n⚠️  DEMO MOD:")
    print("   • Sadece arayüz gösterimi")
    print("   • Örnek verilerle çalışır")
    print("   • Gerçek veritabanına bağlanmaz")
    print("\n💻 Windows'ta tam sürüm tüm özelliklerle çalışır!")
    print("\n" + "="*70 + "\n")
    
    app = DemoApp()
    app.mainloop()


if __name__ == "__main__":
    main()

