#!/usr/bin/env python3
"""
Basit SQL Server Test - ODBC Olmadan (pymssql kullanarak)
macOS'ta çalışır
"""
import pymssql
import pandas as pd
from datetime import datetime

print("\n" + "="*70)
print("🎯 LOGO - FAYS WMS Stok Karşılaştırma Testi")
print("="*70 + "\n")

# Bağlantı bilgileri
SERVER = 'localhost'
PORT = 1433
USER = 'sa'
PASSWORD = 'E123456.'
DATABASE_LOGO = 'GOLD'
DATABASE_FAYS = 'FaysWMSAkturk'

print("📋 Bağlantı Bilgileri:")
print(f"   Server: {SERVER}:{PORT}")
print(f"   User: {USER}")
print(f"   Password: {'*' * len(PASSWORD)}")
print()

try:
    # Test 1: LOGO Veritabanı
    print("="*70)
    print("📊 Test 1: LOGO (ERP) Veritabanı")
    print("="*70)
    
    conn_logo = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE_LOGO
    )
    print("✅ LOGO veritabanına bağlandı!\n")
    
    # LOGO Stok Kartları
    query = """
    SELECT 
        CODE AS [Ürün Kodu],
        NAME AS [Ürün Adı],
        STGRPCODE AS [Grup Kodu]
    FROM LG_013_ITEMS
    ORDER BY CODE
    """
    df_logo_items = pd.read_sql(query, conn_logo)
    print(f"📦 LOGO Stok Kartları ({len(df_logo_items)} adet):")
    print(df_logo_items.to_string(index=False))
    print()
    
    # LOGO Stok Durumu
    query = """
    SELECT 
        ITEMS.CODE AS [Ürün Kodu],
        RTRIM(LTRIM(ITEMS.NAME)) AS [Ürün Adı],
        AMBARLAR.NAME AS [Depo],
        ROUND(SUM(ST.ONHAND),2) AS [LOGO Stok]
    FROM LG_013_ITEMS AS ITEMS
    INNER JOIN LV_013_01_STINVTOT AS ST ON ST.STOCKREF = ITEMS.LOGICALREF 
    LEFT JOIN L_CAPIWHOUSE AS AMBARLAR ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013'
    WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
    GROUP BY ITEMS.CODE, ITEMS.NAME, ST.INVENNO, AMBARLAR.NAME
    ORDER BY ITEMS.CODE
    """
    df_logo_stock = pd.read_sql(query, conn_logo)
    print(f"📊 LOGO Stok Durumu ({len(df_logo_stock)} kayıt):")
    print(df_logo_stock.to_string(index=False))
    print()
    
    conn_logo.close()
    
    # Test 2: FAYS Veritabanı
    print("="*70)
    print("📊 Test 2: FAYS (WMS) Veritabanı")
    print("="*70)
    
    conn_fays = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE_FAYS
    )
    print("✅ FAYS veritabanına bağlandı!\n")
    
    # FAYS Stok Hareketleri
    query = """
    SELECT 
        StokKodu AS [Ürün Kodu],
        UrunGrup1 AS [Ürün Adı],
        Depo AS [Depo],
        NetMiktar AS [Miktar]
    FROM stk_FisLines
    ORDER BY StokKodu
    """
    df_fays_lines = pd.read_sql(query, conn_fays)
    print(f"📦 FAYS Stok Hareketleri ({len(df_fays_lines)} kayıt):")
    print(df_fays_lines.to_string(index=False))
    print()
    
    # FAYS Stok Durumu (Toplam)
    query = """
    SELECT 
        RTRIM(LTRIM(LN.StokKodu)) AS [Ürün Kodu],
        RTRIM(LTRIM(LN.UrunGrup1)) AS [Ürün Adı],
        RTRIM(LTRIM(LN.Depo)) AS [Depo],
        SUM(CASE WHEN FS.GirisCikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) AS [FAYS Stok]
    FROM stk_Fis AS FS
    INNER JOIN stk_FisLines AS LN ON LN.Link_FisNo = FS.FisNo
    GROUP BY LN.StokKodu, LN.UrunGrup1, LN.Depo
    HAVING SUM(CASE WHEN FS.GirisCikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) <> 0
    ORDER BY LN.StokKodu
    """
    df_fays_stock = pd.read_sql(query, conn_fays)
    print(f"📊 FAYS Stok Durumu ({len(df_fays_stock)} kayıt):")
    print(df_fays_stock.to_string(index=False))
    print()
    
    conn_fays.close()
    
    # Test 3: Karşılaştırma
    print("="*70)
    print("📊 Test 3: Stok Karşılaştırması")
    print("="*70 + "\n")
    
    # Her iki veritabanına bağlanıp karşılaştırma sorgusu çalıştır
    conn_fays = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE_FAYS
    )
    
    # Ana karşılaştırma sorgusu
    comparison_query = """
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
        SELECT     
            [AMBAR ADI] = AMBARLAR.NAME, 
            ITEMS.CODE AS [MALZEME KODU], 
            RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
            ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
            ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
            0 AS [FAYS STOK]
        FROM         
            GOLD..LG_013_ITEMS AS ITEMS
            INNER JOIN GOLD..LV_013_01_STINVTOT AS ST ON ST.STOCKREF = ITEMS.LOGICALREF 
            LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013' 
        WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
        GROUP BY ITEMS.CODE, ITEMS.NAME, ITEMS.STGRPCODE, ST.INVENNO, AMBARLAR.NAME
        
        UNION ALL
        
        SELECT    
            CAST(A.DEPO AS VARCHAR(50)) AS [AMBAR ADI],
            CAST(A.StokKodu AS VARCHAR(50)) AS MALZEME_KODU, 
            RTRIM(LTRIM(CAST(A.STOK_ADI AS VARCHAR(50)))) AS MALZEME_ADI,
            A.[GRUP KODU] AS [GRUP KODU],
            0 AS [FİİLİ STOK],
            ROUND(ISNULL(SUM(A.GIRIS_TOPLAM),0),2) - ROUND(ISNULL(SUM(A.CIKIS_TOPLAM),0),2) AS FAYS_MIKTAR
        FROM         
        (
            SELECT     
                FL.Depo AS DEPO,
                FL.StokKodu, 
                FL.UrunGrup1 AS STOK_ADI,
                I.STGRPCODE AS [GRUP KODU],
                CASE F.GirisCikis 
                    WHEN 1 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) 
                    ELSE 0 
                END AS GIRIS_TOPLAM,
                CASE F.GirisCikis 
                    WHEN 2 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) 
                    ELSE 0 
                END AS CIKIS_TOPLAM
            FROM          
                dbo.stk_Fis AS F
                INNER JOIN stk_FisLines AS FL ON F.FisNo = FL.Link_FisNo 
                LEFT OUTER JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=FL.StokKodu
            GROUP BY FL.Depo, FL.StokKodu, FL.UrunGrup1, I.STGRPCODE, F.GirisCikis
        ) AS A
        GROUP BY A.DEPO, A.STOKKODU, A.STOK_ADI, A.[GRUP KODU]
    ) X
    GROUP BY X.[MALZEME KODU], X.[MALZEME ADI], X.[GRUP KODU], X.[AMBAR ADI]
    HAVING ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) <> 0
    ORDER BY X.[MALZEME KODU]
    """
    
    df_comparison = pd.read_sql(comparison_query, conn_fays)
    
    if len(df_comparison) > 0:
        print(f"⚠️  Stok Farkları Bulundu! ({len(df_comparison)} kalem)\n")
        print(df_comparison.to_string(index=False))
        print()
        
        # İstatistikler
        print("📈 İstatistikler:")
        print("-" * 70)
        
        fazla = df_comparison[df_comparison['FARK'] > 0]
        eksik = df_comparison[df_comparison['FARK'] < 0]
        
        print(f"\n🔴 FAYS FAZLA (Logo'da eksik): {len(fazla)} kalem")
        if len(fazla) > 0:
            print("   → Sayım Eksiği Fişi Gerekli (FisTuru=51, Çıkış)")
            for _, row in fazla.iterrows():
                print(f"      • {row['MALZEME KODU']}: +{row['FARK']:.2f} (LOGO:{row['LOGO FİİLİ STOK']:.2f}, FAYS:{row['FAYS STOK']:.2f})")
        
        print(f"\n🟢 FAYS EKSİK (Logo'da fazla): {len(eksik)} kalem")
        if len(eksik) > 0:
            print("   → Sayım Fazlası Fişi Gerekli (FisTuru=50, Giriş)")
            for _, row in eksik.iterrows():
                print(f"      • {row['MALZEME KODU']}: {row['FARK']:.2f} (LOGO:{row['LOGO FİİLİ STOK']:.2f}, FAYS:{row['FAYS STOK']:.2f})")
        
        print(f"\n💡 Eşitleme İşlemi:")
        print(f"   • {2 if len(fazla) > 0 and len(eksik) > 0 else 1} adet fiş oluşturulacak")
        print(f"   • Toplam {len(df_comparison)} kalem işlenecek")
        
    else:
        print("✅ Harika! Tüm stoklar eşit - Fark yok!")
    
    conn_fays.close()
    
    # Test 4: FisNo Kontrolü
    print("\n" + "="*70)
    print("📊 Test 4: FisNo Yönetimi")
    print("="*70 + "\n")
    
    conn_fays = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE_FAYS
    )
    
    query = "SELECT Link_Numarasi, Deger FROM yr_BilgiLines WHERE Link_Numarasi = 99102"
    df_fisno = pd.read_sql(query, conn_fays)
    
    if len(df_fisno) > 0:
        current_fisno = df_fisno.iloc[0]['Deger']
        print(f"✅ FisNo Yönetimi Aktif")
        print(f"   Mevcut FisNo: {current_fisno}")
        print(f"   Sonraki FisNo: {current_fisno + 1}")
    else:
        print("⚠️  FisNo kaydı bulunamadı!")
    
    conn_fays.close()
    
    # Özet
    print("\n" + "="*70)
    print("✅ TEST BAŞARILI - Tüm Kontroller Tamamlandı!")
    print("="*70)
    print(f"\n📅 Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 Sonraki Adımlar:")
    print("   1. Windows Server'a programı aktarın")
    print("   2. ODBC Driver 17 kurun")
    print("   3. main.py ile tam programı çalıştırın")
    print("   4. Stok eşitleme yapın")
    print("\n🎯 Test veritabanı hazır ve çalışıyor!")
    
except pymssql.Error as e:
    print(f"\n❌ SQL Server Hatası:")
    print(f"   {e}")
    print("\n💡 Kontrol Edin:")
    print("   • Docker container çalışıyor mu: docker ps")
    print("   • Port açık mı: docker port sqlserver-container")
    print("   • Şifre doğru mu: E123456.")
    
except Exception as e:
    print(f"\n❌ Hata: {e}")
    import traceback
    traceback.print_exc()

print("\n")

