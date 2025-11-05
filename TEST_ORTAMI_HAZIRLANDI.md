# 🎉 Test Ortamı Hazır!

## ✅ Tamamlanan Adımlar

### 1. Docker SQL Server
- ✅ SQL Server container çalışıyor: `sqlserver-container`
- ✅ Port: `localhost:1433`
- ✅ Kullanıcı: `sa`
- ✅ Şifre: `E123456.`

### 2. Test Veritabanları Oluşturuldu

#### GOLD (LOGO ERP)
- ✅ 5 Stok kartı
- ✅ 5 Stok durumu kaydı
- ✅ 3 Depo (MERKEZ, ŞUBE-1, ŞUBE-2)

#### FaysWMSAkturk (FAYS WMS)
- ✅ 1 Giriş fişi
- ✅ 5 Stok hareketi
- ✅ FisNo yönetimi (yr_BilgiLines)

### 3. Test Verileri

| Stok Kodu | LOGO Stok | FAYS Stok | Fark | Durum |
|-----------|-----------|-----------|------|-------|
| 61007030 | 100 | 120 | +20 | 🔴 FAYS FAZLA → Sayım Eksiği Fişi Gerekli |
| 509V0004 | 56 | 56 | 0 | ✅ EŞİT |
| 343403022 | 75 | 60 | -15 | 🟢 FAYS EKSİK → Sayım Fazlası Fişi Gerekli |
| TEST001 | 200 | 180 | -20 | 🟢 FAYS EKSİK → Sayım Fazlası Fişi Gerekli |
| TEST002 | 0 | 30 | +30 | 🔴 FAYS FAZLA → Sayım Eksiği Fişi Gerekli |

**Beklenen Eşitleme Sonucu:**
- 1 adet Sayım Eksiği Fişi (FisTuru=51) → 61007030 ve TEST002 için
- 1 adet Sayım Fazlası Fişi (FisTuru=50) → 343403022 ve TEST001 için

---

## 🚀 Nasıl Test Edilir?

### Yöntem 1: Azure Data Studio (ÖNERİLEN - macOS için)

1. **Azure Data Studio'yu açın**

2. **Bağlantı oluşturun:**
   ```
   Server: localhost,1433
   Authentication type: SQL Login
   User name: sa
   Password: E123456.
   Encrypt: Optional
   Trust server certificate: Yes
   ```

3. **Test sorgularını çalıştırın:**
   - Dosyayı açın: `test_queries.sql`
   - Tüm sorguları çalıştırın
   - Karşılaştırma sonuçlarını görün

4. **Beklenen Sonuçlar:**
   ```
   MALZEME KODU  LOGO STOK  FAYS STOK  FARK
   61007030      100.00     120.00     +20.00
   343403022     75.00      60.00      -15.00
   TEST001       200.00     180.00     -20.00
   TEST002       0.00       30.00      +30.00
   ```

---

### Yöntem 2: Windows'ta Program ile Test

**Windows Server'a kopyalayın:**

1. Proje klasörünü Windows'a aktarın
2. ODBC Driver 17 for SQL Server'ı kurun
3. `.env` dosyası oluşturun:
   ```
   DB_SERVER=localhost,1433
   DB_LOGO=GOLD
   DB_FAYS=FaysWMSAkturk
   DB_USER=sa
   DB_PASSWORD=E123456.
   DB_DRIVER=ODBC Driver 17 for SQL Server
   DEFAULT_WAREHOUSE=MERKEZ
   LOG_LEVEL=INFO
   ```

4. Programı çalıştırın:
   ```cmd
   python main.py
   ```

5. **Test Akışı:**
   - ✅ Bağlantı sekmesi → Bağlan
   - ✅ Stok Karşılaştırma → Karşılaştır
   - ✅ 4 fark kaydı görmeli
   - ✅ Excel'e aktar
   - ✅ Stok Eşitleme → Önizleme
   - ✅ 2 fiş oluşturulacağını görmeli
   - ✅ Eşitlemeyi başlat
   - ✅ Tekrar karşılaştır → Fark kalmamalı!

---

## 📊 Veritabanı Yapısı

### GOLD Tabloları
```sql
LG_013_ITEMS        -- Stok Kartları
LV_013_01_STINVTOT  -- Stok Durumu
L_CAPIWHOUSE        -- Depolar
```

### FaysWMSAkturk Tabloları
```sql
stk_Fis         -- Ana Fiş Tablosu
stk_FisLines    -- Fiş Satırları
yr_BilgiLines   -- FisNo Yönetimi (Link_Numarasi=99102)
```

---

## 🔧 Docker Komutları

### Container Yönetimi
```bash
# Container durumunu kontrol
docker ps

# Container'ı durdur
docker stop sqlserver-container

# Container'ı başlat
docker start sqlserver-container

# Container'ı yeniden başlat
docker restart sqlserver-container

# SQL Server loglarını gör
docker logs sqlserver-container
```

### Veritabanı Yönetimi
```bash
# SQL komut satırı
docker exec -it sqlserver-container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "E123456." -C

# Hızlı sorgu çalıştır
docker exec -i sqlserver-container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "E123456." -C \
  -Q "SELECT name FROM sys.databases"

# Veritabanlarını sil (yeniden başlamak için)
docker exec -i sqlserver-container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "E123456." -C \
  -Q "DROP DATABASE GOLD; DROP DATABASE FaysWMSAkturk"

# Veritabanlarını yeniden oluştur
docker exec -i sqlserver-container /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "E123456." -C < setup_test_db.sql
```

---

## 📝 Test Senaryoları

### Senaryo 1: Basit Karşılaştırma
1. Azure Data Studio'da `test_queries.sql` çalıştır
2. 4 fark kaydı görmeli
3. Farkları Excel'e kaydet

### Senaryo 2: Önizleme
1. Programı aç
2. Karşılaştırma yap
3. Eşitleme → Önizleme
4. 2 fiş oluşturulacağını gör
5. **EŞITLEME YAPMA** (önizleme sadece)

### Senaryo 3: Tam Eşitleme
1. Programı aç
2. Karşılaştırma yap → 4 fark
3. Eşitleme → Önizleme
4. Eşitlemeyi başlat → 2 fiş oluşturuldu
5. Tekrar karşılaştır → 0 fark (başarılı!)

### Senaryo 4: Yeniden Test
1. Veritabanlarını sil (yukarıdaki komut)
2. Yeniden oluştur (`setup_test_db.sql`)
3. Test tekrarla

---

## 🎓 Notlar

### macOS'ta Program Çalıştırma
- ❌ ODBC Driver kurulu değil
- ✅ Azure Data Studio ile SQL testleri yapılabilir
- ✅ Windows'a aktarıp tam test yapılabilir

### Windows'ta Tam Test
- ✅ ODBC Driver kurulmalı
- ✅ Program tam çalışır
- ✅ Eşitleme yapılabilir

### Gerçek Ortama Geçiş
1. Test başarılı olunca
2. `.env` dosyasına gerçek bağlantı bilgileri
3. Önce gerçek veritabanında karşılaştırma
4. Yedek al
5. Eşitleme yap

---

## 📞 Yardım

### Sorun: Container başlamıyor
```bash
docker logs sqlserver-container
docker restart sqlserver-container
```

### Sorun: Bağlantı hatası
- Port 1433'ün açık olduğundan emin olun
- Firewall kontrolü yapın
- Container çalışıyor mu: `docker ps`

### Sorun: Şifre hatası
- Doğru şifre: `E123456.`
- Container'ı yeniden başlatın

---

**Test ortamı hazır! Azure Data Studio ile test edebilirsiniz.** 🚀

**Dosyalar:**
- `setup_test_db.sql` - Veritabanı kurulum scripti
- `test_queries.sql` - Test sorguları
- `config_local.py` - Local test ayarları

