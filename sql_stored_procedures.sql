-- ============================================================================
-- LOGO - FAYS WMS Stok Eşitleme - SQL Stored Procedures
-- Python OLMADAN çalışır - Sadece SQL Server Management Studio / Azure Data Studio
-- ============================================================================

USE FaysWMSAkturk;
GO

-- ============================================================================
-- 1. Stored Procedure: Stok Karşılaştırma
-- ============================================================================

IF OBJECT_ID('sp_StokKarsilastirma', 'P') IS NOT NULL
    DROP PROCEDURE sp_StokKarsilastirma;
GO

CREATE PROCEDURE sp_StokKarsilastirma
    @Depo NVARCHAR(50) = NULL  -- NULL = Tüm depolar
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT
        X.[MALZEME KODU],
        X.[MALZEME ADI],
        X.[GRUP KODU],
        X.[AMBAR ADI],
        ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [LOGO FİİLİ STOK],
        ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2) AS [FAYS STOK],
        ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [FARK],
        CASE 
            WHEN ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) > 0 
            THEN 'FAYS FAZLA - Sayım Eksiği Gerekli'
            WHEN ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) < 0 
            THEN 'FAYS EKSİK - Sayım Fazlası Gerekli'
            ELSE 'EŞİT'
        END AS [DURUM]
    FROM
    (
        SELECT     
            [AMBAR ADI] = AMBARLAR.NAME, 
            ITEMS.CODE AS [MALZEME KODU], 
            RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
            ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
            ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
            0 AS [FAYS STOK]
        FROM         
            GOLD..LG_013_ITEMS AS ITEMS WITH (NOLOCK)
            INNER JOIN GOLD..LV_013_01_STINVTOT AS ST WITH (NOLOCK) ON ST.STOCKREF = ITEMS.LOGICALREF 
            LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR WITH (NOLOCK) ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013' 
        WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
        GROUP BY ITEMS.CODE, ITEMS.NAME, ITEMS.STGRPCODE, ST.INVENNO, AMBARLAR.NAME
        
        UNION ALL
        
        SELECT    
            CAST(A.DEPO AS VARCHAR(50)) COLLATE Turkish_CI_AS AS [AMBAR ADI],
            CAST(A.StokKodu AS VARCHAR(50)) COLLATE Turkish_CI_AS AS MALZEME_KODU, 
            RTRIM(LTRIM(CAST(A.STOK_ADI AS VARCHAR(50)) COLLATE Turkish_CI_AS)) AS MALZEME_ADI,
            A.[GRUP KODU] AS [GRUP KODU],
            0 AS [FİİLİ STOK],
            ROUND(ISNULL(SUM(A.GIRIS_TOPLAM),0),2) - ROUND(ISNULL(SUM(A.CIKIS_TOPLAM),0),2) AS FAYS_MIKTAR
        FROM         
        (
            SELECT     
                FL.Depo AS DEPO,
                FL.StokKodu, 
                FL.UrunGrup1 AS STOK_ADI,
                I.STGRPCODE AS [GRUP KODU],
                CASE F.GirisCikis 
                    WHEN 1 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) 
                    ELSE 0 
                END AS GIRIS_TOPLAM,
                CASE F.GirisCikis 
                    WHEN 2 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) 
                    ELSE 0 
                END AS CIKIS_TOPLAM
            FROM          
                dbo.stk_Fis AS F WITH (NOLOCK)  
                INNER JOIN stk_FisLines AS FL WITH (NOLOCK) ON F.FisNo = FL.Link_FisNo 
                LEFT OUTER JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=FL.StokKodu COLLATE Turkish_CI_AS
            GROUP BY FL.Depo, FL.StokKodu, FL.UrunGrup1, I.STGRPCODE, F.GirisCikis
        ) AS A
        GROUP BY A.DEPO, A.STOKKODU, A.STOK_ADI, A.[GRUP KODU]
    ) X
    WHERE (@Depo IS NULL OR X.[AMBAR ADI] = @Depo)
    GROUP BY X.[MALZEME KODU], X.[MALZEME ADI], X.[GRUP KODU], X.[AMBAR ADI]
    HAVING ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) <> 0
    ORDER BY X.[MALZEME KODU];
END
GO

PRINT '✓ sp_StokKarsilastirma oluşturuldu';
GO

-- ============================================================================
-- 2. Stored Procedure: Otomatik Stok Eşitleme
-- ============================================================================

IF OBJECT_ID('sp_StokEsitleme', 'P') IS NOT NULL
    DROP PROCEDURE sp_StokEsitleme;
GO

CREATE PROCEDURE sp_StokEsitleme
    @Depo NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @FisNo BIGINT;
    DECLARE @FisNoFazla BIGINT;
    DECLARE @FisNoEksik BIGINT;
    DECLARE @Tarih DATETIME = GETDATE();
    DECLARE @ToplamFazla INT = 0;
    DECLARE @ToplamEksik INT = 0;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Geçici tablo: Farkları sakla
        CREATE TABLE #StokFarklari (
            MalzemeKodu NVARCHAR(50),
            MalzemeAdi NVARCHAR(100),
            GrupKodu NVARCHAR(20),
            LogoStok DECIMAL(18,2),
            FaysStok DECIMAL(18,2),
            Fark DECIMAL(18,2),
            StokRefNo INT
        );
        
        -- Farkları hesapla
        INSERT INTO #StokFarklari
        SELECT
            X.[MALZEME KODU],
            X.[MALZEME ADI],
            X.[GRUP KODU],
            ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [LOGO STOK],
            ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2) AS [FAYS STOK],
            ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [FARK],
            (SELECT TOP 1 LOGICALREF FROM GOLD..LG_013_ITEMS WHERE CODE = X.[MALZEME KODU]) AS StokRefNo
        FROM
        (
            SELECT     
                [AMBAR ADI] = AMBARLAR.NAME, 
                ITEMS.CODE AS [MALZEME KODU], 
                RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
                ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
                ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
                0 AS [FAYS STOK]
            FROM         
                GOLD..LG_013_ITEMS AS ITEMS
                INNER JOIN GOLD..LV_013_01_STINVTOT AS ST ON ST.STOCKREF = ITEMS.LOGICALREF 
                LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013' 
            WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
            GROUP BY ITEMS.CODE, ITEMS.NAME, ITEMS.STGRPCODE, ST.INVENNO, AMBARLAR.NAME
            
            UNION ALL
            
            SELECT    
                CAST(A.DEPO AS VARCHAR(50)) AS [AMBAR ADI],
                CAST(A.StokKodu AS VARCHAR(50)) AS MALZEME_KODU, 
                RTRIM(LTRIM(CAST(A.STOK_ADI AS VARCHAR(50)))) AS MALZEME_ADI,
                A.[GRUP KODU],
                0 AS [FİİLİ STOK],
                ROUND(ISNULL(SUM(A.GIRIS_TOPLAM),0),2) - ROUND(ISNULL(SUM(A.CIKIS_TOPLAM),0),2)
            FROM         
            (
                SELECT     
                    FL.Depo AS DEPO,
                    FL.StokKodu, 
                    FL.UrunGrup1 AS STOK_ADI,
                    I.STGRPCODE AS [GRUP KODU],
                    CASE F.GirisCikis WHEN 1 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) ELSE 0 END AS GIRIS_TOPLAM,
                    CASE F.GirisCikis WHEN 2 THEN ROUND(ISNULL(SUM(FL.NetMiktar),0),2) ELSE 0 END AS CIKIS_TOPLAM
                FROM dbo.stk_Fis AS F  
                INNER JOIN stk_FisLines AS FL ON F.FisNo = FL.Link_FisNo 
                LEFT OUTER JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=FL.StokKodu
                GROUP BY FL.Depo, FL.StokKodu, FL.UrunGrup1, I.STGRPCODE, F.GirisCikis
            ) AS A
            GROUP BY A.DEPO, A.STOKKODU, A.STOK_ADI, A.[GRUP KODU]
        ) X
        WHERE X.[AMBAR ADI] = @Depo
        GROUP BY X.[MALZEME KODU], X.[MALZEME ADI], X.[GRUP KODU], X.[AMBAR ADI]
        HAVING ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) <> 0;
        
        -- FAZLA OLANLAR (Sayım Eksiği Fişi - FisTuru=51)
        IF EXISTS (SELECT 1 FROM #StokFarklari WHERE Fark > 0)
        BEGIN
            -- FisNo al
            SELECT @FisNoEksik = CAST(Deger AS BIGINT) + 1
            FROM yr_BilgiLines WHERE Link_Numara = 99102;
            
            -- yr_BilgiLines güncelle
            UPDATE yr_BilgiLines SET Deger = @FisNoEksik WHERE Link_Numara = 99102;
            
            -- Ana fiş oluştur
            INSERT INTO stk_Fis (FisTuru, FisNo, GirisCikis, Tarih, Aciklamalar, Grup3, 
                                KdvOrani, AraToplam, calcGenelToplam, DovizKuru, KdvDegeri,
                                LogoKontrol, Status, DepoRefNo, Islemvar, IslemKullanici, IadeKontrol, DevamDurumu)
            VALUES (51, @FisNoEksik, 2, @Tarih, '0.KAT:SAYILMAYAN VE STOKTA FAZLA OLAN STOKLAR', @Depo,
                    0, 0.00, 0.00, 0.00, 0.00, 0, 0, 1, 0, 0, 0, 3);
            
            -- Satırları ekle
            INSERT INTO stk_FisLines (Link_FisNo, StokKodu, NetMiktar, Depo, UrunGrup1, MiktarBirimi,
                                     StokRefNo, DepoRefNo, RafRefNo, GUIDX, KULLANICI, SatirNo)
            SELECT 
                @FisNoEksik,
                MalzemeKodu,
                ABS(Fark),
                @Depo,
                MalzemeAdi,
                'ADET',
                StokRefNo,
                1,
                5346,
                CAST(@FisNoEksik AS VARCHAR) + CAST(ROW_NUMBER() OVER (ORDER BY MalzemeKodu) AS VARCHAR),
                8215,
                ROW_NUMBER() OVER (ORDER BY MalzemeKodu)
            FROM #StokFarklari WHERE Fark > 0;
            
            SET @ToplamEksik = @@ROWCOUNT;
        END
        
        -- EKSİK OLANLAR (Sayım Fazlası Fişi - FisTuru=50)
        IF EXISTS (SELECT 1 FROM #StokFarklari WHERE Fark < 0)
        BEGIN
            -- FisNo al
            SELECT @FisNoFazla = CAST(Deger AS BIGINT) + 1
            FROM yr_BilgiLines WHERE Link_Numara = 99102;
            
            -- yr_BilgiLines güncelle
            UPDATE yr_BilgiLines SET Deger = @FisNoFazla WHERE Link_Numara = 99102;
            
            -- Ana fiş oluştur
            INSERT INTO stk_Fis (FisTuru, FisNo, GirisCikis, Tarih, Aciklamalar, Grup3,
                                KdvOrani, AraToplam, calcGenelToplam, DovizKuru, KdvDegeri,
                                LogoKontrol, Status, DepoRefNo, Islemvar, IslemKullanici, IadeKontrol, DevamDurumu)
            VALUES (50, @FisNoFazla, 1, @Tarih, '0.KAT:SAYIM YAPILAN VE SAYIM FAZLASI VEREN STOKLAR', @Depo,
                    0, 0.00, 0.00, 0.00, 0.00, 0, 0, 1, 0, 0, 0, 3);
            
            -- Satırları ekle
            INSERT INTO stk_FisLines (Link_FisNo, StokKodu, NetMiktar, Depo, UrunGrup1, MiktarBirimi,
                                     StokRefNo, DepoRefNo, RafRefNo, GUIDX, KULLANICI, SatirNo)
            SELECT 
                @FisNoFazla,
                MalzemeKodu,
                ABS(Fark),
                @Depo,
                MalzemeAdi,
                'ADET',
                StokRefNo,
                1,
                5346,
                CAST(@FisNoFazla AS VARCHAR) + CAST(ROW_NUMBER() OVER (ORDER BY MalzemeKodu) AS VARCHAR),
                8215,
                ROW_NUMBER() OVER (ORDER BY MalzemeKodu)
            FROM #StokFarklari WHERE Fark < 0;
            
            SET @ToplamFazla = @@ROWCOUNT;
        END
        
        COMMIT TRANSACTION;
        
        -- Sonuç mesajı
        SELECT 
            'Eşitleme Başarılı!' AS Mesaj,
            @ToplamFazla + @ToplamEksik AS [Toplam İşlem],
            @ToplamFazla AS [Sayım Fazlası Kalem],
            @ToplamEksik AS [Sayım Eksiği Kalem],
            @FisNoFazla AS [Fazla FisNo],
            @FisNoEksik AS [Eksik FisNo];
        
        DROP TABLE #StokFarklari;
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SELECT 
            'HATA!' AS Durum,
            ERROR_MESSAGE() AS Mesaj,
            ERROR_LINE() AS Satir;
    END CATCH
END
GO

PRINT '✓ sp_StokEsitleme oluşturuldu';
GO

-- ============================================================================
-- KULLANIM ÖRNEKLERİ
-- ============================================================================

PRINT '';
PRINT '════════════════════════════════════════════════════════════════';
PRINT 'KULLANIM ÖRNEKLERİ:';
PRINT '════════════════════════════════════════════════════════════════';
PRINT '';
PRINT '1. STOK KARŞILAŞTIRMA:';
PRINT '   EXEC sp_StokKarsilastirma ''MERKEZ''';
PRINT '   EXEC sp_StokKarsilastirma NULL  -- Tüm depolar';
PRINT '';
PRINT '2. STOK EŞİTLEME:';
PRINT '   EXEC sp_StokEsitleme ''MERKEZ''';
PRINT '';
PRINT '3. SON OLUŞTURULAN FİŞLERİ GÖRME:';
PRINT '   SELECT TOP 10 * FROM stk_Fis ORDER BY idNo DESC';
PRINT '   SELECT TOP 10 * FROM stk_FisLines ORDER BY idNo DESC';
PRINT '';
PRINT '════════════════════════════════════════════════════════════════';
PRINT '✅ Stored Procedures hazır!';
PRINT '════════════════════════════════════════════════════════════════';
GO

