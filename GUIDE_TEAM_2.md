# HƯỚNG DẪN PHÂN CÔNG NHIỆM VỤ TEAM 2 THÀNH VIÊN
## Đồ án: Quán Ăn Chợ Nổi (Day 12 — AI SDLC)

> **Bối cảnh:** Dự án diễn ra trong **3 giờ** qua **4 phase** liên tục. Đề bài gốc được thiết kế cho nhóm 4–6 người với 4 module (`sim/gather`, `sim/quan`, `client/ui`, `qa`) và 4 vai quy trình (PO, Integrator, QA Lead, Scrum/Release).  
> Với **team 2 người**, mỗi thành viên sẽ **đảm nhận 2 mảng kỹ thuật + 2 vai quy trình** (kiêm nhiệm song hành) để đảm bảo không bị quá tải, không đụng độ code và đạt trọn vẹn 100 điểm.

---

## 1. BẢNG TỔNG QUAN PHÂN VAI & TRÁCH NHIỆM

| Tiêu chí | THÀNH VIÊN 1 (Dev A - Core Sim & System) | THÀNH VIÊN 2 (Dev B - Gameplay & Quality) |
|---|---|---|
| **Module Code chính** | **`sim/gather`** (Thu hoạch trên sông) + Headless Contract | **`sim/quan`** (Vận hành quán ăn) + **`client/ui`** (Giao diện / Live) |
| **Vai trò quy trình** | **Integrator** & **Release Lead** (Git Master) | **Product Owner (PO)** & **QA Lead** |
| **Dự phòng (Backup)** | Sẵn sàng gánh phụ phần `sim/quan` nếu trễ | Sẵn sàng gánh phụ phần `sim/gather` nếu trễ |
| **Các file code sở hữu** | `chonoi/sim/gather.py`<br>`chonoi/inventory.py`<br>`chonoi/headless.py`<br>`game.contract.json` (tuning gather) | `chonoi/sim/quan.py`<br>`chonoi/web/index.html`<br>`chonoi/live.py`<br>`game.contract.json` (tuning quan/menu) |
| **Tài liệu phụ trách** | `AGENTS.md`<br>`.agents/skills/*`<br>`docs/contracts/*`<br>`TEAM.md` (đồng bộ config)<br>`docs/members/<handle-tv1>.md` | `docs/clarify.md`<br>`docs/plan/phase-*.md`<br>`docs/verification/phase-*.md`<br>`docs/proof/*`<br>`docs/standup.md` & `docs/retro.md`<br>`docs/members/<handle-tv2>.md` |
| **Cam kết Git** | Tối thiểu **≥ 3 commit có nội dung thật** từ tài khoản GitHub của mình | Tối thiểu **≥ 3 commit có nội dung thật** từ tài khoản GitHub của mình |

---

## 2. NHIỆM VỤ CHI TIẾT CỦA TỪNG THÀNH VIÊN

### 👤 THÀNH VIÊN 1: DEV A (Hệ Thống, Thu Thập & Tích Hợp)

#### A. Nhiệm vụ Kỹ thuật (Code & Sim)
1. **Lõi `sim/gather.py` (Lát 1 - Di chuyển & Sinh tồn):**
   - Lập trình cơ chế bơi ngang (`x`), lặn sâu (`d`).
   - Xử lý oxy: nạp lại đầy khi nổi mặt nước (`d <= surface_depth`), tụt dần khi lặn sâu.
   - Xử lý ngạt thở (`oxygen_empty`), trừ máu (`hp`), ngất đưa về bến xuất phát.
   - Cơ chế giỏ đồ (`hold`): ngăn xếp LIFO, kiểm tra sức chứa tối đa (`hold_capacity`).
2. **Lõi `sim/gather.py` (Lát 2 - Thu hoạch & Kho):**
   - Hái bông điên điển, bông súng (`interact`) trong bán kính quy định khi nổi mặt nước. Thời gian mọc lại (`regrow_s`).
   - Bắt cá linh, cá lóc (`catch` bằng phím Space) khi ở dưới nước, cooldown bắt cá.
   - Cập bến: khi chạm vùng cầu tàu (`dock_pos`, `dock_radius`), kết thúc ca thu hoạch, chuyển đồ từ giỏ vào file kho (`inventory.json`).
3. **Headless & Tính tất định (Determinism):**
   - Đảm bảo đầu ra JSONL chạy với cùng một seed luôn giống hệt nhau từng byte (không dùng thư viện ngoài, không dùng clock hệ thống, chỉ dùng `Streams`).

#### B. Trách nhiệm Quy trình & Quản trị (Integrator & Release)
1. **Git & Release Management:**
   - Tạo và duy trì cấu trúc nhánh (ví dụ: `main`, `feat/gather`, `feat/quan`).
   - Review và merge code từ Thành viên 2 vào `main`.
   - Thực hiện gắn tag chuẩn giờ: `phase-1`, `phase-2`, `phase-3`, `phase-4` và Release `v1.0.0`.
2. **Quản trị AI Harness:**
   - Cập nhật file `AGENTS.md` qua từng phase (ghi rõ lệnh chạy, quy tắc context cho AI).
   - Xây dựng tối thiểu **2 custom skills/hooks** trong `.agents/skills/` (yêu cầu bắt buộc của lab).
3. **Quản lý Hợp đồng (Contracts):**
   - Quản lý file `game.contract.json` (giữ đúng `team_size = 2`, đường dẫn lệnh).
   - Quản lý schema kho `docs/contracts/inventory.sample.json`.

---

### 👤 THÀNH VIÊN 2: DEV B (Nghiệp Vụ Quán, Giao Diện & QA)

#### A. Nhiệm vụ Kỹ thuật (Code & UI)
1. **Lõi `sim/quan.py` (Lát 3 - Khách hàng & Điều phối):**
   - Khách vào quán theo chu kỳ (`customer_interval_s`) tại bàn ăn (`tables`).
   - Khách chọn món có thể nấu dựa trên nguyên liệu tồn kho.
   - Cơ chế giữ chỗ nguyên liệu (`reserved`): trừ tạm kho để khách sau không chọn trùng khi hết hàng.
   - Quản lý thanh kiên nhẫn (`patience_s`), khách bỏ về khi hết kiên nhẫn -> trừ uy tín (`reputation`).
2. **Lõi `sim/quan.py` (Lát 4 - Bếp & Phục vụ):**
   - Tương tác với bếp (`stoves`): bắt đầu nấu (`cook_started`), thời gian nấu chín (`cook_s`), món chín (`dish_ready`).
   - Bưng món chín đến bàn khách đúng yêu cầu (`served`).
   - Tính tiền, cộng tiền tip nếu phục vụ nhanh (`tip_rate`), cập nhật điểm uy tín.
3. **Giao diện & Chơi trực tiếp (`chonoi/web/` & `chonoi.live`):**
   - Kiểm tra hiển thị hình ảnh/HUD (thanh oxy, máu, tiền, uy tín, trạng thái bếp/bàn).
   - Đảm bảo phím bấm WASD, E, Space, R phản hồi mượt mà trên browser.

#### B. Trách nhiệm Quy trình & Chất lượng (PO & QA Lead)
1. **Product Owner (PO):**
   - Canh mốc giờ trên **Lab Board** (link Claude artifact) để lấy PRD/yêu cầu mới của từng phase.
   - Đặt câu hỏi làm rõ với Giảng viên/AI TA khi có điểm mơ hồ; ghi nhật ký vào `docs/clarify.md`.
   - Viết kế hoạch từng phase vào `docs/plan/phase-1.md` -> `phase-4.md`.
2. **QA Lead & Kiểm chứng:**
   - Chạy bộ test smoke: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`.
   - Chạy lệnh headless xuất file JSONL để nghiệm thu.
   - Lưu trữ log chạy/kết quả thực tế vào `docs/proof/phase-n/...`.
   - Điền ma trận truy vết Acceptance Criteria (AC) trong `docs/verification/phase-n.md`.
3. **Scrum & Phản tư:**
   - Ghi biên bản họp nhanh Standup giữa phase vào `docs/standup.md`.
   - Điều phối buổi Retro sau Phase 2 và Phase 4, điền vào `docs/retro.md`.

---

## 3. LỘ TRÌNH 3 GIỜ CHI TIẾT (TIMELINE THEO PHASE)

```
0:00 ──────────────── 1:00 ───────────── 1:55 ───────────── 2:30 ───────────── 3:00
      PHASE 1                 PHASE 2          PHASE 3          PHASE 4
 [Kickoff + P1 Core]     [Yêu cầu mới 1]   [Yêu cầu mới 2]   [Tích hợp & Release]
 Tag: phase-1            Tag: phase-2      Tag: phase-3      Tag: phase-4 + v1.0.0
```

### ⏱️ Giai đoạn Kickoff (15 phút đầu: 0:00 - 0:15)
- [ ] **Thành viên 1:**
  - Sửa `game.contract.json`: đổi `"team": "CoLap"`, `"team_size": 2`.
  - Cập nhật `tools/check_team.py` nếu cần (cho phép `2 <= len(members) <= 6` để CI pass).
  - Điền phần thỏa thuận làm việc vào `TEAM.md`.
- [ ] **Thành viên 2:**
  - Đọc kỹ PRD-0 của Phase 1.
  - Điền danh sách 2 thành viên vào bảng trong `TEAM.md` (khớp GitHub handle).
  - Khởi tạo file `docs/plan/phase-1.md`.
- [ ] **Cả 2:** Thống nhất kênh trao đổi, tạo nhánh làm việc riêng trên Git.

---

### ⏱️ PHASE 1 (0:15 - 1:00) — Mục tiêu: Core Sim chạy đúng Test Contract
*Hạn chót gắn tag `phase-1`: Trước 1:00*

- [ ] **Thành viên 1:**
  - Hoàn thành Lát 1 & Lát 2 trong `chonoi/sim/gather.py`.
  - Kiểm tra test headless: `python3 -m chonoi.headless --mode gather --seed 1 --ticks 600 --out out_gather.jsonl`.
  - Đảm bảo xuất file kho `inventory.json` đúng format khi kết thúc ca lặn.
- [ ] **Thành viên 2:**
  - Hoàn thành Lát 3 & Lát 4 trong `chonoi/sim/quan.py`.
  - Kiểm tra đọc file `inventory.json` vào quán và chu kỳ phục vụ khách.
  - Chạy test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`.
- [ ] **Hoàn tất Phase 1 (50-60 phút):**
  - Thành viên 2 lưu log test vào `docs/proof/phase-1/` và điền `docs/verification/phase-1.md`.
  - Cả 2 ghi nhật ký AI vào `docs/ai-usage-log.md`.
  - Thành viên 1 gộp nhánh vào `main`, test lại toàn bộ, chạy lệnh:
    ```bash
    git tag phase-1
    git push origin main --tags
    ```

---

### ⏱️ PHASE 2 (1:00 - 1:55) — Mục tiêu: Tiếp nhận yêu cầu mở rộng đợt 1
*Hạn chót gắn tag `phase-2`: Trước 1:55*

- [ ] **Thành viên 2:**
  - Lên Lab Board lấy yêu cầu Phase 2 (thường thêm loại cá, bẫy dòng chảy, hoặc món mới/khách VIP).
  - Nếu có chỗ mơ hồ, hỏi ngay và ghi vào `docs/clarify.md`.
  - Viết `docs/plan/phase-2.md`.
- [ ] **Thành viên 1:**
  - Cập nhật số liệu mới vào `game.contract.json` (không hard-code trong file python).
  - Cập nhật logic thu hoạch / né chướng ngại vật trong `sim/gather.py`.
  - Cập nhật `AGENTS.md` (phản ánh luật mới cho AI agent biết).
- [ ] **Thành viên 2:**
  - Cập nhật logic chế biến / phục vụ tương ứng trong `sim/quan.py`.
  - Kiểm thử lại cả 2 chế độ `gather` và `quan`.
- [ ] **Hoàn tất Phase 2 (1:45 - 1:55):**
  - Chạy toàn bộ test suite.
  - Họp Retro nhanh 5 phút, Thành viên 2 điền mục `## Phase 2 (nhanh)` trong `docs/retro.md`.
  - Lưu proof vào `docs/proof/phase-2/` và điền `docs/verification/phase-2.md`.
  - Thành viên 1 gắn tag:
    ```bash
    git tag phase-2
    git push origin main --tags
    ```

---

### ⏱️ PHASE 3 (1:55 - 2:30) — Mục tiêu: Biến động thị trường / Cơ chế mới đợt 2
*Hạn chót gắn tag `phase-3`: Trước 2:30*

- [ ] **Thành viên 2:** Lấy PRD Phase 3 trên Lab Board, phân tích tác động, cập nhật `docs/plan/phase-3.md`.
- [ ] **Thành viên 1 & 2:** Chia đôi tính năng theo đúng ranh giới `sim/gather` vs `sim/quan`.
- [ ] **Tạo Agent Skill (Bắt buộc):** Thành viên 1 viết ít nhất 2 skill trong `.agents/skills/` (ví dụ: skill tự động chạy kiểm thử determinism hoặc skill validate inventory schema).
- [ ] **Hoàn tất Phase 3:**
  - Kiểm tra tính hồi quy (Regression Test): Phase 3 chạy được nhưng KHÔNG làm gãy test Phase 1, Phase 2.
  - Điền `docs/verification/phase-3.md` + proof.
  - Gắn tag:
    ```bash
    git tag phase-3
    git push origin main --tags
    ```

---

### ⏱️ PHASE 4 (2:30 - 3:00) — Mục tiêu: Tích hợp hoàn thiện, Polish & Đóng gói Release
*Hạn chót gắn tag `phase-4` và Release `v1.0.0`: Trước 3:00*

- [ ] **Thành viên 1 (Integrator & Release):**
  - Rà soát toàn bộ source code, loại bỏ code thừa, đảm bảo clean code.
  - Kiểm tra `game.contract.json` (mọi tham số đều chuẩn xác).
  - Đảm bảo headless chạy mượt với cả 2 mode `gather` và `quan`.
  - Tạo tag `phase-4` và tạo GitHub Release chính thức `v1.0.0`.
- [ ] **Thành viên 2 (QA & PO):**
  - Chạy full test smoke + headless kiểm chứng cuối cùng, chụp ảnh/copy log vào `docs/proof/phase-4/`.
  - Hoàn tất bảng `docs/verification/phase-4.md`.
  - Điều phối làm Retro cuối cùng, điền mục `## Phase 4 (cuối)` trong `docs/retro.md`.
- [ ] **Cả hai thành viên (Bắt buộc - tính điểm cá nhân):**
  - Mỗi người tạo file phản tư cá nhân:
    - Thành viên 1 tạo: `docs/members/<handle-tv1>.md` (dựa trên `TEMPLATE.md`).
    - Thành viên 2 tạo: `docs/members/<handle-tv2>.md` (dựa trên `TEMPLATE.md`).
  - Cập nhật đầy đủ `docs/ai-usage-log.md` (ghi nhận số token, prompt, tình huống AI hallucination).
  - Đảm bảo mỗi người đã có **≥ 3 commit có nội dung** trên GitHub.

---

## 4. QUY TẮC PHỐI HỢP GIT & TRÁNH CONFLICT (CHO 2 NGƯỜI)

1. **Ranh giới file rõ ràng:**
   - TV1 chỉ sửa: `chonoi/sim/gather.py`, `chonoi/inventory.py`, `AGENTS.md`, `.agents/skills/`.
   - TV2 chỉ sửa: `chonoi/sim/quan.py`, `chonoi/web/*`, `chonoi/live.py`, `docs/*`.
   - Khi cần sửa `game.contract.json`: TV nào sửa phải báo trước cho người kia, hoặc tạo PR riêng.
2. **Quy tắc commit:**
   - Commit nhỏ, ghi rõ thông điệp theo cú pháp: `feat(gather): ...`, `fix(quan): ...`, `docs(verification): ...`.
   - Nếu làm cặp trên cùng 1 máy, phải thêm dòng cuối trong commit message:  
     `Co-authored-by: Tên <email@users.noreply.github.com>`
3. **Quy tắc xử lý sự cố trễ giờ:**
   - Nếu một người bị tắc (stuck) quá **10 phút**: Lập tức báo người kia vào hỗ trợ/pair programming hoặc chia nhỏ task để hạ độ phức tạp (chấp nhận làm bản tối giản để kịp nộp tag đúng mốc).

---

## 5. CHECKLIST TRƯỚC KHI GẮN TAG Ở MỖI PHASE

- [ ] Test tự động xanh: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v` (0 failures).
- [ ] Chạy thử headless không lỗi: `python3 -m chonoi.headless --mode gather --seed 1 --ticks 60 --out test.jsonl`.
- [ ] Đã có file minh chứng trong `docs/proof/phase-n/`.
- [ ] Đã cập nhật ma trận nghiệm thu `docs/verification/phase-n.md`.
- [ ] Cả 2 thành viên đều đã commit và push lên remote repo.
- [ ] Lệnh gắn tag: `git tag phase-X && git push origin --tags`.
