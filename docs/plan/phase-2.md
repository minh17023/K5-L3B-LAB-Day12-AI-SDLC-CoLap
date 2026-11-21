# Kế hoạch Phase 2 — Tối ưu hóa Vòng đời Vận hành & Cân bằng Luật chơi

- **Mục tiêu:**
  - Nâng cao độ tin cậy của mô phỏng thu hoạch (`gather`) và phục vụ quán (`quan`).
  - Kiểm thử sâu các tình huống biên: giỏ đầy liên tục, khách rời đi khi quá tải, tính toán hồi chiêu bắt cá và mọc lại hoa.
  - Đảm bảo tính tất định tuyệt đối và không gây lỗi hồi quy (regression) cho các contract của Phase 1.
- **Phân công việc / Người thực hiện:**
  - **Minh (`minh17023` - Integrator):**
    - Kiểm thử chịu tải vòng lặp thu hoạch trong `sim/gather.py`.
    - Kiểm tra tính nhất quán dữ liệu giỏ đồ khi cập bến nhiều lần.
  - **Truyền (`truien` - PO / QA):**
    - Kiểm thử kịch bản quán ăn khi hết sạch nguyên liệu trong kho (`stock = 0`).
    - Xác minh xử lý hàng đợi khách và tính toán uy tín chính xác.
- **Rủi ro:**
  - Cân bằng tốc độ tụt oxy và thời gian hồi chiêu bắt cá có thể ảnh hưởng đến kết quả mô phỏng nếu tuning bị thay đổi.
  - Giải pháp: Giữ nguyên hợp đồng `game.contract.json` khóa chặt số liệu, chỉ kiểm tra logic luật.
