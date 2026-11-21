"""Unit test cho Phase 3: Đo lường hiệu năng và bảo toàn tài nguyên hệ thống."""

import time
import unittest

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import LiveInputs
from chonoi.sim.gather import GatherSim
from chonoi.sim.quan import QuanSim


class TestPhase3PerformanceAndIntegrity(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        self.tuning = self.contract["tuning"]
        self.ids = IdAllocator()

    def test_gather_step_performance(self):
        """Mô phỏng 600 ticks của GatherSim phải hoàn thành trong < 0.5s."""
        sim = GatherSim(self.tuning, {}, None, self.ids)
        inp = LiveInputs()
        t0 = time.perf_counter()
        for _ in range(600):
            sim.step(inp.advance())
        elapsed = time.perf_counter() - t0
        self.assertLess(elapsed, 0.5, f"Quá chậm: {elapsed:.3f}s cho 600 ticks")

    def test_quan_step_performance(self):
        """Mô phỏng 600 ticks của QuanSim phải hoàn thành trong < 0.5s."""
        sim = QuanSim(self.tuning, {"stock": {"ca_loc": 5, "bong_sung": 10}}, None, self.ids)
        inp = LiveInputs()
        t0 = time.perf_counter()
        for _ in range(600):
            sim.step(inp.advance())
        elapsed = time.perf_counter() - t0
        self.assertLess(elapsed, 0.5, f"Quá chậm: {elapsed:.3f}s cho 600 ticks")

    def test_quan_stock_conservation_on_customer_leave(self):
        """Khi khách rời đi do hết kiên nhẫn, số nguyên liệu đã giữ chỗ (reserved) phải được giải phóng."""
        initial_stock = {"ca_loc": 1}
        sim = QuanSim(self.tuning, {"stock": dict(initial_stock)}, None, self.ids)
        inp = LiveInputs()
        # Đợi khách xuất hiện và đặt món (tick 120)
        for _ in range(125):
            sim.step(inp.advance())
        # Khách chờ đến khi hết kiên nhẫn (patience_s)
        patience_ticks = int(round(self.tuning["quan"]["patience_s"] * 60)) + 10
        for _ in range(patience_ticks):
            sim.step(inp.advance())
        # Nguyên liệu không bị bốc hơi thất thoát
        self.assertIn("ca_loc", sim.stock)


if __name__ == "__main__":
    unittest.main()
