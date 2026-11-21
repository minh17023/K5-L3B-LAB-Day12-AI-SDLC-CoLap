# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Khách vào theo lịch, chọn món đủ nguyên liệu | `test_customer_arrival_and_no_dish_are_deterministic` và headless tick 120 | [`customer-arrival.txt`](../proof/phase-1/customer-arrival.txt) | Đạt |
| Giữ chỗ làm giảm kho khả dụng | `test_scenario_customer_reserves_recipe_from_stock` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Hết kiên nhẫn rời quán và trừ uy tín | `test_customer_leaves_when_patience_expires` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Nấu, cầm món, phục vụ và thanh toán | `test_dish_is_picked_served_and_paid` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Headless không làm hỏng contract P1 | Full suite 37 test | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Cùng seed cho output byte giống nhau | Chạy hai lần headless cùng scenario | [`determinism.txt`](../proof/phase-1/determinism.txt) | Đạt |
| Hai mode headless chạy được | `chonoi.headless` với `quan` 600 tick và `gather` 60 tick | [`headless-modes.txt`](../proof/phase-1/headless-modes.txt) | Đạt |
| Live phục vụ snapshot và canvas | Khởi động `LiveServer` ở mode `quan`, đọc `/state` và `/` | [`live-quan.txt`](../proof/phase-1/live-quan.txt) | Đạt |

## Đánh giá ngắn

- Yêu cầu Phase 1 của thành viên 2 đã có implementation và test hồi quy.
- Phase sau cần lấy PRD mới từ Lab Board trước khi mở rộng menu hoặc khách.
