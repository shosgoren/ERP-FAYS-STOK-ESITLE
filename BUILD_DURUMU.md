# 🚀 GitHub Actions Build Durumu

## ⏱️ Build Başladı!

**Repository:** https://github.com/shosgoren/ERP-FAYS-STOK-ESITLE

**Build Linki:** https://github.com/shosgoren/ERP-FAYS-STOK-ESITLE/actions

---

## 📊 Build Adımları ve Tahmini Süreler:

```
┌─────────────────────────────────────────────────────┐
│ 1. ✓ Checkout code                    [10 saniye]  │
│ 2. ✓ Setup Python 3.11                [30 saniye]  │
│ 3. ⏳ Install dependencies             [2-3 dakika] │
│ 4. ⏳ Build EXE with PyInstaller       [3-5 dakika] │
│ 5. ⏳ Upload artifact                  [30 saniye]  │
└─────────────────────────────────────────────────────┘

Toplam Tahmini Süre: 5-10 dakika
```

---

## 🔍 Canlı İzleme

### Adım 1: Actions Sayfasına Gidin
```
https://github.com/shosgoren/ERP-FAYS-STOK-ESITLE/actions
```

### Adım 2: En Üstteki Workflow'a Tıklayın
- En son commit mesajını göreceksiniz
- "Fix: Update GitHub Actions to v4"

### Adım 3: İlerlemeyi İzleyin

**Durum İkonları:**
- 🟡 Sarı nokta = Çalışıyor
- 🟢 Yeşil tik = Başarılı
- 🔴 Kırmızı X = Hata

**Adımlar:**
```
Set up job               🟢 ✓
Run actions/checkout@v4  🟢 ✓
Run actions/setup-python@v5  🟡 ⏳
Install dependencies     ⏳
Build EXE               ⏳
Upload artifact         ⏳
Complete job            ⏳
```

---

## 📥 Build Tamamlandığında:

### EXE'yi İndirmek İçin:

1. **Workflow'a tıklayın** (yeşil ✓ işaretli)

2. **Aşağı kaydırın** → "Artifacts" bölümü

3. **"StokEsitleme-Windows"** linkine tıklayın

4. **ZIP dosyası inecek** (~150-200 MB)

5. **ZIP'i açın:**
   ```
   StokEsitleme-Windows.zip
   └── StokEsitleme.exe (~150 MB)
   ```

---

## 💻 Windows Server'da Kullanım:

### Adım 1: EXE ve .env Hazırlayın

```
C:\StokEsitleme\
├── StokEsitleme.exe      ← GitHub'dan indirilen
└── .env                  ← Oluşturacaksınız
```

### Adım 2: .env Dosyası Oluşturun

`C:\StokEsitleme\.env`:
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

### Adım 3: ODBC Driver 17 Kurulu mu?

Eğer **yoksa** indirin:
```
https://aka.ms/downloadmsodbcsql
ODBC Driver 17 for SQL Server (x64)
```

### Adım 4: Çalıştırın!

```
StokEsitleme.exe dosyasına çift tıklayın!
```

**Modern GUI açılacak!** 🎉

---

## 🔴 Build Başarısız Olursa:

### Olası Hatalar:

1. **ModuleNotFoundError**
   - `requirements.txt` eksik paket var
   - Düzeltme: requirements.txt güncelle

2. **PyInstaller Hatası**
   - Hidden import eksik
   - Düzeltme: workflow'da hidden-import ekle

3. **Timeout**
   - Build 60 dakikadan uzun sürdü
   - Düzeltme: Optimize et veya tekrar dene

### Çözüm:

```bash
# Hata loglarını inceleyin
# Actions → Failed workflow → Logları okuyun

# Düzeltme yapın
git add .
git commit -m "Fix: ..."
git push

# Otomatik tekrar build başlar
```

---

## 📊 Beklenen Build Çıktısı:

```
✅ StokEsitleme.exe
   Size: ~150 MB
   Platform: Windows x64
   Python: 3.11 (embedded)
   Dependencies: All included
   ODBC: Requires ODBC Driver 17
```

### İçinde Ne Var?

```
✓ Python 3.11 runtime
✓ customtkinter (GUI)
✓ pyodbc (Database)
✓ pandas (Data processing)
✓ openpyxl (Excel)
✓ PIL/Pillow (Images)
✓ tkcalendar
✓ All your code files
```

---

## 🎯 Test Checklist:

Windows'ta EXE aldıktan sonra:

- [ ] EXE çalışıyor mu?
- [ ] .env dosyası aynı klasörde mi?
- [ ] Bağlantı ekranı açılıyor mu?
- [ ] Veritabanına bağlanabiliyor mu?
- [ ] Karşılaştırma çalışıyor mu?
- [ ] Eşitleme yapabiliyor mu?

---

## 🔄 Güncellemeler İçin:

### Kod değiştirince:

```bash
cd "/Users/shosgoren/Documents/Cursor/ERP Stok Esitle"

# Değişiklikleri commit et
git add .
git commit -m "Update: ..."
git push

# GitHub Actions otomatik yeni EXE oluşturur!
```

---

## 📞 Durum Kontrol:

**Şu anda:**
- ✅ Workflow güncellendi (v4)
- ✅ GitHub'a push yapıldı
- 🟡 Build çalışıyor (5-10 dakika)
- ⏳ Artifacts bekleniyor

**Sonraki:**
- 🎯 EXE indir
- 🎯 Windows'ta test et
- 🎯 Canlı ortama dağıt

---

## ⏰ Tahmini Tamamlanma:

**Başlangıç:** ~17:10 (şimdi)
**Tahmini Bitiş:** ~17:15-17:20 (5-10 dakika sonra)

**Actions sayfasını açık tutun:**
https://github.com/shosgoren/ERP-FAYS-STOK-ESITLE/actions

---

## 🎉 Tamamlanınca:

```
✅ Yeşil tik göreceksiniz
✅ "Artifacts (1)" yazısı çıkacak
✅ ZIP indirme başlayacak
✅ StokEsitleme.exe hazır!
```

---

**5-10 dakika içinde kontrol ediyorum!** ⏱️

**Açık tutun:** https://github.com/shosgoren/ERP-FAYS-STOK-ESITLE/actions

