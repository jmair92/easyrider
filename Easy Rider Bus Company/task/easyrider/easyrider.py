import json
import re
import itertools


class Bus:
    data = {
        "bus_id": {"type": int, "required": True},
        "stop_id": {"type": int, "required": True},
        "stop_name": {
            "type": str,
            "required": True,
            "format": re.compile(r"^([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$"),
        },
        "next_stop": {"type": int, "required": True},
        "stop_type": {
            "type": "char",
            "required": False,
            "format": re.compile(r"^[SOF]?$"),
        },
        "a_time": {
            "type": str,
            "required": True,
            "format": re.compile(r"^([01]\d|2[0-3]):[0-5]\d$"),
        },
    }
    errors = dict.fromkeys(data, 0)
    bus_lines = {}

    def __init__(self, entry: dict):
        self.entry = entry

    def field_check(self):
        for key, value in self.entry.items():
            f = self.data[key].get("format")
            if f and not self.field_format(value, f):
                self.errors[key] += 1

    @classmethod
    def show_bus_lines(cls):
        print("Line names and number of stops:")
        print(*[f"bus_id: {key}, stops: {len(value)}" for key, value in cls.bus_lines.items()], sep="\n",)

    @staticmethod
    def field_type(value, type_) -> bool:
        return (
            type(value) is type_
            if type_ != "char"
            else type(value) is str and len(value) == 1
        )

    @staticmethod
    def field_required(value, required) -> bool:
        return False if required and value == "" else True

    @staticmethod
    def field_format(value, format_: re.Pattern) -> bool:
        return format_.match(value) is not None

    def get_bus_lines(self, data):
        for d in data:
            self.bus_lines.setdefault(d["bus_id"], [])
            self.bus_lines[d["bus_id"]].append(d)

    def sort_stops(self, entry):
        for bus, lines in b.bus_lines.items():
            start_stops, end_stops = 0, 0
            for l in lines:
                if l["stop_type"] == "S":
                    start_stops += 1
                elif l["stop_type"] == "F":
                    end_stops += 1
            if start_stops != 1 or end_stops != 1:
                return print(f"There is no start or end stop for the line: {bus}.")

        all_stops, start_stops, transfer_stops, finish_stops = [], [], [], []
        for e in entry:
            all_stops.append(e["stop_name"])
            if e["stop_type"] == "S":
                start_stops.append(e["stop_name"])
            elif e["stop_type"] == "F":
                finish_stops.append(e["stop_name"])

        for name in set(all_stops):
            if all_stops.count(name) > 1:
                transfer_stops.append(name)

        transfer_stops.sort()
        start_stops = sorted(set(start_stops))
        finish_stops = sorted(set(finish_stops))

        print("Start stops:", len(start_stops), start_stops)
        print("Transfer stops:", len(transfer_stops), transfer_stops)
        print("Finish stops:", len(finish_stops), finish_stops)

    def check_times(self):
        print("Arrival time test:")
        ok = True
        for bus, lines in self.bus_lines.items():
            arrival = lines[0]["a_time"]
            for l in lines[1:]:
                if arrival > l["a_time"]:
                    print("bus_id line", bus, ": wrong time on station", l["stop_name"])
                    ok = False
                    break
                arrival = l["a_time"]
        if ok:
            print("OK")


    def on_demand(self, entry):
        stops = {}
        transfers = []
        for e in entry:
            stops.setdefault(e["stop_type"], [])
            stops[e["stop_type"]].append(e["stop_name"])
        for name in set(itertools.chain(*stops.values())):
            if list(itertools.chain(*stops.values())).count(name) > 1:
                transfers.append(name)
        print("On demand stops test:")
        res = set(stops.get("O", [])) & set(itertools.chain(
            stops.get("S", []),
            stops.get("F", []),
            stops.get("", []),
            transfers
        ))
        print("Wrong stop type:", sorted(res)) if res else print("OK")


def main():
    entry = json.loads(input())
    b = Bus(entry)
    b.get_bus_lines(entry)
    b.on_demand(entry)


if __name__ == "__main__":
    main()
