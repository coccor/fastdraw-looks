# Writes print.look, blueprint.look, high-contrast.look and terminal.look: looks made for a use rather than a cloud.
# Each restyles every style of FastDraw's built-in look (tools/base-styles.txt) and keeps the style names, so a diagram
# drawn for the built-in look switches with one line.
#   python3 tools/gen-purpose-looks.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lookgen import build, colours, fonts, base_styles, write  # noqa: E402

def look(base, head, canvas, c, font_lines, edits, guidance, extra_settings=()):
    settings = [canvas, '', *colours(c), '', *font_lines, *extra_settings]
    return build(base, edits, [], head, settings, [], guidance)

# ---- Print ------------------------------------------------------------------------------------------------
# Black and greys only, for a printer or a PDF read in greyscale: things differ by weight, dashes and texture.
def print_look(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#111111', 'muted': '#4a4a4a', 'soft': '#8a8a8a',
         'accent': '#111111', 'link': '#333333', 'teal': '#555555', 'amber': '#666666', 'rose': '#444444', 'violet': '#777777'}
    plain = {'icon.color': 'ink', 'icon.fill': 'ink/0.08', 'tag.color': 'ink', 'tag.border': 'ink/0.5'}
    edits = {
        'node': {'radius': '2', 'stroke': 'ink', 'sw': '0.8', **plain},
        # the subject: a heavy outline with a fine second rule inside it, no colour
        'focal': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'inner': 'ink', 'inner.gap': '3', 'inner.sw': '0.6', 'title.color': 'ink',
                  'tag.color': 'ink', 'tag.border': 'ink', 'ghost.color': 'ink/0.08'},
        'store': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '0.8', 'halftone': 'ink/0.2', 'halftone.gap': '4', 'halftone.r': '0.6', **plain},
        'cloud': {'fill': '#f0f0f0', 'stroke': 'ink', 'sw': '0.8', **plain},
        'external': {'fill': '#ffffff', 'stroke': 'ink/0.8', 'dash': '4,3', 'icon.color': 'ink', 'icon.fill': 'ink/0.06'},
        'optional': {'fill': '#ffffff', 'stroke': 'ink/0.6', 'dash': '1.5,2.5', 'tag.color': 'muted'},
        'sticky': {'fill': '#f2f2f2', 'stroke': 'ink/0.5', 'tag.color': 'ink'},
        'sticky-orange': {'fill': '#ffffff', 'hatch': 'ink/0.22', 'stroke': 'ink/0.5'},
        'sticky-violet': {'fill': '#ffffff', 'halftone': 'ink/0.2', 'stroke': 'ink/0.5'},
        'terminal': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '0.8'},
        'terminal-focal': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'inner': 'ink', 'inner.sw': '0.6', 'title.color': 'ink'},
        'decision': {'stroke': 'ink', 'sw': '0.8'},
        'zone': {'radius': '2', 'fill': '#f6f6f6', 'stroke': 'ink/0.45', 'sw': '0.6', 'title.color': 'ink/0.7'},
        'bar': {'fill': '#e6e6e6', 'stroke': 'ink', 'sw': '0.8'},
        'table': {'radius': '2', 'stroke': 'ink', 'sw': '0.8', 'head.fill': '#ececec', 'rule': 'ink/0.2'},
        'chart': {'stroke': 'ink'},
        'arrow': {'stroke': 'ink', 'sw': '1', 'radius': '4', 'label.color': 'ink/0.75'},
        # the main path is heavier, a request has an open head, a response is dashed: none of it needs colour
        'primary': {'stroke': 'ink', 'sw': '2.4', 'label.color': 'ink', 'label.weight': '600'},
        'link': {'stroke': 'ink', 'head': 'open', 'label.color': 'ink/0.75'},
        'return': {'dash': '4,3'},
        'relation': {'stroke': 'ink/0.8'},
        'lifeline': {'stroke': 'ink/0.4'},
        'rule': {'stroke': 'ink/0.3'},
        'h1': {'font': 'serif', 'weight': '400', 'spacing': '-0.01'},
        'kicker': {'color': 'ink'},
        'legend': {'rule': 'ink/0.3'},
    }
    head = ['Print: black and greys on white, for a printer or a PDF read in greyscale. The subject has a heavy double rule,',
            'data stores a halftone, the main path a heavier line, requests an open arrowhead and responses a dashed one, so',
            'nothing depends on colour. Libre Franklin, with a Newsreader title. Same style names as the built-in look.']
    guidance = ['Made for black and white: things differ by line weight, dashes and the halftone and hatch fills, never by colour; colour values in a diagram print as greys.']
    return look(base, head, 'canvas paper=paper dots=none', c, fonts('Libre Franklin'), edits, guidance)

# ---- Blueprint --------------------------------------------------------------------------------------------
# A blueprint: white lines on bright blue squared paper. Boxes are outlines with the grid showing through, groups are
# double-line walls, the subject has a hatched wall down two sides, and everything is the one white.
def blueprint(base):
    c = {'paper': '#1060c0', 'card': '#1060c0', 'ink': '#ffffff', 'muted': '#dbe8f8', 'soft': '#a8c6ec',
         'accent': '#ffffff', 'link': '#ffffff', 'teal': '#ffffff', 'amber': '#ffffff', 'rose': '#ffffff', 'violet': '#ffffff'}
    white = {'title.color': 'ink', 'tag.color': 'ink', 'tag.border': 'ink/0.7', 'icon.color': 'ink', 'icon.fill': 'none'}
    edits = {
        'node': {'radius': '0', 'fill': 'none', 'stroke': 'ink', 'sw': '1.2', 'sub.font': 'sans', 'sub.color': 'muted', 'title.weight': '500', **white},
        # the subject: a heavier outline with a hatched wall down its right and bottom, like the walls of a plan; it keeps
        # the paper so the hatching shows only outside it
        'focal': {'fill': 'paper', 'stroke': 'ink', 'sw': '2', 'shade': 'ink', 'shade.size': '7', 'shade.gap': '3', 'shade.sw': '0.9',
                  'title.weight': '700', 'ghost.color': 'ink/0.12', **white},
        'store': {'fill': 'none', 'stroke': 'ink', 'sw': '1.2', **white},
        # a hosted platform: a double outline
        'cloud': {'fill': 'none', 'stroke': 'ink', 'sw': '1', 'inner': 'ink', 'inner.gap': '3', 'inner.sw': '0.7', **white},
        'external': {'fill': 'none', 'stroke': 'ink', 'sw': '1', 'dash': '6,4', **white},
        'optional': {'fill': 'none', 'stroke': 'ink/0.8', 'sw': '1', 'dash': '2,3', **white},
        'sticky': {'fill': 'none', 'stroke': 'ink', 'sw': '1', **white},
        'sticky-orange': {'fill': 'none', 'hatch': 'ink/0.35', 'stroke': 'ink'},
        'sticky-violet': {'fill': 'none', 'halftone': 'ink/0.35', 'stroke': 'ink'},
        'terminal': {'fill': 'none', 'stroke': 'ink', 'sw': '1.2'},
        'terminal-focal': {'fill': 'paper', 'stroke': 'ink', 'sw': '2', 'shade': 'ink', 'shade.size': '7', 'shade.gap': '3', 'shade.sw': '0.9', 'title.color': 'ink'},
        'decision': {'fill': 'none', 'stroke': 'ink', 'sw': '1.2'},
        # a group is a room: walls drawn as two parallel lines
        'zone': {'radius': '0', 'fill': 'none', 'stroke': 'ink', 'sw': '1', 'inner': 'ink', 'inner.gap': '6', 'inner.sw': '1',
                 'title.font': 'sans', 'title.size': '10', 'title.weight': '500', 'title.color': 'ink', 'title.caps': '1', 'title.spacing': '0.08'},
        'bar': {'fill': 'ink/0.15', 'stroke': 'ink'},
        'table': {'radius': '0', 'fill': 'none', 'stroke': 'ink', 'head.fill': 'ink/0.1', 'rule': 'ink/0.35', 'detail.color': 'muted'},
        'chart': {'fill': 'none', 'stroke': 'ink', 'grid.color': 'ink/0.2', 'tick.color': 'muted'},
        # thin lines with small solid heads and plain figures, like dimension lines
        'arrow': {'stroke': 'ink', 'sw': '0.9', 'radius': '0', 'head.size': '0.85', 'label.color': 'ink', 'label.size': '10'},
        'primary': {'stroke': 'ink', 'sw': '1.8', 'label.color': 'ink', 'label.weight': '600'},
        'link': {'stroke': 'ink', 'head': 'open', 'label.color': 'ink'},
        'return': {'dash': '4,3'},
        'relation': {'stroke': 'ink', 'label.color': 'ink'},
        'lifeline': {'stroke': 'ink/0.6'},
        'rule': {'stroke': 'ink/0.5'},
        'h1': {'size': '24', 'weight': '500', 'spacing': '0.06', 'caps': '1'},
        'kicker': {'color': 'ink'},
        'legend': {'rule': 'ink/0.5'},
    }
    head = ['Blueprint: white lines on bright blue squared paper, like an architect\'s plan. Boxes are outlines with the grid',
            'showing through, groups are walls of two parallel lines, the subject has a hatched wall down two sides, and lines',
            'are thin with small solid heads. Everything is the one white; things differ by weight, dashes and hatching.',
            'Same style names as the built-in look.']
    guidance = ['Everything is white on blue: tell things apart by line weight, dashes and hatching, not colour; a colour given in a diagram should be white or a light tint.']
    return look(base, head, 'canvas paper=paper dots=none grid=ink/0.16 gridgap=24', c, fonts('Geist'), edits, guidance)

# ---- High contrast ----------------------------------------------------------------------------------------
# For low vision and colour blindness: black on white, heavy lines, and every style told apart by more than colour.
def high_contrast(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#000000', 'muted': '#2b2b2b', 'soft': '#595959',
         'accent': '#0b3fb5', 'link': '#00593c', 'teal': '#00593c', 'amber': '#7a4100', 'rose': '#a1001a', 'violet': '#4b1fa3'}
    bold = {'title.weight': '700'}  # Atkinson Hyperlegible has regular and bold only
    edits = {
        'node': {'radius': '4', 'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'sub.color': 'muted', 'tag.color': 'ink', 'tag.border': 'ink',
                 'icon.color': 'ink', 'icon.fill': 'ink/0.10', **bold},
        'focal': {'fill': '#e8eeff', 'stroke': 'accent', 'sw': '3.5', 'title.color': 'ink', 'tag.color': 'accent', 'tag.border': 'accent',
                  'icon.color': 'accent', 'icon.fill': 'accent/0.15'},
        'store': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'icon.color': 'ink', 'icon.fill': 'ink/0.1', 'tag.color': 'ink', 'tag.border': 'ink'},
        # a hosted platform has a double outline
        'cloud': {'fill': '#ffffff', 'stroke': 'link', 'sw': '2', 'inner': 'link', 'inner.gap': '3', 'inner.sw': '1', 'icon.color': 'link',
                  'icon.fill': 'link/0.12', 'tag.color': 'link', 'tag.border': 'link'},
        'external': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'dash': '7,4', 'icon.color': 'ink', 'icon.fill': 'ink/0.08'},
        'optional': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2', 'dash': '2,3', 'tag.color': 'ink', 'tag.border': 'ink'},
        'sticky': {'fill': '#fff3b0', 'stroke': 'ink', 'sw': '1.5', 'tag.color': 'ink', 'tag.border': 'ink'},
        'sticky-orange': {'fill': '#ffd6d6', 'stroke': 'ink'},
        'sticky-violet': {'fill': '#e4dcff', 'stroke': 'ink'},
        'terminal': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '2'},
        'terminal-focal': {'fill': '#e8eeff', 'stroke': 'accent', 'sw': '3.5', 'title.color': 'ink'},
        'decision': {'stroke': 'ink', 'sw': '2', **bold},
        'zone': {'radius': '8', 'fill': 'none', 'stroke': 'ink', 'sw': '1.5', 'title.font': 'sans', 'title.size': '10', 'title.weight': '700',
                 'title.color': 'ink', 'title.caps': '0', 'title.spacing': '0'},
        'bar': {'fill': 'accent/0.2', 'stroke': 'accent', 'sw': '1.5'},
        'table': {'stroke': 'ink', 'sw': '2', 'head.fill': '#e8eeff', 'rule': 'ink/0.5', 'detail.color': 'muted', **bold},
        'chart': {'stroke': 'ink', 'sw': '1.5', 'grid.color': 'ink/0.25', 'tick.color': 'ink'},
        'arrow': {'stroke': 'ink', 'sw': '2', 'head.size': '1.3', 'label.color': 'ink', 'label.weight': '700'},
        # the main path is the heaviest line, a request is long dashes, a response short ones: each reads without its colour
        'primary': {'stroke': 'accent', 'sw': '3.5', 'label.color': 'accent'},
        'link': {'stroke': 'link', 'dash': '9,4', 'label.color': 'link'},
        'return': {'dash': '2,4', 'cap': 'round'},
        'relation': {'stroke': 'ink', 'sw': '1.5', 'label.color': 'ink'},
        'lifeline': {'stroke': 'ink/0.6', 'sw': '1.5'},
        'rule': {'stroke': 'ink/0.5'},
        'h1': {'weight': '700'},
        'kicker': {'weight': '700', 'color': 'accent'},
        'caption': {'color': 'ink'},
        'legend': {'rule': 'ink/0.5'},
    }
    head = ['High contrast: for readers with low vision or colour blindness. Black on white, lines 2px and heavier, text at a',
            'contrast of 7:1 or more, and every style told apart by more than its colour: the subject by the heaviest outline, a',
            'hosted platform by a double one, a request by long dashes and a response by short ones. Atkinson Hyperlegible, a face',
            'drawn to keep similar letters apart. Same style names as the built-in look.']
    guidance = ['Keep it readable without colour: do not add colour as the only difference between things; colours given in a diagram should be dark (contrast 7:1 on white).',
                'The font has regular and bold only: use weight=400 or weight=700.']
    return look(base, head, 'canvas paper=paper dots=none', c, fonts('Atkinson Hyperlegible'), edits, guidance)

# ---- Terminal ---------------------------------------------------------------------------------------------
# One monospace face on near-black, square boxes, a double-line border for the subject, phosphor colours.
def terminal(base):
    c = {'paper': '#0e1111', 'card': '#131919', 'ink': '#d6e2d9', 'muted': '#8fa39a', 'soft': '#5d6f67',
         'accent': '#4ef08c', 'link': '#6cc7ff', 'teal': '#5ee0d0', 'amber': '#f2c66d', 'rose': '#ff7a85', 'violet': '#c4a3ff'}
    edits = {
        # a monospace face is wide, so box text is a point smaller to fit the same boxes
        'node': {'radius': '0', 'fill': 'card', 'stroke': 'ink/0.45', 'sw': '1', 'title.size': '11', 'title.weight': '600', 'sub.font': 'mono', 'sub.size': '8.5',
                 'sub.color': 'muted', 'tag.color': 'muted', 'tag.border': 'ink/0.3', 'icon.color': 'accent', 'icon.fill': 'accent/0.12'},
        # the subject's border is doubled, like a box drawn with ═ and ║
        'focal': {'fill': 'accent/0.08', 'stroke': 'accent', 'sw': '1', 'inner': 'accent', 'inner.gap': '3', 'inner.sw': '1', 'title.color': 'accent',
                  'tag.color': 'accent', 'tag.border': 'accent/0.5', 'ghost.color': 'accent/0.10'},
        'store': {'fill': 'card', 'stroke': 'ink/0.45', 'icon.color': 'teal', 'icon.fill': 'teal/0.12', 'tag.color': 'teal', 'tag.border': 'teal/0.4'},
        'cloud': {'fill': 'link/0.06', 'stroke': 'link/0.7', 'icon.color': 'link', 'icon.fill': 'link/0.12', 'tag.color': 'link', 'tag.border': 'link/0.4'},
        'external': {'fill': 'paper', 'stroke': 'ink/0.45', 'dash': '2,3', 'icon.color': 'muted', 'icon.fill': 'ink/0.06'},
        'optional': {'fill': 'paper', 'stroke': 'ink/0.3', 'dash': '1,3', 'tag.color': 'soft', 'tag.border': 'ink/0.2'},
        'sticky': {'fill': 'amber/0.10', 'stroke': 'amber/0.6', 'title.color': 'amber', 'tag.color': 'amber', 'tag.border': 'amber/0.4'},
        'sticky-orange': {'fill': 'rose/0.10', 'stroke': 'rose/0.6', 'title.color': 'rose'},
        'sticky-violet': {'fill': 'violet/0.10', 'stroke': 'violet/0.6', 'title.color': 'violet'},
        'terminal': {'fill': 'card', 'stroke': 'ink/0.45'},
        'terminal-focal': {'fill': 'accent/0.08', 'stroke': 'accent', 'inner': 'accent', 'inner.sw': '1', 'title.color': 'accent'},
        'decision': {'fill': 'card', 'stroke': 'ink/0.45', 'title.size': '11'},
        'zone': {'radius': '0', 'fill': 'none', 'stroke': 'ink/0.3', 'dash': '2,3', 'title.color': 'muted'},
        'bar': {'fill': 'accent/0.12', 'stroke': 'accent/0.7'},
        'table': {'radius': '0', 'fill': 'card', 'stroke': 'ink/0.45', 'head.fill': 'accent/0.08', 'rule': 'ink/0.12'},
        'chart': {'stroke': 'ink/0.5', 'grid.color': 'ink/0.1'},
        'arrow': {'stroke': 'ink/0.55', 'sw': '1', 'radius': '0', 'head': 'triangle', 'label.font': 'mono', 'label.size': '9.5', 'label.color': 'muted'},
        'primary': {'stroke': 'accent', 'sw': '1.6', 'label.color': 'accent'},
        'link': {'stroke': 'link', 'label.color': 'link'},
        'return': {'dash': '3,3'},
        'relation': {'stroke': 'ink/0.6'},
        'lifeline': {'stroke': 'ink/0.25'},
        'rule': {'stroke': 'ink/0.15'},
        'h1': {'size': '22', 'spacing': '0'},
        'dek': {'size': '13'},
        'note': {'size': '12'},
        'legend': {'rule': 'ink/0.15'},
    }
    head = ['Terminal: one monospace face (JetBrains Mono) on near-black, square boxes in thin grey, a double border for the subject',
            'like a box drawn with line characters, faint scan lines, and phosphor green for the subject and the main path. Same',
            'style names as the built-in look.']
    guidance = ['Everything is set in one monospace face, so keep text in boxes short: about 17 characters of a title and 20 of a second line fit a 144px box with an icon.',
                'The page is near-black: colours given in a diagram should be light, and fills tints (accent/0.1), never solid.']
    return look(base, head, 'canvas paper=paper dots=none bars=ink/0.02 bargap=3', c,
                fonts('JetBrains Mono', 'JetBrains Mono', 'JetBrains Mono'), edits, guidance)

if __name__ == '__main__':
    base = base_styles()
    for name, make in [('print', print_look), ('blueprint', blueprint), ('high-contrast', high_contrast), ('terminal', terminal)]:
        write(name, make(base))
    print('wrote print.look, blueprint.look, high-contrast.look, terminal.look')
