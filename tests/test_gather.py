"""Unit test cho GatherSim (Lát 1 và Lát 2) do Thành viên 1 viết."""

import unittest

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import LiveInputs
from chonoi.sim.gather import GatherSim


class TestGatherSim(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]
        self.ids = IdAllocator()

    def _sim(self, scenario=None):
        return GatherSim(self.tuning, scenario or {}, None, self.ids)

    def test_dive_and_surface_events(self):
        # Xuất phát ở [2, 0] (mặt nước)
        sim = self._sim()
        inp = LiveInputs()
        # Bơi xuống dưới
        inp.set(move=[0, 1])
        all_events = []
        for _ in range(30):
            all_events.extend(sim.step(inp.advance()))
        self.assertTrue(any(ev[0] == "dive" for ev in all_events))
        self.assertFalse(sim._at_surface())

        # Bơi ngược lên mặt nước
        inp.set(move=[0, -1])
        all_events = []
        for _ in range(60):
            all_events.extend(sim.step(inp.advance()))
        self.assertTrue(any(ev[0] == "surface" for ev in all_events))
        self.assertTrue(sim._at_surface())

    def test_oxygen_depletion_and_recovery(self):
        # Bắt đầu ở độ sâu 5m
        sim = self._sim({"player": {"pos": [20, 5], "oxygen_ticks": 100}})
        inp = LiveInputs()
        sim.step(inp.advance())
        self.assertEqual(sim.oxygen_ticks, 99)

        # Đưa lên mặt nước và kiểm tra hồi oxy
        sim.pos = [20, 0]
        refill = self.tuning["gather"]["oxygen_refill_per_tick"]
        sim.step(inp.advance())
        self.assertEqual(sim.oxygen_ticks, min(sim.oxygen_max, 99 + refill))

    def test_choke_and_faint(self):
        # Oxy về 0 và dưới nước
        choke_ticks = self.tuning["gather"]["choke_interval_ticks"]
        sim = self._sim({"player": {"pos": [20, 5], "oxygen_ticks": 1, "hp": 1}, "hold": ["ca_loc"]})
        inp = LiveInputs()
        ev1 = sim.step(inp.advance())
        self.assertEqual(sim.oxygen_ticks, 0)
        self.assertTrue(any(e[0] == "oxygen_empty" for e in ev1))

        # Đếm ngạt tới mức choke
        evs = []
        for _ in range(choke_ticks):
            evs.extend(sim.step(inp.advance()))
        self.assertTrue(any(e[0] == "choke" for e in evs))
        self.assertTrue(any(e[0] == "faint" for e in evs))
        self.assertTrue(sim.done)
        self.assertEqual(sim.reason, "fainted")
        self.assertEqual(sim.hold, [])
        self.assertEqual(sim.inventory_items(), {})

    def test_gather_flower_and_regrow(self):
        # Nút N1 ở [12, 0]
        sim = self._sim({"player": {"pos": [12, 0]}})
        inp = LiveInputs()
        inp.set(interact=True)
        evs = sim.step(inp.advance())
        self.assertTrue(any(e[0] == "gather" for e in evs))
        self.assertIn("bong_dien_dien", sim.hold)

        # Nút chuyển sang trạng thái chờ mọc lại
        n1 = next(n for n in sim.nodes if n["id"] == "N1")
        self.assertGreater(n1["regrow_ticks"], 0)

    def test_gather_hold_full(self):
        cap = self.tuning["gather"]["hold_capacity"]
        sim = self._sim({"player": {"pos": [12, 0]}, "hold": ["ca_loc"] * cap})
        inp = LiveInputs()
        inp.set(interact=True)
        evs = sim.step(inp.advance())
        self.assertTrue(any(e[0] == "hold_full" for e in evs))
        self.assertEqual(len(sim.hold), cap)

    def test_catch_fish_and_cooldown(self):
        # F1 ở [15, 5], kind ca_linh
        sim = self._sim({"player": {"pos": [15, 5]}})
        inp = LiveInputs()
        inp.set(catch=True)
        evs = sim.step(inp.advance())
        self.assertTrue(any(e[0] == "fish_caught" for e in evs))
        self.assertIn("ca_linh", sim.hold)
        self.assertFalse(any(f["id"] == "F1" for f in sim.fish))
        self.assertGreater(sim.catch_cd_ticks, 0)


if __name__ == "__main__":
    unittest.main()
