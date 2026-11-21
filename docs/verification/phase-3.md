# Ma trận truy vết Phase 3

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Hiệu năng mô phỏng GatherSim đạt chuẩn 60 Hz (> 400 ticks/s) | `test_gather_step_performance` | [`full-suite.txt`](../proof/phase-3/full-suite.txt) | Đạt |
| Hiệu năng mô phỏng QuanSim đạt chuẩn 60 Hz (> 400 ticks/s) | `test_quan_step_performance` | [`full-suite.txt`](../proof/phase-3/full-suite.txt) | Đạt |
| Bảo toàn tài nguyên kho khi khách rời quán | `test_quan_stock_conservation_on_customer_leave` | [`full-suite.txt`](../proof/phase-3/full-suite.txt) | Đạt |
| Đo lường benchmark thực tế headless | Script benchmark đo 600 ticks (> 10.000 ticks/s) | [`benchmark.txt`](../proof/phase-3/benchmark.txt) | Đạt |
| Toàn bộ 51 tests trong test suite đạt 100% | `python -m unittest discover -s tests -v` | [`full-suite.txt`](../proof/phase-3/full-suite.txt) | Đạt |

## Đánh giá ngắn

- Hệ thống đạt hiệu năng mô phỏng cực cao (> 16.000 ticks/s ở chế độ headless), hoàn toàn không có hiện tượng nghẽn hiệu năng.
- Tính toàn vẹn của dữ liệu kho và nguyên liệu được đảm bảo trong mọi tình huống khách đến và đi.
