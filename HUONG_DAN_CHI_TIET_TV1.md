# HƯỚNG DẪN TỪNG BƯỚC CHO THÀNH VIÊN 1 (MINH - @minh17023)
## Vai trò: Integrator, Release Lead & Developer `sim/gather`

---

## 📌 PHẦN 1: TỔNG KẾT NHỮNG GÌ ĐÃ ĐƯỢC LÀM CHO BẠN

Tôi đã hoàn thiện toàn bộ mã nguồn và cấu hình kỹ thuật cho Thành viên 1:

1. **Cấu hình hợp đồng và nhóm:**
   - [game.contract.json](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/game.contract.json): Đã đổi sang `"team": "CoLap"`, `"team_size": 2`.
   - [TEAM.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/TEAM.md): Đã cấu hình bảng 2 thành viên và thỏa thuận kickoff.
   - [tools/check_team.py](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/tools/check_team.py) & [tests/test_team_check.py](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/tests/test_team_check.py): Đã điều chỉnh cho phép nhóm 2 người để CI kiểm tra đạt 100%.

2. **Lõi mô phỏng Thu hoạch `sim/gather`:**
   - [chonoi/sim/gather.py](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/chonoi/sim/gather.py):
     - **Lát 1 (Sinh tồn & Di chuyển):** Nhận diện lặn (`dive`) / trồi lên mặt nước (`surface`). Cơ chế oxy tụt khi lặn, hồi phục nhanh khi ở mặt nước. Cơ chế ngạt thở (`oxygen_empty`), đếm ngạt (`choke`) trừ máu, máu về 0 ngất xỉu (`faint`) và mất sạch giỏ đồ.
     - **Lát 2 (Thu hoạch & Bắt cá):** Hái hoa súng / điên điển (`interact`) ở mặt nước trong tầm với, xử lý thời gian mọc lại (`regrow_ticks`). Bắt cá (`catch` - Space) ở dưới nước, tính toán bán kính, cộng cá vào giỏ LIFO, kích hoạt cooldown bắt cá. Cập bến tàu (`dock_pos`) kết thúc ca lặn và lưu trữ kho.

3. **Kiểm thử tự động (Unit Test):**
   - Đã viết thêm [tests/test_gather.py](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/tests/test_gather.py) với 6 bài test chuyên sâu cho Lát 1 & Lát 2.
   - Toàn bộ **38/38 tests** trong toàn bộ hệ thống đều **PASS 100% (OK)**.

4. **Harness AI & Minh chứng:**
   - Tạo 2 Agent skills theo đúng quy định:
     - [.agents/skills/test_runner/SKILL.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/.agents/skills/test_runner/SKILL.md)
     - [.agents/skills/validate_contract/SKILL.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/.agents/skills/validate_contract/SKILL.md)
   - Cập nhật [AGENTS.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/AGENTS.md).
   - Cập nhật [docs/clarify.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/docs/clarify.md) và [docs/ai-usage-log.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/docs/ai-usage-log.md).
   - Đã tạo file phản tư cá nhân: [docs/members/minh17023.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/docs/members/minh17023.md).
   - Đã xuất file mô phỏng nghiệm thu tại [docs/proof/phase-1/gather_seed1.jsonl](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/docs/proof/phase-1/gather_seed1.jsonl).

---

## 🚀 PHẦN 2: CÁC BƯỚC BẠN CẦN LÀM TIẾP THEO

### Bước 1: Kiểm tra chạy thử trên máy của bạn
Mở Terminal trong thư mục repo và chạy các lệnh sau:

1. **Kiểm tra danh sách thành viên:**
   ```bash
   python tools/check_team.py
   ```
   *(Kết quả mong đợi: `OK: 2 thành viên: minh17023, teammate-2`)*

2. **Chạy toàn bộ bài test:**
   ```bash
   python -m unittest discover -s tests -v
   ```
   *(Kết quả mong đợi: `Ran 38 tests ... OK`)*

3. **Chơi thử game trên trình duyệt (Chế độ Thu hoạch - Gather):**
   ```bash
   python -m chonoi.live --mode gather
   ```
   Mở trình duyệt vào `http://127.0.0.1:8000/`.
   - **WASD / Phím mũi tên:** Bơi lội (bơi xuống dưới mặt nước thấy thanh oxy tụt).
   - **E:** Hái hoa khi bơi gần cây ở mặt nước, hoặc cập bến tàu.
   - **Space:** Bắt cá khi bơi lại gần đàn cá.
   - **R:** Chơi lại.

---

### Bước 2: Commit mã nguồn lên Git (Đảm bảo chỉ tiêu ≥ 3 commits cá nhân)
Đề bài yêu cầu mỗi thành viên phải có ít nhất **3 commit có nội dung thật**. Bạn hãy chia các thay đổi vừa rồi thành 3 commit độc lập như sau:

#### Commit 1: Cấu hình nhóm và hợp đồng 2 người
```bash
git add game.contract.json TEAM.md tools/check_team.py tests/test_team_check.py docs/clarify.md
git commit -m "chore(config): update team_size to 2 for CoLap team and adjust validator"
```

#### Commit 2: Lập trình Lõi Thu hoạch sim/gather và Unit Tests
```bash
git add chonoi/sim/gather.py tests/test_gather.py
git commit -m "feat(gather): implement Lat 1 (oxygen, choke, faint) and Lat 2 (gather, catch, dock)"
```

#### Commit 3: Bổ sung Agent Skills, Harness AI và Minh chứng Phase 1
```bash
git add .agents/ AGENTS.md docs/ai-usage-log.md docs/members/minh17023.md docs/proof/ GUIDE_TEAM_2.md HUONG_DAN_CHI_TIET_TV1.md
git commit -m "docs(harness): add custom agent skills, AGENTS.md update and phase 1 proof"
```

#### Push lên GitHub:
```bash
git push origin main
```

---

### Bước 3: Phối hợp cùng Thành viên 2 nghiệm thu Phase 1
1. Nhắc **Thành viên 2** (phụ trách `sim/quan`):
   - Thành viên 2 hoàn thành nốt `chonoi/sim/quan.py`.
   - Thành viên 2 điền file ma trận nghiệm thu [docs/verification/phase-1.md](file:///c:/AITHUCCHIEN/K5-L3B-LAB-Day12-AI-SDLC-CoLap/docs/verification/phase-1.md).
2. Khi Thành viên 2 đẩy code lên, bạn pull về và chạy lại:
   ```bash
   git pull origin main
   python -m unittest discover -s tests -v
   ```
3. Khi tất cả đều xanh (trước mốc **1:00** của buổi lab), bạn thực hiện **gắn tag Phase 1**:
   ```bash
   git tag phase-1
   git push origin phase-1
   ```

---

## ⏩ PHẦN 3: KẾ HOẠCH CHO CÁC PHASE TIẾP THEO

- **Phase 2 (1:00 - 1:55):** Canh Lab Board khi mở yêu cầu mới. Bạn tiếp tục giữ `gather.py` (nếu có thêm loài cá mới, chướng ngại vật dòng xoáy nước) và cập nhật tham số vào `game.contract.json`. Đến hạn gắn `git tag phase-2`.
- **Phase 3 (1:55 - 2:30):** Xử lý thay đổi yêu cầu đợt 2, duy trì regression test không bị gãy. Đến hạn gắn `git tag phase-3`.
- **Phase 4 (2:30 - 3:00):** Tích hợp hoàn thiện toàn bộ game, cùng TV2 hoàn thành `docs/retro.md`, tạo tag `phase-4` và tạo GitHub Release `v1.0.0`.
