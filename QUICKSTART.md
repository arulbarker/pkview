# 🚀 Quick Start Guide

Panduan cepat untuk memulai TikTok Live Bubble Application dalam 5 menit!

## ⚡ Quick Setup (5 Menit)

### 1. Install Python
```bash
# Download Python 3.8+ dari python.org
# Pastikan "Add to PATH" dicentang saat install
```

### 2. Download & Extract Project
```bash
# Extract file zip ke folder
# Buka Command Prompt di folder project
```

### 3. Install Dependencies
```bash
# Buat virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 4. Run Application
```bash
python main.py
```

**That's it! 🎉**

---

## 🎮 First Time Usage

### Tanpa TikTok Live (Testing Mode)

1. **Jalankan aplikasi**
   ```bash
   python main.py
   ```

2. **Klik tombol simulasi**
   - Klik "👋 Join" untuk test join event
   - Klik "🎁 Gift" untuk test gift animation
   - Klik "🚀 Rapid Test" untuk 10 events sekaligus

3. **Explore effects**
   - Lihat berbagai animasi bubble
   - Check event log di panel kanan
   - Experiment dengan settings

### Dengan TikTok Live (Real Mode)

1. **Cari TikTok Live yang sedang berlangsung**
   - Buka TikTok app atau website
   - Cari user yang sedang LIVE
   - Catat username mereka

2. **Connect di aplikasi**
   - Masukkan username (tanpa @)
   - Klik "🔴 Start Live"
   - Wait for connection (5-10 detik)

3. **Watch bubbles appear!**
   - Bubble muncul otomatis saat ada event
   - Check log untuk detail
   - Klik "⏹️ Stop Live" untuk disconnect

---

## 🎨 Try Different Effects

### Test Semua Efek dengan Simulasi

```python
# Buka config.py dan ubah default effect
EVENT_CONFIGS = {
    'gift': {
        'effect': 'sparkle_zoom',  # ← Ganti ini
        # Try: fade_in_out, slide_bounce, float_away,
        #      heart_pulse, quick_pop, firework,
        #      rainbow, shake, spiral
    }
}
```

Lalu jalankan:
```bash
python main.py
# Klik tombol simulasi untuk test
```

---

## 🛠️ Common Tasks

### Change Bubble Size
```python
# config.py
EVENT_CONFIGS = {
    'gift': {
        'size': 200,  # ← Change this (50-300)
    }
}
```

### Change Animation Duration
```python
# config.py
EVENT_CONFIGS = {
    'gift': {
        'duration': 5000,  # ← Change this (milliseconds)
    }
}
```

### Change Bubble Color
```python
# config.py
EVENT_CONFIGS = {
    'gift': {
        'color': '#FF0000',  # ← Red (use hex colors)
    }
}
```

### Add Custom User to Simulation
```python
# config.py
DUMMY_USERS = [
    {
        "username": "myuser",
        "nickname": "My Name",
        "avatar": "https://i.pravatar.cc/150?img=1"
    },
    # Add more...
]
```

---

## 🎯 Quick Troubleshooting

### Problem: Application won't start

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try running with console output
python main.py
```

### Problem: Can't connect to TikTok Live

**Checklist:**
- [ ] Username benar? (tanpa @)
- [ ] User sedang LIVE?
- [ ] Internet connection OK?
- [ ] Firewall tidak blocking?

**Try:**
```bash
# Test dengan username terkenal yang sering live
# Contoh: @tiktoklive (jika sedang live)
```

### Problem: Bubbles not appearing

**Check:**
1. Event log ada pesan?
2. Simulation buttons working?
3. Bubble container visible?

**Solution:**
```bash
# Test dengan simulation dulu
# Klik "🚀 Rapid Test"
# Jika simulation works tapi real tidak = connection issue
# Jika simulation juga tidak = code issue
```

### Problem: Application slow/laggy

**Solution:**
```python
# Reduce concurrent bubbles
# config.py - add this:
MAX_CONCURRENT_BUBBLES = 5

# Use simpler effects
EVENT_CONFIGS = {
    'join': {'effect': 'fade_in_out'},  # Simple
    'like': {'effect': 'quick_pop'},    # Fast
}

# Reduce bubble size
BUBBLE_MAX_SIZE = 120  # Instead of 200
```

---

## 📦 Build Executable

### Create Portable .exe

**Simple method:**
```bash
# Double-click build.bat
# Wait 2-5 minutes
# Find .exe in dist folder
```

**Manual method:**
```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller build.spec

# Find output
# dist/TikTokLiveBubble.exe
```

### Share Your Build

1. Copy entire `dist` folder
2. Zip it
3. Share!

**Recipients can:**
- Extract zip
- Run TikTokLiveBubble.exe
- No Python installation needed!

---

## 🎓 Next Steps

### Learn More
1. Read [README.md](README.md) - Full documentation
2. Read [EFFECTS_GUIDE.md](EFFECTS_GUIDE.md) - All effects explained
3. Explore `config.py` - All settings
4. Check `effects.py` - See how effects work

### Customize
1. Try different effect combinations
2. Adjust colors and sizes
3. Add custom dummy data
4. Create your own effects

### Advanced
1. Add AI sentiment analysis
2. Connect to database
3. Add custom particle effects
4. Implement sound effects
5. Add screen recording feature

---

## 💡 Pro Tips

### Tip 1: Fullscreen for OBS/Streaming
```
1. Click "Toggle Fullscreen" in Settings
2. Add to OBS as Window Capture
3. Chroma key the background if needed
```

### Tip 2: Test Before Going Live
```
Always test with simulation before real live!
- Check all effects work
- Verify sizes look good
- Test performance
```

### Tip 3: Backup Config
```bash
# Before making big changes
copy config.py config.backup.py
```

### Tip 4: Performance Mode
```python
# For low-end PC, use simple effects only
EVENT_CONFIGS = {
    'join': {'effect': 'fade_in_out', 'duration': 1500},
    'gift': {'effect': 'quick_pop', 'duration': 2000},
    'comment': {'effect': 'fade_in_out', 'duration': 2000},
    # ... all simple
}
```

### Tip 5: Event Filtering
```python
# Only show important events
# tiktok_handler.py - add filters
if event_type == 'like' and like_count < 10:
    return  # Skip low likes

if event_type == 'join':
    return  # Skip joins entirely
```

---

## 🆘 Get Help

### Can't Figure It Out?

1. **Check Log Panel**
   - Aplikasi menampilkan error messages
   - Look for "ERROR" or "❌"

2. **Enable Console Output**
   ```python
   # build.spec - change:
   console=True  # Instead of False
   ```

3. **Check Files**
   - All .py files present?
   - config.py not corrupted?

4. **Reinstall**
   ```bash
   # Clean install
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## ✅ Checklist: Everything Working?

- [ ] Application starts
- [ ] Simulation buttons work
- [ ] Bubbles appear and animate
- [ ] Event log shows messages
- [ ] Settings can be changed
- [ ] Can toggle fullscreen
- [ ] Can build to .exe (optional)
- [ ] Can connect to TikTok Live (optional)

**All checked? You're ready! 🎉**

---

## 🎬 Example Workflow

### For Content Creator / Streamer

```
1. Setup
   - Install application
   - Test with simulation
   - Customize colors/sizes
   - Test performance

2. Pre-Stream
   - Open application
   - Add to OBS/streaming software
   - Position bubbles overlay
   - Test with simulation

3. During Stream
   - Enter TikTok username
   - Click "Start Live"
   - Bubbles show automatically
   - Monitor event log

4. Post-Stream
   - Click "Stop Live"
   - Review log (optional)
   - Adjust settings for next time
```

### For Developer / Tinkerer

```
1. Explore Code
   - Read effects.py
   - Understand bubble_widget.py
   - Check tiktok_handler.py

2. Customize
   - Create new effect
   - Modify existing effects
   - Add new event types

3. Test
   - Use simulation panel
   - Test all edge cases
   - Check performance

4. Share
   - Build .exe
   - Share with community
   - Get feedback
```

---

**You're all set! Enjoy your bubble animations! 🎈**

Need more help? Check the other documentation files!
