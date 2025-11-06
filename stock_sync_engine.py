"""
Stok Eşitleme İşlemleri
"""
import pandas as pd
import logging
from datetime import datetime
from database import DatabaseManager
from config import Config

logger = logging.getLogger(__name__)


class StockSyncEngine:
    """Stok eşitleme işlemlerini yöneten sınıf"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def compare_stocks(self, warehouse=None, custom_query=None):
        """
        Stokları karşılaştır
        
        Args:
            warehouse: Belirli bir depo için filtreleme
            custom_query: Özel SQL sorgusu
            
        Returns:
            DataFrame: Karşılaştırma sonuçları
        """
        try:
            logger.info(f"Stok karşılaştırması başlatıldı - Depo: {warehouse or 'Tümü'}")
            
            # Karşılaştırma sorgusunu çalıştır
            df = self.db.get_stock_comparison(custom_query)
            
            # Depo filtresi varsa uygula
            if warehouse and warehouse != "Tümü":
                df = df[df['AMBAR ADI'] == warehouse]
            
            # Sadece farkı olan kayıtları göster
            df_diff = df[df['FARK'] != 0].copy()
            
            # Fark türünü belirle
            df_diff['DURUM'] = df_diff['FARK'].apply(
                lambda x: 'FAYS FAZLA (Logo Eksik)' if x > 0 else 'FAYS EKSİK (Logo Fazla)'
            )
            
            logger.info(f"Karşılaştırma tamamlandı - Toplam fark: {len(df_diff)} kayıt")
            
            return df_diff
            
        except Exception as e:
            logger.error(f"Stok karşılaştırma hatası: {e}")
            raise
    
    def synchronize_stocks(self, warehouse, df_comparison=None, default_raf_ref_no=None):
        """
        Stokları eşitle - ÖNCE FAYS stoklarını 0 yap, SONRA LOGO stoklarına göre giriş yap
        
        Args:
            warehouse: Eşitleme yapılacak depo
            df_comparison: Karşılaştırma DataFrame'i (yoksa yeniden hesaplanır)
            default_raf_ref_no: Varsayılan raf referans numarası
            
        Returns:
            dict: Eşitleme sonuç raporu
        """
        try:
            logger.info(f"Stok eşitleme başlatıldı - Depo: {warehouse}")
            
            created_fis = []
            
            # ADIM 1: FAYS özet raporda bulunan TÜM stokları 0 yap (raf bilgisi dahil)
            logger.info("ADIM 1: FAYS stoklarını 0 yapma işlemi başlatılıyor...")
            df_fays_stocks = self.db.get_fays_stocks_with_raf(warehouse)
            
            if len(df_fays_stocks) > 0:
                logger.info(f"FAYS'da {len(df_fays_stocks)} adet stok kalemi bulundu, çıkış fişi oluşturulacak")
                
                # Tüm FAYS stoklarını çıkış fişi ile 0 yap
                fis_info = self._create_fays_zero_fisi(
                    df_fays_stocks,
                    warehouse,
                    default_raf_ref_no
                )
                created_fis.append(fis_info)
            else:
                logger.info("FAYS'da stok bulunamadı, 0 yapma işlemi atlandı")
            
            # ADIM 2: LOGO stoklarına göre giriş fişi oluştur
            logger.info("ADIM 2: LOGO stoklarına göre giriş fişi oluşturuluyor...")
            
            # Karşılaştırma yapılmamışsa yap
            if df_comparison is None:
                df_comparison = self.compare_stocks(warehouse)
            
            # Sadece LOGO'da olan stokları al (FAYS'da olmayan veya eksik olanlar)
            df_logo_stocks = df_comparison[df_comparison['LOGO FİİLİ STOK'] > 0].copy()
            
            if len(df_logo_stocks) > 0:
                logger.info(f"LOGO'da {len(df_logo_stocks)} adet stok kalemi bulundu, giriş fişi oluşturulacak")
                
                # LOGO stoklarına göre giriş fişi oluştur
                fis_info = self._create_logo_entry_fisi(
                    df_logo_stocks,
                    warehouse,
                    default_raf_ref_no
                )
                created_fis.append(fis_info)
            else:
                logger.info("LOGO'da stok bulunamadı, giriş fişi oluşturulmayacak")
            
            if len(created_fis) == 0:
                logger.info("Eşitlenecek kayıt bulunamadı")
                return {
                    'success': True,
                    'message': 'Stoklar zaten eşit, işlem gerekmedi',
                    'created_fis': []
                }
            
            result = {
                'success': True,
                'message': f'{len(created_fis)} adet fiş oluşturuldu',
                'created_fis': created_fis,
                'total_items': len(df_fays_stocks) + len(df_logo_stocks) if 'df_logo_stocks' in locals() else len(df_fays_stocks)
            }
            
            logger.info(f"Stok eşitleme tamamlandı - {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"Stok eşitleme hatası: {e}")
            return {
                'success': False,
                'message': f'Hata: {str(e)}',
                'created_fis': []
            }
    
    def _create_fays_zero_fisi(self, df_fays_stocks, warehouse, default_raf_ref_no=None):
        """
        FAYS stoklarını 0 yapmak için çıkış fişi oluştur (raf bilgisi dahil)
        
        Args:
            df_fays_stocks: FAYS özet raporda bulunan stoklar (raf bilgisi dahil)
            warehouse: Depo adı
            default_raf_ref_no: Varsayılan raf referans numarası
            
        Returns:
            dict: Oluşturulan fiş bilgileri
        """
        try:
            # Yeni FisNo al
            fisno = self.db.get_next_fisno()
            
            # Çıkış fişi (FisTuru=51, GirisCikis=2)
            aciklama = "0.KAT:FAYS STOKLARINI SIFIRLAMA İŞLEMİ"
            
            # Ana fiş kaydı oluştur
            fis_idno = self.db.create_fis_record(
                fisno=fisno,
                fis_turu=Config.FIS_SAYIM_EKSIGI,  # 51
                giris_cikis=2,  # Çıkış
                depo=warehouse,
                aciklama=aciklama
            )
            
            # Fiş satırlarını oluştur
            lines_created = 0
            for _, row in df_fays_stocks.iterrows():
                # Mevcut stok miktarını çıkış yap (0 yapmak için)
                net_miktar = abs(float(row['NetMiktar']))
                
                # RafRefNo'yu al (FAYS özet raporda varsa kullan, yoksa varsayılan)
                raf_ref_no = None
                if 'RafRefNo' in row and pd.notna(row['RafRefNo']):
                    raf_ref_no = int(row['RafRefNo'])
                elif default_raf_ref_no:
                    raf_ref_no = default_raf_ref_no
                else:
                    # stk_urungrup5 tablosundan varsayılan rafı al
                    raf_ref_no = self.db.get_raf_ref_no(warehouse)
                
                # DepoRefNo'yu al (FAYS özet raporda varsa kullan)
                depo_ref_no = None
                if 'DepoRefNo' in row and pd.notna(row['DepoRefNo']):
                    depo_ref_no = int(row['DepoRefNo'])
                
                # StokRefNo'yu al (FAYS özet raporda varsa kullan, yoksa stk_kart'tan)
                stok_ref_no = None
                if 'StokRefNo' in row and pd.notna(row['StokRefNo']):
                    stok_ref_no = int(row['StokRefNo'])
                else:
                    # stk_kart tablosundan al
                    stok_ref_no = self.db.get_stok_ref_no_fays(row['Ürün Kodu'])
                    if stok_ref_no is None:
                        # LOGO'dan al (fallback)
                        stok_ref_no = self._get_stok_ref_no(row['Ürün Kodu'])
                
                # Raf adını al (FAYS özet raporda varsa kullan)
                raf_adi = None
                if 'Raf Adı' in row and pd.notna(row['Raf Adı']):
                    raf_adi = str(row['Raf Adı']).strip()
                elif raf_ref_no:
                    raf_adi = self.db.get_raf_adi(raf_ref_no)
                
                self.db.create_fislines_record(
                    link_fisno=fisno,
                    stok_kodu=row['Ürün Kodu'],
                    barkod_no=row.get('Standart Barkod No', ''),
                    net_miktar=net_miktar,
                    depo=warehouse,
                    urun_grup1=row['Ürün Adı'],
                    grup_kodu=row.get('Grup Kodu', ''),
                    stok_ref_no=stok_ref_no,
                    depo_ref_no=depo_ref_no,
                    raf_ref_no=raf_ref_no,
                    raf_adi=raf_adi
                )
                lines_created += 1
            
            fis_info = {
                'fisno': fisno,
                'fis_idno': fis_idno,
                'fis_turu': Config.FIS_SAYIM_EKSIGI,
                'fis_turu_adi': 'FAYS Stoklarını Sıfırlama (Çıkış)',
                'lines_count': lines_created,
                'aciklama': aciklama
            }
            
            logger.info(f"FAYS sıfırlama fişi oluşturuldu - FisNo: {fisno}, Satır: {lines_created}")
            return fis_info
            
        except Exception as e:
            logger.error(f"FAYS sıfırlama fişi oluşturma hatası: {e}")
            raise
    
    def _create_logo_entry_fisi(self, df_logo_stocks, warehouse, default_raf_ref_no=None):
        """
        LOGO stoklarına göre giriş fişi oluştur
        
        Args:
            df_logo_stocks: LOGO'da bulunan stoklar
            warehouse: Depo adı
            default_raf_ref_no: Varsayılan raf referans numarası
            
        Returns:
            dict: Oluşturulan fiş bilgileri
        """
        try:
            # Yeni FisNo al
            fisno = self.db.get_next_fisno()
            
            # Giriş fişi (FisTuru=50, GirisCikis=1)
            aciklama = "0.KAT:LOGO STOKLARINA GÖRE SAYIM FAZLASI GİRİŞİ"
            
            # Ana fiş kaydı oluştur
            fis_idno = self.db.create_fis_record(
                fisno=fisno,
                fis_turu=Config.FIS_SAYIM_FAZLASI,  # 50
                giris_cikis=1,  # Giriş
                depo=warehouse,
                aciklama=aciklama
            )
            
            # RafRefNo'yu belirle
            raf_ref_no = default_raf_ref_no
            if raf_ref_no is None:
                # stk_urungrup5 tablosundan varsayılan rafı al
                raf_ref_no = self.db.get_raf_ref_no(warehouse)
            
            # Fiş satırlarını oluştur
            lines_created = 0
            for _, row in df_logo_stocks.iterrows():
                # LOGO'daki stok miktarını giriş yap
                net_miktar = abs(float(row['LOGO FİİLİ STOK']))
                
                # StokRefNo'yu LOGO'dan al
                stok_ref_no = self._get_stok_ref_no(row['MALZEME KODU'])
                
                # FAYS'ta stok kartı varsa onu kullan
                fays_stok_ref_no = self.db.get_stok_ref_no_fays(row['MALZEME KODU'])
                if fays_stok_ref_no:
                    stok_ref_no = fays_stok_ref_no
                
                # Raf adını al
                raf_adi = None
                if raf_ref_no:
                    raf_adi = self.db.get_raf_adi(raf_ref_no)
                
                self.db.create_fislines_record(
                    link_fisno=fisno,
                    stok_kodu=row['MALZEME KODU'],
                    barkod_no='',  # Barkod bilgisi LOGO'da yoksa boş
                    net_miktar=net_miktar,
                    depo=warehouse,
                    urun_grup1=row['MALZEME ADI'],
                    grup_kodu=row.get('GRUP KODU', ''),
                    stok_ref_no=stok_ref_no,
                    depo_ref_no=None,  # Otomatik alınacak
                    raf_ref_no=raf_ref_no,
                    raf_adi=raf_adi
                )
                lines_created += 1
            
            fis_info = {
                'fisno': fisno,
                'fis_idno': fis_idno,
                'fis_turu': Config.FIS_SAYIM_FAZLASI,
                'fis_turu_adi': 'LOGO Stoklarına Göre Giriş',
                'lines_count': lines_created,
                'aciklama': aciklama
            }
            
            logger.info(f"LOGO giriş fişi oluşturuldu - FisNo: {fisno}, Satır: {lines_created}")
            return fis_info
            
        except Exception as e:
            logger.error(f"LOGO giriş fişi oluşturma hatası: {e}")
            raise
    
    def _create_sayim_fisi(self, df_items, warehouse, fis_turu, aciklama):
        """
        Sayım fişi ve satırlarını oluştur (ESKİ METOD - Geriye uyumluluk için)
        
        Args:
            df_items: İşlenecek stok kalemleri
            warehouse: Depo adı
            fis_turu: Fiş türü (50 veya 51)
            aciklama: Fiş açıklaması
            
        Returns:
            dict: Oluşturulan fiş bilgileri
        """
        try:
            # Yeni FisNo al
            fisno = self.db.get_next_fisno()
            
            # GirisCikis değerini belirle
            # FisTuru=50 (Sayım Fazlası) -> GirisCikis=1 (Giriş)
            # FisTuru=51 (Sayım Eksiği) -> GirisCikis=2 (Çıkış)
            giris_cikis = 1 if fis_turu == Config.FIS_SAYIM_FAZLASI else 2
            
            # Ana fiş kaydı oluştur
            fis_idno = self.db.create_fis_record(
                fisno=fisno,
                fis_turu=fis_turu,
                giris_cikis=giris_cikis,
                depo=warehouse,
                aciklama=aciklama
            )
            
            # Fiş satırlarını oluştur
            lines_created = 0
            for _, row in df_items.iterrows():
                # Miktar her zaman pozitif olmalı (FARK'ın mutlak değeri)
                net_miktar = abs(row['FARK'])
                
                # StokRefNo'yu almak için LOGO'dan sorgula
                stok_ref_no = self._get_stok_ref_no(row['MALZEME KODU'])
                
                self.db.create_fislines_record(
                    link_fisno=fisno,
                    stok_kodu=row['MALZEME KODU'],
                    barkod_no='',  # Barkod bilgisi yoksa boş
                    net_miktar=net_miktar,
                    depo=warehouse,
                    urun_grup1=row['MALZEME ADI'],
                    grup_kodu=row['GRUP KODU'],
                    stok_ref_no=stok_ref_no
                )
                lines_created += 1
            
            fis_info = {
                'fisno': fisno,
                'fis_idno': fis_idno,
                'fis_turu': fis_turu,
                'fis_turu_adi': 'Sayım Fazlası' if fis_turu == Config.FIS_SAYIM_FAZLASI else 'Sayım Eksiği',
                'lines_count': lines_created,
                'aciklama': aciklama
            }
            
            logger.info(f"Fiş oluşturuldu - FisNo: {fisno}, Satır: {lines_created}")
            return fis_info
            
        except Exception as e:
            logger.error(f"Sayım fişi oluşturma hatası: {e}")
            raise
    
    def _get_stok_ref_no(self, stok_kodu):
        """Logo'dan StokRefNo al"""
        try:
            query = f"""
            SELECT LOGICALREF 
            FROM GOLD..LG_013_ITEMS 
            WHERE CODE = '{stok_kodu}'
            """
            
            df = self.db.execute_query(query, database='LOGO')
            
            if len(df) > 0:
                return int(df.iloc[0]['LOGICALREF'])
            else:
                logger.warning(f"StokRefNo bulunamadı: {stok_kodu}, varsayılan değer kullanılıyor")
                return 0
                
        except Exception as e:
            logger.error(f"StokRefNo alma hatası: {e}")
            return 0
    
    def get_warehouses(self):
        """Depo listesini al"""
        try:
            query = """
            SELECT DISTINCT NAME 
            FROM GOLD..L_CAPIWHOUSE WITH (NOLOCK)
            WHERE FIRMNR = '013' AND NR <> -1
            ORDER BY NAME
            """
            
            df = self.db.execute_query(query, database='LOGO')
            warehouses = df['NAME'].tolist()
            
            logger.info(f"{len(warehouses)} adet depo bulundu")
            return warehouses
            
        except Exception as e:
            logger.error(f"Depo listesi alma hatası: {e}")
            return []
    
    def export_to_excel(self, df, filename=None):
        """DataFrame'i Excel'e aktar"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"Stok_Karsilastirma_{timestamp}.xlsx"
            
            df.to_excel(filename, index=False, sheet_name='Stok Karşılaştırma')
            
            logger.info(f"Excel dosyası oluşturuldu: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Excel export hatası: {e}")
            raise

