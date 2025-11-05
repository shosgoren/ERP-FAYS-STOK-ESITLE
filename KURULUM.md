# 🚀 LOGO - FAYS WMS Stok Eşitleme Programı - Kurulum Kılavuzu

## Windows Server Kurulum Adımları

Bu dokümanda Windows Server üzerinde programın nasıl kurulacağı adım adım anlatılmaktadır.

---

## 📦 1. ADIM: Python Kurulumu

### Python İndirme
1. Web tarayıcınızı açın
2. https://www.python.org/downloads/ adresine gidin
3. "Download Python 3.11.x" butonuna tıklayın (en son kararlı sürüm)
4. İndirilen dosyayı çalıştırın

### Python Yükleme
1. **ÖNEMLİ**: "Add Python to PATH" kutucuğunu işaretleyin ✅
2. "Install Now" seçeneğine tıklayın
3. Yükleme tamamlanana kadar bekleyin
4. "Close" ile kapatın

### Kurulum Kontrolü
1. `Win + R` tuşlarına basın
2. `cmd` yazın ve Enter'a basın
3. Açılan komut satırına şunu yazın:
   ```
   python --version
   ```
4. Python sürümünü görmeli (örn: Python 3.11.5)

---

## 🔌 2. ADIM: ODBC Driver Kurulumu

### Driver İndirme
1. https://aka.ms/downloadmsodbcsql adresine gidin
2. "Download" butonuna tıklayın
3. **x64** versiyonunu seçin (64-bit Windows için)
4. İndirilen `.msi` dosyasını çalıştırın

### Driver Yükleme
1. Lisans sözleşmesini kabul edin
2. "Next" ile devam edin
3. Varsayılan ayarları kullanın
4. "Install" butonuna tıklayın
5. Yükleme tamamlanınca "Finish" ile kapatın

### Driver Kontrolü
1. `Win + R` tuşlarına basın
2. `odbcad32` yazın ve Enter'a basın
3. "Drivers" sekmesine gidin
4. Listede **"ODBC Driver 17 for SQL Server"** görmeli

---

## 📁 3. ADIM: Program Dosyalarını Yerleştirme

### Klasör Oluşturma
1. `C:\` sürücüsünü açın
2. Sağ tık → "New" → "Folder"
3. Klasör adı: `StokEsitleme`
4. Klasör yolu: `C:\StokEsitleme`

### Dosyaları Kopyalama
Aşağıdaki dosyaları `C:\StokEsitleme` klasörüne kopyalayın:

```
C:\StokEsitleme\
├── main.py
├── config.py
├── database.py
├── stock_sync_engine.py
├── ui_components.py
├── requirements.txt
└── README.md
```

---

## ⚙️ 4. ADIM: Python Paketlerini Yükleme

### Komut Satırını Açma
1. `Win + R` tuşlarına basın
2. `cmd` yazın ve Enter'a basın

### Klasöre Gitme
Komut satırına şunu yazın:
```bash
cd C:\StokEsitleme
```

### Paketleri Yükleme
```bash
pip install -r requirements.txt
```

**Not**: İnternet bağlantısı gereklidir. Yükleme 2-5 dakika sürebilir.

### Yükleme Kontrolü
Aşağıdaki komutu çalıştırın:
```bash
pip list
```

Şu paketleri görmelisiniz:
- customtkinter
- pyodbc
- pandas
- openpyxl
- Pillow
- python-dotenv
- tkcalendar

---

## 🔧 5. ADIM: Yapılandırma

### .env Dosyası Oluşturma

1. `C:\StokEsitleme` klasöründe sağ tık
2. "New" → "Text Document"
3. Dosya adını `.env` olarak değiştirin
   - **Uyarı**: Dosya uzantısı olmayacak, sadece `.env`
4. Dosyayı Notepad ile açın

### Yapılandırma Bilgilerini Girme

Aşağıdaki içeriği kopyalayıp `.env` dosyasına yapıştırın:

```env
# SQL Server Bağlantı Bilgileri
DB_SERVER=sizin_server_adresiniz.database.windows.net
DB_LOGO=GOLD
DB_FAYS=FaysWMSAkturk
DB_USER=sizin_kullanici_adiniz
DB_PASSWORD=sizin_sifreniz
DB_DRIVER=ODBC Driver 17 for SQL Server

# Uygulama Ayarları
APP_TITLE=LOGO - FAYS WMS Stok Eşitleme
DEFAULT_WAREHOUSE=MERKEZ
LOG_LEVEL=INFO
```

### Bilgileri Güncelleme

**Değiştirmeniz gerekenler**:

| Parametre | Örnek | Açıklama |
|-----------|-------|----------|
| DB_SERVER | `myserver.database.windows.net` | Azure SQL Server adresi |
| DB_USER | `admin` | SQL Server kullanıcı adı |
| DB_PASSWORD | `P@ssw0rd123` | SQL Server şifresi |

**Değiştirmemeniz gerekenler**:
- DB_LOGO (GOLD olarak kalmalı)
- DB_FAYS (FaysWMSAkturk olarak kalmalı)
- DB_DRIVER

### Dosyayı Kaydetme
1. `File` → `Save`
2. Dosyayı kapatın

---

## ▶️ 6. ADIM: Programı Çalıştırma

### İlk Çalıştırma

1. `Win + R` tuşlarına basın
2. `cmd` yazın ve Enter'a basın
3. Şu komutları sırayla yazın:
   ```bash
   cd C:\StokEsitleme
   python main.py
   ```

### Program Başlatılıyor
- Birkaç saniye sonra program penceresi açılacak
- Modern, koyu renkli bir arayüz göreceksiniz

---

## 🎯 7. ADIM: İlk Bağlantı Testi

### Bağlantı Kurma

1. Program açıldığında **"Bağlantı"** sekmesinde olacaksınız
2. Bilgilerin doğru geldiğini kontrol edin
3. **"🔌 Bağlan"** butonuna tıklayın
4. Yeşil ✓ işareti görmelisiniz

### Bağlantı Testi

1. **"🔍 Bağlantıyı Test Et"** butonuna tıklayın
2. "Bağlantı testi başarılı!" mesajını görmeli

### Sorun mu Var?

Bağlantı başarısız olursa:
- Server adresini kontrol edin
- Kullanıcı adı ve şifreyi kontrol edin
- Güvenlik duvarı ayarlarını kontrol edin
- SQL Server'ın çalıştığından emin olun

---

## 🖥️ 8. ADIM: Masaüstü Kısayolu (Opsiyonel)

### Kısayol Oluşturma

1. Masaüstünde sağ tık
2. "New" → "Shortcut"
3. Location olarak şunu yazın:
   ```
   C:\Windows\System32\cmd.exe /c "cd C:\StokEsitleme && python main.py"
   ```
4. "Next" ile devam edin
5. İsim: `Stok Eşitleme`
6. "Finish" ile tamamlayın

### Kısayol İkonunu Değiştirme (Opsiyonel)

1. Kısayola sağ tık → "Properties"
2. "Change Icon" butonuna tıklayın
3. İstediğiniz ikonu seçin
4. "OK" ile kaydedin

---

## 🔄 9. ADIM: Otomatik Başlatma (Opsiyonel)

### Windows Başlangıcına Ekleme

1. `Win + R` tuşlarına basın
2. `shell:startup` yazın ve Enter'a basın
3. Açılan klasöre masaüstündeki kısayolu kopyalayın

**Artık Windows açıldığında program otomatik başlayacak!**

---

## ✅ Kurulum Tamamlandı!

### Sonraki Adımlar

1. **Test Edin**: İlk olarak test veritabanında deneyin
2. **Karşılaştırma Yapın**: "Stok Karşılaştırma" sekmesini kullanın
3. **Önizleme Yapın**: Eşitlemeden önce mutlaka önizleme yapın
4. **Yedek Alın**: Canlı ortamda kullanmadan önce yedek alın

---

## 🆘 Sorun Giderme

### Python Bulunamadı Hatası
**Hata**: `'python' is not recognized...`

**Çözüm**:
1. Python'u PATH'e ekleyin
2. Veya tam yolu kullanın:
   ```
   C:\Users\YourUser\AppData\Local\Programs\Python\Python311\python.exe main.py
   ```

### ODBC Driver Hatası
**Hata**: `Data source name not found...`

**Çözüm**:
1. ODBC Driver 17'yi kurun
2. Veya `.env` dosyasında:
   ```
   DB_DRIVER=SQL Server
   ```

### ModuleNotFoundError
**Hata**: `No module named 'customtkinter'`

**Çözüm**:
```bash
pip install customtkinter --upgrade
```

### Güvenlik Duvarı Uyarısı
**Uyarı**: Windows Defender güvenlik duvarı uyarısı

**Çözüm**:
- "Allow access" seçeneğine tıklayın
- Hem "Private" hem "Public" network'leri seçin

---

## 📞 Ek Yardım

### Log Dosyasını Kontrol Edin
Sorun yaşıyorsanız:
1. `C:\StokEsitleme\stok_esitleme.log` dosyasını açın
2. En son satırlara bakın
3. Hata mesajlarını kontrol edin

### Temiz Kurulum
Her şeyi sıfırlamak için:
1. `C:\StokEsitleme` klasörünü silin
2. Python'u kaldırın (opsiyonel)
3. Kuruluma baştan başlayın

---

## ✨ Başarılar!

Artık LOGO - FAYS WMS Stok Eşitleme programını kullanmaya hazırsınız!

**Unutmayın**:
- ✅ İlk kullanımda test edin
- ✅ Yedek alın
- ✅ Önizleme yapın
- ✅ Log dosyalarını kontrol edin

---

**Kurulum Tarihi**: {{ KURULUM_TARİHİNİ_BURAYA_YAZIN }}  
**Kurulum Yapan**: {{ İSMİNİZİ_BURAYA_YAZIN }}  
**Sunucu**: {{ SUNUCU_ADI }}

