# 📖 LOGO - FAYS WMS Stok Eşitleme - Kullanım Kılavuzu

## Hızlı Başlangıç

### Programı Başlatma

**Windows'ta**:
- Masaüstündeki kısayola çift tıklayın, VEYA
- `run.bat` dosyasına çift tıklayın, VEYA
- Komut satırında: `python main.py`

---

## 🎯 Ana Ekranlar

Program 5 ana sekmeden oluşur:

### 1️⃣ Bağlantı Ekranı

Bu ekranda veritabanı bağlantısı kurarsınız.

#### Adımlar:
1. **Server Adresi**: Azure SQL Server adresinizi girin
   - Örnek: `myserver.database.windows.net`
   
2. **Kullanıcı Adı**: SQL Server kullanıcı adınızı girin
   
3. **Şifre**: SQL Server şifrenizi girin
   
4. **LOGO Veritabanı**: `GOLD` (varsayılan)
   
5. **FAYS Veritabanı**: `FaysWMSAkturk` (varsayılan)

6. **Bağlan** butonuna tıklayın

#### Durum Göstergeleri:
- 🔴 **Kırmızı Nokta**: Bağlantı yok
- 🟢 **Yeşil Nokta**: Bağlantı başarılı

#### Butonlar:
- **🔌 Bağlan**: Veritabanına bağlan
- **🔍 Bağlantıyı Test Et**: Mevcut bağlantıyı test et
- **💾 Ayarları Kaydet**: Bilgileri .env dosyasına kaydet

---

### 2️⃣ Stok Karşılaştırma Ekranı

LOGO ve FAYS stokları arasındaki farkları görüntülersiniz.

#### Kullanım:

1. **Depo Seçin**:
   - "Tümü" seçeneği: Tüm depoları karşılaştır
   - Belirli depo: Sadece o depoyu karşılaştır

2. **🔄 Depoları Yükle**: Depo listesini veritabanından çek

3. **📊 Karşılaştır**: Karşılaştırmayı başlat

4. Sonuçları inceleyin:
   - 🔴 **Kırmızı satırlar**: FAYS FAZLA (Logo'da eksik)
   - 🟢 **Yeşil satırlar**: FAYS EKSİK (Logo'da fazla)

5. **📥 Excel'e Aktar**: Sonuçları Excel'e kaydet

#### Sütun Açıklamaları:

| Sütun | Açıklama |
|-------|----------|
| MALZEME KODU | Ürün kodu |
| MALZEME ADI | Ürün adı |
| GRUP KODU | Stok grup kodu |
| AMBAR ADI | Depo adı |
| LOGO FİİLİ STOK | LOGO ERP'deki mevcut stok |
| FAYS STOK | FAYS WMS'deki mevcut stok |
| FARK | FAYS - LOGO farkı |
| DURUM | Fark açıklaması |

#### Fark Türleri:

```
FARK > 0  →  FAYS FAZLA (🔴)
   Anlamı: FAYS WMS'de olması gerekenden fazla stok var
   İşlem: Sayım eksiği fişi ile çıkış yapılacak

FARK < 0  →  FAYS EKSİK (🟢)
   Anlamı: FAYS WMS'de olması gerekenden az stok var
   İşlem: Sayım fazlası fişi ile giriş yapılacak

FARK = 0  →  EŞİT (Listede görünmez)
   Anlamı: Stoklar uyumlu
```

---

### 3️⃣ Stok Eşitleme Ekranı

⚠️ **DİKKAT**: Bu ekran kritik işlemler yapar!

#### Eşitleme Süreci:

**ADIM 1: Depo Seçimi**
1. **🔄 Depoları Yükle** butonuna tıklayın
2. Açılan listeden eşitlenecek depoyu seçin
3. Doğru depoyu seçtiğinizden emin olun!

**ADIM 2: Önizleme**
1. **👁️ Önizleme Yap** butonuna tıklayın
2. Yapılacak değişiklikleri inceleyin:
   - Kaç fiş oluşturulacak?
   - Hangi stoklar etkilenecek?
   - Ne kadar miktar değişecek?
3. Sonuçlar metin alanında görüntülenir

**ADIM 3: Eşitleme**
1. **🔄 EŞİTLEMEYİ BAŞLAT** butonuna tıklayın
2. **ÖNEMLİ**: Onay mesajını dikkatle okuyun!
3. "Yes" ile onaylayın
4. İşlem başlar ve sonuçlar gösterilir

#### Eşitleme Sonrası:

Metin alanında şu bilgiler gösterilir:
- ✅ Oluşturulan fiş sayısı
- 📋 Her fişin detayları (FişNo, Tür, Satır sayısı)
- ⏰ İşlem başlangıç ve bitiş zamanı

#### Oluşturulan Fişler:

**Sayım Fazlası Fişi (FisTuru=50)**
- Ne zaman: FAYS EKSİK durumunda
- İşlem: Giriş (GirisCikis=1)
- Amaç: FAYS stoğunu artırma

**Sayım Eksiği Fişi (FisTuru=51)**
- Ne zaman: FAYS FAZLA durumunda
- İşlem: Çıkış (GirisCikis=2)
- Amaç: FAYS stoğunu azaltma

---

### 4️⃣ SQL Sorguları Ekranı

Özel SQL sorguları yazabilir ve test edebilirsiniz.

#### Kullanım:

1. **Sorgu Şablonu Seçin**:
   - Stok Karşılaştırma (Varsayılan)
   - FAYS Stok Raporu
   - LOGO Stok Raporu
   - Boş Sorgu

2. Sorguyu düzenleyin

3. **▶️ Çalıştır** butonuna tıklayın

4. Sonuçları inceleyin

5. **💾 Sorguyu Kaydet**: SQL dosyası olarak kaydedin

#### Özellikler:
- Syntax highlighting yok (basit metin editörü)
- Sadece SELECT sorguları önerilir
- INSERT/UPDATE/DELETE dikkatli kullanılmalı

#### Örnek Sorgular:

**Belirli bir ürünü sorgulama:**
```sql
SELECT * 
FROM GOLD..LG_013_ITEMS 
WHERE CODE = '61007030'
```

**Belirli depodaki stoklar:**
```sql
SELECT 
    ln.StokKodu,
    ln.UrunGrup1,
    SUM(CASE WHEN fs.giriscikis=2 THEN -ln.NetMiktar ELSE ln.NetMiktar END) as Stok
FROM stk_Fis fs
INNER JOIN stk_FisLines ln ON ln.Link_FisNo = fs.FisNo
WHERE ln.Depo = 'MERKEZ'
GROUP BY ln.StokKodu, ln.UrunGrup1
```

---

### 5️⃣ Ayarlar Ekranı

Uygulama ayarlarını yapılandırın.

#### Ayarlar:

**Tema**
- `dark`: Koyu tema (varsayılan)
- `light`: Açık tema
- Değişiklik anında uygulanır

**Varsayılan Depo**
- Uygulama başlatıldığında otomatik seçilen depo

**Log Seviyesi**
- `DEBUG`: Tüm detaylar
- `INFO`: Genel bilgiler (varsayılan)
- `WARNING`: Sadece uyarılar
- `ERROR`: Sadece hatalar

**💾 Ayarları Kaydet**: Değişiklikleri .env dosyasına yazar

---

## 🎓 İş Akışı Örnekleri

### Senaryo 1: Günlük Stok Kontrolü

1. Programı başlatın
2. Bağlantı ekranından bağlanın
3. Stok Karşılaştırma'ya gidin
4. "Tümü" seçip karşılaştırın
5. Fark yoksa işlem yok
6. Fark varsa Excel'e kaydedin ve raporlayın

---

### Senaryo 2: Aylık Stok Eşitleme

1. **YEDEK ALIN!** (Çok önemli)
2. Programı başlatın ve bağlanın
3. Stok Karşılaştırma yapın
4. Excel rapor alın (kayıt için)
5. Stok Eşitleme ekranına gidin
6. Her depo için:
   - Depoyu seçin
   - Önizleme yapın
   - Sonuçları kontrol edin
   - Eşitleyin
7. Log dosyasını kontrol edin

---

### Senaryo 3: Belirli Bir Depo İçin Eşitleme

1. Programı başlatın
2. Karşılaştırma ekranına gidin
3. İlgili depoyu seçin
4. Karşılaştır
5. Sadece o depodaki farkları görürsünüz
6. Eşitleme ekranına geçin
7. Aynı depoyu seçin
8. Önizleme → Eşitle

---

## ⚠️ Önemli Uyarılar

### Eşitlemeden Önce

- ✅ **MUTLAKA YEDEK ALIN**
- ✅ İlk kullanımda test ortamında deneyin
- ✅ Önizleme yapın
- ✅ Sonuçları kontrol edin
- ✅ Doğru depoyu seçin
- ✅ Log dosyasını takip edin

### Eşitleme Sırasında

- ⚠️ Program kapatılmamalı
- ⚠️ İnternet bağlantısı kesilmemeli
- ⚠️ Başka işlem yapılmamalı
- ⚠️ Aynı anda birden fazla eşitleme yapılmamalı

### Eşitlemeden Sonra

- ✅ Log dosyasını kontrol edin
- ✅ FAYS WMS'den stok raporunu kontrol edin
- ✅ Oluşturulan fişleri kontrol edin
- ✅ Bir sonraki karşılaştırmada fark olmamalı

---

## 🔍 Hata Durumları

### "Bağlantı Hatası"

**Neden**:
- Yanlış server adresi
- Yanlış kullanıcı adı/şifre
- Güvenlik duvarı
- SQL Server kapalı

**Çözüm**:
1. `.env` dosyasını kontrol edin
2. SQL Server Management Studio ile test edin
3. Güvenlik duvarını kontrol edin
4. ODBC Driver'ı kontrol edin

---

### "FisNo Alınamadı"

**Neden**:
- `yr_BilgiLines` tablosunda Link_Numarası=99102 yok

**Çözüm**:
SQL Server'da kontrol edin:
```sql
SELECT * FROM yr_BilgiLines WHERE Link_Numarasi = 99102
```

Yoksa ekleyin:
```sql
INSERT INTO yr_BilgiLines (Link_Numarasi, Deger)
VALUES (99102, 1000000)
```

---

### "Yetki Hatası"

**Neden**:
- Kullanıcının yeterli yetkisi yok

**Çözüm**:
Veritabanı yöneticisinden şu yetkileri isteyin:
- GOLD veritabanı: SELECT
- FaysWMSAkturk veritabanı: SELECT, INSERT, UPDATE

---

## 📊 Rapor ve Kayıtlar

### Excel Raporları

Karşılaştırma sonuçları Excel'e aktarılabilir:
- Tarih damgalı dosya adı
- Tüm sütunlar dahil
- Kolayca filtrelenebilir

### Log Dosyası

`stok_esitleme.log` dosyası:
- Tüm işlemleri kaydeder
- Hata mesajlarını içerir
- Sorun giderme için kullanılır

**Log Örneği**:
```
2025-11-05 10:30:15 - INFO - Uygulama başlatıldı
2025-11-05 10:30:20 - INFO - FAYS WMS veritabanına bağlanıldı
2025-11-05 10:30:21 - INFO - LOGO ERP veritabanına bağlanıldı
2025-11-05 10:35:40 - INFO - Stok karşılaştırması tamamlandı: 23 kayıt
2025-11-05 10:40:12 - INFO - Yeni FisNo alındı: 1067969
2025-11-05 10:40:13 - INFO - Fiş kaydı oluşturuldu - FisNo: 1067969
```

---

## 💡 İpuçları

### Performans

1. **Sadece Gerekli Depoyu Seçin**
   - "Tümü" yerine belirli depo seçimi daha hızlıdır

2. **Yoğun Saatlerde Kullanmayın**
   - Mesai saati dışında çalıştırın

3. **Log Dosyasını Temizleyin**
   - Büyük log dosyaları performansı düşürür

### Güvenlik

1. **Şifreleri Paylaşmayın**
   - `.env` dosyasını kimseyle paylaşmayın

2. **Yetkileri Sınırlayın**
   - Sadece gerekli yetkileri verin

3. **Yedek Almayı Unutmayın**
   - Her eşitlemeden önce!

### Bakım

1. **Düzenli Kontrol**
   - Haftada bir karşılaştırma yapın

2. **Log İncelemesi**
   - Aylık log dosyalarını inceleyin

3. **Güncelleme**
   - Python ve paketleri güncel tutun

---

## 📞 Destek

### Sorunuz mu Var?

1. **README.md** dosyasına bakın
2. **Log dosyasını** kontrol edin
3. **KURULUM.md** adımlarını tekrar gözden geçirin
4. IT destek ekibinizle iletişime geçin

### Hata Bildirimi

Hata bildirirken şunları ekleyin:
- Hata mesajı (ekran görüntüsü)
- Log dosyasının son satırları
- Yapılan işlem adımları
- Windows ve Python sürümleri

---

**Son Güncelleme**: 2025-11-05  
**Versiyon**: 1.0.0

---

## ✅ Kontrol Listesi

Her kullanımdan önce:
- [ ] Yedek aldım
- [ ] Bağlantı testi yaptım
- [ ] Önizleme yaptım
- [ ] Doğru depoyu seçtim
- [ ] Yetkim var
- [ ] Log dosyası çalışıyor

Her kullanımdan sonra:
- [ ] Log kontrol ettim
- [ ] Sonuçları doğruladım
- [ ] Fişleri kontrol ettim
- [ ] Rapor aldım
- [ ] Gerekli kişileri bilgilendirdim

