"""
SQL Şablonları
Stored Procedure INSERT cümlelerini düzenlenebilir şekilde saklar
"""
import os
import json
from pathlib import Path

class SQLTemplates:
    """SQL şablonlarını yöneten sınıf"""
    
    TEMPLATES_FILE = "sql_templates.json"
    
    # Varsayılan şablonlar
    DEFAULT_TEMPLATES = {
        "stk_Fis_INSERT": """INSERT INTO stk_Fis (
    FisTuru, FisNo, GirisCikis, Tarih, FirmaKodu, FirmaAdi,
    KdvOrani, AraToplam, calcGenelToplam, DovizKuru,
    Aciklamalar, Grup3, KdvDegeri, LogoKontrol, Status,
    DepoRefNo, Islemvar, IslemKullanici, IadeKontrol, DevamDurumu
) VALUES (
    {FisTuru}, {FisNo}, {GirisCikis}, '{Tarih}', '', '',
    0, 0.00, 0.00, 0.00,
    '{Aciklamalar}', '{Grup3}', 0.00, 0, 0,
    1, 0, 0, 0, 3
)""",
        
        "stk_FisLines_INSERT": """INSERT INTO stk_FisLines (
    Link_FisNo, StokKodu, BarkodNo, NetMiktar, BrutMiktar, BirimFiyat,
    Depo, UrunGrup1, MiktarBirimi, KdvORani, YBrutMiktar, YDara,
    Miktar1, Miktar2, Miktar3, Miktar4, Miktar5, AraToplamLines,
    En, Boy, Yukseklik, Agirlik, Desi, SevkEdildi, AmbalajMiktar,
    indirimtutari, KoliDara, BobinDara, TBobinDara, SatirNo,
    StokRefNo, DepoRefNo, RafRefNo, StokTuru, EtiketKontrol,
    IslemTipi, TransLinesIdno, GUIDX, KULLANICI
) VALUES (
    {Link_FisNo}, '{StokKodu}', '{BarkodNo}', {NetMiktar}, 0, 0.00,
    '{Depo}', '{UrunGrup1}', 'ADET', 0, 0, 0,
    0, 0, 0, 0, 0, 0.00,
    0, 0, 0, 0, 0, 0, 1,
    0.00, 0, 0, 0, {SatirNo},
    {StokRefNo}, 1, 5346, 0, 0,
    0, 0, '{GUIDX}', 8215
)""",
        
        "Sayim_Eksigi_Aciklama": "0.KAT:SAYILMAYAN VE STOKTA FAZLA OLAN STOKLAR",
        "Sayim_Fazlasi_Aciklama": "0.KAT:SAYIM YAPILAN VE SAYIM FAZLASI VEREN STOKLAR"
    }
    
    @staticmethod
    def load_templates():
        """Şablonları yükle"""
        try:
            templates_path = Path(SQLTemplates.TEMPLATES_FILE)
            
            if templates_path.exists():
                with open(templates_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Varsayılan şablonları döndür
                return SQLTemplates.DEFAULT_TEMPLATES.copy()
        except Exception as e:
            print(f"Şablon yükleme hatası: {e}")
            return SQLTemplates.DEFAULT_TEMPLATES.copy()
    
    @staticmethod
    def save_templates(templates):
        """Şablonları kaydet"""
        try:
            templates_path = Path(SQLTemplates.TEMPLATES_FILE)
            with open(templates_path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=4, ensure_ascii=False)
            return True, "SQL şablonları kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"
    
    @staticmethod
    def reset_to_default():
        """Varsayılan şablonlara geri dön"""
        return SQLTemplates.save_templates(SQLTemplates.DEFAULT_TEMPLATES.copy())
    
    @staticmethod
    def format_fis_insert(fis_turu, fisno, giris_cikis, tarih, aciklama, grup3):
        """stk_Fis INSERT cümlesini oluştur"""
        templates = SQLTemplates.load_templates()
        template = templates.get("stk_Fis_INSERT", SQLTemplates.DEFAULT_TEMPLATES["stk_Fis_INSERT"])
        
        return template.format(
            FisTuru=fis_turu,
            FisNo=fisno,
            GirisCikis=giris_cikis,
            Tarih=tarih,
            Aciklamalar=aciklama,
            Grup3=grup3
        )
    
    @staticmethod
    def format_fislines_insert(link_fisno, stok_kodu, barkod_no, net_miktar,
                               depo, urun_grup1, stok_ref_no, guidx, satir_no):
        """stk_FisLines INSERT cümlesini oluştur"""
        templates = SQLTemplates.load_templates()
        template = templates.get("stk_FisLines_INSERT", SQLTemplates.DEFAULT_TEMPLATES["stk_FisLines_INSERT"])
        
        return template.format(
            Link_FisNo=link_fisno,
            StokKodu=stok_kodu,
            BarkodNo=barkod_no if barkod_no else '',
            NetMiktar=net_miktar,
            Depo=depo,
            UrunGrup1=urun_grup1,
            StokRefNo=stok_ref_no,
            GUIDX=guidx,
            SatirNo=satir_no
        )
    
    @staticmethod
    def get_aciklama(fis_type):
        """Fiş türüne göre açıklama getir"""
        templates = SQLTemplates.load_templates()
        
        if fis_type == 51:  # Sayım Eksiği
            return templates.get("Sayim_Eksigi_Aciklama", 
                               SQLTemplates.DEFAULT_TEMPLATES["Sayim_Eksigi_Aciklama"])
        elif fis_type == 50:  # Sayım Fazlası
            return templates.get("Sayim_Fazlasi_Aciklama",
                               SQLTemplates.DEFAULT_TEMPLATES["Sayim_Fazlasi_Aciklama"])
        return ""

