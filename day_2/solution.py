

def are_levels_safe(levels: list[int]) -> bool :
    level_diffs = [y - x for x, y in zip(levels[1::], levels[::1])]
    levels_are_all_increasing_or_decreasing = (all(level_diff > 0 for level_diff in level_diffs) or all(
        level_diff < 0 for level_diff in level_diffs))
    level_diffs_in_range = all(1 <= abs(level_diff) <= 3 for level_diff in level_diffs)
    return levels_are_all_increasing_or_decreasing and level_diffs_in_range

def problem_dampener_can_make_levels_safe(levels: list[int]) -> bool:
    for i, level in enumerate(levels):
        if are_levels_safe(levels[:i] + levels[i+1:]):
            return True
    return False


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        data = map(str.strip, fp.readlines())
        reports = map(lambda x: x.split(" "), data)
        reports = [list(map(int, report)) for report in reports]
        safe_levels = 0
        for levels in reports:
            if are_levels_safe(levels):
                safe_levels += 1
            elif problem_dampener_can_make_levels_safe(levels):
                safe_levels += 1
        print(safe_levels)
