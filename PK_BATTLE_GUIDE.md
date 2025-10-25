# 🎮 PK Battle Mode - Complete Guide

## 🎯 What is PK Battle Mode?

**TikTok-style Player Knockout (PK) Battle** - A competitive live streaming mode where two teams battle for points through viewer gifts!

**Like Soccer Scoring:**
- Round-based competition (default: 60 minutes per round)
- Team with most points wins the round
- Score tracked like soccer: `Team A [2] - [1] Team B`
- Infinite rounds until you end the stream

---

## 📐 Layout Design

### Vertical Content in Horizontal Window

```
Window: 1920 x 1080 (Horizontal)
Content: Arranged VERTICALLY

┌─────────────────────────────────────┐
│  ╔══════════════════════════════╗   │
│  ║   TOP BUBBLE ZONE            ║   │ ← Like/Comment
│  ║   💬 ❤️ 👥                  ║   │   bubbles (random)
│  ╚══════════════════════════════╝   │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  TEAM A    [2] - [1]   TEAM B │  │ ← SCORE
│  │                               │  │
│  │  ┌───────┐       ┌───────┐   │  │
│  │  │ Photo │       │ Photo │   │  │ ← PHOTOS
│  │  │   A   │       │   B   │   │  │   (Draggable!)
│  │  └───────┘       └───────┘   │  │
│  │                               │  │
│  │  15,750 pts  |  7,320 pts    │  │ ← POINTS
│  │                               │  │
│  │  Time: 45:23 / 60:00         │  │ ← TIMER
│  │                               │  │
│  │  [████████░░░░░░░░]           │  │ ← BAR
│  │   68%  vs  32%               │  │
│  └───────────────────────────────┘  │
│                                     │
│  ╔══════════════════════════════╗   │
│  ║   BOTTOM BUBBLE ZONE         ║   │ ← GIFT bubbles
│  ║   🎁→A        🎁→B          ║   │   (Directional!)
│  ╚══════════════════════════════╝   │
└─────────────────────────────────────┘

Monitor Setup:
- Rotate monitor 90° (landscape → portrait)
- OR in OBS: Transform → Rotate 90°
```

---

## 🎁 Gift Point System

### Point Calculation

**Formula:** `Gift Coins × 5 = Points`

Examples:
- Rose (1 coin) = **5 points**
- Doughnut (30 coins) = **150 points**
- Castle (20,000 coins) = **100,000 points**
- Universe (50,000 coins) = **250,000 points**

### Gift Assignment

**ALL gifts must be assigned to Team A or Team B!**

```
Gifts Tab → Assignment UI:
┌────────────────────────────────┐
│ Gift Name    │ Coins │ Team    │
├────────────────────────────────┤
│ Rose         │   1   │ (•)A ( )B │
│ Castle       │20,000 │ ( )A (•)B │
│ Universe     │50,000 │ (•)A ( )B │
└────────────────────────────────┘

Quick Actions:
- [Assign All → Team A]
- [Assign All → Team B]
- [Split 50-50]
```

**When gift received:**
1. System checks assignment
2. Adds points to correct team
3. Gift bubble appears on that team's side

---

## ⚽ Round System (Like Soccer!)

### How Rounds Work

```
Round 1 (60 minutes):
  Team A: 15,750 points
  Team B:  7,320 points

  Timer: 00:00
  → Team A WINS! 🏆

  Score Update: [1] - [0]

  5 seconds later...
  → Points RESET to 0
  → Timer RESTART to 60:00
  → Round 2 begins automatically!
```

### Score Tracking

```
Current State:
TEAM A  [5] - [3]  TEAM B

This means:
- Team A won 5 rounds
- Team B won 3 rounds
- Total 8 rounds played
```

### Win Effects

When a team wins a round:
1. **Visual Effect:** Screen animation from winning side
2. **Sound Effect:** `team_a_win.mp3` or `team_b_win.mp3`
3. **Log Message:** "🏆 TEAM A WINS THE ROUND!"
4. **5 second celebration pause**
5. **Auto-reset and continue**

---

## 🫧 Bubble System

### Two Bubble Zones

**TOP Zone (Like/Comment/Follow):**
- ✅ Random placement
- ✅ Existing bubble effects
- ❌ NO points added (just decoration!)
- Purpose: Memeriahkan suasana

**BOTTOM Zone (Gifts):**
- ✅ Directional placement
  - Team A gifts → LEFT side
  - Team B gifts → RIGHT side
- ✅ Points added based on gift value
- ✅ Gift tier effects (micro to mega)

### Bubble Behavior

```
Event Type:     Zone:      Position:     Points:
─────────────────────────────────────────────────
Like            TOP        Random        NO
Comment         TOP        Random        NO
Follow          TOP        Random        NO
Join            TOP        Random        NO
Share           TOP        Random        NO

Gift → Team A   BOTTOM     Left side     YES (coins×5)
Gift → Team B   BOTTOM     Right side    YES (coins×5)
```

---

## 📸 Photo Management

### Upload Photos

```
Photos Tab:
1. Click "Browse Photo for Team A"
2. Select image (PNG, JPG, WEBP, any format)
3. Photo loads automatically
4. Repeat for Team B
```

### Customize Photos

**Drag to Move:**
- Click and hold photo
- Drag to desired position
- Release to set

**Resize:**
- Hover near photo edge/corner
- Cursor changes to resize icon
- Drag to resize (100px - 600px)

**Features:**
- ✅ Circular crop automatically
- ✅ Team color border (Red for A, Teal for B)
- ✅ Positions saved during session

---

## ⚙️ Settings & Controls

### Battle Tab

**Round Duration:**
- Default: 60 minutes
- Range: 1 - 180 minutes
- Can change anytime (affects next round)

**Controls:**
- ▶️ **Start Battle** - Begin timer and scoring
- ⏸️ **Pause** - Pause timer (resume later)
- 🔄 **Reset All** - Reset scores and points to 0

**Sound Settings:**
- ☑️ Enable Win Sounds
- Volume slider (0-100%)

### TikTok Tab

**Connect to Live:**
1. Enter TikTok username (without @)
2. Click "Connect to Live"
3. Status shows "Connected" when ready
4. Gifts automatically processed!

**Disconnect:**
- Click "Disconnect" to stop

### Photos Tab

**Team A Photo:**
- Browse and upload
- Preview shown

**Team B Photo:**
- Browse and upload
- Preview shown

### Gifts Tab

**Gift Assignment:**
- List of ALL TikTok gifts (~94 total)
- Search filter
- Assign each to Team A or B
- **MUST save after changes!**

**Quick Actions:**
- Assign all to Team A
- Assign all to Team B
- Split 50-50 (alternating)

### Test Tab

**Simulation Controls:**
- ❤️ Simulate Like
- 💬 Simulate Comment
- 🎁 Simulate Gift → Team A (random gift from A's list)
- 🎁 Simulate Gift → Team B (random gift from B's list)
- 🚀 Rapid Test (10 random events)

---

## 🎬 Quick Start Guide

### Step 1: Setup Photos (1 minute)

```
1. Go to "Photos" tab
2. Upload Team A photo
3. Upload Team B photo
4. (Optional) Drag/resize on main display
```

### Step 2: Assign Gifts (2 minutes)

```
1. Go to "Gifts" tab
2. Click "Split 50-50" for quick setup
   OR manually assign each gift
3. Click "💾 Save Gift Assignment"
```

### Step 3: Test Everything (1 minute)

```
1. Go to "Test" tab
2. Click "🎁 Simulate Gift → Team A"
3. Check:
   - Points increase for Team A ✓
   - Bubble appears on LEFT ✓
   - Bar moves ✓
4. Click "🎁 Simulate Gift → Team B"
5. Check same for Team B
```

### Step 4: Start Battle (30 seconds)

```
1. Go to "Battle" tab
2. Check round duration (default: 60 min)
3. Click "▶️ Start Battle"
4. Timer starts counting down!
```

### Step 5: Connect to TikTok Live

```
1. Go to "TikTok" tab
2. Enter username: "yourusername"
3. Click "🔌 Connect to Live"
4. Wait for "Connected" status
5. Gifts now automatically tracked!
```

### Step 6: Stream!

```
- OBS: Add window capture
- Rotate 90° if needed
- Start streaming!
- Gifts add points automatically
- Rounds auto-reset
```

---

## 🔊 Sound Files

### Required Sound Files

Place in `sounds/` folder:

```
sounds/
├── team_a_win.mp3      (plays when Team A wins round)
├── team_b_win.mp3      (plays when Team B wins round)
├── round_end_warning.mp3  (plays at 10 seconds remaining)
└── final_win.mp3       (optional - future use)
```

### If No Sound Files

App creates placeholder files automatically.
Replace with actual MP3 files for real sound effects!

**Where to get sounds:**
- Record your own
- Download from freesound.org
- Use AI voice generator
- Text-to-speech: "Team A wins!"

---

## 📊 Statistics Display

### Real-time Stats

**Score:** `TEAM A [5] - [3] TEAM B`
- Rounds won by each team

**Points:** `15,750 pts | 7,320 pts`
- Current round points

**Timer:** `Time: 45:23 / 60:00`
- Minutes:Seconds remaining

**Bar:** Visual percentage
- Red (Team A) vs Teal (Team B)
- Shows point distribution

---

## 🎨 Customization

### Team Colors

**Team A:**
- Color: Red/Pink `#FF6B6B`
- Photo border: Red
- Points display: Red
- Bar: Red gradient

**Team B:**
- Color: Teal/Cyan `#4ECDC4`
- Photo border: Teal
- Points display: Teal
- Bar: Teal gradient

### Change Colors

Edit `pk_main_window.py`:
```python
# Team A color
QColor(255, 107, 107)  # RGB

# Team B color
QColor(78, 205, 196)   # RGB
```

---

## 🐛 Troubleshooting

### "No gifts assigned to Team X!"

**Problem:** Tried to simulate gift but no gifts assigned
**Solution:** Go to Gifts tab → Assign gifts → Save

### "Sound file not found"

**Problem:** Sound files missing
**Solution:** Add MP3 files to `sounds/` folder

### Photos not showing

**Problem:** Photo upload failed
**Solution:** Check file format (PNG, JPG, WEBP supported)

### Bubbles not appearing

**Problem:** Bubble zone might be hidden
**Solution:** Check if bubbles are behind PK view (z-index issue)

### Timer not starting

**Problem:** Battle not started
**Solution:** Go to Battle tab → Click "▶️ Start Battle"

---

## 💡 Pro Tips

### Tip 1: Gift Strategy

```
High-value gifts → Team you want to promote
Example:
- Team A = Your main streamer
- Assign Universe, Castle, Lion → Team A
- Assign smaller gifts → Team B for balance
```

### Tip 2: Testing Before Live

```
1. Set round duration to 1 minute
2. Test with simulation
3. Verify everything works
4. Change back to 60 minutes
5. Go live!
```

### Tip 3: OBS Setup

```
OBS Scene:
1. Add Window Capture → PK Battle App
2. Transform → Rotate 90° CW
3. Resize to fit canvas
4. Add overlays as needed
```

### Tip 4: Monitor Setup

```
For best experience:
- Use portrait monitor (rotated 90°)
- OR use iPad/tablet as secondary display
- Full immersion!
```

### Tip 5: Save Configurations

```
Gift assignments save to:
  gift_assignment.json

Backup this file!
- Copy before changing
- Restore if needed
```

---

## 📁 File Structure

```
livebuble/
├── main.py                     (Entry point - UPDATED!)
├── pk_main_window.py           (Main PK window - NEW!)
├── pk_battle_system.py         (Score/timer logic - NEW!)
├── photo_manager.py            (Photo widgets - NEW!)
├── gift_assignment_widget.py   (Gift UI - NEW!)
├── sound_manager.py            (Audio - NEW!)
│
├── bubble_widget.py            (Bubble effects - existing)
├── effects.py                  (18 effects - existing)
├── gift_tiers.py               (Gift values - existing)
├── tiktok_handler.py           (TikTok connection - existing)
├── config.py                   (Configuration - existing)
│
├── gift_assignment.json        (Auto-created)
│
└── sounds/                     (Create this!)
    ├── team_a_win.mp3
    ├── team_b_win.mp3
    ├── round_end_warning.mp3
    └── final_win.mp3
```

---

## 🚀 Launch Application

```bash
# Start PK Battle Mode
python main.py
```

**On First Launch:**
1. Upload photos
2. Assign gifts
3. Save settings
4. Test with simulation
5. Ready to stream!

---

## ✅ Feature Checklist

Before going live, verify:

- [ ] Team A photo uploaded
- [ ] Team B photo uploaded
- [ ] Photos positioned correctly (drag/resize)
- [ ] ALL gifts assigned (check Gifts tab)
- [ ] Gift assignment SAVED
- [ ] Sound files in `sounds/` folder (optional)
- [ ] Sound enabled (Battle tab)
- [ ] Round duration set (default: 60 min)
- [ ] Tested with simulation
- [ ] TikTok username entered
- [ ] Connected to TikTok Live
- [ ] Battle started (timer running)
- [ ] OBS capturing correctly

---

## 🎉 Summary

**What You Get:**

✅ **PK Battle System** - Soccer-style scoring
✅ **Gift Tracking** - Automatic point calculation
✅ **Team Photos** - Fully customizable, drag & resize
✅ **94 Gift Support** - All TikTok gifts assignable
✅ **Bubble Effects** - 18 effects, directional placement
✅ **Sound Effects** - Win celebrations
✅ **Auto Rounds** - Infinite rounds, auto-reset
✅ **Real-time Stats** - Score, points, timer, bar
✅ **Vertical Layout** - Perfect for portrait streaming

**The Ultimate TikTok PK Battle Tool! 🔥**

---

**Need Help?** Check logs in Event Log panel (bottom right).

**Enjoy your PK Battles! 🎮🏆**
