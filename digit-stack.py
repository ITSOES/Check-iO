def digit_stack(commands):
    sum, stack = 0, []
    for c in commands:
        if c == 'POP' and stack: sum += stack.pop()
        if c == 'PEEK' and stack: sum += stack[-1]
        if c[:4] == 'PUSH': stack.append(int(c[5:]))
    return sum