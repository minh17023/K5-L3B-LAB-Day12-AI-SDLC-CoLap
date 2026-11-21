# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | minh17023 | Antigravity (Gemini 3.8 Flash) | Thiết lập cấu hình team 2 người, lập trình Lát 1 + Lát 2 trong sim/gather.py | ~15k tokens | Ban đầu test_too_few_members cắt thiếu dòng header làm parse_team rỗng, cần rà soát lại đúng index |
| 1 | truien | Codex | Đọc GUIDE, triển khai `QuanSim`, thêm test và kiểm chứng headless/live | Không đo được trong repo | Lần đầu chạy lệnh `python3` trên Windows trúng alias Microsoft Store, sau đó xác minh bằng `py -3`. |
| 2 | minh17023 | Antigravity (Gemini 3.8 Flash) | Giải quyết merge conflict, viết test_phase2.py kiểm thử trường hợp biên, xác minh determinism | ~12k tokens | Lệnh fc trong PowerShell bị nhầm với Format-Custom, đã chuyển sang dùng Get-FileHash để kiểm tra mã SHA256 |
| 2 | truien | Codex | Rà soát các ca biên trong quán ăn, kiểm tra độ bền của vòng đời khách và uy tín | Không đo được | Không có |
| 3 | minh17023 | Antigravity (Gemini 3.8 Flash) | Thiết kế agent skill sim_benchmark, lập trình test hiệu năng và bảo toàn tài nguyên | ~10k tokens | Không có |
| 3 | truien | Codex | Kiểm chứng headless đường dài và xác nhận tốc độ tick rate | Không đo được | Không có |
| 4 | minh17023 | Antigravity (Gemini 3.8 Flash) | Đóng gói release v1.0.0, cập nhật README sáng tạo, CHANGELOG và phản tư Phase 4 | ~10k tokens | Không có |
| 4 | truien | Codex | Nghiệm thu toàn diện test suite, hoàn tất retro nhóm và phản tư cá nhân | Không đo được | Không có |
