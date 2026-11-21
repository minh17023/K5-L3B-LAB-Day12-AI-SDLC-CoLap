# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Lặn/nổi (dive/surface), oxy tụt khi lặn và hồi phục khi ở mặt nước | `test_dive_and_surface_events`, `test_oxygen_depletion_and_recovery` | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Hết oxy bị ngạt (choke), mất máu, hết máu ngất xỉu (faint) | `test_choke_and_faint` | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Hái hoa súng/điên điển, thời gian mọc lại, giỏ LIFO | `test_gather_flower_and_regrow`, `test_gather_hold_full` | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Bắt cá dưới nước, hồi chiêu catch_cd_ticks | `test_catch_fish_and_cooldown` | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Khách vào theo lịch, chọn món đủ nguyên liệu | `test_customer_arrival_and_no_dish_are_deterministic` và headless tick 120 | [`customer-arrival.txt`](../proof/phase-1/customer-arrival.txt) | Đạt |
| Giữ chỗ làm giảm kho khả dụng | `test_scenario_customer_reserves_recipe_from_stock` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Hết kiên nhẫn rời quán và trừ uy tín | `test_customer_leaves_when_patience_expires` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Nấu, cầm món, phục vụ và thanh toán | `test_dish_is_picked_served_and_paid` | [`quan-tests.txt`](../proof/phase-1/quan-tests.txt) | Đạt |
| Headless không làm hỏng contract P1 (Full suite 45 test) | `python -m unittest discover -s tests -v` | [`full-suite.txt`](../proof/phase-1/full-suite.txt) | Đạt |
| Cùng seed cho output byte giống nhau | Chạy hai lần headless cùng scenario | [`determinism.txt`](../proof/phase-1/determinism.txt) | Đạt |
| Hai mode headless chạy được | `chonoi.headless` với `quan` 600 tick và `gather` 600 tick | [`gather_seed1.jsonl`](../proof/phase-1/gather_seed1.jsonl) | Đạt |
| Live phục vụ snapshot và canvas | Khởi động `LiveServer` ở mode `quan` và `gather`, đọc `/state` | [`live-quan.txt`](../proof/phase-1/live-quan.txt) | Đạt |
| Danh sách team khớp contract (2 thành viên) | `python tools/check_team.py` | [`team-check.txt`](../proof/phase-1/team-check.txt) | Đạt |

## Đánh giá ngắn

- Cả hai module `gather` (Thành viên 1) và `quan` (Thành viên 2) đều hoàn thành trọn vẹn Lát 1-4, test xanh 45/45 tests.
- Hệ thống sẵn sàng cho Phase 2 khi Lab Board công bố yêu cầu mới.
