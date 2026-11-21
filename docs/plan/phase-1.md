# Kế hoạch Phase 1

## Mục tiêu

Hoàn thành vòng đời quán tối thiểu từ khách vào, giữ chỗ nguyên liệu, nấu món,
phục vụ đến thanh toán. Headless và live phải dùng cùng `QuanSim`.

## Việc / người / phụ thuộc

- Thành viên 2: triển khai `chonoi/sim/quan.py`, kiểm tra HUD trong `chonoi/web/index.html`, thêm test hồi quy và lưu proof.
- Thành viên 1: giữ contract, tích hợp nhánh và chạy lại smoke suite.
- Phụ thuộc: `game.contract.json`, `inventory.json` và API snapshot/event của `runner.Session`.

## Tiêu chí nghiệm thu

- Khách đến tại `first_customer_tick` và dùng món có đủ nguyên liệu.
- Kho giảm theo `reserved`, khách hết kiên nhẫn rời bàn và uy tín bị trừ.
- Bếp phát `cook_started`, `dish_ready`, `dish_picked`, sau đó bàn phát `served`, `paid`.
- Điểm, tiền, tip và uy tín được ghi trong snapshot/end row.

## Rủi ro

- PRD-0 đầy đủ không nằm trong repo. Các event dùng tên đã có trong khung và payload có khóa định danh rõ ràng.
- Máy Windows có alias `python3` trỏ Microsoft Store. Proof local dùng `py -3`, CI vẫn chạy lệnh trong repo.
