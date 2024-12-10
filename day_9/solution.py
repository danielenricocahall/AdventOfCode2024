def expand_dense_disk_map_representation(disk_map: str) -> str:
    _id = 0
    i = 0
    result = ""
    while i < len(disk_map) - 2:
        result += int(disk_map[i]) * str(_id) + int(disk_map[i + 1]) * "."
        _id += 1
        i += 2
    result += int(disk_map[-1]) * str(_id)
    return result


def compact_file_blocks(disk_map_expanded_representation: str):
    print(disk_map_expanded_representation)
    checksum = 0
    indices_with_file_blocks = map(lambda x: len(disk_map_expanded_representation)-x[0], filter(lambda x: x[1].isdigit(), enumerate(reversed(disk_map_expanded_representation), 1)))
    used_indices = set()
    for i, memory_block in enumerate(disk_map_expanded_representation):
        if memory_block == ".":
            index = next(indices_with_file_blocks)
        else:
            index = i
        if index in used_indices:
            break
        used_indices.add(index)
        file_block = disk_map_expanded_representation[index]
        checksum += (i * int(file_block))
    return checksum


def calculate_checksum(compacted_file_blocks: list[int]):
    return sum(i * n for i, n in enumerate(compacted_file_blocks))


if __name__ == "__main__":
    with open('./puzzle_test.txt') as fp:
        disk_map = fp.read()
    expanded_disk_map_representation = expand_dense_disk_map_representation(disk_map)

    compacted_file_blocks = compact_file_blocks(expanded_disk_map_representation)
    print(compacted_file_blocks)
