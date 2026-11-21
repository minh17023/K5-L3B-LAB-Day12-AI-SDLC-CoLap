---
name: sim_benchmark
description: "Đo lường và đánh giá hiệu năng (tick rate, thời gian thực thi) của mô phỏng Chợ Nổi nhằm đảm bảo độ mượt 60 FPS."
---

# Skill: Simulation Benchmark & Performance

Skill này hỗ trợ đo đạc hiệu năng mô phỏng để đảm bảo game chạy ổn định ở tần số 60 Hz mà không gây giật lag.

## Khi nào dùng
- Khi kiểm tra tính tối ưu của vòng lặp `step()` trong `GatherSim` và `QuanSim`.
- Khi chuẩn bị bàn giao phiên bản release để đảm bảo không bị nghẽn CPU.

## Lệnh đo benchmark
```bash
python -c "import time, sys; from chonoi.headless import main; t0=time.time(); sys.argv=['headless','--mode','gather','--seed','1','--ticks','600','--out','bench.jsonl']; main(); t1=time.time(); print(f'600 ticks completed in {t1-t0:.3f}s (Rate: {600/(t1-t0):.1f} ticks/s)')"
```
Tiêu chuẩn đạt: Thời gian chạy 600 ticks dưới 1.5 giây (> 400 ticks/giây).
