"""
Veritabanı Bağlantı ve İşlemleri
"""
import pyodbc
import pandas as pd
from datetime import datetime
import logging
from config import Config

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stok_esitleme.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Veritabanı işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.conn_fays = None
        self.conn_logo = None
        
    def connect(self):
        """Veritabanlarına bağlan"""
        try:
            # FAYS WMS bağlantısı
            self.conn_fays = pyodbc.connect(Config.get_connection_string('FAYS'))
            logger.info("FAYS WMS veritabanına bağlanıldı")
            
            # LOGO ERP bağlantısı (aynı sunucuda farklı veritabanı)
            self.conn_logo = pyodbc.connect(Config.get_connection_string('LOGO'))
            logger.info("LOGO ERP veritabanına bağlanıldı")
            
            return True
        except Exception as e:
            logger.error(f"Veritabanı bağlantı hatası: {e}")
            return False
    
    def disconnect(self):
        """Veritabanı bağlantılarını kapat"""
        try:
            if self.conn_fays:
                self.conn_fays.close()
                logger.info("FAYS WMS bağlantısı kapatıldı")
            if self.conn_logo:
                self.conn_logo.close()
                logger.info("LOGO ERP bağlantısı kapatıldı")
        except Exception as e:
            logger.error(f"Bağlantı kapatma hatası: {e}")
    
    def execute_query(self, query, database='FAYS', params=None):
        """SQL sorgusu çalıştır ve sonuçları DataFrame olarak döndür"""
        try:
            conn = self.conn_fays if database == 'FAYS' else self.conn_logo
            
            if params:
                df = pd.read_sql(query, conn, params=params)
            else:
                df = pd.read_sql(query, conn)
            
            logger.info(f"{database} veritabanında sorgu çalıştırıldı: {len(df)} kayıt")
            return df
        except Exception as e:
            logger.error(f"Sorgu çalıştırma hatası ({database}): {e}")
            raise
    
    def execute_non_query(self, query, database='FAYS', params=None):
        """INSERT/UPDATE/DELETE sorgusu çalıştır"""
        try:
            conn = self.conn_fays if database == 'FAYS' else self.conn_logo
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            
            logger.info(f"{database} veritabanında {rows_affected} kayıt etkilendi")
            return rows_affected
        except Exception as e:
            logger.error(f"Non-query çalıştırma hatası ({database}): {e}")
            raise
    
    def get_stock_comparison(self, custom_query=None):
        """
        Logo ve Fays stok karşılaştırması yap
        """
        try:
            if custom_query:
                query = custom_query
            else:
                query = self._get_default_comparison_query()
            
            # Sorguyu çalıştır (FAYS veritabanında)
            df = self.execute_query(query, database='FAYS')
            
            logger.info(f"Stok karşılaştırması tamamlandı: {len(df)} kayıt")
            return df
        except Exception as e:
            logger.error(f"Stok karşılaştırma hatası: {e}")
            raise
    
    def _get_default_comparison_query(self):
        """Varsayılan karşılaştırma sorgusunu döndür"""
        return """
        SELECT
            X.[MALZEME KODU],
            X.[MALZEME ADI],
            X.[GRUP KODU],
            X.[AMBAR ADI],
            ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [LOGO FİİLİ STOK],
            ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2) AS [FAYS STOK],
            ROUND(ISNULL(SUM(X.[FAYS STOK]),0),2)-ROUND(ISNULL(SUM(X.[FİİLİ STOK]),0),2) AS [FARK]
        FROM
        (
            SELECT     
                [AMBAR ADI] = AMBARLAR.NAME, 
                ITEMS.CODE AS [MALZEME KODU], 
                RTRIM(LTRIM(ITEMS.NAME)) AS [MALZEME ADI], 
                ISNULL(ITEMS.STGRPCODE,'') AS [GRUP KODU],
                ROUND(SUM(ST.ONHAND),2) AS [FİİLİ STOK],
                ROUND((SUM(ST.ONHAND) - SUM(ST.RESERVED) + SUM(ST.TEMPOUT) - SUM(ST.TEMPIN)),2) AS [GERÇEK STOK],
                ROUND(SUM(ST.ONHAND)-SUM(ST.RESERVED),2) AS [SEVKEDİLEBİLİR STOK], 
                0 AS [FAYS STOK]
            FROM         
                GOLD..LG_013_ITEMS AS ITEMS WITH (NOLOCK)		 
                INNER JOIN GOLD..LV_013_01_STINVTOT AS ST WITH (NOLOCK) ON ST.STOCKREF = ITEMS.LOGICALREF 
                LEFT JOIN GOLD..L_CAPIWHOUSE AS AMBARLAR WITH (NOLOCK) ON AMBARLAR.NR = ST.INVENNO AND AMBARLAR.FIRMNR = '013' 
            WHERE ST.INVENNO <> -1 AND ITEMS.ACTIVE=0
            GROUP BY  
                ITEMS.CODE, 
                ITEMS.NAME, 
                ITEMS.STGRPCODE,
                ST.INVENNO, 
                AMBARLAR.NAME
            
            UNION ALL
            
            SELECT    
                CAST(A.DEPO AS VARCHAR(50)) COLLATE Turkish_CI_AS AS [AMBAR ADI],
                CAST(A.StokKodu AS VARCHAR(50)) COLLATE Turkish_CI_AS AS MALZEME_KODU, 
                RTRIM(LTRIM(CAST(A.STOK_ADI AS VARCHAR(50)) COLLATE Turkish_CI_AS)) AS MALZEME_ADI,
                A.[GRUP KODU] AS [GRUP KODU],
                0 AS [FİİLİ STOK],
                0 AS [GERÇEK STOK],
                0 AS [SEVKEDİLEBİLİR STOK],
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
                GROUP BY 
                    FL.Depo,
                    FL.StokKodu, 
                    FL.UrunGrup1, 
                    I.STGRPCODE,
                    F.GirisCikis
            ) AS A
            GROUP BY 
                A.DEPO,
                A.STOKKODU,
                A.STOK_ADI,
                A.[GRUP KODU]
        ) X
        GROUP BY 
            X.[MALZEME KODU],
            X.[MALZEME ADI],
            X.[GRUP KODU],
            X.[AMBAR ADI]
        """
    
    def get_next_fisno(self):
        """yr_BilgiLines tablosundan sonraki FisNo'yu al ve artır"""
        try:
            # Mevcut numarayı al
            query = f"""
            SELECT Deger 
            FROM yr_BilgiLines 
            WHERE Link_Numara = {Config.FISNO_LINK_NUMARASI}
            """
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            
            if row:
                current_fisno = int(row[0])
                next_fisno = current_fisno + 1
                
                # Numarayı güncelle
                update_query = f"""
                UPDATE yr_BilgiLines 
                SET Deger = {next_fisno}
                WHERE Link_Numara = {Config.FISNO_LINK_NUMARASI}
                """
                cursor.execute(update_query)
                self.conn_fays.commit()
                cursor.close()
                
                logger.info(f"Yeni FisNo alındı: {next_fisno}")
                return next_fisno
            else:
                logger.error("yr_BilgiLines tablosunda FisNo bulunamadı")
                raise Exception("FisNo alınamadı")
                
        except Exception as e:
            logger.error(f"FisNo alma hatası: {e}")
            raise
    
    def create_fis_record(self, fisno, fis_turu, giris_cikis, depo, aciklama, depo_ref_no=None):
        """stk_Fis tablosuna kayıt oluştur"""
        try:
            # Tarih formatı: YYYY-MM-DD (Yıl-Ay-Gün)
            tarih = datetime.now().strftime('%Y-%m-%d')
            
            # DepoRefNo yoksa stk_depo tablosundan al
            if depo_ref_no is None:
                depo_ref_no = self.get_depo_ref_no(depo)
            
            query = """
            INSERT INTO stk_Fis (
                FisTuru, FisNo, GirisCikis, Tarih, FirmaKodu, FirmaAdi, 
                KdvOrani, AraToplam, calcGenelToplam, DovizKuru, 
                Aciklamalar, Grup3, KdvDegeri, LogoKontrol, Status, 
                DepoRefNo, Islemvar, IslemKullanici, IadeKontrol, DevamDurumu
            ) VALUES (
                ?, ?, ?, ?, '', '', 0, 0.00, 0.00, 0.00, ?, ?, 0.00,
                0, 0, ?, 0, 0, 0, 3
            )
            """
            
            params = (fis_turu, fisno, giris_cikis, tarih, aciklama, depo, depo_ref_no)
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query, params)
            self.conn_fays.commit()
            
            # idNo'yu al
            cursor.execute("SELECT @@IDENTITY")
            idno = cursor.fetchone()[0]
            cursor.close()
            
            logger.info(f"Fiş kaydı oluşturuldu - FisNo: {fisno}, idNo: {idno}, DepoRefNo: {depo_ref_no}")
            return idno
            
        except Exception as e:
            logger.error(f"Fiş kayıt oluşturma hatası: {e}")
            raise
    
    def create_fislines_record(self, link_fisno, stok_kodu, barkod_no, net_miktar, 
                              depo, urun_grup1, grup_kodu, stok_ref_no, depo_ref_no=None, raf_ref_no=None, raf_adi=None):
        """stk_FisLines tablosuna kayıt oluştur"""
        try:
            # GUIDX oluştur
            guidx = f"{link_fisno}{len(str(link_fisno))}{stok_ref_no}{depo[0] if depo else 'X'}"
            
            # DepoRefNo yoksa stk_depo tablosundan al
            if depo_ref_no is None:
                depo_ref_no = self.get_depo_ref_no(depo)
            
            # RafRefNo yoksa varsayılan kullan (kullanıcı seçmemişse)
            if raf_ref_no is None:
                raf_ref_no = 5346  # Varsayılan raf
            
            # Raf adını al (raf_ref_no'dan veya parametreden)
            if raf_adi is None and raf_ref_no:
                raf_adi = self.get_raf_adi(raf_ref_no)
            
            query = """
            INSERT INTO stk_FisLines (
                Link_FisNo, StokKodu, BarkodNo, NetMiktar, BrutMiktar, BirimFiyat,
                Depo, UrunGrup1, UrunGrup5, MiktarBirimi, KdvORani, YBrutMiktar, YDara,
                Miktar1, Miktar2, Miktar3, Miktar4, Miktar5, AraToplamLines,
                En, Boy, Yukseklik, Agirlik, Desi, SevkEdildi, AmbalajMiktar,
                indirimtutari, KoliDara, BobinDara, TBobinDara, SatirNo,
                StokRefNo, DepoRefNo, RafRefNo, StokTuru, EtiketKontrol,
                IslemTipi, TransLinesIdno, GUIDX, KULLANICI
            ) VALUES (
                ?, ?, ?, ?, 0, 0.00,
                ?, ?, ?, 'ADET', 0, 0, 0,
                0, 0, 0, 0, 0, 0.00,
                0, 0, 0, 0, 0, 0, 1,
                0.00, 0, 0, 0, 1,
                ?, ?, ?, 0, 0,
                0, 0, ?, 8215
            )
            """
            
            params = (
                link_fisno, stok_kodu, barkod_no, net_miktar,
                depo, urun_grup1, raf_adi or '', stok_ref_no, depo_ref_no, raf_ref_no, guidx
            )
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query, params)
            self.conn_fays.commit()
            
            # idNo'yu al
            cursor.execute("SELECT @@IDENTITY")
            idno = cursor.fetchone()[0]
            cursor.close()
            
            logger.info(f"Fiş satırı oluşturuldu - StokKodu: {stok_kodu}, Miktar: {net_miktar}, DepoRefNo: {depo_ref_no}, RafRefNo: {raf_ref_no}")
            return idno
            
        except Exception as e:
            logger.error(f"Fiş satırı oluşturma hatası: {e}")
            raise
    
    def get_depo_ref_no(self, depo_adi):
        """stk_depo tablosundan DepoRefNo al"""
        try:
            query = """
            SELECT idNo 
            FROM stk_depo 
            WHERE DepoAdi = ? OR DepoAdi COLLATE Turkish_CI_AS = ?
            """
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query, (depo_adi, depo_adi))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return int(row[0])
            else:
                logger.warning(f"DepoRefNo bulunamadı: {depo_adi}, varsayılan 1 kullanılıyor")
                return 1
        except Exception as e:
            logger.error(f"DepoRefNo alma hatası: {e}")
            return 1
    
    def get_raf_ref_no(self, depo_adi, raf_adi=None):
        """stk_urungrup5 tablosundan RafRefNo al"""
        try:
            if raf_adi:
                # Belirli raf adına göre ara
                query = """
                SELECT idNo 
                FROM stk_urungrup5 
                WHERE DepoRefNo = (SELECT idNo FROM stk_depo WHERE DepoAdi = ? OR DepoAdi COLLATE Turkish_CI_AS = ?)
                  AND (RafAdi = ? OR RafAdi COLLATE Turkish_CI_AS = ?)
                """
                depo_ref_no = self.get_depo_ref_no(depo_adi)
                cursor = self.conn_fays.cursor()
                cursor.execute(query, (depo_adi, depo_adi, raf_adi, raf_adi))
            else:
                # Varsayılan rafı bul (depoya göre)
                depo_ref_no = self.get_depo_ref_no(depo_adi)
                query = """
                SELECT TOP 1 idNo 
                FROM stk_urungrup5 
                WHERE DepoRefNo = ?
                ORDER BY idNo
                """
                cursor = self.conn_fays.cursor()
                cursor.execute(query, (depo_ref_no,))
            
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return int(row[0])
            else:
                logger.warning(f"RafRefNo bulunamadı - Depo: {depo_adi}, Raf: {raf_adi or 'Varsayılan'}, varsayılan 5346 kullanılıyor")
                return 5346
        except Exception as e:
            logger.error(f"RafRefNo alma hatası: {e}")
            return 5346
    
    def get_raf_adi(self, raf_ref_no):
        """RafRefNo'ya göre raf adını al"""
        try:
            query = """
            SELECT RafAdi 
            FROM stk_urungrup5 
            WHERE idNo = ?
            """
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query, (raf_ref_no,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return row[0] if row[0] else ''
            else:
                logger.warning(f"Raf adı bulunamadı - RafRefNo: {raf_ref_no}")
                return ''
        except Exception as e:
            logger.error(f"Raf adı alma hatası: {e}")
            return ''
    
    def get_raflar(self, depo_adi):
        """Seçilen depoya göre raf listesini al"""
        try:
            depo_ref_no = self.get_depo_ref_no(depo_adi)
            
            query = """
            SELECT idNo, RafAdi 
            FROM stk_urungrup5 
            WHERE DepoRefNo = ?
            ORDER BY RafAdi
            """
            
            df = self.execute_query(query, database='FAYS', params=(depo_ref_no,))
            
            # DataFrame'den liste oluştur [(idNo, RafAdi), ...]
            raflar = []
            if len(df) > 0:
                for _, row in df.iterrows():
                    raflar.append({
                        'idNo': int(row['idNo']),
                        'RafAdi': row['RafAdi'] if pd.notna(row['RafAdi']) else ''
                    })
            
            logger.info(f"{depo_adi} deposu için {len(raflar)} adet raf bulundu")
            return raflar
        except Exception as e:
            logger.error(f"Raf listesi alma hatası: {e}")
            return []
    
    def get_stok_ref_no_fays(self, stok_kodu):
        """stk_kart tablosundan StokRefNo al (FAYS)"""
        try:
            query = """
            SELECT idNo 
            FROM stk_kart 
            WHERE StokKodu = ? OR StokKodu COLLATE Turkish_CI_AS = ?
            """
            
            cursor = self.conn_fays.cursor()
            cursor.execute(query, (stok_kodu, stok_kodu))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return int(row[0])
            else:
                logger.warning(f"FAYS StokRefNo bulunamadı: {stok_kodu}, LOGO'dan alınacak")
                return None
        except Exception as e:
            logger.error(f"FAYS StokRefNo alma hatası: {e}")
            return None
    
    def get_fays_stocks_with_raf(self, depo_adi):
        """FAYS özet raporda bulunan stokları raf bilgisiyle birlikte al"""
        query = """
        SELECT 
            RTRIM(LTRIM(ln.depo)) AS [Depo Adı],
            RTRIM(LTRIM(LN.StokKodu)) AS [Ürün Kodu],
            RTRIM(LTRIM(LN.barkodno)) AS [Standart Barkod No],
            RTRIM(LTRIM(LN.urungrup1)) AS [Ürün Adı],
            I.STGRPCODE AS [Grup Kodu],
            RTRIM(LTRIM(LN.miktarbirimi)) AS [Birimi],
            RTRIM(LTRIM(LN.urungrup5)) AS [Raf Adı],
            LN.RafRefNo AS [RafRefNo],
            LN.DepoRefNo AS [DepoRefNo],
            LN.StokRefNo AS [StokRefNo],
            SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) as NetMiktar
        FROM dbo.stk_Fis AS FS WITH (NOLOCK) 
        LEFT OUTER JOIN dbo.stk_FisLines AS LN WITH (NOLOCK) ON LN.Link_FisNo = FS.FisNo
        LEFT JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=LN.StokKodu COLLATE Turkish_CI_AS
        WHERE LN.depo = ? OR LN.depo COLLATE Turkish_CI_AS = ?
        GROUP BY 
            ln.depo,
            LN.StokKodu,
            LN.barkodno,
            LN.urungrup1,
            I.STGRPCODE,
            LN.miktarbirimi,
            LN.urungrup5,
            LN.RafRefNo,
            LN.DepoRefNo,
            LN.StokRefNo
        HAVING SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) <> 0.00
        """
        
        return self.execute_query(query, database='FAYS', params=(depo_adi, depo_adi))
    
    def get_fays_stock_summary(self):
        """FAYS WMS özet stok raporu"""
        query = """
        SELECT 
            RTRIM(LTRIM(ln.depo)) AS [Depo Adı],
            RTRIM(LTRIM(LN.StokKodu)) AS [Ürün Kodu],
            RTRIM(LTRIM(LN.barkodno)) AS [Standart Barkod No],
            RTRIM(LTRIM(LN.urungrup1)) AS [Ürün Adı],
            I.STGRPCODE AS [Grup Kodu],
            RTRIM(LTRIM(LN.miktarbirimi)) AS [Birimi],
            RTRIM(LTRIM(LN.urungrup5)) AS [Raf Adı],
            SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) as NetMiktar
        FROM dbo.stk_Fis AS FS WITH (NOLOCK) 
        LEFT OUTER JOIN dbo.stk_FisLines AS LN WITH (NOLOCK) ON LN.Link_FisNo = FS.FisNo
        LEFT JOIN GOLD..LG_013_ITEMS AS I ON I.CODE=LN.StokKodu COLLATE Turkish_CI_AS
        GROUP BY 
            ln.depo,
            LN.StokKodu,
            LN.barkodno,
            LN.urungrup1,
            I.STGRPCODE,
            LN.miktarbirimi,
            LN.urungrup5
        HAVING SUM(CASE WHEN FS.giriscikis=2 THEN (-1)*LN.NetMiktar ELSE LN.NetMiktar END) <> 0.00
        """
        
        return self.execute_query(query, database='FAYS')
    
    def test_connection(self):
        """Bağlantıyı test et"""
        try:
            # FAYS test
            cursor_fays = self.conn_fays.cursor()
            cursor_fays.execute("SELECT 1")
            cursor_fays.close()
            
            # LOGO test
            cursor_logo = self.conn_logo.cursor()
            cursor_logo.execute("SELECT 1")
            cursor_logo.close()
            
            return True
        except Exception as e:
            logger.error(f"Bağlantı test hatası: {e}")
            return False

