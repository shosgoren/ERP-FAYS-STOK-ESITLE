# LOGO - FAYS WMS Stok Eşitleme Programı

Modern ve kullanıcı dostu Windows masaüstü uygulaması ile LOGO ERP ve FAYS WMS veritabanları arasındaki stok farklarını tespit edin ve otomatik eşitleyin.

## 🎯 Özellikler

### ✨ Ana Özellikler
- **Gerçek Zamanlı Stok Karşılaştırma**: LOGO ERP ve FAYS WMS stokları arasındaki farkları anında tespit edin
- **Otomatik Stok Eşitleme**: LOGO ERP'deki doğru stok değerlerine göre FAYS WMS'i otomatik eşitleyin
- **Akıllı Fiş Oluşturma**: Farkları otomatik olarak sayım fazlası/eksiği fişlerine dönüştürün
- **SQL Sorgu Editörü**: Karşılaştırma sorgularını kendi ihtiyacınıza göre düzenleyin
- **Excel Rapor**: Sonuçları Excel formatında dışa aktarın

### 🎨 Modern Arayüz
- **Karanlık/Aydınlık Tema**: Göz yorgunluğunu azaltan modern tema desteği
- **Kolay Navigasyon**: Tab bazlı kullanıcı dostu arayüz
- **Görsel Geri Bildirim**: Renkli durum göstergeleri ve ilerleme bildirimleri
- **Responsive Tasarım**: Farklı ekran çözünürlüklerine uyumlu

### 🔒 Güvenlik
- **Bağlantı Testi**: Veritabanı bağlantılarını kullanmadan önce test edin
- **Onay Mekanizması**: Kritik işlemler için çift onay
- **Detaylı Loglama**: Tüm işlemler kaydedilir

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **İşletim Sistemi**: Windows Server 2012+ veya Windows 10+
- **Python**: 3.8 veya üzeri
- **Bellek**: Minimum 4 GB RAM
- **Disk**: 100 MB boş alan

### Veritabanı Gereksinimleri
- **SQL Server**: Azure SQL Database veya SQL Server 2012+
- **ODBC Driver**: ODBC Driver 17 for SQL Server
- **Bağlantı**: GOLD (LOGO) ve FaysWMSAkturk veritabanlarına erişim

## 🚀 Kurulum

### 1. Python Kurulumu
Windows için Python 3.8+ sürümünü indirin ve kurun:
```
https://www.python.org/downloads/
```

Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin.

### 2. ODBC Driver Kurulumu
Microsoft ODBC Driver 17 for SQL Server'ı indirin ve kurun:
```
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### 3. Proje Dosyalarını İndirin
Proje klasörünü bilgisayarınıza kopyalayın.

### 4. Gerekli Paketleri Yükleyin
Komut satırını (CMD) açın ve proje klasörüne gidin:
```bash
cd "C:\Users\...\ERP Stok Esitle"
```

Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

### 5. Yapılandırma
Proje klasöründe `.env` dosyası oluşturun:

```env
# Azure SQL Server Bağlantı Bilgileri
DB_SERVER=your_server.database.windows.net
DB_LOGO=GOLD
DB_FAYS=FaysWMSAkturk
DB_USER=your_username
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

# Uygulama Ayarları
APP_TITLE=LOGO - FAYS WMS Stok Eşitleme
DEFAULT_WAREHOUSE=MERKEZ
LOG_LEVEL=INFO
```

**Önemli**: `.env` dosyasındaki bilgileri kendi veritabanı bilgilerinizle güncelleyin!

## 💻 Kullanım

### Programı Başlatma
```bash
python main.py
```

### İlk Kullanım

#### 1. Veritabanı Bağlantısı
- **"Bağlantı"** sekmesine gidin
- Veritabanı bilgilerinizi girin
- **"Bağlan"** butonuna tıklayın
- Bağlantıyı test etmek için **"Bağlantıyı Test Et"** butonunu kullanın

#### 2. Stok Karşılaştırma
- **"Stok Karşılaştırma"** sekmesine gidin
- Depo seçin (veya "Tümü" seçin)
- **"Karşılaştır"** butonuna tıklayın
- Sonuçları inceleyin
- İsterseniz **"Excel'e Aktar"** ile kaydedin

#### 3. Stok Eşitleme
- **"Stok Eşitleme"** sekmesine gidin
- Eşitlenecek depoyu seçin
- **"Önizleme Yap"** ile değişiklikleri görün
- **"EŞİTLEMEYİ BAŞLAT"** ile işlemi başlatın
- Onay verin ve sonuçları inceleyin

## 🔧 İşleyiş Mantığı

### Stok Karşılaştırma
Program, LOGO ERP ve FAYS WMS stokları arasındaki farkları tespit eder:

```
FARK = FAYS STOK - LOGO FİİLİ STOK

FARK > 0  ⟹  FAYS FAZLA (Logo'da eksik var)
FARK < 0  ⟹  FAYS EKSİK (Logo'da fazla var)
FARK = 0  ⟹  STOKLAR EŞİT
```

### Otomatik Fiş Oluşturma

#### FAYS Fazla Durumu (FARK > 0)
- **Fiş Türü**: 51 (Sayım Eksiği)
- **İşlem**: Çıkış (GirisCikis=2)
- **Amaç**: FAYS stokunu azaltarak LOGO'ya eşitlemek

#### FAYS Eksik Durumu (FARK < 0)
- **Fiş Türü**: 50 (Sayım Fazlası)
- **İşlem**: Giriş (GirisCikis=1)
- **Amaç**: FAYS stokunu artırarak LOGO'ya eşitlemek

### Fiş Numarası Yönetimi
- FisNo, `yr_BilgiLines` tablosundan otomatik alınır (Link_Numarası=99102)
- Her fiş oluşturulduğunda numara otomatik artırılır
- stk_Fis ve stk_FisLines tabloları otomatik doldurulur

## 📊 SQL Sorguları

### Varsayılan Karşılaştırma Sorgusu
Program, iki veritabanındaki stokları karşılaştırmak için aşağıdaki mantığı kullanır:

1. **LOGO ERP Stokları**: `GOLD..LG_013_ITEMS` ve `LV_013_01_STINVTOT` tablolarından
2. **FAYS WMS Stokları**: `stk_Fis` ve `stk_FisLines` tablolarından
3. **UNION ALL** ile birleştirilip farklar hesaplanır

### Özel Sorgu Kullanımı
**"SQL Sorguları"** sekmesinde kendi özel sorgularınızı yazabilir ve test edebilirsiniz.

## 🛡️ Güvenlik Uyarıları

### ⚠️ ÖNEMLİ UYARILAR

1. **Yedek Alın**: Eşitleme işleminden önce MUTLAKA veritabanı yedeği alın!
2. **Test Edin**: Önce test ortamında deneyin
3. **Önizleme Yapın**: Eşitleme öncesi mutlaka önizleme yapın
4. **Depo Kontrolü**: Doğru depoyu seçtiğinizden emin olun
5. **Geri Alınamaz**: Eşitleme işlemi geri alınamaz!

### Yetkilendirme
Program için gerekli veritabanı yetkileri:
- **LOGO (GOLD)**: READ yetkisi
- **FAYS (FaysWMSAkturk)**: READ/WRITE yetkisi
  - stk_Fis (INSERT)
  - stk_FisLines (INSERT)
  - yr_BilgiLines (UPDATE)

## 📝 Log Dosyaları

Tüm işlemler `stok_esitleme.log` dosyasına kaydedilir:
- Bağlantı durumları
- Karşılaştırma sonuçları
- Oluşturulan fişler
- Hata mesajları

Log seviyesi `.env` dosyasından ayarlanabilir:
```
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## 🐛 Sorun Giderme

### Bağlantı Hataları
**Sorun**: "Veritabanına bağlanılamadı" hatası
**Çözüm**:
- SQL Server adresini kontrol edin
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- ODBC Driver'ın kurulu olduğunu doğrulayın
- Güvenlik duvarı ayarlarını kontrol edin

### ODBC Driver Hatası
**Sorun**: "ODBC Driver bulunamadı" hatası
**Çözüm**:
- ODBC Driver 17'yi yükleyin
- Veya `.env` dosyasında farklı bir driver adı deneyin:
  ```
  DB_DRIVER=SQL Server
  ```

### Import Hataları
**Sorun**: "ModuleNotFoundError" hatası
**Çözüm**:
```bash
pip install -r requirements.txt --upgrade
```

### Yetki Hataları
**Sorun**: "Permission denied" hatası
**Çözüm**:
- Veritabanı kullanıcısının gerekli yetkilere sahip olduğundan emin olun
- DBA ile iletişime geçin

## 🎓 Teknik Detaylar

### Kullanılan Teknolojiler
- **Python 3.8+**: Ana programlama dili
- **CustomTkinter**: Modern UI framework
- **PyODBC**: SQL Server bağlantısı
- **Pandas**: Veri işleme ve analiz
- **OpenPyXL**: Excel export

### Proje Yapısı
```
ERP Stok Esitle/
│
├── main.py                 # Ana uygulama
├── config.py              # Konfigürasyon yönetimi
├── database.py            # Veritabanı işlemleri
├── stock_sync_engine.py   # Stok eşitleme motoru
├── ui_components.py       # UI bileşenleri
│
├── requirements.txt       # Python paketleri
├── .env                  # Yapılandırma dosyası (oluşturulacak)
├── README.md             # Bu dosya
│
└── stok_esitleme.log     # Log dosyası (otomatik oluşur)
```

### Veritabanı Tabloları

#### stk_Fis (Ana Fiş Tablosu)
- **FisTuru**: 50=Sayım Fazlası, 51=Sayım Eksiği
- **GirisCikis**: 1=Giriş, 2=Çıkış
- **FisNo**: Benzersiz fiş numarası

#### stk_FisLines (Fiş Satırları)
- **Link_FisNo**: Ana fişe bağlantı
- **StokKodu**: Malzeme kodu
- **NetMiktar**: Hareket miktarı
- **Depo**: Depo adı

#### yr_BilgiLines (Numara Yönetimi)
- **Link_Numarasi**: 99102
- **Deger**: Sıradaki FisNo

## 📞 Destek

### Sık Sorulan Sorular

**S: Program Windows Server'da çalışır mı?**
C: Evet, Windows Server 2012 ve üzeri sürümlerde sorunsuz çalışır.

**S: Eşitleme geri alınabilir mi?**
C: Hayır, bu yüzden önce önizleme yapın ve test ortamında deneyin.

**S: Birden fazla depoyu aynı anda eşitleyebilir miyim?**
C: Şu anda tek seferde bir depo eşitlenebilir. Her depo için işlemi tekrarlayın.

**S: SQL sorgularını değiştirebilir miyim?**
C: Evet, "SQL Sorguları" sekmesinde özel sorgular yazabilir ve test edebilirsiniz.

## 📄 Lisans

Bu proje özel kullanım için geliştirilmiştir.

## 🔄 Versiyon Geçmişi

### v1.0.0 (2025-11-05)
- ✨ İlk sürüm
- ✅ LOGO - FAYS stok karşılaştırma
- ✅ Otomatik eşitleme
- ✅ Modern UI
- ✅ SQL sorgu editörü
- ✅ Excel export

## 💡 İpuçları

### Performans
- Büyük veritabanları için karşılaştırmalar birkaç dakika sürebilir
- Sadece ihtiyacınız olan depoyu seçin
- Logları düzenli olarak temizleyin

### Güvenlik
- `.env` dosyasını paylaşmayın
- Düzenli şifre değiştirin
- Sadece gerekli yetkileri verin

### Bakım
- Log dosyasını düzenli kontrol edin
- Aylık yedek alın
- Python ve paketleri güncel tutun

---

**Not**: Bu program LOGO ERP ve FAYS WMS entegrasyonu için özel olarak geliştirilmiştir. Kullanmadan önce test ortamında denemeniz önerilir.

**Geliştirici Notu**: Herhangi bir sorun veya özellik talebi için lütfen geliştirici ile iletişime geçin.

