# 🚀 GitHub Actions ile Otomatik EXE Oluşturma

## ✅ HAZIRLIK TAMAMLANDI

Gerekli dosyalar zaten hazır:
- ✅ `.github/workflows/build-exe.yml` - GitHub Actions workflow
- ✅ `StokEsitleme.spec` - PyInstaller config
- ✅ Tüm kaynak kodlar

---

## 📋 ADIMLAR (10 Dakika)

### ADIM 1: GitHub Repository Oluşturun

1. **GitHub'a gidin:** https://github.com/new
2. **Repository adı:** `stok-esitleme`
3. **Visibility:** Private (önerilir) veya Public
4. **❌ Initialize ile README eklemeyin** (zaten var)
5. **"Create repository"** tıklayın

---

### ADIM 2: Dosyaları GitHub'a Yükleyin

Terminal'de şu komutları çalıştırın:

```bash
cd "/Users/shosgoren/Documents/Cursor/ERP Stok Esitle"

# Git başlat
git init

# .gitignore kontrolü (zaten var)
git add .gitignore

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit - LOGO FAYS WMS Stok Esitleme v1.0"

# GitHub repository'nize bağlayın (KENDİ KULLANICI ADINIZI YAZIN!)
git remote add origin https://github.com/KULLANICI_ADINIZ/stok-esitleme.git

# Ana branch'i main olarak ayarla
git branch -M main

# Push yapın
git push -u origin main
```

**Not:** `KULLANICI_ADINIZ` yerine kendi GitHub kullanıcı adınızı yazın!

---

### ADIM 3: GitHub Actions Otomatik Başlayacak

1. **GitHub repository sayfasına gidin**
2. **"Actions"** sekmesine tıklayın
3. **"Build Windows EXE"** workflow'unu göreceksiniz
4. **Otomatik çalışacak!** (yaklaşık 5-10 dakika)

Eğer otomatik başlamazsa:
- Actions sekmesinde
- "Build Windows EXE" workflow'una tıklayın
- "Run workflow" → "Run workflow" butonuna basın

---

### ADIM 4: İlerlemeyi İzleyin

Workflow çalışırken:
```
✓ Checkout code
✓ Setup Python
✓ Install dependencies (2-3 dakika)
✓ Build EXE (3-5 dakika)
✓ Upload artifact
```

**Toplam süre:** 5-10 dakika ⏱️

---

### ADIM 5: EXE Dosyasını İndirin

Build tamamlandığında:

1. **Actions** sekmesinde
2. En üstteki **yeşil ✓ işaretli** workflow'a tıklayın
3. Aşağıda **"Artifacts"** bölümünü görün
4. **"StokEsitleme-Windows"** linkine tıklayın
5. **ZIP dosyası inecek!**
6. ZIP'i açın → `StokEsitleme.exe` (~150 MB)

---

### ADIM 6: Windows Server'da Kullanın

1. **StokEsitleme.exe** dosyasını Windows Server'a kopyalayın

2. **Aynı klasöre `.env` dosyası oluşturun:**
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

3. **Çift tıklayın!** ✅

**TAMAM!** Program açılacak! 🎉

---

## 🔄 Otomatik Güncelleme

Her kod değişikliğinde otomatik EXE oluşturulur:

```bash
# Kod değiştirip push yaptığınızda:
git add .
git commit -m "Güncelleme: ..."
git push

# GitHub Actions otomatik çalışır
# Yeni EXE hazır olur!
```

---

## 🎯 SORUN GİDERME

### Hata: "Push rejected"

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Hata: "Authentication failed"

GitHub token gerekli:
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scopes: `repo`, `workflow`
4. Token'ı kopyalayın

Sonra:
```bash
git remote set-url origin https://TOKEN@github.com/KULLANICI/stok-esitleme.git
git push -u origin main
```

### Workflow Çalışmıyor

1. Actions sekmesini kontrol edin
2. "Enable workflows" butonuna basın
3. Manuel tetikleyin: Run workflow

---

## 📊 WORKFLOW DETAYLARI

`.github/workflows/build-exe.yml` dosyası:

```yaml
✓ Windows latest kullanır
✓ Python 3.11 kurar
✓ Tüm bağımlılıkları yükler
✓ PyInstaller ile EXE oluşturur
✓ Artifact olarak yükler (30 gün saklanır)
```

**Özellikler:**
- ✅ Tek dosya EXE
- ✅ Windowless mode (GUI)
- ✅ Tüm kütüphaneler dahil
- ✅ ODBC Driver gerekli (Windows'ta)

---

## 🎁 BONUS: Release Oluşturma

Tag ile release yapın:

```bash
git tag -a v1.0.0 -m "İlk sürüm"
git push origin v1.0.0
```

GitHub otomatik olarak:
- Release oluşturur
- EXE'yi ekler
- İndirme linki verir

---

## ✅ ÖZET

1. ✅ Repository oluştur
2. ✅ `git push` yap
3. ✅ GitHub Actions çalışsın (5-10 dk)
4. ✅ Artifacts'ten EXE indir
5. ✅ Windows'ta çalıştır

**Hazır!** 🎉

---

## 🔒 GÜVENLİK

**ÖNEMLİ:** 
- `.env` dosyası `.gitignore`'da (GitHub'a gitmez)
- Şifreler güvende
- Private repository kullanın

---

## 📞 YARDIM

Herhangi bir adımda takılırsanız:
1. Actions sekmesindeki hata loglarına bakın
2. Workflow'u tekrar çalıştırın
3. Manuel build deneyin (build_exe.py)

---

**Başarılar!** 🚀

