# Kế hoạch Phase 3 — Đo lường Hiệu năng & Bảo toàn Trạng thái Mô phỏng

- **Mục tiêu:**
  - Đảm bảo hiệu năng vòng lặp mô phỏng đạt tiêu chuẩn chạy mượt mà ở tần số 60 Hz (> 400 ticks/s ở chế độ headless).
  - Kiểm tra tính bảo toàn tài nguyên (Resource Conservation) trong toàn bộ vòng đời của quán ăn: nguyên liệu giữ chỗ + nguyên liệu trên bếp + nguyên liệu tồn kho luôn bằng tổng nguyên liệu ban đầu.
  - Xây dựng Agent Skill `sim_benchmark` để tự động hóa đo lường.
- **Phân công việc / Người thực hiện:**
  - **Minh (`minh17023` - Integrator):**
    - Viết Agent Skill `sim_benchmark` trong `.agents/skills/`.
    - Viết test kiểm tra benchmark hiệu năng và tính bảo toàn tài nguyên trong `tests/test_phase3.py`.
  - **Truyền (`truien` - PO / QA):**
    - Chạy thử nghiệm kiểm chứng headless trên cả 2 chế độ `gather` và `quan`.
    - Cập nhật ma trận nghiệm thu Phase 3 và nhật ký kiểm thử.
- **Rủi ro:**
  - Quá tải I/O khi ghi snapshot JSONL liên tục trong quá trình benchmark.
  - Giải pháp: Chỉ ghi snapshot định kỳ hoặc đo tốc độ sim độc lập với I/O đĩa.
