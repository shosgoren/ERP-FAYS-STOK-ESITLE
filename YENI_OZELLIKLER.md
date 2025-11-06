# 🎉 Yeni Özellikler

## 🔐 1. Şifreli Bağlantı Bilgileri

### Ne Değişti?
Artık veritabanı bağlantı bilgilerinizi **şifreli olarak** kaydedebilir ve her yeni EXE'de **tekrar girmek zorunda kalmazsınız**!

### Nasıl Kullanılır?

1. **Bağlantı Ekranında**:
   - Veritabanı bilgilerinizi girin
   - **"🔌 Bağlan"** butonuna tıklayın
   - Bağlantı başarılı olunca **"💾 Bağlantıyı Şifreli Kaydet"** butonuna tıklayın

2. **Bir Sonraki Açılışta**:
   - **"📂 Kayıtlı Bağlantıyı Yükle"** butonuna tıklayın
   - Tüm bilgiler otomatik yüklenir!
   - Sadece **"🔌 Bağlan"** butonuna basın

3. **Kaydı Silmek İsterseniz**:
   - **"🗑️ Kaydı Sil"** butonunu kullanın

### Güvenlik
- Bağlantı bilgileri **AES-256 şifreleme** ile korunur
- Şifreleme anahtarı **bilgisayar ve kullanıcı adına özel** oluşturulur
- Dosya: `connection.dat` (şifreli)

---

## 📝 2. Düzenlenebilir INSERT Şablonları

### Ne Değişti?
Artık stok eşitleme sırasında kullanılan **SQL INSERT cümleleri**ni program içinden **görüntüleyebilir ve düzenleyebilirsiniz**!

### Nasıl Kullanılır?

1. **SQL Sorguları Sekmesine** gidin
2. **"📝 INSERT Şablonları"** butonuna tıklayın
3. Açılan pencerede **3 sekme** göreceksiniz:
   - **stk_Fis INSERT**: Ana fiş oluşturma şablonu
   - **stk_FisLines INSERT**: Fiş satırları oluşturma şablonu
   - **Fiş Açıklamaları**: Sayım Eksiği ve Sayım Fazlası açıklamaları

4. **Şablonları düzenleyin**:
   - `{Değişken}` formatındaki alanlar otomatik doldurulur
   - Örnek: `{FisNo}`, `{StokKodu}`, `{NetMiktar}`

5. **"💾 Kaydet"** butonuna tıklayın

6. **"🔄 Varsayılana Dön"** ile orijinal şablonlara geri dönebilirsiniz

### Örnek Kullanım Senaryoları

#### Senaryo 1: Farklı bir FirmaKodu kullanmak istiyorsunuz
```sql
-- Önceden:
VALUES (..., '', '', ...)

-- Şimdi:
VALUES (..., 'ABC123', 'ABC Firma', ...)
```

#### Senaryo 2: Farklı bir açıklama eklemek istiyorsunuz
```
Önceden: "0.KAT:SAYILMAYAN VE STOKTA FAZLA OLAN STOKLAR"
Şimdi: "2025 STOK SAYIMI - FAZLA OLANLAR"
```

#### Senaryo 3: Ek bir kolon eklemek istiyorsunuz
```sql
INSERT INTO stk_Fis (
    FisTuru, FisNo, ..., YeniKolonunuz
) VALUES (
    {FisTuru}, {FisNo}, ..., 'Sabit Değer'
)
```

### Dosya Konumu
- Şablonlar: `sql_templates.json` (JSON formatında)
- Varsayılan şablonlar: Kod içinde `sql_templates.py`

---

## 🎯 Avantajlar

### Bağlantı Bilgileri İçin:
- ✅ Her EXE güncellemesinde **tekrar girmek zorunda kalmazsınız**
- ✅ Şifreli olarak saklanır (**güvenli**)
- ✅ Bilgisayara özel (**başka PC'de açılmaz**)
- ✅ Tek tuşla yükleme

### INSERT Şablonları İçin:
- ✅ Veritabanı yapınıza göre **özelleştirebilirsiniz**
- ✅ Kod değiştirmeden **SQL'i düzenleyebilirsiniz**
- ✅ Test edip **eski haline dönebilirsiniz**
- ✅ JSON formatında **kolayca paylaşabilirsiniz**

---

## 📦 Dosya Yapısı

```
StokEsitleme.exe           ← Ana program
connection.dat             ← Şifreli bağlantı bilgileri (otomatik oluşur)
sql_templates.json         ← Özelleştirilmiş INSERT şablonları (otomatik oluşur)
```

---

## 🔧 Teknik Detaylar

### Şifreleme:
- **Algoritma**: Fernet (AES-256)
- **Anahtar Türetme**: PBKDF2 (100,000 iterasyon)
- **Salt**: Uygulama bazlı sabit salt
- **Makine Bazlı**: COMPUTERNAME + USERNAME

### Şablonlar:
- **Format**: JSON
- **Encoding**: UTF-8
- **Değişken Formatı**: `{DeğişkenAdı}`
- **Python String Formatting** kullanılır

---

## ⚠️ Önemli Notlar

1. **`connection.dat` dosyası**:
   - Bilgisayarınıza özeldir
   - Başka bir PC'ye kopyalarsanız **açılmaz**
   - Silip tekrar oluşturabilirsiniz

2. **`sql_templates.json` dosyası**:
   - İsterseniz **yedekleyebilirsiniz**
   - Başka PC'lere **kopyalayabilirsiniz**
   - Bozulursa **"Varsayılana Dön"** ile düzeltebilirsiniz

3. **GitHub Actions**:
   - Her push'ta yeni EXE **otomatik build edilir**
   - Yeni özellikler **otomatik dahil edilir**
   - EXE indirdikten sonra **eski ayarlarınızı yükleyebilirsiniz**

---

## 🚀 Hızlı Başlangıç

### İlk Kurulum:
1. `StokEsitleme.exe` çalıştırın
2. Bağlantı bilgilerini girin → **"Bağlan"**
3. **"Bağlantıyı Şifreli Kaydet"** tıklayın
4. İsterseniz **"INSERT Şablonları"** düzenleyin

### Güncellemeden Sonra:
1. Yeni `StokEsitleme.exe` indirin
2. Eski klasöre kopyalayın (üzerine yazın)
3. **"Kayıtlı Bağlantıyı Yükle"** → **"Bağlan"**
4. Hazır! 🎉

---

## 📞 Destek

Herhangi bir sorun yaşarsanız:
- **connection.dat** ve **sql_templates.json** dosyalarını silin
- Programı yeniden başlatın
- Ayarları tekrar yapın

---

**Geliştirme Tarihi**: 2025-11-06  
**Versiyon**: 2.0  
**Yeni Özellikler**: Şifreli Ayarlar + Düzenlenebilir Şablonlar

