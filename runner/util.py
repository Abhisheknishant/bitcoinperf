import itertools
import hashlib


def sha256(inp: str):
    return hashlib.sha256(inp.encode()).hexdigest()


def is_hex(s: str) -> bool:
    try:
        int(s, 16)
    except ValueError:
        return False
    return True


def shuffled_sequence(seed: int, items: list, run_count: int):
    """
    Args:
        seed: used to determine how to permute the branch order
    """
    perms = itertools.cycle(itertools.permutations(items))

    for i in range(seed):
        next(perms)
    bench_order = list(next(perms))

    # Run everything twice.
    return bench_order * run_count


def md_table(headers, values) -> str:
    """
    Turn headers and values into a valid markdown table.
    """
    out = ''
    col_lengths = [0] * len(headers)
    MAX_COL_WIDTH = 60

    for row in tuple([headers]) + tuple(values):
        for i, val in enumerate(row):
            col_lengths[i] = min(max(len(str(val)), col_lengths[i]),
                                 MAX_COL_WIDTH)

    row_fmt = '|' + ''.join(' {' + str(i) + ':<' + str(collen + 2) + '} |'
                            for i, collen in enumerate(col_lengths)) + '\n'

    dividers = ['-' * col_lengths[i] for i, h in enumerate(headers)]
    out += row_fmt.format(*headers)
    out += row_fmt.format(*dividers)

    for row in values:
        out += row_fmt.format(*[str(i) for i in row])

    return out
