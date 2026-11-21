import unittest
from copy import deepcopy

from chonoi.contract import load_contract
from chonoi.inputs import InputPlayer
from chonoi.runner import Session


class QuanLifecycle(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]

    def test_scenario_customer_reserves_recipe_from_stock(self):
        scenario = {
            "stock": {"ca_loc": 1},
            "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui"}],
        }
        session = Session("quan", self.tuning, scenario, 1)
        snap = session.snapshot()
        self.assertEqual(snap["stock"], {})
        self.assertEqual(snap["customers"][0]["reserved"], {"ca_loc": 1})

    def test_customer_leaves_when_patience_expires(self):
        scenario = {
            "stock": {"ca_loc": 1},
            "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                            "patience_ticks_left": 1}],
        }
        session = Session("quan", self.tuning, scenario, 1)
        events = session.step(InputPlayer([]).advance(0))
        self.assertEqual([e["name"] for e in events], ["customer_left"])
        self.assertEqual(session.sim.reputation, self.tuning["quan"]["reputation_initial"] +
                         self.tuning["quan"]["left_reputation_delta"])

    def test_interact_stove_starts_cooking(self):
        scenario = {
            "stock": {"ca_loc": 1},
            "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui"}],
            "player": {"pos": [2, 8]},
        }
        session = Session("quan", self.tuning, scenario, 1)
        inp = InputPlayer([{"tick": 0, "interact": True}]).advance(0)
        events = session.step(inp)
        self.assertEqual([e["name"] for e in events], ["cook_started"])
        self.assertEqual(session.snapshot()["stoves"][0]["state"], "cooking")

    def test_customer_arrival_and_no_dish_are_deterministic(self):
        session = Session("quan", self.tuning, {}, 7)
        events = []
        for _ in range(self.tuning["quan"]["first_customer_tick"]):
            events.extend(session.step(InputPlayer([]).advance(0)))
        names = [event["name"] for event in events]
        self.assertEqual(names, ["customer_arrived", "no_dish"])
        self.assertEqual(session.snapshot()["customers"], [])

    def test_dish_is_picked_served_and_paid(self):
        tuning = deepcopy(self.tuning)
        tuning["menu"]["ca_loc_nuong_trui"]["cook_s"] = 0.02
        tuning["quan"]["eat_s"] = 0.02
        scenario = {
            "stock": {"ca_loc": 1},
            "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui"}],
            "tables": [{"id": "T1", "pos": [2, 8]}],
            "player": {"pos": [2, 8]},
        }
        session = Session("quan", tuning, scenario, 1)
        session.step(InputPlayer([{"tick": 0, "interact": True}]).advance(0))
        session.step(InputPlayer([]).advance(1))
        picked = session.step(InputPlayer([{"tick": 0, "interact": True}]).advance(0))
        served = session.step(InputPlayer([{"tick": 0, "interact": True}]).advance(0))
        paid = session.step(InputPlayer([]).advance(0))
        self.assertEqual([event["name"] for event in picked], ["dish_picked"])
        self.assertEqual([event["name"] for event in served], ["served"])
        self.assertEqual([event["name"] for event in paid], ["paid"])
        self.assertEqual(session.sim.money, 72)


if __name__ == "__main__":
    unittest.main()
