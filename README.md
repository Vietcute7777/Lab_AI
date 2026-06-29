# AI Lab — Các Thuật Toán Trí Tuệ Nhân Tạo

Repository chứa các bài tập mô phỏng thuật toán trong AI, gồm 3 chủ đề chính: **8-Puzzle**, **Máy Hút Bụi (Vacuum Cleaner Agent)**, và **Bài Toán Thỏa Mãn Ràng Buộc (CSP)**.

---

## Cấu Trúc Dự Án

```
.
├── 8_puzzle.ipynb                              # 8-Puzzle: Greedy Agent (Manhattan)
├── 8_puzzle_bfs_dfs.ipynb                      # 8-Puzzle: Heuristic AI + BFS + DFS
├── 8_puzzle_greedy.ipynb                       # 8-Puzzle: Greedy Best-First Search
├── 8_puzzle_hill_climbing.ipynb                # 8-Puzzle: Hill Climbing (Simple & Steepest Ascent)
├── 8_puzzle_pluss.ipynb                        # 8-Puzzle: Heuristic AI (Misplaced Tiles)
├── vacuum_cleaner_agent.ipynb                  # Máy Hút Bụi: Random Walk (có tường)
├── vacuum_cleaner_agent_1.ipynb                # Máy Hút Bụi: Boustrophedon + Trực quan hóa
├── vacuum_cleaner_agent_and_or.ipynb           # Máy Hút Bụi: AND-OR Graph Search
├── vacuum_cleaner_agent_astar.ipynb            # Máy Hút Bụi: A* Algorithm
├── vacuum_cleaner_agent_astar_and_Greedy.zip   # File nén: A* + Greedy
├── vacuum_cleaner_agent_backtracking.ipynb     # Máy Hút Bụi: Backtracking (DFS + Quay lui)
├── vacuum_cleaner_agent_bfs_dfs.ipynb          # Máy Hút Bụi: BFS & DFS tìm bụi gần nhất
├── vacuum_cleaner_agent_forward_checking.ipynb # Máy Hút Bụi: Forward Checking
├── vacuum_cleaner_agent_greedy.ipynb           # Máy Hút Bụi: Greedy Algorithm
├── vacuum_cleaner_agent_hill_climbing.ipynb    # Máy Hút Bụi: Random Restart Hill Climbing
├── vacuum_cleaner_agent_ids.ipynb              # Máy Hút Bụi: IDS (Early vs Late Goal Test)
├── vacuum_cleaner_agent_ids_ucs.zip            # File nén: IDS + UCS
├── vacuum_cleaner_agent_local_beam_search.ipynb # Máy Hút Bụi: Local Beam Search
├── vacuum_cleaner_agent_local_beam_search_and_Random_Restart_Climbing_and_Simulated_Annealing.zip
├── vacuum_cleaner_agent_simulated_annealing.ipynb # Máy Hút Bụi: Simulated Annealing
├── vacuum_cleaner_agent_ucs.ipynb              # Máy Hút Bụi: UCS + UI Animation
├── Thuat_Toan_AC_3.ipynb                       # CSP: AC-3 — Tô màu bản đồ Việt Nam
├── Thuat_Toan_Min_Conflict.ipynb               # CSP: Min-Conflict — Bài toán 6 con Hậu
└── 2 bài tập tuần trước.zip                    # File nén bài tập tổng hợp
```

---

## 1. Bài Toán 8-Puzzle

Trạng thái đích: `[[1,2,3],[4,5,6],[7,8,0]]` với `0` là ô trống. Agent di chuyển ô trống để đưa bảng về đích.

| File | Thuật Toán | Heuristic | Đặc Điểm |
|------|------------|-----------|----------|
| `8_puzzle_pluss.ipynb` | Heuristic AI (step-by-step) | Misplaced Tiles | Phiên bản đầu tiên, chọn nước đi tốt nhất từng bước |
| `8_puzzle.ipynb` | Greedy Agent | Manhattan Distance | Tự động chọn nước đi có `h(n)` nhỏ nhất |
| `8_puzzle_bfs_dfs.ipynb` | BFS + DFS + Heuristic AI | Misplaced Tiles | So sánh 3 thuật toán trên cùng bàn cờ |
| `8_puzzle_greedy.ipynb` | Greedy Best-First Search | Manhattan Distance | Dùng min-heap với `f = h`, truy vết đường đi |
| `8_puzzle_hill_climbing.ipynb` | Hill Climbing | Manhattan Distance | Simple + Steepest Ascent, minh họa local maximum |

### So sánh thuật toán

| Tiêu chí | Heuristic AI | BFS | DFS | Greedy Best-First | Hill Climbing |
|----------|-------------|-----|-----|-------------------|---------------|
| Đảm bảo tối ưu | Không | Có | Không | Không | Không |
| Tìm thấy lời giải | Không đảm bảo | Có | Tùy depth | Có (nếu giải được) | Có thể kẹt local max |
| Heuristic | Số ô sai | Không | Không | Manhattan | Manhattan |
| Tốc độ | Nhanh | Chậm (bài toán phức tạp) | Phụ thuộc depth | Nhanh | Rất nhanh |

---

## 2. Bài Toán Máy Hút Bụi (Vacuum Cleaner)

Môi trường lưới 5×7. Quy ước: `0` = ô sạch/máy, `1` = bụi, `2` = tường. Agent khởi đầu tại `(0,0)` và tìm cách hút sạch mọi ô bụi.

### 2.1. Thuật toán Tìm kiếm Cơ bản

| File | Thuật Toán | Cơ Chế | Đặc Điểm |
|------|------------|--------|----------|
| `vacuum_cleaner_agent.ipynb` | Random Walk | Chọn hướng ngẫu nhiên | Môi trường có **tường (2)** |
| `vacuum_cleaner_agent_1.ipynb` | Boustrophedon | Quét zigzag theo hàng | Trực quan hóa matplotlib |
| `vacuum_cleaner_agent_bfs_dfs.ipynb` | BFS + DFS | Tìm đường đến bụi gần nhất | So sánh BFS vs DFS |
| `vacuum_cleaner_agent_ucs.ipynb` | UCS | Hàng đợi ưu tiên theo chi phí | UI Animation real-time |
| `vacuum_cleaner_agent_ids.ipynb` | IDS | DLS tăng dần depth limit | Early vs Late Goal Test |

### 2.2. Thuật toán Tìm kiếm Heuristic & Cục bộ

| File | Thuật Toán | Heuristic | Đặc Điểm |
|------|------------|-----------|----------|
| `vacuum_cleaner_agent_greedy.ipynb` | Greedy | Manhattan Distance | Chọn ô kề có bụi, nếu không thì BFS tìm bụi gần nhất |
| `vacuum_cleaner_agent_astar.ipynb` | A* | Manhattan Distance | `f(n) = g(n) + h(n)`, đảm bảo đường đi tối ưu |
| `vacuum_cleaner_agent_hill_climbing.ipynb` | Random Restart Hill Climbing | Manhattan Distance | Steepest Ascent + Random Restart khi kẹt local max |
| `vacuum_cleaner_agent_simulated_annealing.ipynb` | Simulated Annealing | Manhattan Distance | Chấp nhận bước xấu với xác suất `e^(-ΔE/T)`, trực quan Roomba |
| `vacuum_cleaner_agent_local_beam_search.ipynb` | Local Beam Search | Manhattan Distance | k=3 chùm tia, sinh tất cả successor rồi chọn k tốt nhất |

### 2.3. Thuật toán Tìm kiếm Có Ràng buộc & Suy luận

| File | Thuật Toán | Cơ Chế | Đặc Điểm |
|------|------------|--------|----------|
| `vacuum_cleaner_agent_backtracking.ipynb` | Backtracking | DFS + Quay lui | Khám phá lưới, quay lui khi ngõ cụt |
| `vacuum_cleaner_agent_forward_checking.ipynb` | Forward Checking | Nhìn trước N bước | Đánh giá hướng đi tối ưu bằng điểm số |
| `vacuum_cleaner_agent_and_or.ipynb` | AND-OR Graph Search | Kế hoạch điều kiện | Môi trường non-deterministic, lưới 3×3 |

### Sơ đồ tiến hóa thuật toán

```
Random Walk → Boustrophedon (quét toàn bộ)
                  ↓
           BFS / DFS / UCS (tìm bụi gần nhất)
                  ↓
           IDS (kết hợp ưu điểm DFS & BFS)
                  ↓
           Greedy / A* (tìm kiếm có thông tin)
                  ↓
           Hill Climbing / Simulated Annealing / Local Beam Search (tối ưu cục bộ)
                  ↓
           Backtracking / Forward Checking / AND-OR (ràng buộc & suy luận)
```

---

## 3. Bài Toán Thỏa Mãn Ràng Buộc (CSP)

| File | Thuật Toán | Bài Toán | Đặc Điểm |
|------|------------|----------|----------|
| `Thuat_Toan_AC_3.ipynb` | AC-3 + Backtracking | Tô màu bản đồ Việt Nam | 22 tỉnh, 4 màu, lan truyền ràng buộc + MRV |
| `Thuat_Toan_Min_Conflict.ipynb` | Min-Conflict | 6 con Hậu (6×6) | Local search, sửa chữa lặp, benchmark đa kích thước |

---

## Cách Chạy

Mở file `.ipynb` bằng **Jupyter Notebook**, **JupyterLab** hoặc **VS Code** và chạy từng cell theo thứ tự.

```bash
# Cài đặt dependencies
pip install numpy matplotlib
```

---

## Công Nghệ Sử Dụng

- **Python 3**
- **NumPy** — xử lý ma trận
- **Matplotlib** — trực quan hóa lưới, bản đồ, bàn cờ
- **heapq / collections.deque** — hàng đợi ưu tiên và BFS
- **Jupyter Notebook** — môi trường tương tác
