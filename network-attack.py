def capture(matrix):
    minutes, captured = 0, {0}
    while len(matrix) != len(captured):
        minutes += 1
        targets = set()
        for comp in captured.copy():
            for j, x in enumerate(matrix[comp]):
                if x and j not in captured | targets:
                    targets.add(j)
                    matrix[j][j] -= 1
                    if not matrix[j][j]:
                        captured.add(j)
    return minutes