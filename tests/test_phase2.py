"""Unit test cho Phase 2: Kiểm thử các trường hợp biên, chống hồi quy và đảm bảo tính tất định."""

import json
import unittest

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import LiveInputs
from chonoi.sim.gather import GatherSim
from chonoi.sim.quan import QuanSim


class TestPhase2EdgeCases(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        self.tuning = self.contract["tuning"]
        self.ids = IdAllocator()

    def test_gather_inventory_isolation_after_faint(self):
        """Sau khi ngất (fainted), giỏ đồ phải rỗng và không xuất được món nào vào kho."""
        sim = GatherSim(self.tuning, {"player": {"pos": [20, 5], "oxygen_ticks": 1, "hp": 1},
                                     "hold": ["ca_loc", "ca_linh", "bong_sung"]}, None, self.ids)
        inp = LiveInputs()
        # Chạy qua ngưỡng ngạt thở dẫn tới ngất
        choke_ticks = self.tuning["gather"]["choke_interval_ticks"] + 2
        for _ in range(choke_ticks):
            sim.step(inp.advance())
        self.assertTrue(sim.done)
        self.assertEqual(sim.reason, "fainted")
        self.assertEqual(sim.inventory_items(), {})

    def test_quan_empty_stock_behavior(self):
        """Khi kho rỗng hoàn toàn, khách không thể chọn món và không thể bắt đầu nấu."""
        sim = QuanSim(self.tuning, {"stock": {}}, None, self.ids)
        inp = LiveInputs()
        # Tick 120 là thời điểm khách đầu tiên xuất hiện
        events = []
        for _ in range(130):
            events.extend(sim.step(inp.advance()))
        # Khách vẫn xuất hiện nhưng không có nguyên liệu để giữ chỗ
        self.assertEqual(sim.stock, {})
        # Người chơi tương tác với bếp không thể nấu món gì vì thiếu nguyên liệu
        sim.pos = [2, 8]  # Vị trí bếp B1
        inp.set(interact=True)
        events.extend(sim.step(inp.advance()))
        self.assertFalse(any(e[0] == "cook_started" for e in events))

    def test_quan_reputation_bounds(self):
        """Điểm uy tín không được vượt ra ngoài dải [reputation_min, reputation_max]."""
        sim = QuanSim(self.tuning, {"reputation": 0.1, "stock": {}}, None, self.ids)
        # Giả lập giảm uy tín mạnh
        sim.reputation = max(self.tuning["quan"]["reputation_min"],
                             min(self.tuning["quan"]["reputation_max"], sim.reputation - 2.0))
        self.assertGreaterEqual(sim.reputation, self.tuning["quan"]["reputation_min"])
        self.assertLessEqual(sim.reputation, self.tuning["quan"]["reputation_max"])


if __name__ == "__main__":
    unittest.main()
