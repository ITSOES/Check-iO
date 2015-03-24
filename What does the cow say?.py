COW = r'''
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

import re, textwrap, time
# 'gh'.ljust()
def cowsay(text):
    lines =  textwrap.wrap(' ' * (text.startswith(' ')) + ' '.join(text.split()), 39)
    lines[-1] += ' '*(text.endswith(' '))
    length = max([len(x) for x in lines])
    fill = lambda x='', pre=' ', post='', space=' ': pre + space + x + space * (length - len(x) + 1) + post
    lines[0] = lines[1:] and fill(lines[0], *'/\\') or fill(lines[0], *'<>')
    if lines[1:]:
        for i, x in enumerate(lines[1:len(lines)-1]):
            lines[i+1] = fill(x, *'||')
        lines[-1] = fill(lines[-1], *'\\/')

    return '\n'.join(['', fill(space='_')] + lines + [fill(space='-') + COW])

# print(cowsay(' a  '))
print(cowsay(' 0123456789012345678901234567890123456789 '))
# print(cowsay('Lorem ipsum dolor         sit amet, consectetur adipisicing elit, sed do '
#                                 'eiusmod tempor incididunt ut labore et dolore magna aliqua.'))

if __name__ == '__macin__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    expected_cowsay_one_line = r'''
 ________________
< Checkio rulezz >
 ----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
    expected_cowsay_two_lines = r'''
 ________________________________________
/ A                                      \
\ longtextwithonlyonespacetofittwolines. /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

    expected_cowsay_many_lines = r'''
 _________________________________________
/ Lorem ipsum dolor sit amet, consectetur \
| adipisicing elit, sed do eiusmod tempor |
| incididunt ut labore et dolore magna    |
\ aliqua.                                 /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

    cowsay_one_line = cowsay('Checkio rulezz')
    print(cowsay_one_line)
    time.sleep(.1)
    assert cowsay_one_line == expected_cowsay_one_line, 'Wrong answer:\n%s' % cowsay_one_line

    cowsay_two_lines = cowsay('A longtextwithonlyonespacetofittwolines.')
    assert cowsay_two_lines == expected_cowsay_two_lines, 'Wrong answer:\n%s' % cowsay_two_lines

    cowsay_many_lines = cowsay('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
                                'eiusmod tempor incididunt ut labore et dolore magna aliqua.')
    print('real', expected_cowsay_many_lines, cowsay_many_lines)
    time.sleep(.1)
    assert cowsay_many_lines == expected_cowsay_many_lines, 'Wrong answer:\n%s' % cowsay_many_lines



COW = r'''
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

def cowsay(text):

    def cowsay_format(say):
        lines, beg , end, sp = [], 0, 39, 0
        while('  ' in say):
            say = say.replace('  ', ' ')
        while end < len(say):
            sp_pos = say.rfind(' ', beg, end+1)
            end, sp = (sp_pos, 1) if sp_pos != -1 else (end, 0)
            lines.append(say[beg:end])
            beg, end = end + sp, end + sp + 39
        lines.append(say[beg:len(say)])
        return lines

    moo, moo_say = cowsay_format(text), ['']
    width = max((len(t) for t in moo))
    moo_say.append(' {}'.format('_'*(width+2)))
    if len(moo) == 1:
        moo_say.append('< {:<{w}} >'.format(moo[0], w=width))
    else:
        moo_say.append('/ {:<{w}} \\'.format(moo[0], w=width))
        for m in moo[1:-1]:
            moo_say.append('| {:<{w}} |'.format(m, w=width))
        moo_say.append('\ {:<{w}} /'.format(moo[-1], w=width))
    moo_say.append(' {}{}'.format('-'*(width+2), COW))

    return '\n'.join(moo_say)