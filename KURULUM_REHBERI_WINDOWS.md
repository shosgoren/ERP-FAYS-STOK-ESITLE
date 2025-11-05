# 🚀 Windows Server Kurulum Rehberi

## TAM PAKET İÇERİĞİ

Masaüstünüzdeki `StokEsitleme-Tam-Paket.tar.gz` dosyası:

✅ Tüm kaynak kodlar
✅ SQL stored procedures  
✅ Dokümantasyon
✅ Otomatik kurulum scriptleri
✅ Demo versiyonu
✅ Test veritabanı scriptleri

---

## 🎯 3 KOLAY YÖNTEM

### YÖNTEM 1: WinPython (ÖNERİLEN - 10 Dakika)

#### Adım 1: WinPython İndirin
```
https://github.com/winpython/winpython/releases/latest
İndirin: Winpython64-3.11.x.exe (~400 MB)
```

#### Adım 2: Kurulum
1. İndirilen dosyayı çalıştırın
2. **Extract** → `C:\WinPython`
3. Bekleyin (2-3 dakika)

#### Adım 3: Proje Dosyalarını Açın
1. `StokEsitleme-Tam-Paket.tar.gz` dosyasını 7-Zip ile açın
2. İçindekileri `C:\StokEsitleme` klasörüne çıkartın

#### Adım 4: .env Dosyası Oluşturun
`C:\StokEsitleme\.env` dosyası oluşturun:

```
DB_SERVER=your_server.database.windows.net
DB_LOGO=GOLD
DB_FAYS=FaysWMSAkturk
DB_USER=sa
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server
DEFAULT_WAREHOUSE=MERKEZ
LOG_LEVEL=INFO
```

#### Adım 5: Paketleri Kurun
CMD açın:
```cmd
C:\WinPython\WPy64-xxxx\scripts\env.bat
cd C:\StokEsitleme
pip install -r requirements.txt
```

#### Adım 6: Çalıştırın!
`CALISTIR.bat` oluşturun:
```bat
@echo off
C:\WinPython\WPy64-xxxx\python.exe C:\StokEsitleme\main.py
pause
```

**Çift tıklayın!** ✅

---

### YÖNTEM 2: SQL-Only (Python GEREKMİYOR!)

#### Adım 1: Proje Açın
`StokEsitleme-Tam-Paket.tar.gz` → `sql_stored_procedures.sql` dosyasını bulun

#### Adım 2: Azure Data Studio
1. Azure Data Studio açın
2. Sunucunuza bağlanın
3. `sql_stored_procedures.sql` dosyasını açın
4. F5 ile çalıştırın

#### Adım 3: Kullanın!
```sql
-- Karşılaştırma
EXEC sp_StokKarsilastirma 'MERKEZ'

-- Eşitleme
EXEC sp_StokEsitleme 'MERKEZ'
```

**ÇALIŞTI!** ✅

---

### YÖNTEM 3: Normal Python (Eğer Zaten Kuruluysa)

```cmd
cd C:\StokEsitleme
pip install -r requirements.txt
python main.py
```

---

## 📁 Paket İçeriği

```
StokEsitleme-Tam-Paket/
├── Ana Program
│   ├── main.py                          - Ana uygulama
│   ├── config.py                        - Ayarlar
│   ├── database.py                      - Veritabanı
│   ├── stock_sync_engine.py             - Eşitleme motoru
│   └── ui_components.py                 - Arayüz
│
├── Python Olmadan Çalıştırma
│   ├── sql_stored_procedures.sql        - SQL çözümü
│   ├── WINDOWS_HAZIR_PAKET.bat          - Otomatik kurulum
│   └── PYTHON_OLMADAN_CALISTIRMA.md     - Kılavuz
│
├── Dokümantasyon
│   ├── README.md                        - Genel bilgi
│   ├── KURULUM.md                       - Kurulum
│   ├── KULLANIM.md                      - Kullanım
│   ├── EN_KOLAY_YONTEM.md               - Hızlı başlangıç
│   └── HIZLI_EXE_OLUSTURMA.md           - EXE build
│
├── Test ve Demo
│   ├── demo_app.py                      - Demo arayüz
│   ├── simple_test.py                   - Terminal test
│   ├── test_program.py                  - Veritabanı test
│   ├── setup_test_db.sql                - Test DB kurulum
│   └── test_queries.sql                 - Test sorguları
│
└── Diğer
    ├── requirements.txt                 - Python paketleri
    ├── env_example.txt                  - Ayar örneği
    └── .gitignore
```

---

## 🎯 HANGİSİNİ SEÇMELİYİM?

| Durum | Çözüm | Süre |
|-------|-------|------|
| Python kurulu DEĞİL | WinPython | 10 dk |
| Python kurulu | Normal Python | 5 dk |
| Python istemiyorum | SQL-Only | 0 dk |
| Sadece test | demo_app.py | 1 dk |

---

## 🔧 Sorun Giderme

### Hata: "ODBC Driver bulunamadı"

**Çözüm 1:** ODBC Driver 17 kurun
```
https://aka.ms/downloadmsodbcsql
```

**Çözüm 2:** SQL-Only yöntemini kullanın
```sql
EXEC sp_StokKarsilastirma 'MERKEZ'
```

### Hata: "ModuleNotFoundError"

```cmd
pip install -r requirements.txt
```

### Hata: "Bağlantı hatası"

1. SQL Server çalışıyor mu?
2. .env dosyası doğru mu?
3. Güvenlik duvarı açık mı?

---

## ✅ BAŞARIYLA KURULDU!

Artık:
- ✅ Modern GUI ile stok karşılaştırma
- ✅ Otomatik eşitleme
- ✅ Excel export
- ✅ SQL sorgu editörü

Tüm özellikler kullanıma hazır! 🎉

---

## 📞 YARDIM

Sorun yaşarsanız:
1. `stok_esitleme.log` dosyasını kontrol edin
2. Dokümantasyonları okuyun
3. SQL-Only yöntemini deneyin (garanti çalışır!)

---

**NOT:** GitHub token'ınızı iptal etmeyi unutmayın! 🔴

