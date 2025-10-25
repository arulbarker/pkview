# ⚡ PK Battle - Quick Start (5 Minutes!)

## 🎯 What Changed?

**OLD System:** Bubble animations only
**NEW System:** Full PK Battle Mode (like TikTok PK!)

---

## 🚀 Launch App

```bash
python main.py
```

---

## ⏱️ 5-Minute Setup

### 1️⃣ Upload Photos (1 min)

```
Click "📸 Photos" tab
→ Browse Team A photo
→ Browse Team B photo
✓ Done!
```

### 2️⃣ Assign Gifts (1 min)

```
Click "🎁 Gifts" tab
→ Click "Split 50-50" button
→ Click "💾 Save Gift Assignment"
✓ Done!
```

### 3️⃣ Test (1 min)

```
Click "🧪 Test" tab
→ Click "🎁 Simulate Gift → Team A"
→ See points increase? ✓
→ Click "🎁 Simulate Gift → Team B"
→ See points increase? ✓
✓ Done!
```

### 4️⃣ Start Battle (30 sec)

```
Click "⚔️ Battle" tab
→ Click "▶️ Start Battle"
→ Timer starts? ✓
✓ Done!
```

### 5️⃣ Connect TikTok (1 min)

```
Click "📺 TikTok" tab
→ Enter your username
→ Click "🔌 Connect to Live"
→ Wait for "Connected" ✓
✓ Done!
```

### 6️⃣ Stream! (30 sec)

```
Open OBS
→ Window Capture → PK Battle app
→ (Optional) Rotate 90° for portrait
→ Start streaming!
✓ You're LIVE! 🎉
```

---

## 🎁 How It Works

### Gift System

```
Viewer sends gift
    ↓
App checks: Team A or B?
    ↓
Add points (coins × 5)
    ↓
Bubble appears on that side
    ↓
Bar updates
```

**Example:**
- Rose (1 coin) → **5 points**
- Castle (20,000 coins) → **100,000 points**

### Round System

```
60 minutes round
    ↓
Timer hits 00:00
    ↓
Compare points
    ↓
Winner gets +1 score
    ↓
🎉 Win effects + sound
    ↓
Reset to 0 points
    ↓
Next round starts automatically!
```

**Score like soccer:** `[5] - [3]`

---

## 📐 Layout

```
┌──────────────────┐
│  TOP: Bubbles    │ ← Like/Comment (decoration)
├──────────────────┤
│  CENTER:         │
│  [A] vs [B]      │ ← Photos, Score, Bar
│  Timer: 45:23    │
├──────────────────┤
│  BOTTOM: Gifts   │ ← Gift bubbles (directional)
│  🎁→A    🎁→B   │
└──────────────────┘

Rotate monitor 90° or in OBS for portrait mode!
```

---

## 🎮 Controls

### Battle Tab
- **Start Battle** - Begin timer
- **Pause** - Pause timer
- **Reset All** - Reset scores to 0-0

### Photos Tab
- **Drag photo** - Click & drag to move
- **Resize** - Drag corners

### Gifts Tab
- **Assign** - Choose Team A or B per gift
- **Save** - MUST save after changes!

### Test Tab
- **Simulate** - Test without TikTok Live

---

## 🔊 Sound (Optional)

Add to `sounds/` folder:
- `team_a_win.mp3`
- `team_b_win.mp3`

App works without sounds (just no audio).

---

## ✅ Before Going Live

Check:
- [ ] Photos uploaded ✓
- [ ] Gifts assigned & saved ✓
- [ ] Tested with simulation ✓
- [ ] Battle started ✓
- [ ] Connected to TikTok ✓

---

## 🆘 Quick Fixes

**"No gifts assigned"**
→ Go to Gifts tab → Save

**Photos not showing**
→ Check file format (PNG/JPG)

**Timer not starting**
→ Click "Start Battle" in Battle tab

**No points adding**
→ Check gift assignment saved

---

## 📖 Full Guide

Read `PK_BATTLE_GUIDE.md` for complete details!

---

**Ready? GO! 🚀**

```bash
python main.py
```
