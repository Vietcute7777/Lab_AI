# CleanBot Saga — Design System

## Overview

CleanBot Saga is a dual-phase strategy game: solve an 8-puzzle (Phase 1) to earn Action Points, then guide a vacuum-cleaning robot across a grid (Phase 2). The UI is built entirely with **Pygame** (no HTML/CSS). This document formalizes the visual and layout system.

---

## 1. Screen Canvas

| Property      | Value |
|---------------|-------|
| Resolution    | 1200 × 800 px |
| Aspect Ratio  | 3:2 |
| Frame Rate    | 60 FPS |
| Font Rendering | Pygame `.render()` with Tahoma (best Vietnamese Unicode support on Windows) |

---

## 2. Color Palette

### Backgrounds

| Token       | Hex       | RGB            | Usage                        |
|-------------|-----------|----------------|------------------------------|
| BG_DARK     | `#12121E` | `(18, 18, 30)` | Main screen background       |
| BG_MID      | `#1C1C30` | `(28, 28, 48)` | Secondary panels             |
| BG_LIGHT    | `#28283C` | `(40, 40, 60)` | Borders, grid cells          |
| SIDEBAR_BG  | `#161626` | `(22, 22, 38)` | Right sidebar panel          |

### Text

| Token       | Hex       | RGB              | Usage                         |
|-------------|-----------|------------------|-------------------------------|
| WHITE       | `#FFFFFF` | `(255,255,255)`  | Primary body text             |
| GRAY_LIGHT  | `#B4B4C8` | `(180,180,200)`  | Labels, descriptions          |
| GRAY_MID    | `#505064` | `(80,80,100)`    | Disabled elements, separators |

### Accents

| Token       | Hex       | RGB              | Usage                             |
|-------------|-----------|------------------|-----------------------------------|
| CYAN        | `#3CD2D2` | `(60,210,210)`   | Section titles, info highlights   |
| CYAN_BRIGHT | `#64FFFF` | `(100,255,255)`  | Main title glow, active states    |
| BLUE        | `#4682E6` | `(70,130,230)`   | Primary buttons, robot body       |
| GREEN       | `#50D25A` | `(80,210,90)`    | Success, optimal algorithm, AP    |
| ORANGE      | `#FF961E` | `(255,150,30)`   | Score display, warnings           |
| RED         | `#EB4646` | `(235,70,70)`    | Failure, locked elements          |
| YELLOW      | `#FFC828` | `(255,200,40)`   | Star ratings, dust particles      |
| PURPLE      | `#A050DC` | `(160,80,220)`   | Special achievements              |

### Semantic Tokens

| Token           | Color    | When                          |
|-----------------|----------|-------------------------------|
| TILE_DEFAULT    | BG_MID   | Puzzle tile, not in place     |
| TILE_CORRECT    | GREEN    | Puzzle tile in goal position  |
| TILE_HIGHLIGHT  | BLUE     | Tile being moved              |
| TILE_EMPTY      | BG_DARK  | Empty cell (tile #0)          |
| DUST_COLOR      | YELLOW   | Dust cell on grid             |
| DUST_GLOW       | YELLOW+  | Animated dust glow            |
| ROBOT_PLAYER    | BLUE     | Player's robot body           |
| ROBOT_ENEMY     | RED      | Enemy robot (PvE mode)        |

---

## 3. Typography

| Font Token    | Size | Weight | Uses                                  |
|---------------|------|--------|---------------------------------------|
| FONT_TITLE    | 48   | bold   | Main title "CLEANBOT SAGA"            |
| FONT_LARGE    | 32   | regular| Section headers, score, star display  |
| FONT_NORMAL   | 24   | regular| Button labels, body text              |
| FONT_SMALL    | 18   | regular| Descriptions, log entries, footers    |
| FONT_EMOJI    | 36   | regular| Star/emoji display                    |

**Font Family**: Tahoma (covers full Vietnamese Unicode range). Falls back to Arial → Segoe UI → Verdana → Pygame default.

### Text Conventions

- **Titles**: ALL CAPS (e.g., "CLEANBOT SAGA", "PHA 1: GIẢI 8-PUZZLE")
- **Buttons**: UPPERCASE Vietnamese (e.g., "CHƠI LẠI", "TIẾP TỤC")
- **Body**: Sentence case (e.g., "Bụi đã hút: 12 / 20")
- **Log panel**: Mixed case with technical details (e.g., "Bước 5: RIGHT - h=3")

---

## 4. Layout System

### Grid structure

```
+----------------------------------+
|         1200 × 800               |
|  +-----------+  +-------------+  |
|  |           |  |             |  |
|  |  Main     |  |  Sidebar    |  |
|  |  Content  |  |  350×800    |  |
|  |  850×800  |  |             |  |
|  |           |  |             |  |
|  +-----------+  +-------------+  |
+----------------------------------+
```

### Spacing Tokens

| Token          | Value | Usage                              |
|----------------|-------|------------------------------------|
| MARGIN_X (mx)  | 40    | Horizontal page edge margin        |
| MARGIN_Y (my)  | 30    | Vertical page edge margin          |
| PADDING_SMALL  | 8     | Inner padding, gaps between items  |
| PADDING_MEDIUM | 16    | Section spacing, button gaps       |
| PADDING_LARGE  | 24    | Between major sections             |
| PADDING_XL     | 40    | Title-to-content distance           |

### Main Content Area (left, x: 0–850)

| Screen   | Content offsets                     |
|----------|-------------------------------------|
| Menu     | Centered on entire canvas           |
| Phase 1  | Puzzle at `(mx, my+50)`, goal below |
| Phase 2  | Grid at `(mx, my+60)`               |
| Result   | Text at `(mx+60, my+100)`           |

### Sidebar (right, x: 850–1200)

| Element    | Position                  |
|------------|---------------------------|
| Panel      | `(850, 0, 350, 800)`     |
| Title      | `(860, MARGIN_Y)`        |
| Select box | `(860, 170)`             |
| Log panel  | `(850, 310, 330, 400)`   |
| Controls   | `(860, 740)`             |

---

## 5. Components

### 5.1 Buttons

```
┌─────────────────────┐
│   Gradient fill      │
│   Rounded rect 8px   │
│   White border       │  ← hover: glow + lighter fill
│   Shadow offset 3px  │
│   Text centered      │
└─────────────────────┘
```

**States**: normal / hover / disabled (grayed).
**Categories**: primary (BLUE), success (GREEN), danger (RED), warning (ORANGE).
**Standard size**: `260 × 44px`.

### 5.2 Puzzle Board

3×3 grid of tiles with gap. Each tile is `80×80px` with `4px` gap.
- Empty tile: dark muted background
- Correct-position tile: green border + glow
- Highlighted tile (being moved): blue
- Shadow under each tile

### 5.3 Vacuum Grid

Variable-dimension grid cells, each `50×50px` with `2px` gap.
- Empty: BG_MID
- Dust: yellow with animated pulsing glow
- Cleaned: GRAY_LIGHT
- Robot: blue cell with robot SVG

### 5.4 Log Panel

```
┌──────────────────────┐
│ NHẬT KÝ THUẬT TOÁN    │  ← title
│ Bước 1: LEFT - h=4    │
│ Bước 2: RIGHT - h=3   │  ← max 18 visible lines
│   >> HÚT BỤI tại (1,0)│
│ HOÀN THÀNH!            │
└──────────────────────┘
```

Scrollable (by eviction): keeps last 20 entries, renders last 18 visible.

### 5.5 Game Controls

Play/Pause toggle + speed selector (1×, 2×, 4×). Active speed highlighted in GREEN.

### 5.6 Modals

Overlay system:
- Semi-transparent dark backdrop (`(0,0,0,160)`)
- Centered panel with title, body, and action buttons
- Close on backdrop click or explicit button
- Used for: transition confirmations, info/help, achievements

### 5.7 Progress Bar

Filled bar with gradient, used in Phase 2 to show dust-cleaning progress.

---

## 6. Animation Effects

| Effect              | Where                          | Detail                                        |
|---------------------|--------------------------------|-----------------------------------------------|
| Gradient background | Menu bg                        | Sine-wave color bands scrolling over time     |
| Tile movement       | Phase 1 anim                   | (Future: smooth slide between steps)         |
| Dust pulsing        | Phase 2 dust cells             | `1.0 + 0.15 × sin(time / 300)`               |
| Robot LED blink     | Robot body                     | `0.6 + 0.4 × sin(time / 200)`                |
| Button hover glow   | All buttons                    | Glow circle + lighter gradient on hover       |
| Glow under title    | Menu                           | Radial cyan glow behind "CLEANBOT SAGA"       |
| Star burst          | Result screen (3⭐)            | Rotating particle burst                       |
| Suction particles   | Menu vacuum character          | Cyan dots below vacuum (50% duty cycle)       |

---

## 7. Screen Flow

```
┌─────────┐
│  MENU   │  ← MainMenu (mode selection)
└────┬────┘
     │ click Campaign / Daily / PvE
     ▼
┌─────────┐
│ PHASE 1 │  ← Phase1Screen — 8-puzzle solver selection
│         │     Select algorithm → watch solution anim
│         │     → "QUA PHA 2" button
└────┬────┘
     │
     ▼
┌─────────┐
│ PHASE 2 │  ← Phase2Screen — vacuum robot control
│         │     Select pathfinding → watch robot clean
│         │     → "XEM KẾT QUẢ" button
└────┬────┘
     │
     ▼
┌─────────┐
│ RESULT  │  ← ResultScreen — score, stars, actions
│         │     "TIẾP TỤC" / "CHƠI LẠI"
└────┬────┘
     │
     ▼
    MENU
```

Transition points are guarded by a **confirmation modal** when switching phases.

---

## 8. UI Conventions

- **Shadows** on all interactive elements (buttons, tiles, panels).
- **Gradients** (vertical) on buttons, panels, progress bars.
- **Glow circles** on hover states, highlights, and decorative elements.
- All text has a **drop shadow** for readability against dark backgrounds.
- Vietnamese text throughout (Tahoma font for full diacritic support).
- 60 FPS target with `pygame.time.Clock.tick()`.
