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
    
    def synchronize_stocks(self, warehouse, df_comparison=None):
        """
        Stokları eşitle - FAYS tarafını LOGO'ya göre düzelt
        
        Args:
            warehouse: Eşitleme yapılacak depo
            df_comparison: Karşılaştırma DataFrame'i (yoksa yeniden hesaplanır)
            
        Returns:
            dict: Eşitleme sonuç raporu
        """
        try:
            logger.info(f"Stok eşitleme başlatıldı - Depo: {warehouse}")
            
            # Karşılaştırma yapılmamışsa yap
            if df_comparison is None:
                df_comparison = self.compare_stocks(warehouse)
            
            if len(df_comparison) == 0:
                logger.info("Eşitlenecek kayıt bulunamadı")
                return {
                    'success': True,
                    'message': 'Stoklar zaten eşit, işlem gerekmedi',
                    'created_fis': []
                }
            
            created_fis = []
            
            # Farklı stokları grupla
            df_fazla = df_comparison[df_comparison['FARK'] > 0]  # FAYS fazla -> Sayım Eksiği
            df_eksik = df_comparison[df_comparison['FARK'] < 0]  # FAYS eksik -> Sayım Fazlası
            
            # Sayım Eksiği Fişi (FisTuru=51, FAYS fazla, çıkış yapılacak)
            if len(df_fazla) > 0:
                fis_info = self._create_sayim_fisi(
                    df_fazla, 
                    warehouse,
                    Config.FIS_SAYIM_EKSIGI,
                    "0.KAT:SAYILMAYAN VE STOKTA FAZLA OLAN STOKLAR"
                )
                created_fis.append(fis_info)
            
            # Sayım Fazlası Fişi (FisTuru=50, FAYS eksik, giriş yapılacak)
            if len(df_eksik) > 0:
                fis_info = self._create_sayim_fisi(
                    df_eksik,
                    warehouse,
                    Config.FIS_SAYIM_FAZLASI,
                    "0.KAT:SAYIM YAPILAN VE SAYIM FAZLASI VEREN STOKLAR"
                )
                created_fis.append(fis_info)
            
            result = {
                'success': True,
                'message': f'{len(created_fis)} adet fiş oluşturuldu',
                'created_fis': created_fis,
                'total_items': len(df_comparison)
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
    
    def _create_sayim_fisi(self, df_items, warehouse, fis_turu, aciklama):
        """
        Sayım fişi ve satırlarını oluştur
        
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

