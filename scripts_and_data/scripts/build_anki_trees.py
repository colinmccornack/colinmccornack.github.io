#!/usr/bin/env python3
"""Build the JSON data for the Step 2 B&B and Shelf lesson explorer pages.

Inputs are tab-separated card exports from the Anki browser (Sort Field, Card,
Due, Deck, Note, Tags), one row per card.

    python3 build_anki_trees.py \
        --step2-bnb "Step2_B&B_no_Step1Step2_Overlap.csv" \
        --shelf "Shelf_tag.csv" \
        --out ../../assets/data

Writes:
  bnb-step2-only-lessons.json  same shape as bnb-lessons.json (Step 2 only)
  shelf-lessons.json           per-shelf totals plus B&B and OME trees per shelf

Every count is the number of unique cards in that node's subtree, so a card
tagged to two lessons in the same chapter counts once for the chapter.
"""
import argparse
import csv
import json
import os
import re
from collections import defaultdict

BNB_STEP2 = "#AK_Step2_v12::#B&B::"
OME_STEP2 = "#AK_Step2_v12::#OME::"
SHELF = "#AK_Step2_v12::!Shelf::"
SHELF_SKIP = ("#Cards_AnKing_Did", "#Cards_AnKing_Skipped")
OME_SKIP = ("Removed",)

csv.field_size_limit(1 << 30)


def load_cards(path):
    """Return a list of tag sets, one per card."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    header_i = next(i for i, r in enumerate(rows) if r[:2] == ["Sort Field", "Card"])
    tags_col = rows[header_i].index("Tags")
    return [set(r[tags_col].split()) for r in rows[header_i + 1:] if len(r) > tags_col]


def bnb_paths(tags):
    """Step 2 B&B tags as (subject, chapter, lesson); deeper levels like ::Extra stay in the lesson name."""
    for t in tags:
        if t.startswith(BNB_STEP2):
            parts = t[len(BNB_STEP2):].split("::")
            if len(parts) >= 3:
                yield (parts[0], parts[1], "::".join(parts[2:]))


def ome_paths(tags):
    """Step 2 OME tags as variable-depth paths. The Clinical:: branch mirrors the numbered courses, so it is merged into them."""
    for t in tags:
        if t.startswith(OME_STEP2):
            parts = t[len(OME_STEP2):].split("::")
            if parts[0] == "Clinical":
                parts = parts[1:]
            # Clinical::Intern_Bootcamp::Intern_Bootcamp repeats its own name
            while len(parts) > 1 and parts[0] == parts[1]:
                parts = parts[1:]
            if parts and parts[0] not in OME_SKIP:
                yield tuple(parts)


def shelves_of(tags):
    return {t[len(SHELF):].split("::")[0] for t in tags if t.startswith(SHELF)} - set(SHELF_SKIP)


def sort_key(name):
    # Numbered names sort by their number; the rest alphabetically after them
    m = re.match(r"(\d+)_", name)
    return (0, int(m.group(1)), name) if m else (1, 0, name.lower())


class Strings:
    def __init__(self):
        self.list, self.index = [], {}

    def __call__(self, s):
        if s not in self.index:
            self.index[s] = len(self.list)
            self.list.append(s)
        return self.index[s]


def build_tree(card_paths, strings, top_by_count=True):
    """card_paths: {card_id: iterable of path tuples}. Returns nested [name_i, count, children?] nodes."""
    root = {}

    def node():
        return {"cards": set(), "kids": {}}

    for cid, paths in card_paths.items():
        for path in paths:
            level = root
            for name in path:
                n = level.setdefault(name, node())
                n["cards"].add(cid)
                level = n["kids"]

    def emit(level, by_count):
        names = sorted(level, key=lambda k: (-len(level[k]["cards"]), sort_key(k)) if by_count else sort_key(k))
        out = []
        for name in names:
            n = level[name]
            entry = [strings(name), len(n["cards"])]
            if n["kids"]:
                entry.append(emit(n["kids"], False))
            out.append(entry)
        return out

    return emit(root, top_by_count)


def build_step2_bnb(cards):
    strings = Strings()
    paths = {i: list(bnb_paths(tags)) for i, tags in enumerate(cards)}
    paths = {i: p for i, p in paths.items() if p}
    subjects = build_tree(paths, strings)
    step = [strings("Step 2"), len(paths), subjects]
    return {"s": strings.list, "steps": [step], "total_cards": len(paths)}


def build_shelf(cards):
    strings = Strings()
    shelf_cards = defaultdict(set)
    for i, tags in enumerate(cards):
        for s in shelves_of(tags):
            shelf_cards[s].add(i)
    shelf_order = sorted(shelf_cards, key=lambda s: (-len(shelf_cards[s]), s))
    all_cards = set().union(*shelf_cards.values())

    trees = {}
    for key, label, get_paths in (("bnb", "Boards & Beyond", bnb_paths), ("ome", "OnlineMedEd", ome_paths)):
        card_paths = {i: list(get_paths(cards[i])) for i in all_cards}
        card_paths = {i: p for i, p in card_paths.items() if p}
        shelves = []
        for s in shelf_order:
            sub = {i: card_paths[i] for i in shelf_cards[s] if i in card_paths}
            shelves.append([strings(s), len(sub), build_tree(sub, strings)])
        trees[key] = {"label": label, "tagged_cards": len(card_paths), "shelves": shelves}

    return {
        "s": strings.list,
        "shelves": [[strings(s), len(shelf_cards[s])] for s in shelf_order],
        "total_cards": len(all_cards),
        "trees": trees,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step2-bnb", required=True, help="export of Step 2 B&B cards without the Step 1&2 overlap tag")
    ap.add_argument("--shelf", required=True, help="export of cards with a Step 2 !Shelf tag")
    ap.add_argument("--out", required=True, help="output directory (assets/data)")
    args = ap.parse_args()

    step2 = build_step2_bnb(load_cards(args.step2_bnb))
    shelf = build_shelf(load_cards(args.shelf))

    for name, data in (("bnb-step2-only-lessons.json", step2), ("shelf-lessons.json", shelf)):
        with open(os.path.join(args.out, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Step 2 B&B (no overlap): {step2['total_cards']} cards")
    print(f"Shelf: {shelf['total_cards']} cards")
    for (si, n) in shelf["shelves"]:
        print(f"  {shelf['s'][si]}: {n}")
    for key, t in shelf["trees"].items():
        print(f"  {t['label']}-tagged: {t['tagged_cards']}")


if __name__ == "__main__":
    main()
