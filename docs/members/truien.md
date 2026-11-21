# truien — phản tư cá nhân

- Tôi đã làm: Hoàn thiện vòng đời khách, giữ chỗ, bếp, phục vụ, tip và HUD trong Phase 1. Các commit chính là `103de11`, `6b0aaac`, `174cbff`, `ac04145`, `c0ceefd`, `49b909e`, `ee8e33a`.
- Tôi đã review: `runner.Session`, `scenario.py`, `tests/test_smoke_p1.py` và `chonoi/web/index.html` để giữ đúng contract.
- AI sai ở đâu và tôi phát hiện thế nào: Lệnh `python3` trên Windows trả mã 9009. Tôi kiểm tra executable thực tế và chạy lại bằng `py -3`, sau đó tạo shim local chỉ cho proof.
- Điều tôi học được: Event và snapshot cần deterministic như nhau để headless và live dùng chung luật mà không phải nhân đôi logic.
