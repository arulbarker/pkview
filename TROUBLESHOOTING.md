# 🔧 Troubleshooting Guide

Common issues and solutions for TikTok Live Bubble Application.

## 🚀 Quick Fixes

### App Won't Start

**Error**: `setHighDpiScaleFactorRoundingPolicy must be called before creating the QGuiApplication instance`

**Solution**: This has been fixed in the latest version. If you still see this:
```bash
# Update to latest code
git pull
# Or re-download the latest version
```

### Bubbles Not Showing

**Error**: `QRadialGradient(): argument 1 has unexpected type 'QPoint'`

**Solution**: This has been fixed. Update your `bubble_widget.py` to latest version.

**Manual fix** (if needed):
```python
# In bubble_widget.py, line ~166, change:
gradient = QRadialGradient(rect.center(), rect.width() / 2)

# To:
center = QPointF(rect.center())
gradient = QRadialGradient(center, rect.width() / 2)
```

---

## 📡 TikTok Connection Issues

### Connection Timeout

**Error**: `httpx.ReadTimeout` or `Connection timeout`

**Common Causes**:
1. Username is incorrect
2. User is not currently LIVE
3. Internet connection issues
4. Firewall blocking connection

**Solutions**:

✅ **Test with Simulation First**
```bash
# Always test with simulation before trying real connection
python main.py
# Click simulation buttons - these work offline!
```

✅ **Verify Username**
- Use username WITHOUT @ symbol
- Check spelling carefully
- Make sure user is actually LIVE right now

✅ **Check Internet**
```bash
# Test internet connection
ping google.com
# Test TikTok access
curl https://www.tiktok.com
```

✅ **Check Firewall**
- Windows Defender might block Python
- Allow Python in Firewall settings
- Try running as Administrator (right-click → Run as administrator)

✅ **Use Popular Live Streamers**
```python
# For testing, try well-known TikTok streamers who are often live
# Examples (check if they're live first):
# - gaming streamers
# - news channels
# - 24/7 live streams
```

### Connection Takes Forever

**Issue**: Stuck on "Starting connection..." for 30+ seconds

**Solution**:
- This is normal for first connection (10-30 seconds)
- If > 60 seconds, probably not live or wrong username
- Click "⏹️ Stop Live" and try again
- Use simulation panel instead for testing

### App Crashes When Connecting

**Solution**:
```bash
# Run with error output visible
python main.py

# Check the console for specific error
# Report issue with full error message
```

---

## 🎨 Bubble/Animation Issues

### Bubbles Appear But No Animation

**Check**:
1. Effect is set correctly in `config.py`
2. Duration is not too short (minimum 500ms recommended)

**Fix**:
```python
# config.py
EVENT_CONFIGS = {
    'gift': {
        'effect': 'sparkle_zoom',  # Make sure this exists
        'duration': 3000,  # Not too short
    }
}
```

### Bubbles Appear in Wrong Position

**Issue**: Bubbles overlap or appear off-screen

**Solution**:
```python
# config.py - adjust bubble size
BUBBLE_MIN_SIZE = 80
BUBBLE_MAX_SIZE = 150  # Reduce if too large

EVENT_CONFIGS = {
    'gift': {
        'size': 120,  # Adjust individual event sizes
    }
}
```

### Avatar Not Loading

**Common Causes**:
1. No internet connection
2. Avatar URL invalid
3. Network timeout

**Solution**:
- Placeholder avatar will show automatically
- Check internet connection
- Avatar loading happens in background (non-blocking)

### Too Many Bubbles / Performance Issues

**Solution**:
```python
# Limit concurrent bubbles
# main_window.py, in _create_bubble():

if len(self.active_bubbles) >= 10:  # Add this check
    oldest = self.active_bubbles.pop(0)
    oldest.deleteLater()

# Or reduce bubble duration
# config.py
EVENT_CONFIGS = {
    'join': {
        'duration': 1500,  # Shorter = less overlap
    }
}
```

---

## 💻 Installation Issues

### PyQt6 Installation Fails

**Error**: `Could not find a version that satisfies the requirement PyQt6`

**Solution**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install PyQt6
pip install PyQt6

# If still fails, try:
pip install PyQt6-Qt6
pip install PyQt6
```

### TikTokLive Installation Fails

**Solution**:
```bash
# Install specific version
pip install TikTokLive==5.0.0

# Or latest
pip install --upgrade TikTokLive
```

### Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'PyQt6'`

**Solution**:
```bash
# Make sure you're in the right environment
# Check which Python
python --version
which python  # Linux/Mac
where python  # Windows

# Reinstall all requirements
pip install -r requirements.txt

# Or individual packages
pip install PyQt6 TikTokLive Pillow requests
```

---

## 🏗️ Build Issues

### PyInstaller Build Fails

**Error**: Various build errors

**Solution**:
```bash
# Clean previous builds
rmdir /s /q build dist  # Windows
rm -rf build dist       # Linux/Mac

# Update PyInstaller
pip install --upgrade pyinstaller

# Build again
pyinstaller build.spec

# If still fails, try simple build:
pyinstaller --onefile --windowed main.py
```

### Built .exe Won't Run

**Issue**: Double-click .exe, nothing happens

**Solution**:
```bash
# Run from command line to see errors
cd dist
TikTokLiveBubble.exe

# Check for missing DLLs
# Might need to install Visual C++ Redistributable
# Download from Microsoft website
```

### Built .exe is Too Large

**Issue**: .exe is 200MB+

**Solution**:
```python
# This is normal for PyQt6 apps
# Includes Python runtime + Qt libraries
# To reduce size:
# - Use UPX compression (in build.spec)
# - Exclude unnecessary modules
# - Use --onefile (slower startup but single file)
```

---

## 🐛 Runtime Errors

### QPainter Errors

**Error**: `QPainter::begin: A paint device can only be painted by one painter at a time`

**Solution**: This has been fixed. Update `bubble_widget.py`.

**Cause**: Widget being painted while another paint is active.

### Painter Not Active

**Error**: `QPainter::translate: Painter not active`

**Solution**: Update to latest code. Fixed in paintEvent handling.

### QBackingStore Errors

**Error**: `QBackingStore::endPaint() called with active painter`

**Solution**: Fixed in latest version. Make sure painter.end() is called or using context manager.

---

## 📊 Performance Issues

### App is Slow/Laggy

**Solutions**:

1. **Reduce Concurrent Bubbles**
```python
# Limit to 5-10 bubbles max
MAX_BUBBLES = 5
```

2. **Use Simpler Effects**
```python
# config.py
EVENT_CONFIGS = {
    'join': {'effect': 'fade_in_out'},  # Simple
    'like': {'effect': 'quick_pop'},     # Fast
    # Avoid: 'firework', 'sparkle_zoom' (complex)
}
```

3. **Reduce Animation Duration**
```python
# Shorter = less time on screen = better performance
'duration': 1500  # Instead of 3000+
```

4. **Reduce Bubble Size**
```python
BUBBLE_MAX_SIZE = 120  # Instead of 200
```

5. **Close Other Apps**
- Minimize browser tabs
- Close video players
- Free up RAM

### High CPU Usage

**Normal**: 5-15% when bubbles are animating
**High**: 30%+ constantly

**Solutions**:
- Reduce concurrent bubbles
- Use simpler effects
- Increase animation intervals
- Check for infinite loops in custom effects

---

## 🎮 Simulation Panel Issues

### Simulation Buttons Don't Work

**Check**:
1. Console for errors
2. Event log for messages

**Solution**:
```bash
# Test if events are being created
# Should see log messages when clicking

# If no logs appear:
# - Check _simulate_event() in main_window.py
# - Check DUMMY_USERS in config.py
# - Restart application
```

### Rapid Test Crashes App

**Issue**: Clicking "🚀 Rapid Test" freezes or crashes

**Solution**:
```python
# Reduce number of rapid events
# main_window.py, _simulate_rapid_events()

for i in range(5):  # Instead of 10
    # ...
```

---

## 🔍 Debug Mode

### Enable Console Output

**Windows**:
```python
# build.spec - change:
console=True  # Instead of False

# Rebuild:
pyinstaller build.spec
```

**Running from source**:
```bash
# Console output is automatic
python main.py

# Redirect to file:
python main.py > output.log 2>&1
```

### Verbose Logging

**Add to main_window.py**:
```python
def _on_event_received(self, event_data):
    print(f"DEBUG: Received event: {event_data}")  # Add this
    self._create_bubble(event_data)
```

---

## 📝 Common Questions

### Q: Why can't I connect to my own live stream?

**A**: TikTok API limitations. Try:
- Use another account's stream
- Test with simulation panel
- Check if your stream is actually visible to others

### Q: Bubbles appear too fast/slow?

**A**: Adjust in `config.py`:
```python
EVENT_CONFIGS = {
    'gift': {
        'duration': 5000,  # Slower (show longer)
        'duration': 1000,  # Faster (hide quicker)
    }
}
```

### Q: Can I add custom images?

**A**: Yes! Modify `DUMMY_USERS` in `config.py`:
```python
DUMMY_USERS = [
    {
        "username": "myuser",
        "nickname": "My Name",
        "avatar": "path/to/image.png"  # Local or URL
    }
]
```

### Q: How to change bubble colors?

**A**: Edit `config.py`:
```python
EVENT_CONFIGS = {
    'gift': {
        'color': '#FF0000',  # Red
        'color': '#00FF00',  # Green
        'color': '#0000FF',  # Blue
        # Use any hex color code
    }
}
```

---

## 🆘 Still Having Issues?

### Collect Debug Information

1. **Python Version**
```bash
python --version
```

2. **Package Versions**
```bash
pip list | grep PyQt6
pip list | grep TikTokLive
```

3. **Error Messages**
```bash
# Run with full error output
python main.py 2>&1 | tee error.log
```

4. **System Info**
- OS: Windows 10/11
- RAM: 4GB/8GB/16GB
- Python: 3.8/3.9/3.10/3.11

### Report Issue

Include:
- Error message (full traceback)
- Python version
- Package versions
- Steps to reproduce
- What you expected vs what happened

### Quick Reset

**Start Fresh**:
```bash
# Delete virtual environment
rmdir /s /q venv

# Recreate
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Test
python main.py
```

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Running from correct directory
- [ ] No syntax errors in config.py (if modified)
- [ ] Simulation buttons work (tests basic functionality)
- [ ] Console shows no errors when starting app
- [ ] Latest version of code

---

**Most issues are fixed by:**
1. Updating to latest code
2. Reinstalling dependencies
3. Testing with simulation first (not TikTok connection)

**Remember**: Simulation panel works 100% offline - use it for testing!
