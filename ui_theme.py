"""
Modern UI Tema ve Stil Tanımlamaları
"""
import customtkinter as ctk

class ModernTheme:
    """Modern UI tema renkleri ve stilleri"""
    
    # Renk Paleti - Modern ve Yumuşak
    COLORS = {
        'primary': '#4F46E5',      # Indigo - Ana renk
        'primary_hover': '#4338CA', # Koyu indigo
        'secondary': '#10B981',     # Yeşil - Başarı
        'secondary_hover': '#059669',
        'danger': '#EF4444',        # Kırmızı - Uyarı/Tehlike
        'danger_hover': '#DC2626',
        'warning': '#F59E0B',       # Turuncu - Uyarı
        'warning_hover': '#D97706',
        'info': '#3B82F6',          # Mavi - Bilgi
        'info_hover': '#2563EB',
        'success': '#10B981',        # Yeşil
        'success_hover': '#059669',
        
        # Nötr Renkler
        'bg_primary': '#0F172A',    # Çok koyu mavi-gri (arka plan)
        'bg_secondary': '#1E293B',   # Koyu mavi-gri (kartlar)
        'bg_tertiary': '#334155',   # Orta gri
        'text_primary': '#F1F5F9',   # Açık gri (ana metin)
        'text_secondary': '#94A3B8', # Orta gri (ikincil metin)
        'text_muted': '#64748B',    # Koyu gri (soluk metin)
        'border': '#334155',        # Kenarlık
        'border_light': '#475569',
        
        # Özel Durumlar
        'connected': '#10B981',     # Bağlı durumu
        'disconnected': '#64748B',  # Bağlantı yok
        'loading': '#3B82F6',       # Yükleniyor
    }
    
    # Tipografi - Lazy initialization (font'lar kullanıldığında oluşturulur)
    _fonts_cache = {}
    
    @staticmethod
    def get_font(font_name):
        """Font'u lazy olarak oluştur veya cache'den döndür"""
        if font_name not in ModernTheme._fonts_cache:
            font_configs = {
                'h1': {'size': 32, 'weight': 'bold'},
                'h2': {'size': 24, 'weight': 'bold'},
                'h3': {'size': 20, 'weight': 'bold'},
                'h4': {'size': 18, 'weight': 'bold'},
                'body_large': {'size': 16},
                'body': {'size': 14},
                'body_small': {'size': 12},
                'caption': {'size': 11},
                'code': {'family': 'Courier New', 'size': 12},
            }
            config = font_configs.get(font_name, {'size': 14})
            ModernTheme._fonts_cache[font_name] = ctk.CTkFont(**config)
        return ModernTheme._fonts_cache[font_name]
    
    @staticmethod
    def FONTS():
        """Font dictionary - property olarak erişim"""
        return {
            'h1': ModernTheme.get_font('h1'),
            'h2': ModernTheme.get_font('h2'),
            'h3': ModernTheme.get_font('h3'),
            'h4': ModernTheme.get_font('h4'),
            'body_large': ModernTheme.get_font('body_large'),
            'body': ModernTheme.get_font('body'),
            'body_small': ModernTheme.get_font('body_small'),
            'caption': ModernTheme.get_font('caption'),
            'code': ModernTheme.get_font('code'),
        }
    
    # Spacing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
    }
    
    # Border Radius
    RADIUS = {
        'sm': 6,
        'md': 8,
        'lg': 12,
        'xl': 16,
    }
    
    @staticmethod
    def apply_theme():
        """Temayı uygula"""
        ctk.set_appearance_mode("dark")
        # Özel renk teması (blue yerine custom)
        ctk.set_default_color_theme("blue")  # CustomTkinter'ın kendi teması
    
    @staticmethod
    def create_card(parent, **kwargs):
        """Modern kart bileşeni oluştur"""
        # Varsayılan değerler
        default_kwargs = {
            'corner_radius': ModernTheme.RADIUS['lg'],
            'fg_color': ModernTheme.COLORS['bg_secondary'],
            'border_width': 1,
            'border_color': ModernTheme.COLORS['border'],
        }
        # kwargs'tan gelen değerler varsayılanları override eder
        default_kwargs.update(kwargs)
        return ctk.CTkFrame(parent, **default_kwargs)
    
    @staticmethod
    def create_primary_button(parent, text, command, **kwargs):
        """Ana buton stili"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ModernTheme.get_font('body'),
            fg_color=ModernTheme.COLORS['primary'],
            hover_color=ModernTheme.COLORS['primary_hover'],
            corner_radius=ModernTheme.RADIUS['md'],
            height=40,
            **kwargs
        )
    
    @staticmethod
    def create_success_button(parent, text, command, **kwargs):
        """Başarı butonu"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ModernTheme.get_font('body'),
            fg_color=ModernTheme.COLORS['success'],
            hover_color=ModernTheme.COLORS['success_hover'],
            corner_radius=ModernTheme.RADIUS['md'],
            height=40,
            **kwargs
        )
    
    @staticmethod
    def create_danger_button(parent, text, command, **kwargs):
        """Tehlike butonu"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ModernTheme.get_font('body'),
            fg_color=ModernTheme.COLORS['danger'],
            hover_color=ModernTheme.COLORS['danger_hover'],
            corner_radius=ModernTheme.RADIUS['md'],
            height=40,
            **kwargs
        )
    
    @staticmethod
    def create_warning_button(parent, text, command, **kwargs):
        """Uyarı butonu"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ModernTheme.get_font('body'),
            fg_color=ModernTheme.COLORS['warning'],
            hover_color=ModernTheme.COLORS['warning_hover'],
            corner_radius=ModernTheme.RADIUS['md'],
            height=40,
            **kwargs
        )
    
    @staticmethod
    def create_secondary_button(parent, text, command, **kwargs):
        """İkincil buton (outline)"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ModernTheme.get_font('body'),
            fg_color="transparent",
            border_width=2,
            border_color=ModernTheme.COLORS['border_light'],
            text_color=ModernTheme.COLORS['text_primary'],
            hover_color=ModernTheme.COLORS['bg_tertiary'],
            corner_radius=ModernTheme.RADIUS['md'],
            height=40,
            **kwargs
        )
    
    @staticmethod
    def create_modern_entry(parent, placeholder="", width=400, **kwargs):
        """Modern input alanı"""
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=width,
            height=40,
            font=ModernTheme.get_font('body'),
            corner_radius=ModernTheme.RADIUS['md'],
            border_width=1,
            border_color=ModernTheme.COLORS['border'],
            fg_color=ModernTheme.COLORS['bg_tertiary'],
            text_color=ModernTheme.COLORS['text_primary'],
            **kwargs
        )
    
    @staticmethod
    def create_section_title(parent, text):
        """Bölüm başlığı"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ModernTheme.get_font('h3'),
            text_color=ModernTheme.COLORS['text_primary'],
            anchor="w"
        )
    
    @staticmethod
    def create_label(parent, text, size='body', color='text_primary'):
        """Etiket oluştur"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ModernTheme.get_font(size if size in ['h1', 'h2', 'h3', 'h4', 'body_large', 'body', 'body_small', 'caption', 'code'] else 'body'),
            text_color=ModernTheme.COLORS.get(color, ModernTheme.COLORS['text_primary'])
        )

