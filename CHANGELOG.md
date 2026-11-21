# Changelog

Tất cả các thay đổi đáng chú ý của dự án Quán Ăn Chợ Nổi (Team CoLap) được ghi nhận tại đây.

## [1.0.0] - Phase 4 (Bàn giao Release) - 2026-11-21
### Added
- Đóng gói toàn bộ sản phẩm hoàn chỉnh, sẵn sàng demo.
- Bổ sung tài liệu retro tổng kết 4 phase, phản tư cá nhân chi tiết của 2 thành viên.
- Cập nhật mục "Sáng tạo của nhóm CoLap" trong README.
- Hoàn thiện 51 bài test kiểm thử tự động đạt tỷ lệ pass 100%.

## [0.3.0] - Phase 3 (Hiệu năng & Benchmark) - 2026-11-21
### Added
- Agent Skill `sim_benchmark` phục vụ đo lường tốc độ mô phỏng.
- Bộ test hiệu năng `tests/test_phase3.py` xác nhận tốc độ > 16.000 ticks/giây.
- Kiểm tra tính bảo toàn tài nguyên kho và nguyên liệu giữ chỗ.

## [0.2.0] - Phase 2 (Tích hợp & Ca biên) - 2026-11-21
### Added
- Tích hợp 2 module `gather` và `quan` vào nhánh `main`.
- Bộ test ca biên `tests/test_phase2.py`: cô lập giỏ sau ngất, xử lý kho cạn kiệt, kiểm soát dải uy tín.
- Bằng chứng kiểm tra tính tất định determinism mã SHA256 trùng khớp từng byte.

## [0.1.0] - Phase 1 (Core Simulation) - 2026-11-21
### Added
- Lõi thu hoạch `sim/gather`: bơi, lặn, oxy, ngạt thở, choke, faint, hái hoa, bắt cá, cập bến và xuất kho.
- Lõi quán ăn `sim/quan`: đón khách, giữ chỗ nguyên liệu, nấu nướng, phục vụ, thanh toán và uy tín.
- Cấu hình nhóm 2 người trong `game.contract.json` và `TEAM.md`.
- 2 Agent skills đầu tiên: `test_runner` và `validate_contract`.
