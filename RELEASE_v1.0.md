# 🎉 TikTok Live PK Battle - Version 1.0 Release

## 📦 Download

**Executable (Windows):** `dist/TikTokLiveBubble.exe`

**File Size:** ~60-80 MB (single executable, no installation needed)

---

## ✨ New Features in v1.0

### 1. **Custom Points System** 🎯
- Configure points for Like (1-1000 points)
- Configure points for Comment (1-1000 points)
- Quick presets: 1:1, 5:10, 10:50
- Auto-save/load from `point_settings.json`

### 2. **Developer Tab** 👨‍💻
- Social media links (YouTube, Instagram, Facebook, Threads, X, LYNKID)
- Direct links to developer channels
- One-click access to support

### 3. **Connection Stability** 🔌
- Auto-retry on first connection (3 attempts)
- Auto-reconnect on disconnect (5 max attempts)
- Extended timeouts (90s read, 45s connect)
- HTTP/2 support for better performance
- Exponential backoff reconnection (5s → 30s max)

### 4. **Enhanced Logging** 📝
- Detailed point calculations: `[LIKE] Team A (+15 poin) [3 x 5]`
- Clear connection status messages
- Comprehensive error reporting

### 5. **Bug Fixes** 🐛
- Fixed race condition in settings loading
- Fixed like counting (now counts ALL likes, no spam filter)
- Fixed z-order (Gift bubbles on top, Like/Comment behind)
- Fixed missing imports causing crashes

---

## 🚀 Quick Start

### Method 1: Run Executable (Recommended)

1. Extract the release package
2. Double-click `TikTokLiveBubble.exe`
3. Configure your settings in the tabs
4. Connect to TikTok Live and start battle!

### Method 2: Run from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 📋 System Requirements

### Minimum:
- Windows 10/11 (64-bit)
- 4GB RAM
- Internet connection
- Display: 1920×1080 (recommended)

### Recommended:
- Windows 11 (64-bit)
- 8GB RAM
- Stable internet (for live streaming)
- Dual monitor setup

---

## 🎮 Features Checklist

✅ **PK Battle System**
- Round-based timer (customizable duration)
- Soccer-style scoring (5-3 format)
- Auto-reset after round ends
- Score accumulation across rounds

✅ **TikTok Live Integration**
- Real-time event processing
- All event types supported (Like, Comment, Gift, Share, Follow, Join)
- Avatar loading with 6 fallback methods
- Robust connection management

✅ **Bubble System**
- Animated bubbles for all events
- 18+ animation effects
- Configurable positions (top, bottom, left, right)
- Z-order: Gift bubbles on top, Like/Comment behind

✅ **Point Configuration**
- Gift assignment to teams (16+ gifts supported)
- Like/Comment assignment to teams
- Custom points per Like/Comment
- Auto-save settings

✅ **Sound System**
- Win sounds for Team A/B
- Custom sound file picker
- Event sounds (configurable)
- Round end warning (10 seconds)

✅ **UI Features**
- Draggable elements (Score, Timer, Points, Photos)
- Resizable photos (100-600px)
- Rotatable elements (Ctrl + Mouse Wheel)
- 10 tabs for different settings

---

## 🛠️ Building from Source

### Prerequisites:
```bash
pip install PyQt6 TikTokLive httpx pyinstaller
```

### Build Command:
```bash
# Clean build
pyinstaller build.spec --clean

# Output: dist/TikTokLiveBubble.exe
```

### Build Configuration:
- Single-file executable
- No console (set `console=True` for debugging)
- UPX compression enabled
- All dependencies included

---

## 📁 File Structure

### Executable Distribution:
```
TikTokLiveBubble/
├── TikTokLiveBubble.exe       # Main executable
└── sounds/                     # Sound files folder
    ├── team_a_win.mp3         # Team A win sound (optional)
    ├── team_b_win.mp3         # Team B win sound (optional)
    ├── like.mp3               # Like event sound (optional)
    ├── comment.mp3            # Comment event sound (optional)
    └── README.txt             # Sound setup instructions
```

### Settings Files (Auto-generated):
```
gift_assignment.json           # Gift → Team mappings
interaction_assignment.json    # Like/Comment → Team
bubble_positions.json          # Bubble spawn positions
event_sounds.json              # Sound settings
point_settings.json            # Custom points (NEW!)
win_sounds.json                # Custom win sound paths
```

---

## 🎯 Usage Guide

### 1. **Setup Battle (Tab 1: ⚔️ Battle)**
- Set round duration (default: 60 minutes)
- Configure volume
- Start/Pause/Reset battle
- Browse custom win sounds for Team A/B

### 2. **Connect to TikTok (Tab 2: 📺 TikTok)**
- Enter TikTok username (without @)
- Click "Connect to Live"
- Wait 30-90 seconds for connection
- Auto-retry if first attempt fails

### 3. **Upload Photos (Tab 3: 📸 Photos)**
- Click "Upload Photo A" and "Upload Photo B"
- Photos appear as draggable circles
- Resize: Drag corners
- Rotate: Ctrl + Mouse Wheel
- Move: Drag anywhere

### 4. **Assign Gifts (Tab 4: 🎁 Gifts)**
- Assign each gift to Team A or Team B
- Quick assign: All → Team A/B, or Split 50-50
- Search gifts by name
- Click "💾 Save Gift Assignment"

### 5. **Assign Interactions (Tab 5: 👍💬 Like/Comment)**
- Assign Like to Team A or B
- Assign Comment to Team A or B
- Quick assign: All to one team
- Click "💾 Simpan Assignment"

### 6. **Configure Bubble Positions (Tab 6: 🫧 Posisi Bubble)**
- Set where Like bubbles appear (top/bottom/left/right)
- Set where Comment bubbles appear
- Click "💾 Simpan Posisi"

### 7. **Configure Sounds (Tab 7: 🔊 Suara)**
- Toggle on/off for each event type
- Browse custom sound files
- Click "💾 Simpan Pengaturan"

### 8. **Configure Custom Points (Tab 8: 🎯 Custom Points)** ⭐ NEW
- Set points per Like (1-1000)
- Set points per Comment (1-1000)
- Use quick presets or custom values
- Click "💾 Simpan Point Settings"

### 9. **Developer Info (Tab 9: 👨‍💻 Developer)**
- Links to social media
- Contact information
- Support channels

### 10. **Test Mode (Tab 10: 🧪 Test)**
- Simulate events without live connection
- Test Like, Comment, Share, Follow, Join
- Test Gift points for Team A/B

---

## ⚙️ Advanced Configuration

### Point System:

**Gifts:**
```
Points = Gift Coin Value × 5
Example: Rose (1 coin) = 5 points
         Universe (34,999 coins) = 174,995 points
```

**Likes & Comments (Configurable):**
```
Points = Count × Custom Points Per Interaction
Default: 1 Like = 1 point, 1 Comment = 1 point

Examples:
  1 Like = 5 points (custom) → 10 likes = 50 points
  1 Comment = 10 points (custom) → 1 comment = 10 points
```

### Auto-Reconnect:
```
Attempt 1: Immediate
Attempt 2: Wait 5s
Attempt 3: Wait 10s
Attempt 4: Wait 15s
Attempt 5: Wait 20s
Max wait: 30s
```

---

## 🐛 Troubleshooting

### "Connection Failed" or "Timeout"
**Solution:**
1. Verify the user is LIVE right now
2. Check internet connection
3. Wait a few seconds and try again
4. App will auto-retry 3 times on first connect

### "No bubbles appearing"
**Solution:**
1. Check bubble position settings (Tab 6)
2. Verify interaction assignments (Tab 5)
3. Test with simulation mode (Tab 10)

### "No sound playing"
**Solution:**
1. Check sound settings (Tab 7)
2. Enable sounds for events
3. Add valid MP3 files to sounds folder
4. Check system volume

### "Settings not saving"
**Solution:**
1. Click "Save" button in each tab
2. Settings auto-load on next startup
3. Check for .json files in app folder

### "Exe won't start"
**Solution:**
1. Run as administrator
2. Check Windows Defender/antivirus
3. Extract to folder without special characters
4. Ensure .NET Framework is installed

---

## 📞 Support

**Issues & Bug Reports:**
- GitHub: https://github.com/arulbarker/pkview/issues

**Developer Contact:**
- YouTube: https://www.youtube.com/@arulcg
- Instagram: https://www.instagram.com/arul.cg/
- Facebook: https://www.facebook.com/profile.php?id=61578938703730

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🙏 Credits

- **Developer:** Arul CG
- **Framework:** PyQt6
- **TikTok API:** TikTokLive Python Library
- **Built with:** Claude Code

---

## 🎊 Thank You!

Terima kasih telah menggunakan TikTok Live PK Battle v1.0!

Jangan lupa subscribe & follow untuk update terbaru:
- YouTube: @arulcg
- Instagram: @arul.cg

**Selamat streaming! 🎮🔥**
