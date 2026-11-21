---
name: test_runner
description: "Chạy toàn bộ kiểm thử tự động (unit test, contract smoke test) và kiểm tra tính tất định determinism của mô phỏng Chợ Nổi."
---

# Skill: Test Runner & Verification

Skill này hướng dẫn agent hoặc thành viên nhóm cách chạy và xác minh chất lượng mã nguồn trước khi commit hoặc gắn tag.

## Khi nào dùng
- Trước khi merge nhánh tính năng vào `main`.
- Trước khi gắn tag từng phase (`phase-1` .. `phase-4`).
- Khi cần kiểm chứng tính tất định (cùng seed sinh ra cùng byte output).

## Lệnh chạy kiểm thử

### 1. Chạy toàn bộ Unit & Smoke Tests
```bash
python -m unittest discover -s tests -v
```
Yêu cầu: Toàn bộ test phải `OK` (0 failures, 0 errors).

### 2. Kiểm thử hợp lệ danh sách thành viên
```bash
python tools/check_team.py
```
Yêu cầu: Đầu ra `OK: 2 thành viên: minh17023, teammate-2`.

### 3. Kiểm thử tính tất định (Determinism Check)
Chạy 2 lần cùng seed `42` và so sánh mã hash hoặc so sánh nhị phân:
```bash
python -m chonoi.headless --mode gather --seed 42 --ticks 300 --out run1.jsonl
python -m chonoi.headless --mode gather --seed 42 --ticks 300 --out run2.jsonl
fc /b run1.jsonl run2.jsonl   # Trên Windows
# hoặc cmp run1.jsonl run2.jsonl trên Linux
```
Hai file phải trùng khớp từng byte.
