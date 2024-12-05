from collections import defaultdict


def convert_to_page_ordering_rule(page_ordering_rules: dict[int, set], page_ordering_rule: str):
    before, after = page_ordering_rule.split("|")
    page_ordering_rules[int(before)].add(int(after))


def convert_to_page_update(page_update: str) -> list[int]:
    return list(map(int, page_update.split(",")))

def page_update_order_is_valid(page_update: list[int], page_ordering_rules: dict[int, set]) -> bool:
    for i, page in enumerate(page_update):
        if pages_that_can_only_come_after := page_ordering_rules.get(page):
            previous_pages = set(page_update[:i+1])
            if pages_that_can_only_come_after & previous_pages:
                return False
    return True


def compute_part_1(page_updates: list[list[int]], page_ordering_rules: dict[int, set]) -> int:
    sum_of_middle_number_for_valid_page_updates = 0
    for page_update in page_updates:
        if page_update_order_is_valid(page_update, page_ordering_rules):
            sum_of_middle_number_for_valid_page_updates += page_update[len(page_update) // 2]
    return sum_of_middle_number_for_valid_page_updates

if __name__ == "__main__":
    page_ordering_rules = defaultdict(set)
    converter = lambda rule: convert_to_page_ordering_rule(page_ordering_rules, rule)
    page_updates = []
    with open('./puzzle.txt') as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line:
                converter = lambda page_update: page_updates.append(convert_to_page_update(page_update))
                continue
            converter(line)
    print(compute_part_1(page_updates, page_ordering_rules))
