"""Buổi tối — vận hành quán ăn.

Khách được xếp vào bàn theo lịch trong contract. Nguyên liệu được giữ chỗ
ngay khi khách chọn món, sau đó đi qua vòng đời bếp → cầm món → phục vụ →
thanh toán. Headless và cửa sổ live cùng gọi lớp mô phỏng này.
"""

import math

from ..errors import BadInput
from ..ids import sort_by_id
from .ramp import ramp_velocity

TICK = 60.0
AXES = ("x", "z")


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cli đã chặn trường hợp cả hai)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.hand = scenario.get("hand")
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * TICK)))
        self.reputation = scenario.get("reputation", t["reputation_initial"])
        self.stoves = [self._normalise_stove(s) for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.customers = []
        for customer in scenario.get("customers", []):
            self._restore_customer(customer)
        for e in self.customers:
            ids.reserve(e["id"])
        self._link_scenario_stoves()
        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def _normalise_stove(self, stove):
        result = dict(stove)
        result["state"] = result.get("state", "idle")
        result["dish"] = result.get("dish")
        result["customer_id"] = result.get("customer_id")
        result["cook_ticks_left"] = result.get("cook_ticks_left", 0)
        result["ready_ticks"] = result.get("ready_ticks", 0)
        return result

    def _restore_customer(self, raw):
        customer = dict(raw)
        dish_id = customer.get("dish_id", customer.get("dish"))
        if dish_id is None:
            dish_id = self._choose_dish()
        if dish_id is not None and dish_id not in self.menu:
            raise BadInput(f"customers.{customer.get('id')}: món không có trong menu: {dish_id}")
        state = customer.get("state", "waiting")
        if state in ("left", "paid"):
            return
        reserved = dict(customer.get("reserved") or {})
        if dish_id and not reserved:
            recipe = self.menu[dish_id]["recipe"]
            if self._can_reserve(recipe):
                reserved = self._reserve(recipe)
            else:
                state = "no_dish"
        max_patience = int(round(self.t["patience_s"] * TICK))
        customer.update({
            "dish_id": dish_id,
            "state": state,
            "reserved": reserved,
            "patience_max_ticks": customer.get("patience_max_ticks", max_patience),
            "patience_ticks_left": customer.get("patience_ticks_left", max_patience),
            "eat_ticks_left": customer.get("eat_ticks_left", int(round(self.t["eat_s"] * TICK))),
            "stove_id": customer.get("stove_id"),
        })
        self.customers.append(customer)

    def _link_scenario_stoves(self):
        known = {c["id"]: c for c in self.customers}
        for stove in self.stoves:
            customer = known.get(stove.get("customer_id"))
            if customer is not None:
                customer["stove_id"] = stove["id"]
                if stove["state"] == "cooking":
                    customer["state"] = "cooking"
                elif stove["state"] == "ready":
                    customer["state"] = "ready"

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        reserved = {}
        for customer in self.customers:
            for item, count in customer.get("reserved", {}).items():
                reserved[item] = reserved.get(item, 0) + count
        return {
            "player": {"pos": self.pos, "vel": self.vel},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "reserved": {k: reserved[k] for k in sorted(reserved) if reserved[k] > 0},
            "hand": self.hand,
            "carry_limit": self.t["carry_limit"],
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "customer_id", "cook_ticks_left", "ready_ticks")}
                       for s in sort_by_id(self.stoves)],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])}
                       for tb in sort_by_id(self.tables)],
            "customers": sort_by_id(self.customers),
        }

    def step(self, inp):
        events = []
        if self.done:
            return events

        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self._advance_cooking(events)
        self._move(inp)
        self._spawn_due(events)
        self._advance_customers(events)
        if not self.done and inp.pressed("interact"):
            self._interact(events)
        if self.time_left_ticks <= 0:
            self._finish("time", events)
        return events

    def _advance_cooking(self, events):
        for stove in sort_by_id(self.stoves):
            if stove["state"] != "cooking":
                continue
            stove["cook_ticks_left"] = max(0, stove["cook_ticks_left"] - 1)
            if stove["cook_ticks_left"] == 0:
                stove["state"] = "ready"
                stove["ready_ticks"] = 0
                events.append(("dish_ready", {
                    "stove_id": stove["id"],
                    "customer_id": stove.get("customer_id"),
                    "dish_id": stove.get("dish"),
                }))

    def _spawn_due(self, events):
        duration = int(round(self.t["duration_s"] * TICK))
        elapsed = duration - self.time_left_ticks
        first = self.t["first_customer_tick"]
        interval = max(1, int(round(self.t["customer_interval_s"] * TICK)))
        if elapsed < first or (elapsed - first) % interval:
            return
        occupied = {c["table_id"] for c in self.customers}
        table = next((tb for tb in sort_by_id(self.tables) if tb["id"] not in occupied), None)
        if table is None:
            return
        customer_id = self.ids.new("C")
        dish_id = self._choose_dish()
        events.append(("customer_arrived", {"customer_id": customer_id, "table_id": table["id"], "dish_id": dish_id}))
        if dish_id is None:
            events.append(("no_dish", {"customer_id": customer_id, "table_id": table["id"]}))
            return
        customer = {
            "id": customer_id,
            "table_id": table["id"],
            "dish_id": dish_id,
            "state": "waiting",
            "reserved": self._reserve(self.menu[dish_id]["recipe"]),
            "patience_max_ticks": int(round(self.t["patience_s"] * TICK)),
            "patience_ticks_left": int(round(self.t["patience_s"] * TICK)),
            "eat_ticks_left": int(round(self.t["eat_s"] * TICK)),
            "stove_id": None,
        }
        self.customers.append(customer)

    def _advance_customers(self, events):
        remaining = []
        for customer in sort_by_id(self.customers):
            if customer["state"] == "eating":
                customer["eat_ticks_left"] = max(0, customer["eat_ticks_left"] - 1)
                if customer["eat_ticks_left"] == 0:
                    self._pay(customer, events)
                else:
                    remaining.append(customer)
                continue
            customer["patience_ticks_left"] = max(0, customer["patience_ticks_left"] - 1)
            if customer["patience_ticks_left"] == 0:
                self._customer_left(customer, events)
            else:
                remaining.append(customer)
        self.customers = remaining

    def _customer_left(self, customer, events):
        self._release_customer(customer)
        self.reputation = max(self.t["reputation_min"], self.reputation + self.t["left_reputation_delta"])
        events.append(("customer_left", {
            "customer_id": customer["id"],
            "table_id": customer["table_id"],
            "reason": "patience",
            "reputation": self.reputation,
        }))

    def _pay(self, customer, events):
        dish = self.menu[customer["dish_id"]]
        price = dish["price"]
        ratio = customer["patience_ticks_left"] / max(1, customer["patience_max_ticks"])
        tip = int(round(price * self.t["tip_rate"])) if ratio >= self.t["tip_min_patience_ratio"] else 0
        total = price + tip
        self.money += total
        self.earned += total
        self.shift_earned += total
        self.reputation = min(self.t["reputation_max"], self.reputation + self.t["tip_reputation"])
        events.append(("paid", {
            "customer_id": customer["id"],
            "table_id": customer["table_id"],
            "dish_id": customer["dish_id"],
            "price": price,
            "tip": tip,
            "total": total,
            "reputation": self.reputation,
        }))

    def _interact(self, events):
        candidates = []
        for stove in sort_by_id(self.stoves):
            distance = math.dist(self.pos, stove["pos"])
            if distance > self.t["interact_radius"]:
                continue
            actionable = stove["state"] == "ready" and self.hand is None
            actionable = actionable or (stove["state"] == "idle" and self._waiting_customer() is not None)
            if actionable:
                candidates.append((distance, 0, stove["id"], "stove", stove))
        for table in sort_by_id(self.tables):
            customer = next((c for c in self.customers if c["table_id"] == table["id"]), None)
            if customer is None or customer["state"] != "ready" or self.hand != customer["dish_id"]:
                continue
            distance = math.dist(self.pos, table["pos"])
            if distance <= self.t["interact_radius"]:
                candidates.append((distance, 1, table["id"], "table", customer))
        if not candidates:
            return
        _, _, _, kind, target = min(candidates, key=lambda c: c[:3])
        if kind == "stove":
            if target["state"] == "idle":
                self._start_cooking(target, events)
            else:
                self._pick_dish(target, events)
        else:
            self._serve(target, events)

    def _start_cooking(self, stove, events):
        customer = self._waiting_customer()
        if customer is None:
            return
        stove["state"] = "cooking"
        stove["dish"] = customer["dish_id"]
        stove["customer_id"] = customer["id"]
        stove["cook_ticks_left"] = max(1, int(round(self.menu[customer["dish_id"]]["cook_s"] * TICK)))
        stove["ready_ticks"] = 0
        customer["state"] = "cooking"
        customer["stove_id"] = stove["id"]
        customer["reserved"] = {}
        events.append(("cook_started", {
            "stove_id": stove["id"],
            "customer_id": customer["id"],
            "dish_id": customer["dish_id"],
            "cook_ticks": stove["cook_ticks_left"],
        }))

    def _pick_dish(self, stove, events):
        customer_id = stove.get("customer_id")
        customer = self._customer_by_id(customer_id)
        dish_id = stove.get("dish")
        if dish_id is None or self.hand is not None:
            return
        self.hand = dish_id
        stove["state"] = "idle"
        stove["dish"] = None
        stove["customer_id"] = None
        stove["cook_ticks_left"] = 0
        stove["ready_ticks"] = 0
        if customer is not None:
            customer["state"] = "ready"
            customer["stove_id"] = None
        events.append(("dish_picked", {"stove_id": stove["id"], "customer_id": customer_id, "dish_id": dish_id}))

    def _serve(self, customer, events):
        dish_id = self.hand
        self.hand = None
        customer["state"] = "eating"
        customer["eat_ticks_left"] = max(1, int(round(self.t["eat_s"] * TICK)))
        events.append(("served", {
            "customer_id": customer["id"],
            "table_id": customer["table_id"],
            "dish_id": dish_id,
        }))

    def _finish(self, reason, events):
        self.done = True
        self.reason = reason
        events.append(("quan_end", {
            "reason": reason,
            "money": self.money,
            "earned": self.earned,
            "shift_earned": self.shift_earned,
            "reputation": self.reputation,
        }))

    def _waiting_customer(self):
        waiting = [c for c in self.customers if c["state"] == "waiting" and c.get("dish_id") in self.menu]
        return sort_by_id(waiting)[0] if waiting else None

    def _customer_by_id(self, customer_id):
        return next((c for c in self.customers if c["id"] == customer_id), None)

    def _release_customer(self, customer):
        if customer.get("reserved"):
            for item, count in customer["reserved"].items():
                self.stock[item] = self.stock.get(item, 0) + count
            customer["reserved"] = {}
        stove_id = customer.get("stove_id")
        if stove_id:
            stove = next((s for s in self.stoves if s["id"] == stove_id), None)
            if stove is not None and stove.get("customer_id") == customer["id"]:
                stove.update(state="idle", dish=None, customer_id=None, cook_ticks_left=0, ready_ticks=0)

    def _choose_dish(self):
        for dish_id in sorted(self.menu):
            if self._can_reserve(self.menu[dish_id]["recipe"]):
                return dish_id
        return None

    def _can_reserve(self, recipe):
        return all(self.stock.get(item, 0) >= count for item, count in recipe.items())

    def _reserve(self, recipe):
        if not self._can_reserve(recipe):
            return {}
        reserved = {}
        for item, count in recipe.items():
            self.stock[item] = self.stock.get(item, 0) - count
            reserved[item] = count
        return reserved

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        if (mx, mz) != (0.0, 0.0):
            self.heading = math.degrees(math.atan2(mz, mx)) % 360
        bounds = self.t["bounds"]
        for i, axis in enumerate(AXES):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = bounds[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
