# 🎯 Custom Points System - Panduan Penggunaan

## Fitur Baru

Sekarang Anda dapat mengatur **berapa poin** yang diberikan untuk setiap Like dan Comment!

### Perubahan dari Sebelumnya:
- **Dulu**: 1 Like = 1 poin, 1 Comment = 1 poin (fixed)
- **Sekarang**: Anda bisa atur sendiri! Misal:
  - 1 Like = 5 poin
  - 1 Comment = 10 poin
  - Atau kombinasi lain sesuai keinginan

---

## Cara Menggunakan

### 1. **Buka Tab "🎯 Custom Points"**

Di aplikasi, ada tab baru bernama **"🎯 Custom Points"** (tab ke-8, sebelum Developer).

### 2. **Atur Custom Points**

Anda akan melihat dua pengaturan:

#### ❤️ LIKE - Custom Points
- Spinner untuk mengatur berapa poin per Like
- Range: 1 - 1000 poin
- Default: 1 poin

#### 💬 COMMENT - Custom Points
- Spinner untuk mengatur berapa poin per Comment
- Range: 1 - 1000 poin
- Default: 1 poin

### 3. **Quick Presets**

Untuk mempermudah, tersedia 3 preset siap pakai:

| Preset | Like | Comment |
|--------|------|---------|
| **1:1 (Default)** | 1 poin | 1 poin |
| **5:10** | 5 poin | 10 poin |
| **10:50** | 10 poin | 50 poin |

Klik salah satu tombol untuk langsung menerapkan preset.

### 4. **Simpan Pengaturan**

Setelah mengatur poin sesuai keinginan, klik tombol **"💾 Simpan Point Settings"**.

Pengaturan akan tersimpan di file `point_settings.json` dan otomatis di-load saat aplikasi dibuka lagi.

---

## Contoh Penggunaan

### Scenario 1: Like lebih berharga
```
1 Like = 10 poin
1 Comment = 1 poin
```
Cocok jika Anda ingin like lebih berpengaruh di battle.

### Scenario 2: Comment lebih berharga
```
1 Like = 1 poin
1 Comment = 20 poin
```
Cocok jika Anda ingin mendorong audience untuk lebih aktif komentar.

### Scenario 3: Balanced tapi boosted
```
1 Like = 5 poin
1 Comment = 5 poin
```
Keduanya sama penting, tapi poin naik lebih cepat untuk battle yang lebih seru.

---

## Cara Kerja Teknis

### Point Calculation

**Like:**
```
Total Points = Jumlah Like × Custom Points Per Like
Contoh: 3 likes × 5 poin = 15 poin
```

**Comment:**
```
Total Points = 1 comment × Custom Points Per Comment
Contoh: 1 comment × 10 poin = 10 poin
```

### Log Output

Saat Like/Comment masuk, log akan menampilkan detail:

**Like:**
```
[LIKE] Team A (+15 poin) [3 x 5]
         ^       ^        ^   ^
         |       |        |   Custom points per like
         |       |        Jumlah like
         |       Total points
         Team yang dapat
```

**Comment:**
```
[COMMENT] Team B (+10 poin): Halo semua!
           ^       ^          ^
           |       |          Teks comment
           |       Points
           Team yang dapat
```

---

## File Konfigurasi

### `point_settings.json`
```json
{
  "like": 5,
  "comment": 10
}
```

File ini otomatis dibuat saat Anda klik "Simpan".
Jika file dihapus, sistem akan kembali ke default (1:1).

---

## FAQ

### Q: Apakah pengaturan tersimpan setelah restart aplikasi?
**A:** Ya! Pengaturan otomatis di-load dari `point_settings.json` saat startup.

### Q: Apa yang terjadi jika saya tidak klik "Simpan"?
**A:** Pengaturan hanya berlaku untuk session saat ini. Saat restart, kembali ke pengaturan terakhir yang disimpan.

### Q: Berapa maksimal poin yang bisa diatur?
**A:** Maksimal 1000 poin per interaction. Tapi Anda bisa edit `point_settings.json` manual jika ingin lebih.

### Q: Apakah ini mempengaruhi Gift points?
**A:** Tidak. Gift tetap menggunakan sistem `coin value × 5`. Custom points hanya untuk Like dan Comment.

### Q: Bagaimana cara reset ke default?
**A:** Klik preset "1:1 (Default)" lalu klik "Simpan".

---

## Update di Kode

### File yang Diubah:

1. **`point_settings_widget.py`** (BARU)
   - Widget UI untuk custom points
   - Spinbox dengan range 1-1000
   - Quick preset buttons
   - Save/load dari JSON

2. **`pk_battle_system.py`**
   - Update `add_interaction_points()` untuk terima parameter `points_per_interaction`

3. **`pk_main_window.py`**
   - Import PointSettingsWidget
   - Tambah tab "🎯 Custom Points"
   - Handler `_on_point_settings_changed()`
   - Update logic di `_handle_bubble_event()` untuk gunakan custom points
   - Update log output untuk tampilkan detail perhitungan

4. **`tiktok_handler.py`**
   - Auto-retry connection (3× retry untuk first connect)
   - Auto-reconnect saat disconnect (5× max dengan exponential backoff)
   - HTTP/2 support dan extended timeout (90s read, 45s connect)

---

## Tips & Trik

### 🔥 Battle Cepat
Gunakan poin tinggi (10:50) agar battle selesai lebih cepat dan lebih seru.

### 🐢 Battle Marathon
Gunakan poin rendah (1:1) untuk battle yang panjang dan menantang.

### ⚖️ Balanced Strategy
Sesuaikan ratio Like:Comment berdasarkan audience Anda:
- Audience suka spam like? → Like poin lebih rendah
- Audience aktif comment? → Comment poin lebih tinggi

---

## Version History

- **v1.1** (2025-10-26): Custom Points System added
  - Tab baru "Custom Points"
  - Spinbox configuration (1-1000)
  - Quick presets (1:1, 5:10, 10:50)
  - Auto-save/load dari JSON
  - Detail log output

- **v1.0**: Initial PK Battle System
  - Fixed points (1:1)

---

**Selamat Mencoba! 🎉**

Jika ada pertanyaan atau saran, hubungi Developer:
- YouTube: @arulcg
- Instagram: @arul.cg
