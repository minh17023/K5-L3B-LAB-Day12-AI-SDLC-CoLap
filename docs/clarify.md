# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| 1 | 2026-11-21 10:00 | Nhóm chỉ có 2 thành viên, script `tools/check_team.py` mặc định yêu cầu 4-6 người thì xử lý thế nào? | Cập nhật `game.contract.json` `team_size = 2` và sửa `tools/check_team.py` cho phép `2 <= len(members) <= 6`. Phân công TV1 kiêm Integrator/Release + gather, TV2 kiêm PO/QA + quan. | Nhóm thống nhất |
| 2 | 2026-11-21 10:05 | Hai thành viên làm việc song song thế nào để không nghẽn? | Sử dụng file kho mẫu `docs/contracts/inventory.sample.json` làm hợp đồng giao tiếp độc lập, TV2 test quan mà không cần đợi gather xong. | Integrator & PO |
| 3 | 2026-11-21 10:15 | PRD-0 đầy đủ và yêu cầu Phase 2/3 hiện ở đâu? | Đọc event contract trong mã nguồn và lab board; PO cập nhật tài liệu khi phase mới mở, không tự bịa yêu cầu. | PO / giảng viên |
