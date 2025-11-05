#!/usr/bin/env python3
"""
Basit Test Programı - Veritabanı Bağlantısını Test Eder
"""
import sys
import os

# config_local'ı yükle
try:
    import config_local
    print("✅ Test konfigürasyonu yüklendi")
except ImportError:
    print("⚠️  config_local bulunamadı, varsayılan ayarlar kullanılacak")

from config import Config
from database import DatabaseManager
from stock_sync_engine import StockSyncEngine

print("\n" + "="*60)
print("LOGO - FAYS WMS Stok Eşitleme - Test Programı")
print("="*60 + "\n")

# Bağlantı bilgilerini göster
print("📋 Bağlantı Bilgileri:")
print(f"   Server: {Config.DB_SERVER}")
print(f"   LOGO DB: {Config.DB_LOGO}")
print(f"   FAYS DB: {Config.DB_FAYS}")
print(f"   User: {Config.DB_USER}")
print()

# Veritabanına bağlan
print("🔌 Veritabanına bağlanılıyor...")
db = DatabaseManager()

try:
    success = db.connect()
    
    if success:
        print("✅ Bağlantı başarılı!\n")
        
        # Test 1: LOGO Stok Sayısı
        print("📊 Test 1: LOGO Stok Kartları")
        try:
            query = "SELECT COUNT(*) as Adet FROM GOLD..LG_013_ITEMS"
            result = db.execute_query(query, database='LOGO')
            print(f"   ✓ Toplam {result.iloc[0]['Adet']} stok kartı bulundu\n")
        except Exception as e:
            print(f"   ✗ Hata: {e}\n")
        
        # Test 2: FAYS Stok Sayısı
        print("📊 Test 2: FAYS Stok Hareketleri")
        try:
            query = "SELECT COUNT(*) as Adet FROM stk_FisLines"
            result = db.execute_query(query, database='FAYS')
            print(f"   ✓ Toplam {result.iloc[0]['Adet']} hareket bulundu\n")
        except Exception as e:
            print(f"   ✗ Hata: {e}\n")
        
        # Test 3: Stok Karşılaştırma
        print("📊 Test 3: Stok Karşılaştırması")
        try:
            engine = StockSyncEngine(db)
            df = engine.compare_stocks(warehouse='MERKEZ')
            
            if len(df) > 0:
                print(f"   ✓ {len(df)} adet fark bulundu:\n")
                print(df[['MALZEME KODU', 'MALZEME ADI', 'LOGO FİİLİ STOK', 'FAYS STOK', 'FARK']].to_string(index=False))
                print()
                
                # İstatistikler
                fazla = len(df[df['FARK'] > 0])
                eksik = len(df[df['FARK'] < 0])
                print(f"\n   📈 İstatistik:")
                print(f"      🔴 FAYS Fazla: {fazla} kalem")
                print(f"      🟢 FAYS Eksik: {eksik} kalem")
            else:
                print("   ✓ Stoklar eşit, fark yok!")
        except Exception as e:
            print(f"   ✗ Hata: {e}\n")
        
        # Test 4: Depo Listesi
        print("\n📊 Test 4: Depo Listesi")
        try:
            warehouses = engine.get_warehouses()
            print(f"   ✓ {len(warehouses)} adet depo bulundu:")
            for w in warehouses:
                print(f"      • {w}")
        except Exception as e:
            print(f"   ✗ Hata: {e}\n")
        
        print("\n" + "="*60)
        print("✅ Tüm testler tamamlandı!")
        print("="*60)
        
        db.disconnect()
        
    else:
        print("❌ Bağlantı başarısız!")
        print("\n💡 Çözüm Önerileri:")
        print("   1. Docker SQL Server'ın çalıştığını kontrol edin:")
        print("      docker ps | grep sqlserver")
        print("   2. Bağlantı bilgilerini kontrol edin (config_local.py)")
        print("   3. Azure Data Studio ile bağlantı test edin")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ Hata oluştu: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

