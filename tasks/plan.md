# Implementation Plan: Quán ăn và QA của thành viên 2

## Overview

Hoàn thiện vòng đời khách, bếp và phục vụ trong `QuanSim`, bảo đảm headless và live dùng cùng trạng thái, sau đó ghi bằng chứng QA cho Phase 1.

## Architecture Decisions

- Kho được trừ ngay khi khách nhận món. Trường `reserved` của khách ghi lại phần nguyên liệu đang giữ.
- Bếp và bàn được chọn theo khoảng cách, rồi loại đối tượng và id để headless tất định.
- Một tick chỉ xử lý tối đa một thao tác tương tác. Di chuyển vẫn dùng `ramp_velocity` và số liệu từ contract.

## Task List

### Phase 1

- [ ] Sinh khách theo lịch, chọn món và giữ chỗ.
- [ ] Xử lý kiên nhẫn, khách rời quán và uy tín.
- [ ] Xử lý bếp, món chín, cầm món, phục vụ và thanh toán.
- [ ] Cập nhật snapshot/HUD và kiểm thử headless/live.

### Checkpoint

- [ ] Full test suite xanh.
- [ ] Hai lần chạy headless cùng seed cho kết quả byte giống nhau.
- [ ] Proof và ma trận truy vết Phase 1 đã ghi.

## Open Questions

- Chưa có PRD-0 đầy đủ trong repo, nên event payload dùng tên trường rõ nghĩa và tương thích với snapshot hiện tại.
