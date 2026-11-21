# Retro nhóm

## Phase 2 (nhanh)
- Điều tốt: Đã merge thành công 2 nhánh độc lập của TV1 và TV2 vào main; test suite đạt 48 bài kiểm thử xanh 100%, bảo đảm tính tất định SHA256 trùng khớp.
- Điều tệ: Khi merge nhánh xuất hiện xung đột ở 4 file cấu hình/tài liệu chung (TEAM.md, game.contract.json, clarify.md, ai-usage-log.md) do chỉnh sửa song song.
- 1 hành động cho Phase 3: Duy trì ranh giới file rõ ràng, thống nhất người chủ trì chỉnh sửa tài liệu chung để tránh xung đột khi tích hợp.

## Phase 4 (cuối)
- Rà lại hành động Phase 2: Đã làm triệt để; nhóm phân chia ranh giới rõ ràng nên Phase 3 và Phase 4 tích hợp trơn tru, không còn xung đột tài liệu.
- Điều tốt: Cả hai thành viên phối hợp nhịp nhàng theo mô hình Contract-First; toàn bộ 51 bài test đều xanh 100%; tốc độ headless vượt trội > 16.000 ticks/s; đạt đúng tiến độ 4 phase theo lịch 3 giờ.
- Điều tệ: Khâu setup môi trường ban đầu trên Windows gặp trục trặc về alias python của Microsoft Store và quyền hạn sandbox.
- Số liệu:
  - Số commit: `truien` (11 commit), `minh17023` (10 commit) — cả 2 đều vượt xa yêu cầu ≥ 3 commit.
  - Cách đọc code của nhau: TV1 review module `quan` qua pull request, TV2 review module `gather`.
  - Token ước tính: TV1 dùng ~37k tokens (Gemini 3.8 Flash), TV2 dùng Codex.
- Một lần AI sai và cách nhóm phát hiện: Khi viết script so sánh file determinism trên Windows PowerShell, AI đã dùng lệnh `fc /b`, nhưng trong PowerShell `fc` bị map sang alias `Format-Custom` gây lỗi positional parameter. Nhóm đã phát hiện qua log lỗi và đổi sang dùng `Get-FileHash` SHA256 chính xác tuyệt đối.
- Nếu làm lại, đổi gì: Thống nhất cấu hình môi trường chạy Python và PowerShell script trước giờ kickoff để tránh mất thời gian ở 15 phút đầu.
