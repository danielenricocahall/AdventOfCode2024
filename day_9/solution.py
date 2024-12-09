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
    num_file_blocks = sum(1 for x in disk_map_expanded_representation if x.isdigit())

    def is_contiguous(x: list[str]):
        return all(x[i].isdigit() for i in range(num_file_blocks))

    disk_map_expanded_representation = list(disk_map_expanded_representation)
    while not is_contiguous(disk_map_expanded_representation):
        next_free_space = next(
            i for i in range(len(disk_map_expanded_representation)) if disk_map_expanded_representation[i] == ".")
        next_file_block = -next(i for i in range(1, len(disk_map_expanded_representation)) if
                                disk_map_expanded_representation[-i].isdigit())
        disk_map_expanded_representation[next_free_space], disk_map_expanded_representation[next_file_block] = \
        disk_map_expanded_representation[next_file_block], disk_map_expanded_representation[next_free_space]
    return map(int, disk_map_expanded_representation[:num_file_blocks])


def calculate_checksum(compacted_file_blocks: list[int]):
    return sum(i * n for i, n in enumerate(compacted_file_blocks))


if __name__ == "__main__":
    with open('./puzzle.txt') as fp:
        disk_map = fp.read()
    expanded_disk_map_representation = expand_dense_disk_map_representation(disk_map)

    compacted_file_blocks = compact_file_blocks(expanded_disk_map_representation)
    checksum = calculate_checksum(compacted_file_blocks)
    print(checksum)
