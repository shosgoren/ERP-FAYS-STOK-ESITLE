-- Test Veritabanları ve Tablolar Oluşturma Script'i
-- LOGO ve FAYS WMS Test Ortamı

USE master;
GO

-- Varsa sil
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'GOLD')
    DROP DATABASE GOLD;
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'FaysWMSAkturk')
    DROP DATABASE FaysWMSAkturk;
GO

-- GOLD (LOGO ERP) Veritabanı
CREATE DATABASE GOLD;
GO

USE GOLD;
GO

-- LG_013_ITEMS Tablosu (LOGO Stok Kartları)
CREATE TABLE LG_013_ITEMS (
    LOGICALREF INT IDENTITY(1,1) PRIMARY KEY,
    CODE NVARCHAR(50) NOT NULL,
    NAME NVARCHAR(100),
    STGRPCODE NVARCHAR(20),
    ACTIVE INT DEFAULT 0,
    MARKREF INT DEFAULT 0
);

-- LV_013_01_STINVTOT Tablosu (LOGO Stok Durumu)
CREATE TABLE LV_013_01_STINVTOT (
    STOCKREF INT,
    INVENNO INT,
    ONHAND DECIMAL(18,2) DEFAULT 0,
    RESERVED DECIMAL(18,2) DEFAULT 0,
    TEMPOUT DECIMAL(18,2) DEFAULT 0,
    TEMPIN DECIMAL(18,2) DEFAULT 0
);

-- L_CAPIWHOUSE Tablosu (Depolar)
CREATE TABLE L_CAPIWHOUSE (
    NR INT,
    FIRMNR NVARCHAR(10),
    NAME NVARCHAR(50)
);

-- Test Verileri - LOGO
-- Depolar
INSERT INTO L_CAPIWHOUSE (NR, FIRMNR, NAME) VALUES 
(1, '013', 'MERKEZ'),
(2, '013', 'ŞUBE-1'),
(3, '013', 'ŞUBE-2');

-- Stok Kartları
INSERT INTO LG_013_ITEMS (CODE, NAME, STGRPCODE, ACTIVE) VALUES
('61007030', 'BULAŞIK MAKİNESİ DETERJAN', 'GRUP-A', 0),
('509V0004', 'P-50 GİYOTİN BULAŞIK MAK.', 'GRUP-B', 0),
('343403022', 'TEMİZLİK MALZEMESİ', 'GRUP-A', 0),
('TEST001', 'TEST ÜRÜN 1', 'GRUP-C', 0),
('TEST002', 'TEST ÜRÜN 2', 'GRUP-C', 0);

-- Stok Durumları (LOGO'da doğru stoklar)
-- MERKEZ Deposu (NR=1)
INSERT INTO LV_013_01_STINVTOT (STOCKREF, INVENNO, ONHAND, RESERVED, TEMPOUT, TEMPIN) VALUES
(1, 1, 100.00, 10.00, 0.00, 0.00),  -- 61007030: 100 adet
(2, 1, 56.00, 0.00, 0.00, 0.00),    -- 509V0004: 56 adet (FAYS'da aynı olacak - fark yok)
(3, 1, 75.00, 5.00, 0.00, 0.00),    -- 343403022: 75 adet
(4, 1, 200.00, 0.00, 0.00, 0.00),   -- TEST001: 200 adet
(5, 1, 0.00, 0.00, 0.00, 0.00);     -- TEST002: 0 adet (FAYS'da var olacak)

GO

-- FaysWMSAkturk Veritabanı
USE master;
GO
CREATE DATABASE FaysWMSAkturk;
GO

USE FaysWMSAkturk;
GO

-- stk_Fis Tablosu (Ana Fiş)
CREATE TABLE stk_Fis (
    idNo INT IDENTITY(1,1) PRIMARY KEY,
    FisTuru INT,
    FisNo BIGINT,
    GirisCikis INT,
    Tarih DATETIME,
    FirmaKodu NVARCHAR(50),
    FirmaAdi NVARCHAR(100),
    KdvOrani DECIMAL(5,2) DEFAULT 0,
    AraToplam DECIMAL(18,2) DEFAULT 0,
    calcGenelToplam DECIMAL(18,2) DEFAULT 0,
    ParaBirimi NVARCHAR(10),
    DovizKuru DECIMAL(18,4) DEFAULT 0,
    Aciklamalar NVARCHAR(MAX),
    Grup1 NVARCHAR(50),
    Grup2 NVARCHAR(50),
    Grup3 NVARCHAR(50),
    Grup4 NVARCHAR(50),
    Grup5 NVARCHAR(50),
    Grup6 NVARCHAR(50),
    Grup7 NVARCHAR(50),
    Grup8 NVARCHAR(50),
    Grup9 NVARCHAR(50),
    KaynakTuru INT,
    KaynakNo NVARCHAR(50),
    KdvDegeri DECIMAL(18,2) DEFAULT 0,
    upsize_ts BINARY(8),
    LogoKontrol INT DEFAULT 0,
    HareketTipi NVARCHAR(50),
    Status INT DEFAULT 0,
    DepoRefNo INT DEFAULT 1,
    CariRefNo INT,
    Islemvar INT DEFAULT 0,
    IslemKullanici INT DEFAULT 0,
    IadeFisNo NVARCHAR(50),
    IadeKontrol INT DEFAULT 0,
    DevamDurumu INT DEFAULT 3
);

-- stk_FisLines Tablosu (Fiş Satırları)
CREATE TABLE stk_FisLines (
    idNo INT IDENTITY(1,1) PRIMARY KEY,
    Link_FisNo BIGINT,
    Link_saSiparisLines INT DEFAULT 0,
    Link_serSiparisLines INT DEFAULT 0,
    FisNo2 INT DEFAULT 0,
    StokKodu NVARCHAR(50),
    BarkodNo NVARCHAR(50),
    NetMiktar DECIMAL(18,2),
    BrutMiktar DECIMAL(18,2) DEFAULT 0,
    BirimFiyat DECIMAL(18,4) DEFAULT 0,
    Depo NVARCHAR(50),
    Parti NVARCHAR(50),
    SeriNo NVARCHAR(50),
    UrunGrup1 NVARCHAR(100),
    UrunGrup2 NVARCHAR(50),
    UrunGrup3 NVARCHAR(50),
    UrunGrup4 NVARCHAR(50),
    UrunGrup5 NVARCHAR(50),
    Aciklamalar NVARCHAR(MAX),
    Grup1 NVARCHAR(50),
    Grup2 NVARCHAR(50),
    Grup3 NVARCHAR(50),
    Grup4 NVARCHAR(50),
    Grup5 NVARCHAR(50),
    MiktarBirimi NVARCHAR(20) DEFAULT 'ADET',
    YeniBarkodNo NVARCHAR(50),
    KdvORani DECIMAL(5,2) DEFAULT 0,
    YBrutMiktar DECIMAL(18,2) DEFAULT 0,
    YDara DECIMAL(18,2) DEFAULT 0,
    Miktar1 DECIMAL(18,2) DEFAULT 0,
    Miktar2 DECIMAL(18,2) DEFAULT 0,
    Miktar3 DECIMAL(18,2) DEFAULT 0,
    Miktar4 DECIMAL(18,2) DEFAULT 0,
    Miktar5 DECIMAL(18,2) DEFAULT 0,
    AraToplamLines DECIMAL(18,2) DEFAULT 0,
    upsize_ts BINARY(8),
    En DECIMAL(18,2) DEFAULT 0,
    Boy DECIMAL(18,2) DEFAULT 0,
    Yukseklik DECIMAL(18,2) DEFAULT 0,
    Agirlik DECIMAL(18,2) DEFAULT 0,
    Desi DECIMAL(18,2) DEFAULT 0,
    SevkEdildi INT DEFAULT 0,
    AmbalajMiktar INT DEFAULT 1,
    indirimtutari DECIMAL(18,2) DEFAULT 0,
    KoliDara DECIMAL(18,2) DEFAULT 0,
    BobinDara DECIMAL(18,2) DEFAULT 0,
    TBobinDara DECIMAL(18,2) DEFAULT 0,
    SatirNo INT DEFAULT 1,
    StokRefNo INT,
    DepoRefNo INT DEFAULT 1,
    RafRefNo INT DEFAULT 5346,
    StokTuru INT DEFAULT 0,
    EtiketKontrol INT DEFAULT 0,
    IslemTipi INT DEFAULT 0,
    TransLinesIdno INT DEFAULT 0,
    GUIDX NVARCHAR(100),
    KULLANICI INT DEFAULT 8215,
    ProjeKodu NVARCHAR(50),
    YeniPartiNo NVARCHAR(50)
);

-- yr_BilgiLines Tablosu (FisNo Yönetimi)
CREATE TABLE yr_BilgiLines (
    Link_Numara INT PRIMARY KEY,
    Deger BIGINT
);

-- Test Verileri - FAYS
-- FisNo başlangıç değeri
INSERT INTO yr_BilgiLines (Link_Numara, Deger) VALUES (99102, 1067968);

-- Test Fişleri (Mevcut stok hareketleri)
-- Giriş Fişi
INSERT INTO stk_Fis (FisTuru, FisNo, GirisCikis, Tarih, Aciklamalar, Grup3, Status, DepoRefNo, Islemvar, IslemKullanici, IadeKontrol, DevamDurumu)
VALUES (10, 1000001, 1, '2025-01-01', 'İLK GİRİŞ', 'MERKEZ', 0, 1, 0, 0, 0, 3);

-- Fiş Satırları (FAYS stokları - LOGO'dan farklı olacak şekilde)
-- 61007030: LOGO'da 100, FAYS'da 120 olacak (20 fazla - sayım eksiği gerekecek)
INSERT INTO stk_FisLines (Link_FisNo, StokKodu, BarkodNo, NetMiktar, Depo, UrunGrup1, MiktarBirimi, StokRefNo, GUIDX)
VALUES (1000001, '61007030', '343405444', 120.00, 'MERKEZ', 'BULAŞIK MAKİNESİ DETERJAN', 'ADET', 1, '10000011MERKEZ');

-- 509V0004: Her iki tarafta da 56 (fark yok)
INSERT INTO stk_FisLines (Link_FisNo, StokKodu, BarkodNo, NetMiktar, Depo, UrunGrup1, MiktarBirimi, StokRefNo, GUIDX)
VALUES (1000001, '509V0004', '343405445', 56.00, 'MERKEZ', 'P-50 GİYOTİN BULAŞIK MAK.', 'ADET', 2, '10000012MERKEZ');

-- 343403022: LOGO'da 75, FAYS'da 60 olacak (15 eksik - sayım fazlası gerekecek)
INSERT INTO stk_FisLines (Link_FisNo, StokKodu, BarkodNo, NetMiktar, Depo, UrunGrup1, MiktarBirimi, StokRefNo, GUIDX)
VALUES (1000001, '343403022', '343403022', 60.00, 'MERKEZ', 'TEMİZLİK MALZEMESİ', 'ADET', 3, '10000013MERKEZ');

-- TEST001: LOGO'da 200, FAYS'da 180 olacak (20 eksik - sayım fazlası gerekecek)
INSERT INTO stk_FisLines (Link_FisNo, StokKodu, BarkodNo, NetMiktar, Depo, UrunGrup1, MiktarBirimi, StokRefNo, GUIDX)
VALUES (1000001, 'TEST001', 'TEST001', 180.00, 'MERKEZ', 'TEST ÜRÜN 1', 'ADET', 4, '10000014MERKEZ');

-- TEST002: LOGO'da 0, FAYS'da 30 olacak (30 fazla - sayım eksiği gerekecek)
INSERT INTO stk_FisLines (Link_FisNo, StokKodu, BarkodNo, NetMiktar, Depo, UrunGrup1, MiktarBirimi, StokRefNo, GUIDX)
VALUES (1000001, 'TEST002', 'TEST002', 30.00, 'MERKEZ', 'TEST ÜRÜN 2', 'ADET', 5, '10000015MERKEZ');

GO

-- Özet Kontrol
USE GOLD;
SELECT 'LOGO Stok Kartları' as Info, COUNT(*) as Adet FROM LG_013_ITEMS;
SELECT 'LOGO Stok Durumu' as Info, COUNT(*) as Adet FROM LV_013_01_STINVTOT;
SELECT 'LOGO Depolar' as Info, COUNT(*) as Adet FROM L_CAPIWHOUSE;

USE FaysWMSAkturk;
SELECT 'FAYS Fişler' as Info, COUNT(*) as Adet FROM stk_Fis;
SELECT 'FAYS Fiş Satırları' as Info, COUNT(*) as Adet FROM stk_FisLines;

-- Beklenen Farklar (TEST İÇİN):
-- 61007030: FAYS 120, LOGO 100 = +20 FAZLA (Sayım Eksiği gerekli)
-- 509V0004: FAYS 56, LOGO 56 = 0 FARK YOK
-- 343403022: FAYS 60, LOGO 75 = -15 EKSİK (Sayım Fazlası gerekli)
-- TEST001: FAYS 180, LOGO 200 = -20 EKSİK (Sayım Fazlası gerekli)
-- TEST002: FAYS 30, LOGO 0 = +30 FAZLA (Sayım Eksiği gerekli)

PRINT 'Test veritabanları başarıyla oluşturuldu!';
GO

