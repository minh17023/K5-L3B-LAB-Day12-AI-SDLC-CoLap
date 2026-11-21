# Ma trận truy vết Phase 2

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Xử lý cô lập giỏ đồ sau ngất (faint reset giỏ) | `test_gather_inventory_isolation_after_faint` | [`full-suite.txt`](../proof/phase-2/full-suite.txt) | Đạt |
| Vận hành quán khi kho cạn kiệt (stock rỗng) | `test_quan_empty_stock_behavior` | [`full-suite.txt`](../proof/phase-2/full-suite.txt) | Đạt |
| Giới hạn điểm uy tín trong dải hợp lệ | `test_quan_reputation_bounds` | [`full-suite.txt`](../proof/phase-2/full-suite.txt) | Đạt |
| Tính tất định determinism trên seed 100 | Chạy 2 lần so sánh mã SHA256 trùng khớp | [`determinism.txt`](../proof/phase-2/determinism.txt) | Đạt |
| Toàn bộ 48 tests trong test suite đạt 100% | `python -m unittest discover -s tests -v` | [`full-suite.txt`](../proof/phase-2/full-suite.txt) | Đạt |

## Đánh giá ngắn

- Phase 2 đã kiểm thử thành công các tình huống biên khó của cả 2 module `gather` và `quan`.
- Không có bất kỳ lỗi hồi quy nào đối với các bài test của Phase 1.
