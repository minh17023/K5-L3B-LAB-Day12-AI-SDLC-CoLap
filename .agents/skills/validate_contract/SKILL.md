---
name: validate_contract
description: "Kiểm tra tính hợp lệ của game.contract.json và schema kho nguyên liệu inventory.json."
---

# Skill: Validate Contract & Inventory Schema

Skill này hướng dẫn kiểm tra và đảm bảo không phá vỡ hợp đồng tích hợp giữa các module `gather` và `quan`.

## Khi nào dùng
- Khi điều chỉnh tham số cấu hình game trong `game.contract.json`.
- Khi kiểm tra tính tương thích giữa file kho được xuất từ `gather` và file kho được nạp vào `quan`.

## Quy tắc hợp đồng
1. **Không hard-code số liệu:** Mọi hằng số thời gian, tốc độ, dung lượng giỏ phải đọc từ `game.contract.json`.
2. **Schema kho:** Phải đúng format JSON:
   ```json
   {
     "items": {
       "ca_loc": 1,
       "bong_sung": 2
     }
   }
   ```
3. Số lượng nguyên liệu không được âm, tên mặt hàng phải thuộc danh mục hợp lệ (`ca_loc`, `ca_linh`, `bong_sung`, `bong_dien_dien`).

## Lệnh kiểm tra nhanh
```bash
python -c "import json, chonoi.contract; chonoi.contract.load_contract(); print('Contract valid!')"
```
