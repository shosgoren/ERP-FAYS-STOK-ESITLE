# 🍎 macOS'ta Test Etme Kılavuzu

## ⚠️ Önemli Bilgi

Bu program **Windows Server** için tasarlanmıştır ve **ODBC Driver 17 for SQL Server** gerektirir. 

macOS'ta:
- ❌ Ana program çalışmaz (ODBC driver uyumsuz)
- ✅ Azure Data Studio ile veritabanı testleri yapılabilir
- ✅ Kod yapısı incelenebilir
- ✅ Windows'a aktarılıp çalıştırılabilir

---

## ✅ macOS'ta Yapabilecekleriniz

### 1️⃣ Azure Data Studio ile SQL Testleri (ÖNERİLEN)

#### Adım 1: Azure Data Studio'yu Açın

#### Adım 2: Yeni Bağlantı Oluşturun

**File → New Connection** veya **⌘+N**

```
Connection Details:
├─ Connection type: Microsoft SQL Server
├─ Server: localhost,1433
├─ Authentication type: SQL Login
├─ User name: sa
├─ Password: E123456.
├─ Database: <Default>
├─ Encrypt: Optional
└─ Trust server certificate: ✅ Yes (MUTLAKA İŞARETLEYİN!)
```

#### Adım 3: Test Et

**Connect** butonuna tıklayın. Başarılıysa ✅ yeşil işaret göreceksiniz.

#### Adım 4: Test Sorgularını Çalıştırın

1. **File → Open File** → `test_queries.sql` dosyasını açın

2. **Sorgu 3: KARŞILAŞTIRMA** bölümünü seçin (USE FaysWMSAkturk'tan başlayan)

3. **▶ Run** butonuna tıklayın veya **F5**

#### Beklenen Sonuç:

```
MALZEME KODU  LOGO FİİLİ STOK  FAYS STOK  FARK
61007030      100.00            120.00     +20.00
343403022     75.00             60.00      -15.00
TEST001       200.00            180.00     -20.00
TEST002       0.00              30.00      +30.00
```

**4 satır fark bulmalısınız!** ✅

---

### 2️⃣ Veritabanı Yapısını İnceleyin

Azure Data Studio'da sol tarafta **Databases** altında:

```
📂 GOLD
  └─ Tables
      ├─ dbo.LG_013_ITEMS (Stok Kartları)
      ├─ dbo.LV_013_01_STINVTOT (Stok Durumu)
      └─ dbo.L_CAPIWHOUSE (Depolar)

📂 FaysWMSAkturk
  └─ Tables
      ├─ dbo.stk_Fis (Ana Fiş)
      ├─ dbo.stk_FisLines (Fiş Satırları)
      └─ dbo.yr_BilgiLines (FisNo Yönetimi)
```

Tablolara sağ tık → **Select Top 1000** ile verileri görün.

---

### 3️⃣ Özel Sorgular Yazın

Azure Data Studio'da yeni sorgu penceresi açıp test yapın:

#### LOGO Stokları:
```sql
USE GOLD;

SELECT 
    CODE AS [Ürün Kodu],
    NAME AS [Ürün Adı],
    STGRPCODE AS [Grup]
FROM LG_013_ITEMS;
```

#### FAYS Stokları:
```sql
USE FaysWMSAkturk;

SELECT 
    StokKodu,
    UrunGrup1,
    NetMiktar,
    Depo
FROM stk_FisLines;
```

---

## 📊 Test Senaryoları

### Senaryo 1: Basit Kontrol ✅
```sql
-- LOGO'da kaç stok var?
USE GOLD;
SELECT COUNT(*) FROM LG_013_ITEMS;
-- Sonuç: 5

-- FAYS'da kaç hareket var?
USE FaysWMSAkturk;
SELECT COUNT(*) FROM stk_FisLines;
-- Sonuç: 5
```

### Senaryo 2: Stok Karşılaştırma ✅
`test_queries.sql` dosyasındaki 3. sorguyu çalıştırın.
4 fark bulmalısınız.

### Senaryo 3: Depo Kontrolü ✅
```sql
USE GOLD;
SELECT * FROM L_CAPIWHOUSE WHERE FIRMNR = '013';
-- MERKEZ, ŞUBE-1, ŞUBE-2 görmeli
```

---

## 🚀 Windows'ta Tam Test

Program Windows'ta tam çalışır. Windows'a aktarmak için:

### Adım 1: Proje Klasörünü Kopyalayın
```
ERP Stok Esitle/ klasörünü Windows'a USB veya ağ üzerinden kopyalayın
```

### Adım 2: Windows'ta Python Kurun
```
https://www.python.org/downloads/
Python 3.8+ sürümü
"Add to PATH" seçeneğini işaretleyin ✅
```

### Adım 3: ODBC Driver Kurun
```
https://aka.ms/downloadmsodbcsql
ODBC Driver 17 for SQL Server (x64)
```

### Adım 4: Paketleri Yükleyin
```cmd
cd "C:\StokEsitleme"
pip install -r requirements.txt
```

### Adım 5: .env Dosyası Oluşturun
```
DB_SERVER=localhost,1433
DB_LOGO=GOLD
DB_FAYS=FaysWMSAkturk
DB_USER=sa
DB_PASSWORD=E123456.
DB_DRIVER=ODBC Driver 17 for SQL Server
DEFAULT_WAREHOUSE=MERKEZ
```

### Adım 6: Programı Çalıştırın
```cmd
python main.py

VEYA

run.bat (çift tıklama)
```

---

## 📱 Program Arayüzü (Windows'ta)

Windows'ta program açıldığında görecekleriniz:

```
┌─────────────────────────────────────────────────────┐
│ STOK EŞİTLEME SİSTEMİ                     v1.0.0   │
│                                                     │
│ ● Bağlı                                            │
│                                                     │
│ [🔌 Bağlan]                                        │
│ [📊 Karşılaştır]                                   │
│ [🔄 Eşitle]                                        │
│                                                     │
│ ┌───────────────────────────────────────────────┐  │
│ │ Bağlantı | Karşılaştırma | Eşitleme | SQL   │  │
│ ├───────────────────────────────────────────────┤  │
│ │                                               │  │
│ │  [Burada içerik görünür]                     │  │
│ │                                               │  │
│ └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🎥 Demo Video (Hayal Edin)

**Bağlantı Sekmesi:**
1. Bilgileri girin
2. "Bağlan" tıklayın
3. ✅ Yeşil "Bağlı" göreceksiniz

**Karşılaştırma Sekmesi:**
1. Depo: MERKEZ
2. "Karşılaştır" tıklayın
3. 📊 Tabloda 4 fark göreceksiniz
4. "Excel'e Aktar" ile kaydedin

**Eşitleme Sekmesi:**
1. Depo: MERKEZ
2. "Önizleme Yap" → 2 fiş oluşturulacağını görün
3. "EŞİTLEMEYİ BAŞLAT" → Onaylayın
4. ✅ Başarılı mesajı

**Sonuç:**
- Tekrar karşılaştırınca 0 fark!
- FAYS stokları LOGO'ya eşitlendi

---

## 💡 İpuçları

### macOS'ta:
✅ Azure Data Studio ile SQL testleri yapın
✅ Kod yapısını inceleyin
✅ Dokümantasyonu okuyun
❌ Ana programı çalıştırmayın (çalışmaz)

### Windows'ta:
✅ Her şey çalışır
✅ Tam test yapabilirsiniz
✅ Canlı veritabanına bağlanabilirsiniz

---

## 📞 Sorun Giderme

### Azure Data Studio bağlanmıyor?

**1. Docker container çalışıyor mu?**
```bash
docker ps | grep sqlserver
```

**2. Port açık mı?**
```bash
docker port sqlserver-container
# 1433/tcp -> 0.0.0.0:1433 görmeli
```

**3. Trust Server Certificate işaretli mi?**
Bağlantı ayarlarında mutlaka ✅ olmalı!

**4. Şifre doğru mu?**
`E123456.` (sonunda nokta var!)

---

## ✅ Başarı Kriterleri

### macOS'ta Test Başarılı Sayılır:
- [x] Docker SQL Server çalışıyor
- [x] Azure Data Studio bağlanıyor
- [x] test_queries.sql çalışıyor
- [x] 4 fark kaydı bulundu
- [x] Tablolar görüntüleniyor

### Windows'ta Test Başarılı Sayılır:
- [ ] Program arayüzü açılıyor
- [ ] Veritabanına bağlanıyor
- [ ] Karşılaştırma yapılıyor
- [ ] Eşitleme yapılıyor
- [ ] Fişler oluşturuluyor
- [ ] Loglar yazılıyor

---

**Şu anda Azure Data Studio ile test edebilirsiniz!** 🚀

**Dosya:** `test_queries.sql`  
**Bağlantı:** `localhost,1433` / `sa` / `E123456.`  
**Beklenen Sonuç:** 4 fark kaydı

