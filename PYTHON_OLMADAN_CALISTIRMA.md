# 🚀 Python Olmadan Çalıştırma Kılavuzu

Windows Server'da Python kurulumu yapamıyorsanız **3 alternatif çözüm**.

---

## ✅ Çözüm 1: Standalone EXE Dosyası (EN KOLAY)

### Avantajlar:
- ✅ Python kurulumu gerekmez
- ✅ Tek dosya (.exe)
- ✅ Çift tıklayarak çalışır
- ✅ Tüm kütüphaneler dahil

### Nasıl Yapılır?

#### A) Başka Bir Windows Bilgisayarda:

1. **Python kurun** (başka bilgisayarda)
   ```
   https://www.python.org/downloads/
   ```

2. **Projeyi kopyalayın**
   ```
   USB veya ağ ile proje klasörünü kopyalayın
   ```

3. **Paketleri kurun**
   ```cmd
   cd "C:\StokEsitleme"
   pip install -r requirements.txt
   pip install pyinstaller
   ```

4. **EXE oluşturun**
   ```cmd
   python build_exe.py
   pyinstaller StokEsitleme.spec
   ```

5. **Çıktı dosyası**
   ```
   dist/StokEsitleme.exe oluşacak (yaklaşık 80-150 MB)
   ```

6. **Windows Server'a kopyalayın**
   ```
   StokEsitleme.exe
   .env (bağlantı bilgileri)
   ```

7. **Çalıştırın**
   ```
   Çift tıklayın!
   ```

#### B) Online EXE Builder Servisleri:

Eğer elinizde Windows bilgisayar yoksa:
- GitHub Actions ile otomatik build
- Azure DevOps pipeline
- (Ancak güvenlik nedeniyle önerilmez)

---

## ✅ Çözüm 2: Portable Python (KURULUM GEREKMİYOR)

### Adımlar:

1. **WinPython İndirin** (Portable)
   ```
   https://winpython.github.io/
   Download: WinPython 3.11.x (örn: Winpython64-3.11.5.0)
   Size: ~600 MB
   ```

2. **Kurulum Gerektirmez**
   - ZIP dosyasını açın
   - İstediğiniz klasöre çıkartın (örn: `C:\WinPython`)

3. **Proje Klasörünü Kopyalayın**
   ```
   C:\WinPython\
   └── StokEsitleme\
       ├── main.py
       ├── requirements.txt
       └── ...
   ```

4. **Paketleri Kurun**
   ```cmd
   C:\WinPython\WPy64-xxxx\scripts\env.bat
   pip install -r requirements.txt
   ```

5. **Çalıştırın**
   ```cmd
   C:\WinPython\WPy64-xxxx\python.exe main.py
   ```

6. **Başlatıcı Script (.bat)**
   ```bat
   @echo off
   C:\WinPython\WPy64-xxxx\python.exe "C:\StokEsitleme\main.py"
   pause
   ```

### Avantajlar:
- ✅ Admin yetkisi gerekmez
- ✅ Registry'ye yazmaz
- ✅ Taşınabilir (USB'de çalışır)

---

## ✅ Çözüm 3: SQL-Only Çözüm (PYTHON HİÇ GEREKMİYOR)

Azure Data Studio veya SQL Server Management Studio ile.

### Özellikler:
- ✅ Sadece SQL script'leri
- ✅ Hiç Python gerekmez
- ✅ Manuel çalıştırma

### Script'ler:

#### A) Stok Karşılaştırma (Rapor)

Dosya: `sql_karsilastirma.sql`

```sql
-- Karşılaştırma sonuçları
EXEC sp_StokKarsilastirma 'MERKEZ'

-- Excel'e aktarmak için:
-- Results → Save As → CSV/Excel
```

#### B) Manuel Eşitleme (Stored Procedure)

Dosya: `sql_esitleme.sql`

```sql
-- Eşitleme yap
EXEC sp_StokEsitleme 'MERKEZ'

-- Sonuçları kontrol et
SELECT * FROM stk_Fis WHERE FisNo IN (SELECT MAX(FisNo) FROM stk_Fis)
```

### Kullanım:

1. **Azure Data Studio'yu açın**
2. **Bağlantı kurun**
3. **Script'i açın** (`sql_karsilastirma.sql`)
4. **F5 ile çalıştırın**
5. **Sonuçları görün**

### Sınırlamalar:
- ❌ GUI yok
- ❌ Manuel çalıştırma
- ❌ Otomasyonsuz

---

## 🎯 Karşılaştırma

| Özellik | EXE | Portable Python | SQL-Only |
|---------|-----|----------------|----------|
| Python Kurulumu | ❌ Gerek yok | ❌ Gerek yok | ❌ Gerek yok |
| Admin Yetkisi | ❌ Gerek yok | ❌ Gerek yok | ❌ Gerek yok |
| GUI Arayüz | ✅ Var | ✅ Var | ❌ Yok |
| Otomatik Eşitleme | ✅ Var | ✅ Var | ❌ Manuel |
| Kolay Kullanım | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Dosya Boyutu | ~150 MB | ~600 MB | <1 MB |

---

## 📦 Hazır Paket İçeriği

Size EXE göndermem için:

### Gerekli Bilgiler:
1. ✅ Test veritabanı hazır (Docker'da)
2. ✅ Tüm kodlar hazır
3. ❓ EXE oluşturmak için Windows bilgisayar?

### Seçenekler:

**A) Size EXE gönderebilirim:**
- Ben Windows VM'de build ederim
- Size .exe dosyasını gönderirim
- Siz Windows Server'da çalıştırırsınız

**B) Siz build edersiniz:**
- Başka Windows bilgisayarda
- Yukarıdaki adımları izleyin
- 10 dakika sürer

**C) Portable Python kullanırsınız:**
- En kolay admin yetkisi gerektirmeyen yol
- WinPython indirin
- Çalıştırın

---

## 🔧 Hangi Çözümü Öneriyorum?

### En İyi Seçim: Portable Python (WinPython)

**Neden?**
1. ✅ Kurulum gerektirmez
2. ✅ Admin yetkisi gerekmez  
3. ✅ Tam özellikli GUI
4. ✅ Güvenli (official Python)
5. ✅ Kolay güncelleme

**Adımlar (5 dakika):**

```
1. WinPython indir → winpython.github.io
2. ZIP aç → C:\WinPython
3. Proje kopyala → C:\StokEsitleme
4. CMD aç:
   C:\WinPython\WPy64-xxxx\scripts\env.bat
   cd C:\StokEsitleme
   pip install -r requirements.txt
5. Çalıştır:
   python main.py
```

**İşte bu kadar!** 🎉

---

## 📞 Yardım

Hangisini tercih edersiniz?

1. **EXE oluşturayım mı?** (Ben build edip gönderirim)
2. **Portable Python kurulum kılavuzu mu?** (Detaylı anlatım)
3. **SQL-only script'ler mi?** (GUI olmadan)

Söyleyin, seçtiğiniz çözüm için detaylı kılavuz hazırlayayım! 🚀

