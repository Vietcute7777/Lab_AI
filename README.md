# AI Lab — Các Thuật Toán Tìm Kiếm (Search Algorithms)

Repository chứa các bài tập mô phỏng thuật toán tìm kiếm trong AI, gồm 2 bài toán chính: **8-Puzzle** và **Máy Hút Bụi (Vacuum Cleaner Agent)**.

---

## Cấu Trúc Dự Án

```
.
├── 8_puzzle.ipynb                       # 8-Puzzle: Greedy Agent (Manhattan)
├── 8_puzzle_bfs_dfs.ipynb               # 8-Puzzle: Heuristic AI + BFS + DFS
├── 8_puzzle_greedy.ipynb                # 8-Puzzle: Greedy Best-First Search (Manhattan)
├── 8_puzzle_pluss.ipynb                 # 8-Puzzle: Heuristic AI cơ bản (Misplaced Tiles)
├── vacuum_cleaner_agent.ipynb           # Máy Hút Bụi: Random Walk (có tường)
├── vacuum_cleaner_agent_1.ipynb         # Máy Hút Bụi: Quét Boustrophedon + Trực quan hóa
├── vacuum_cleaner_agent_bfs_dfs.ipynb   # Máy Hút Bụi: BFS & DFS tìm bụi gần nhất
├── vacuum_cleaner_agent_ids.ipynb       # Máy Hút Bụi: IDS (Early vs Late Goal Test)
├── vacuum_cleaner_agent_ucs.ipynb       # Máy Hút Bụi: UCS + UI Animation
└── vacuum_cleaner_agent_ids_ucs.zip     # File nén bài tập IDS + UCS
```

---

## 1. Bài Toán 8-Puzzle

Trạng thái đích: `[[1,2,3],[4,5,6],[7,8,0]]` với `0` là ô trống. Agent di chuyển ô trống để đưa bảng về đích.

| File | Thuật Toán | Heuristic | Đặc Điểm |
|------|------------|-----------|----------|
| `8_puzzle_pluss.ipynb` | Heuristic AI (step-by-step) | Misplaced Tiles | Phiên bản đầu tiên, chọn nước đi tốt nhất từng bước, phạt lặp +100 điểm |
| `8_puzzle.ipynb` | Greedy Agent | Manhattan Distance | Agent tự động chọn nước đi có `h(n)` nhỏ nhất. Phát hiện và dừng khi bị kẹt (lặp lại trạng thái) |
| `8_puzzle_bfs_dfs.ipynb` | BFS + DFS + Heuristic AI | Misplaced Tiles | **So sánh 3 thuật toán** trên cùng bàn cờ: BFS (đường đi ngắn nhất), DFS (có giới hạn độ sâu), Heuristic AI |
| `8_puzzle_greedy.ipynb` | Greedy Best-First Search | Manhattan Distance | Dùng hàng đợi ưu tiên (min-heap) với `f = h`, có tập `visited`, truy vết được đường đi. So sánh Misplaced Tiles vs Manhattan |

### So sánh kết quả giữa các thuật toán

| Tiêu chí | Heuristic AI | BFS | DFS | Greedy Best-First |
|----------|-------------|-----|-----|-------------------|
| Đảm bảo tối ưu | Không | Có | Không | Không |
| Tìm thấy lời giải | Không đảm bảo | Có | Tùy giới hạn depth | Có (nếu bài toán giải được) |
| Tái tạo đường đi | Không | Có | Có | Có |
| Heuristic | Số ô sai | Không dùng | Không dùng | Manhattan Distance |
| Tốc độ | Nhanh | Chậm với bài toán phức tạp | Phụ thuộc depth limit | Nhanh |

---

## 2. Bài Toán Máy Hút Bụi (Vacuum Cleaner)

Môi trường lưới 5x7. Quy ước: `0` = ô sạch/máy, `1` = bụi, `2` = tường (chỉ file đầu). Agent khởi đầu tại `(0,0)` và tìm cách hút sạch mọi ô bụi.

| File | Thuật Toán | Cơ Chế | Đặc Điểm |
|------|------------|--------|----------|
| `vacuum_cleaner_agent.ipynb` | Random Walk | Chọn hướng ngẫu nhiên | Môi trường có **tường (2)**. Có cơ chế phát hiện lặp để dừng. |
| `vacuum_cleaner_agent_1.ipynb` | Boustrophedon | Quét zigzag theo hàng | Quét toàn bộ lưới. Có **trực quan hóa matplotlib**. |
| `vacuum_cleaner_agent_bfs_dfs.ipynb` | BFS + DFS | Tìm đường đến bụi gần nhất | So sánh BFS (ngắn nhất) vs DFS. So sánh với Boustrophedon baseline. |
| `vacuum_cleaner_agent_ids.ipynb` | IDS | DLS tăng dần depth limit | So sánh **Early Goal Test** vs **Late Goal Test**. |
| `vacuum_cleaner_agent_ucs.ipynb` | UCS | Hàng đợi ưu tiên theo chi phí | Chi phí mỗi bước = 1. Có **UI Animation** real-time. |

### Tiến hóa thuật toán qua các file

```
Random Walk → Boustrophedon (quét toàn bộ)
                   ↓
            BFS / DFS (tìm bụi gần nhất)
                   ↓
            IDS (kết hợp ưu điểm DFS & BFS)
                   ↓
            UCS (tối ưu chi phí đường đi)
```

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
- **Matplotlib** — trực quan hóa lưới và agent
- **heapq / collections.deque** — hàng đợi ưu tiên và BFS
- **Jupyter Notebook** — môi trường tương tác
