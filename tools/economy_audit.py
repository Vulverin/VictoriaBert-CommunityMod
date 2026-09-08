"""Estimate factory recipe margins at base prices; this is not a game simulation.

Run from any directory: python tools/economy_audit.py
Assumes full sales and one unmodified recipe plus template efficiency goods.
Excludes wages, tariffs, employment, technology, bonuses and changing prices.
"""

import re
from pathlib import Path


COMMON = Path(__file__).resolve().parents[1] / "Victoria2 B&C mod/Victoria2/common"


def blocks(source):
    source = re.sub(r"#[^\n]*", "", source)
    depth = 0
    for match in re.finditer(r"(\w+)\s*=\s*\{|[{}]", source):
        if match.group().endswith("{"):
            if depth == 0:
                name, start = match.group(1), match.end()
                if name is None:
                    raise ValueError("Unexpected anonymous top-level block")
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                raise ValueError("Unmatched closing brace")
            if depth == 0:
                yield name, source[start:match.start()]
    if depth:
        raise ValueError("Unclosed block")


def number(source, key):
    match = re.search(r"\b" + re.escape(key) + r"\s*=\s*([\d.]+)", source)
    if match is None:
        raise ValueError(f"Missing numeric field: {key}")
    return float(match[1])


def main():
    prices = {
        name: number(body, "cost")
        for _, category in blocks((COMMON / "goods.txt").read_text(encoding="utf-8-sig"))
        for name, body in blocks(category)
    }
    recipes = dict(blocks((COMMON / "production_types.txt").read_text(encoding="utf-8-sig")))

    def cost(source):
        return sum(
            float(amount) * prices[good]
            for good, amount in re.findall(r"(\w+)\s*=\s*([\d.]+)", source)
        )

    count = losses = 0
    print("Base-price estimate BEFORE wages/tariffs; assumes full sales.")
    print(f"{'Factory':30} {'Sales':>9} {'Inputs':>9} {'Upkeep':>9} {'Remainder':>10}")
    for name, recipe in recipes.items():
        template = re.search(r"\btemplate\s*=\s*(\w+)", recipe)
        if not template:
            continue
        inherited = recipes[template[1]]
        if not re.search(r"\btype\s*=\s*factory\b", inherited):
            continue
        output = re.search(r"\boutput_goods\s*=\s*(\w+)", recipe)
        if not output:
            raise ValueError(f"Missing output: {name}")
        fields = dict(blocks(recipe))
        revenue = number(recipe, "value") * prices[output[1]]
        inputs = cost(fields.get("input_goods", ""))
        upkeep = cost(fields.get("efficiency", dict(blocks(inherited)).get("efficiency", "")))
        remainder = revenue - inputs - upkeep
        count += 1
        losses += remainder < 0
        print(f"{name:30} {revenue:9.2f} {inputs:9.2f} {upkeep:9.2f} {remainder:10.2f}")
    print(f"\n{count} factories; {losses} negative base-price recipe margins.")
    if not count:
        raise ValueError("No factory recipes found")


if __name__ == "__main__":
    main()
