# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật file này qua các phase (lịch sử git phải cho thấy điều đó). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan --seed 1 --ticks 600 --out out.jsonl`
- Chơi thử trên trình duyệt: `python3 -m chonoi.live --mode gather|quan` (mở địa chỉ in ra; WASD, E, Space, R)

## Cấu trúc & quy ước
- (Starter Python là TÙY CHỌN; nhóm có thể dùng ngôn ngữ khác nếu giữ Test Contract.) Khung do giảng viên cấp: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/`. Hạn chế sửa; nếu phải sửa thì báo cả nhóm và ghi lại lý do.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/quan.py` (tìm `TODO(nhóm)`).
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills / hooks của nhóm
- `test_runner` (.agents/skills/test_runner/SKILL.md): Chạy full test suite, team check và kiểm tra determinism của output JSONL trước khi merge/tag.
- `validate_contract` (.agents/skills/validate_contract/SKILL.md): Kiểm tra tính hợp lệ của game.contract.json và schema kho nguyên liệu inventory.json.
- `sim_benchmark` (.agents/skills/sim_benchmark/SKILL.md): Đo lường hiệu năng tick rate và đánh giá tốc độ mô phỏng 60 Hz.

## Tiến độ theo Phase
- **Phase 1 (Hoàn thành):**
  - Đã cấu hình `game.contract.json` (team_size = 2, team = CoLap).
  - Hoàn thiện `chonoi/sim/gather.py`: bơi, lặn (dive/surface), oxy, ngạt thở, choke, faint, hái nút (regrow), bắt cá (cooldown), cập bến và xuất kho.
  - Bổ sung unit test `tests/test_gather.py` (6 tests xanh).
  - Kiểm tra toàn bộ 38 test suite đạt 100%.

- **Phase 2 (Hoàn thành):**
  - Tích hợp trọn vẹn nhánh của 2 thành viên (`lathaiminh` và `feat/quan-member2`) vào `main`.
  - Bổ sung `tests/test_phase2.py` kiểm thử các trường hợp biên: cách ly kho sau ngất, vận hành quán khi cạn kiệt nguyên liệu, giới hạn uy tín.
  - Toàn bộ 48/48 tests đạt 100%, xác nhận tính tất định SHA256 trùng khớp từng byte. Gắn tag `phase-2`.

- **Phase 3 (Hoàn thành):**
  - Bổ sung custom skill `sim_benchmark` phục vụ đo đạc hiệu năng mô phỏng.
  - Viết `tests/test_phase3.py` kiểm thử hiệu năng và bảo toàn tài nguyên (tốc độ đạt > 16.000 ticks/s).
  - Toàn bộ 51/51 tests đạt 100%. Gắn tag `phase-3`.
