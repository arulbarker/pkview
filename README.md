# 🎉 TikTok Live Bubble Animation

Desktop application untuk menampilkan animasi bubble interaktif berdasarkan event TikTok Live secara real-time menggunakan Python dan PyQt6.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fitur Utama

- **Real-time TikTok Live Events**: Menangkap event live TikTok (join, gift, comment, share, follow, like)
- **10+ Efek Animasi Keren**: Berbagai efek animasi yang berbeda untuk setiap jenis event
- **Simulasi Event**: Panel untuk testing event tanpa perlu live TikTok sungguhan
- **Modular & Extensible**: Mudah menambahkan efek animasi baru
- **Auto-Reconnect**: Reconnect otomatis jika koneksi terputus
- **Event Logging**: Panel log untuk melihat semua event real-time
- **Fullscreen Mode**: Mode fullscreen untuk tampilan maksimal
- **Portable .exe**: Build menjadi standalone executable untuk Windows

## 📋 Requirements

- Windows 10/11
- Python 3.8 atau lebih tinggi
- Koneksi internet (untuk TikTok Live)

## 🚀 Installation

### 1. Clone atau Download Repository

```bash
git clone <repository-url>
cd livebuble
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Run Application

```bash
python main.py
```

## 🏗️ Build Executable

Untuk membuat file .exe yang portable:

```bash
# Windows
build.bat

# Atau manual
pyinstaller build.spec
```

Executable akan tersedia di folder `dist/TikTokLiveBubble.exe`

## 🎨 Efek Animasi Tersedia

Aplikasi ini menyediakan 10+ efek animasi keren yang bisa digunakan:

### 1. **Fade In Out** (`fade_in_out`)
- Efek fade sederhana dan elegan
- Bubble muncul perlahan, hold, lalu menghilang
- Perfect untuk: Join events

### 2. **Sparkle Zoom** (`sparkle_zoom`)
- Zoom in dari kecil dengan efek berkilau
- Animasi elastic yang menarik perhatian
- Perfect untuk: Gift events
- Fitur: Sparkle particles, glow effect

### 3. **Slide Bounce** (`slide_bounce`)
- Slide dari samping kiri/kanan dengan bouncing
- Animasi bounce seperti bola memantul
- Perfect untuk: Comment events

### 4. **Float Away** (`float_away`)
- Bubble melayang ke atas screen
- Fade out sambil bergerak
- Perfect untuk: Share events

### 5. **Heart Pulse** (`heart_pulse`)
- Pulsing effect seperti detak jantung
- 3 kali pulse kemudian fade
- Perfect untuk: Follow events
- Efek romantis dan menarik

### 6. **Quick Pop** (`quick_pop`)
- Pop in/out cepat
- Bounce effect yang energetic
- Perfect untuk: Like events
- Durasi singkat tapi impactful

### 7. **Firework Explosion** (`firework`)
- Efek ledakan kembang api
- Particles terbang ke segala arah
- Perfect untuk: Special gifts, milestones
- Sangat eye-catching

### 8. **Rainbow Rotate** (`rainbow`)
- Rainbow gradient dengan rotasi
- Warna-warni yang menarik
- Perfect untuk: Celebration events

### 9. **Shake Vibrate** (`shake`)
- Getaran/shake effect
- Energetic dan dynamic
- Perfect untuk: High-value events

### 10. **Spiral In** (`spiral`)
- Spiral masuk dari pojok screen
- Path animation yang smooth
- Perfect untuk: VIP user entrance

## 📊 Event Types & Default Effects

| Event Type | Emoji | Default Effect | Bubble Size | Duration | Color |
|-----------|-------|----------------|-------------|----------|-------|
| Join | 👋 | fade_in_out | 100px | 2s | Green |
| Gift | 🎁 | sparkle_zoom | 180px | 4s | Gold |
| Comment | 💬 | slide_bounce | 120px | 3s | Blue |
| Share | 🔗 | float_away | 110px | 2.5s | Orange |
| Follow | ❤️ | heart_pulse | 140px | 3.5s | Pink |
| Like | 👍 | quick_pop | 90px | 1.5s | Hot Pink |

## 🎮 Cara Penggunaan

### Menghubungkan ke TikTok Live

1. Buka aplikasi
2. Masukkan username TikTok (tanpa @) di field "Username"
3. Klik tombol "🔴 Start Live"
4. Aplikasi akan connect ke live stream
5. Bubble akan muncul otomatis saat ada event

### Simulasi Event (Testing)

Untuk testing tanpa live TikTok:

1. Gunakan panel "Event Simulation"
2. Klik tombol event yang ingin di-test:
   - 👋 Join - Simulate user join
   - 🎁 Gift - Simulate gift
   - 💬 Comment - Simulate comment
   - 🔗 Share - Simulate share
   - ❤️ Follow - Simulate follow
   - 👍 Like - Simulate like
3. Klik "🚀 Rapid Test" untuk simulate 10 event sekaligus

### Settings

- **Toggle Fullscreen**: Switch antara windowed dan fullscreen mode
- **Default Effect**: Pilih efek default yang akan digunakan
- **Clear Log**: Bersihkan event log

## 🛠️ Customization

### Menambahkan Efek Animasi Baru

1. Buka file `effects.py`
2. Tambahkan method baru di class `BubbleEffects`:

```python
@staticmethod
def my_custom_effect(widget, duration=3000):
    """Custom animation effect"""
    # Your animation code here
    pass
```

3. Register efek di `EFFECT_REGISTRY`:

```python
EFFECT_REGISTRY = {
    'my_custom': BubbleEffects.my_custom_effect,
    # ... other effects
}
```

4. Update `config.py` untuk menggunakan efek baru:

```python
EVENT_CONFIGS = {
    'gift': {
        'effect': 'my_custom',
        # ... other settings
    }
}
```

### Mengubah Warna & Size

Edit file `config.py`:

```python
EVENT_CONFIGS = {
    'gift': {
        'size': 200,  # Bubble size in pixels
        'duration': 5000,  # Duration in milliseconds
        'color': '#FF0000',  # Hex color code
        'emoji': '🎁',
        'effect': 'sparkle_zoom'
    }
}
```

### Menambahkan Dummy Data

Edit `DUMMY_USERS` dan `DUMMY_COMMENTS` di `config.py`:

```python
DUMMY_USERS = [
    {"username": "new_user", "nickname": "Name", "avatar": "url"},
    # Add more...
]
```

## 📁 Struktur Project

```
livebuble/
│
├── main.py                 # Entry point
├── main_window.py          # Main window UI
├── bubble_widget.py        # Bubble widget component
├── effects.py              # Animation effects
├── tiktok_handler.py       # TikTok Live handler
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── build.spec              # PyInstaller spec
├── build.bat               # Build script
└── README.md               # Documentation
```

## 🔧 Configuration

Semua konfigurasi ada di `config.py`:

- `WINDOW_WIDTH/HEIGHT`: Ukuran window
- `BUBBLE_MIN/MAX_SIZE`: Range size bubble
- `EVENT_CONFIGS`: Konfigurasi per event type
- `EFFECTS_CONFIG`: Settings untuk efek animasi
- `TIKTOK_USERNAME`: Default username
- `RECONNECT_DELAY`: Delay reconnect
- `MAX_RECONNECT_ATTEMPTS`: Max reconnect attempts

## 🐛 Troubleshooting

### Aplikasi tidak bisa connect ke TikTok Live

- Pastikan username benar dan sedang live
- Check koneksi internet
- Coba restart aplikasi

### Bubble tidak muncul

- Check event log untuk error messages
- Gunakan simulasi untuk testing
- Pastikan bubble container terlihat (tidak di-minimize)

### Build .exe gagal

```bash
# Clean build
rmdir /s /q build dist
pyinstaller build.spec
```

### Import Error saat run

```bash
# Reinstall dependencies
pip uninstall -y PyQt6 TikTokLive
pip install -r requirements.txt
```

## 🎓 Advanced Features (Optional)

### AI Sentiment Analysis

Untuk menambahkan analisis sentimen komentar:

1. Uncomment di `requirements.txt`:
```
transformers>=4.35.0
torch>=2.0.0
```

2. Install:
```bash
pip install transformers torch
```

3. Implementasi sentiment analysis di `tiktok_handler.py`

### Database Logging

Untuk menyimpan event history ke database, tambahkan SQLite integration.

### Custom Particle Effects

Extend `effects.py` dengan particle system custom.

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

Jika ada pertanyaan atau issues, silakan buat issue di GitHub repository.

## 🎉 Credits

- PyQt6 - GUI Framework
- TikTokLive - TikTok Live API
- Python Community

---

**Happy Coding! 🚀**

Dibuat dengan ❤️ menggunakan Python & PyQt6
