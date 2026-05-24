# CleanBot Saga — Game Chiến Thuật AI (Design Spec)

**Ngày:** 2026-05-23
**Trạng thái:** Design Approved

---

## 1. Tổng Quan

CleanBot Saga là web game chiến thuật kết hợp 2 bài toán AI kinh điển trong 1 trò chơi 2-pha:

- **Pha 1:** Người chơi chọn thuật toán (BFS/DFS/Greedy) cho AI giải bài toán 8-Puzzle. Số bước giải quyết định Action Points (AP) cho Pha 2.
- **Pha 2:** Người chơi chọn thuật toán tìm đường (BFS/DFS/IDS/UCS) cho robot hút bụi. Robot dùng AP để di chuyển và dọn bụi trên bản đồ lưới.

Game có 3 chế độ: Chiến Dịch (Campaign 15 màn), Daily Challenge, và PvE Arena.

**Mục tiêu:** Vừa giải trí vừa học — người chơi hiểu được điểm mạnh/yếu của từng thuật toán tìm kiếm thông qua trải nghiệm thực tế.

---

## 2. Chế Độ Chơi

### 2.1 Chiến Dịch (Campaign)
- 15 màn, độ khó tăng dần
- Mỗi màn: 1 puzzle + 1 map riêng
- Thuật toán mở khóa dần: BFS/DFS (màn 1-3) → Greedy (màn 4-6) → IDS (màn 7-9) → UCS (màn 10-12) → PvE Arena (màn 13-15)
- Đánh giá sao 1-3 mỗi màn
- Cần ≥ 20⭐ để mở PvE Arena

### 2.2 Daily Challenge
- 1 puzzle + 1 map cố định mỗi ngày (seed từ ngày)
- Tất cả thuật toán có sẵn
- 1 lượt chơi duy nhất mỗi ngày
- Bảng xếp hạng ngày (localStorage-based, top 10)

### 2.3 PvE Arena (mở khóa sau campaign)
- Đấu với AI đối thủ trên cùng bản đồ
- Cả 2 cùng chọn thuật toán puzzle (đồng thời, không thấy lựa chọn của nhau)
- 2 robot (xanh và đỏ) xuất phát từ 2 góc đối diện
- Tranh nhau hút bụi — ai hút được nhiều hơn thắng
- Hệ thống Elo Rating
- AI có 3 mức độ (Easy/Medium/Hard) theo Elo người chơi

---

## 3. Cơ Chế Chi Tiết

### 3.1 Pha 1: 8-Puzzle

**Luồng:**
1. Hiển thị bảng puzzle ngẫu nhiên (luôn giải được)
2. Người chơi chọn 1 thuật toán từ danh sách đã mở khóa
3. AI chạy thuật toán, animation từng bước:
   - Bên trái: Bảng puzzle cập nhật từng nước đi
   - Bên phải: Nhật ký (bước, hướng, heuristic, nodes đã duyệt)
   - Nút điều khiển: ▶ Play, ⏸ Pause, 2x Speed
4. Khi hoàn thành → hiển thị bảng so sánh (nếu chọn thuật toán khác thì kết quả ra sao)

**AP = max(1, 20 - số_bước_puzzle)**
- Không giải được (quá giới hạn) → AP = 0 → Thua màn

### 3.2 Pha 2: Vacuum Cleaner Robot

**Luồng:**
1. Hiển thị bản đồ lưới với bụi (0=sạch, 1=bụi)
2. Người chơi chọn 1 thuật toán tìm đường
3. Robot dùng thuật toán đã chọn tìm bụi gần nhất, di chuyển từng bước:
   - Bên trái: Bản đồ + vị trí robot (🤖) + bụi (●) + AP còn lại
   - Bên phải: Nhật ký (bước, hướng, hút bụi, đang tìm đường...)
   - Nút điều khiển: ▶ Play, ⏸ Pause, 2x Speed
4. Robot tiếp tục tìm bụi tiếp theo cho đến khi hết AP hoặc hết bụi

### 3.3 Cách Tính Điểm

```
Điểm = (bụi_đã_hút × 200) + (AP_còn_dư × 50) + bonus_thuật_toán
```

- **Bụi đã hút:** 200 điểm/ô
- **AP còn dư:** 50 điểm/AP — khuyến khích chọn thuật toán puzzle tối ưu
- **Bonus thuật toán:** 500 điểm nếu chọn đúng thuật toán tối ưu cho map đó
  - Pha 1: BFS luôn tối ưu (đường đi ngắn nhất). Greedy nhanh nhưng không đảm bảo tối ưu. DFS thường kém nhất.
  - Pha 2: BFS, UCS, IDS đều tối ưu trên lưới đều (cost=1). DFS không tối ưu. Bonus trao nếu chọn 1 trong nhóm tối ưu.

### 3.4 Đánh Giá Sao

| ⭐ | Điều kiện |
|---|-----------|
| ⭐ | Hút ≥ 50% bụi — hoàn thành màn |
| ⭐⭐ | Hút ≥ 80% bụi |
| ⭐⭐⭐ | Hút 100% bụi + chọn đúng thuật toán tối ưu |

---

## 4. AI Đối Thủ (PvE)

| Mức | Elo | Hành vi |
|-----|-----|---------|
| Easy | < 1200 | Chọn ngẫu nhiên, 50% đúng. Cùng thuật toán cho cả 2 pha. |
| Medium | 1200-1600 | Phân tích puzzle, 70% đúng. Thay đổi chiến lược theo map. |
| Hard | 1600+ | Chạy thử tất cả thuật toán trước khi chọn. Luôn tối ưu. Ưu tiên tranh bụi gần người chơi. |

---

## 5. Campaign Progression

| Màn | Map | Puzzle (shuffle) | Mở Khóa |
|-----|-----|------------------|---------|
| 1-3 | 5×7, 8-10 bụi | 5-10 bước | BFS, DFS |
| 4-6 | 5×7, 12-16 bụi | 12-18 bước | Greedy Best-First |
| 7-9 | 7×9, 18-22 bụi | 20-30 bước | IDS |
| 10-12 | 7×9, 22-28 bụi | 30-40 bước | UCS |
| 13-15 | 10×10, 30-35 bụi | 40-50 bước | PvE Arena |

---

## 6. Animation & UX

- **Puzzle animation:** Ô số trượt mượt với Pygame surface translation (200ms mặc định, có tua nhanh)
- **Robot animation:** Sprite di chuyển từ ô này sang ô khác + hiệu ứng hút bụi (vòng tròn lan tỏa)
- **Bảng nhật ký:** Panel bên phải cuộn tự động, màu sắc theo loại sự kiện (di chuyển/xanh dương, hút bụi/vàng, hoàn thành/xanh lá)
- **Nút điều khiển:** Play/Pause, 1x/2x/4x tốc độ — vẽ bằng Pygame rect + text
- **Bảng so sánh:** Overlay hiển thị sau mỗi pha, so sánh kết quả nếu chọn thuật toán khác + nhận xét

---

## 7. Kiến Trúc Kỹ Thuật

### 7.1 Technology Stack

| Layer | Công Nghệ |
|-------|-----------|
| Game Engine | **Pygame** — game loop, render, animation |
| AI Engine | **Python** — tái sử dụng trực tiếp code từ notebooks |
| Lưu trữ | **JSON files** — thay cho localStorage |
| UI Components | **Pygame** — button, panel, text rendering |

### 7.2 Cấu Trúc File

```
cleanbot-saga/
├── main.py                  # Entry point, game loop, state machine
├── config.py                # Hằng số: màu sắc, kích thước, FPS
├── core/
│   ├── game_state.py        # State machine (MENU → PHASE1 → PHASE2 → RESULT)
│   ├── scoring.py           # Tính điểm, sao, AP
│   └── storage.py           # Lưu/đọc tiến độ ra JSON
├── puzzle/
│   ├── __init__.py           # PuzzleSolverRegistry — đăng ký solver
│   ├── board.py              # 8-puzzle: sinh, in, di chuyển
│   ├── heuristic.py          # Manhattan, solvability check
│   ├── bfs.py                # BFS solver
│   ├── dfs.py                # DFS solver (depth limit)
│   └── greedy.py             # Greedy Best-First (Manhattan)
├── vacuum/
│   ├── __init__.py            # PathfindingRegistry — đăng ký thuật toán
│   ├── grid.py                # Map: sinh môi trường, quản lý bụi
│   ├── robot.py               # Robot: di chuyển, hút bụi, animation
│   ├── bfs.py                 # BFS pathfinding
│   ├── dfs.py                 # DFS pathfinding
│   ├── ids.py                 # IDS (Early + Late goal test)
│   └── ucs.py                 # UCS (priority queue)
├── campaign/
│   ├── __init__.py
│   └── levels.py              # Dữ liệu 15 màn campaign
├── pve/
│   ├── __init__.py
│   └── ai_opponent.py         # AI đối thủ 3 mức
├── ui/
│   ├── __init__.py
│   ├── renderer.py            # Vẽ puzzle, lưới, robot, animation
│   ├── log_panel.py           # Bảng nhật ký từng bước
│   ├── controls.py            # Nút Play/Pause/Speed
│   ├── menu.py                # Màn hình menu chính
│   └── scoreboard.py          # Bảng điểm, sao, xếp hạng
└── data/
    └── (save files: campaign_progress.json, daily.json, elo.json)
```

### 7.3 Game State Machine

```
MENU → PHASE1 (chọn thuật toán → AI chạy) → PHASE2 (chọn thuật toán → robot chạy) → RESULT (điểm + sao + so sánh) → MENU
```

---

## 8. Bảng Xếp Hạng

- **Campaign:** Tổng điểm 15 màn, lưu localStorage
- **Daily:** Điểm ngày, seed từ ngày để đảm bảo công bằng, lưu theo ngày
- **PvE Elo:** Hệ thống Elo, lưu localStorage

---

## 9. Phạm Vi & Giới Hạn

### Trong phạm vi
- Desktop app chạy bằng Pygame
- Tái sử dụng trực tiếp code AI từ Python notebooks (không cần port)
- Animation từng bước cho cả 2 pha
- 3 chế độ chơi (Campaign, Daily, PvE)
- Lưu tiến độ qua JSON files
- Kiến trúc plugin để dễ thêm thuật toán mới

### Ngoài phạm vi
- Không multiplayer online
- Không backend/server
- Không mobile app
- Không âm thanh bắt buộc (optional)

---

## 10. Tiêu Chí Thành Công

1. Game chạy mượt trên browser (Chrome/Firefox/Edge)
2. Animation rõ ràng, người chơi hiểu được thuật toán đang làm gì
3. Cảm giác progression rõ rệt qua 15 màn campaign
4. Người chơi học được khi nào nên dùng BFS/DFS/UCS/IDS/Greedy
5. PvE AI đủ thách thức ở cả 3 mức độ
