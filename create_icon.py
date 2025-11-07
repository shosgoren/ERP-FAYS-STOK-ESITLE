"""
Icon Oluşturma Script'i
Stok Eşitleme uygulaması için icon oluşturur
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Uygulama icon'unu oluştur"""
    # Icon boyutları (Windows için standart boyutlar)
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Yeni bir görüntü oluştur (transparent arka plan)
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Arka plan - Koyu mavi (header rengi)
        bg_color = (30, 58, 138)  # #1E3A8A
        draw.rectangle([0, 0, size, size], fill=bg_color)
        
        # Kutu/depo ikonu çiz
        # Ana kutu
        box_margin = size // 6
        box_width = size - (box_margin * 2)
        box_height = size - (box_margin * 2)
        
        # Kutu gövdesi
        box_color = (255, 255, 255)  # Beyaz
        draw.rectangle(
            [box_margin, box_margin + size//8, 
             box_margin + box_width, box_margin + box_height],
            fill=box_color,
            outline=(200, 200, 200),
            width=max(1, size//32)
        )
        
        # Kutu kapağı (üst kısım)
        lid_height = size // 8
        draw.rectangle(
            [box_margin - size//16, box_margin, 
             box_margin + box_width + size//16, box_margin + lid_height],
            fill=(240, 240, 240),
            outline=(200, 200, 200),
            width=max(1, size//32)
        )
        
        # Ok ikonu (eşitleme simgesi) - kutu içinde
        arrow_size = size // 4
        arrow_x = size // 2
        arrow_y = size // 2 + size // 16
        
        # Sol ok
        draw.polygon([
            (arrow_x - arrow_size//2, arrow_y),
            (arrow_x - arrow_size//3, arrow_y - arrow_size//4),
            (arrow_x - arrow_size//3, arrow_y - arrow_size//8),
            (arrow_x - arrow_size//6, arrow_y - arrow_size//8),
            (arrow_x - arrow_size//6, arrow_y + arrow_size//8),
            (arrow_x - arrow_size//3, arrow_y + arrow_size//8),
            (arrow_x - arrow_size//3, arrow_y + arrow_size//4),
        ], fill=(30, 58, 138))
        
        # Sağ ok
        draw.polygon([
            (arrow_x + arrow_size//2, arrow_y),
            (arrow_x + arrow_size//3, arrow_y - arrow_size//4),
            (arrow_x + arrow_size//3, arrow_y - arrow_size//8),
            (arrow_x + arrow_size//6, arrow_y - arrow_size//8),
            (arrow_x + arrow_size//6, arrow_y + arrow_size//8),
            (arrow_x + arrow_size//3, arrow_y + arrow_size//8),
            (arrow_x + arrow_size//3, arrow_y + arrow_size//4),
        ], fill=(30, 58, 138))
        
        images.append(img)
    
    # ICO dosyası olarak kaydet - Windows ve PyInstaller için optimize edilmiş
    if images:
        # PyInstaller ve Windows için en önemli boyutlar: 16, 32, 48, 256
        # Pillow'un ICO formatı desteği sınırlı, bu yüzden en büyük boyutu (256x256) kaydet
        # Windows bu boyutu otomatik olarak diğer boyutlara ölçekler
        # PyInstaller için 256x256 yeterli ve en güvenilir yöntem
        
        # En büyük ve en kaliteli görüntüyü (256x256) ICO olarak kaydet
        images[-1].save('app_icon.ico', format='ICO')
        print("✓ app_icon.ico oluşturuldu! (256x256 - Windows otomatik ölçekler)")
        print("  → PyInstaller bu icon'u EXE dosyasına ekleyecek")
        print("  → Windows Explorer ve görev çubuğunda görünecek")
        print("  → Icon dosyası boyutu kontrol ediliyor...")
        
        # Dosya boyutunu kontrol et
        import os
        file_size = os.path.getsize('app_icon.ico')
        print(f"  → Icon dosyası boyutu: {file_size} bytes")
        
        if file_size < 1000:
            print("  ⚠️  UYARI: Icon dosyası çok küçük, PyInstaller sorun yaşayabilir!")
        else:
            print("  ✓ Icon dosyası boyutu uygun")
        
        # PNG olarak da kaydet (önizleme için)
        images[-1].save('app_icon.png', format='PNG')
        print("✓ app_icon.png oluşturuldu!")
        
        return True
    return False

if __name__ == "__main__":
    try:
        create_app_icon()
        print("\n✅ Icon başarıyla oluşturuldu!")
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

