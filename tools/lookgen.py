# What the look generators share: the base styles as statements, setting properties on a style, and writing a
# look file from a header, settings, the edited styles, guidance and icon lines.
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')

def base_styles():
    """The built-in look's styles (tools/base-styles.txt), without the file's own comment lines."""
    return open(os.path.join(HERE, 'base-styles.txt')).read().split('\n', 3)[3]

def write(name, text):
    open(os.path.join(ROOT, name + '.look'), 'w').write(text)

# Fonts from Fontsource, served by jsDelivr at a fixed version (the addresses FastDraw's look guide lists as checked).
FONTS = {
    'Open Sans': 'https://cdn.jsdelivr.net/fontsource/fonts/open-sans@5.3.0/latin-{weight}-{style}.ttf',
    'Inter': 'https://cdn.jsdelivr.net/fontsource/fonts/inter@5.3.0/latin-{weight}-{style}.ttf',
    'Roboto': 'https://cdn.jsdelivr.net/fontsource/fonts/roboto@5.3.0/latin-{weight}-{style}.ttf',
    'IBM Plex Sans': 'https://cdn.jsdelivr.net/fontsource/fonts/ibm-plex-sans@5.3.0/latin-{weight}-{style}.ttf',
    # regular and bold only: a look that uses it sets every weight to 400 or 700
    'Atkinson Hyperlegible': 'https://cdn.jsdelivr.net/fontsource/fonts/atkinson-hyperlegible@5.3.0/latin-{weight}-{style}.ttf',
    'JetBrains Mono': 'https://cdn.jsdelivr.net/fontsource/fonts/jetbrains-mono@5.3.0/latin-{weight}-normal.ttf',
}

# ---- statements -------------------------------------------------------------------------------------------
# The base is a list of statements: a line and the indented lines that continue it, with the comments between.

def statements(text):
    out = []
    for line in text.split('\n'):
        if line.startswith((' ', '\t')) and out and out[-1][0] == 'style':
            out[-1][1].append(line)
        elif line.startswith('style '):
            out.append(('style', [line]))
        else:
            out.append(('other', [line]))
    return out

def style_name(st):
    return st[1][0].split()[1]

def set_props(st, props):
    """Sets key=value pairs on a style: replaced where the key is, added to the first line otherwise."""
    lines = list(st[1])
    for k, v in props.items():
        pat = re.compile(r'(?<=\s)' + re.escape(k) + r'=(?:"[^"]*"|\S+)')
        for i, l in enumerate(lines):
            if pat.search(l):
                lines[i] = pat.sub(f'{k}={v}', l, count=1)
                break
        else:
            first = lines[0]
            m = re.search(r'\s+use="', first)
            lines[0] = first[:m.start()] + f' {k}={v}' + first[m.start():] if m else first + f' {k}={v}'
    return ('style', lines)

def build(base, edits, extra_after_zone, head, settings, icons, guidance):
    sts = statements(base)
    out = []
    for st in sts:
        if st[0] == 'style' and style_name(st) in edits:
            st = set_props(st, edits[style_name(st)])
        out.append(st)
        if st[0] == 'style' and style_name(st) == 'zone':
            out += [('style', [l]) for l in extra_after_zone]
    body = '\n'.join(l for st in out for l in st[1]).rstrip('\n')
    lines = ['// ' + l for l in head] + [''] + settings + [''] + body.split('\n')
    lines += [f'guidance "{g}"' for g in guidance]
    lines += ['', '// ---- icons ' + '-' * 70] + icons
    return '\n'.join(lines) + '\n'

def colours(c):
    return [f'color {k.ljust(6)} {v}' for k, v in c.items()]

def fonts(sans, mono='Geist Mono', serif='Newsreader'):
    """The three font roles: a family from FONTS is named with its address, a shipped one by name alone."""
    line = lambda role, fam: f'font {role.ljust(5)} "{fam}"' + (f' "{FONTS[fam]}"' if fam in FONTS else '')
    return [line('sans', sans), line('mono', mono), line('serif', serif)]

