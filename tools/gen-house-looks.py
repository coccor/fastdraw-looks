# Writes carbon.look, vercel.look and figjam.look: looks drawn the way a company draws its own diagrams. Each
# restyles every style of FastDraw's built-in look (tools/base-styles.txt), keeps the style names so a diagram drawn
# for the built-in look still draws, and adds the company's own kinds of element as extra styles.
#   python3 tools/gen-house-looks.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lookgen import build, colours, fonts, base_styles, write, FONTS  # noqa: E402

FONTS['IBM Plex Mono'] = 'https://cdn.jsdelivr.net/fontsource/fonts/ibm-plex-mono@5.3.0/latin-{weight}-{style}.ttf'

def look(base, head, canvas, c, font_lines, edits, extra, guidance):
    settings = [canvas, '', *colours(c), '', *font_lines]
    return build(base, edits, extra, head, settings, [], guidance)

# ---- Carbon -----------------------------------------------------------------------------------------------
# IBM's technical diagrams (ibm.com/design/language/infographics/technical-diagrams). Most things are small nodes:
# a 48px square in the category's colour with a white 24px icon, the name in semibold under it. People are black
# circles. A resource with details is a large colour-block node: the icon in a block of its colour at the left,
# text left-aligned after it. Groups are framed, with a bar down their left side: IBM Cloud and subnets in blue,
# a region in grey, an availability zone dotted. Connectors are black, 1px, with square elbows. IBM Plex Sans.
def carbon(base):
    # IBM Design Language: Gray 100 text; Blue 60 network, Teal 60 data, Purple 60 application, Red 60 security,
    # Green 60 compute, Magenta 60 DevOps, Gray 60 backend
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#161616', 'muted': '#525252', 'soft': '#8d8d8d',
         'accent': '#0f62fe', 'link': '#0f62fe', 'teal': '#007d79', 'amber': '#f1c21b', 'rose': '#da1e28', 'violet': '#8a3ffc'}
    tag = {'tag.color': 'ink', 'tag.border': 'ink/0.4', 'tag.font': 'mono'}
    # a small node: no box, a coloured square with a white icon, the name centred under it
    def small(colour, shape='square'):
        d = {'shape': 'rect', 'radius': '0', 'size': '144x104', 'fill': 'none', 'stroke': 'none', 'sw': '0', 'dash': 'none',
             'icon.pos': 'top', 'icon.size': '24', 'icon.bg': colour, 'icon.color': '#ffffff', 'icon.fill': 'none',
             'title.color': 'ink', 'title.size': '12', 'title.weight': '600', 'title.align': 'center',
             'sub.color': 'ink', 'sub.font': 'sans', 'sub.size': '10', **tag}
        if shape == 'circle':
            d['icon.bg.shape'] = 'circle'
        return d
    # a large colour-block node: outline and block in one colour, the icon white in the block, text left-aligned
    def block(colour, fill='#ffffff'):
        return {'shape': 'rect', 'radius': '0', 'size': '192x96', 'fill': fill, 'stroke': colour, 'sw': '1', 'dash': 'none',
                'icon.pos': 'left', 'icon.bg': 'none', 'icon.block': colour, 'icon.block.w': '48', 'icon.size': '24',
                'icon.color': '#ffffff', 'icon.fill': 'none', 'title.color': 'ink', 'title.size': '12', 'title.weight': '600',
                'title.align': 'left', 'sub.color': 'ink', 'sub.font': 'sans', 'sub.size': '10', **tag}
    edits = {
        'node': small('accent'),
        # the subject is the one large node: Blue 60 colour block on Blue 10, the details in its second lines
        'focal': {**block('accent', '#edf5ff'), 'ghost.color': 'accent/0.10'},
        'store': {**small('teal'), 'path': 'none'},
        'cloud': small('violet'),
        # an actor: a person or another system, a black circle with a white icon
        'external': small('ink', 'circle'),
        'optional': small('soft'),
        'sticky': {'radius': '0', 'fill': '#fcf4d6', 'stroke': 'amber', 'side': 'amber', 'side.w': '6', 'title.align': 'left',
                   'title.color': 'ink', 'title.weight': '400', **tag},
        'sticky-orange': {'fill': '#fff1f1', 'stroke': 'rose', 'side': 'rose'},
        'sticky-violet': {'fill': '#f6f2ff', 'stroke': 'violet', 'side': 'violet'},
        # flowchart shapes are outlined nodes
        'step': {'shape': 'rect', 'radius': '0', 'size': '160x48', 'fill': '#ffffff', 'stroke': 'ink', 'sw': '1', 'icon.pos': 'left', 'icon.bg': 'none',
                 'icon.color': 'ink', 'title.weight': '600', 'title.size': '12', 'title.color': 'ink', 'title.align': 'center', 'sub.color': 'ink', 'sub.size': '10', **tag},
        'terminal': {'radius': '24', 'fill': '#ffffff', 'stroke': 'ink', 'sw': '1', 'title.color': 'ink'},
        'terminal-focal': {'fill': '#edf5ff', 'stroke': 'accent', 'sw': '2', 'title.color': 'ink'},
        'decision': {'fill': '#ffffff', 'stroke': 'ink', 'sw': '1', 'title.color': 'ink'},
        # a location: white, a 1px Gray 50 frame with a bar down its left side, the name inside at the top-left
        'zone': {'radius': '0', 'fill': '#ffffff', 'stroke': 'soft', 'sw': '1', 'side': 'soft', 'side.w': '4',
                 'title.font': 'sans', 'title.size': '12', 'title.weight': '600', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0',
                 'title.dy': '12', 'title.fill': 'none', **tag},
        'bar': {'radius': '0', 'fill': 'accent/0.12', 'stroke': 'accent'},
        'table': {'radius': '0', 'stroke': 'soft', 'head.fill': '#edf5ff', 'rule': 'ink/0.12', 'cell.font': 'sans', 'detail.color': 'muted'},
        'chart': {'stroke': 'ink/0.6', 'bar.radius': '0'},
        'arrow': {'stroke': 'ink', 'sw': '1', 'radius': '0', 'head': 'arrow', 'head.size': '0.8', 'label.color': 'ink'},
        'primary': {'stroke': 'accent', 'sw': '1', 'label.color': 'ink'},
        'link': {'stroke': 'accent', 'sw': '1', 'label.color': 'ink'},
        'return': {'dash': '4,4'},
        'relation': {'stroke': 'ink'},
        'lifeline': {'stroke': 'ink/0.3', 'dash': '4,4'},
        'rule': {'stroke': 'ink/0.15'},
        'h1': {'size': '24', 'weight': '600', 'spacing': '0'},
        'kicker': {'color': 'accent', 'spacing': '0', 'caps': '0', 'weight': '400', 'font': 'sans', 'size': '12'},
        'eyebrow': {'spacing': '0', 'caps': '0', 'font': 'sans', 'size': '10'},
        'caption': {'color': 'ink'},
        'legend': {'rule': 'ink/0.15', 'title.font': 'sans', 'title.caps': '0', 'title.spacing': '0', 'item.size': '10'},
    }
    grp = "radius=0 sw=1 layer=back title.pos=top title.align=left title.font=sans title.size=12 title.weight=600 title.color=ink title.spacing=0 title.caps=0 title.dy=12 title.fill=none tag.color=ink tag.border=ink/0.4 tag.font=mono"
    extra = [
        f'style cloud-group shape=rect {grp} fill=#edf5ff stroke=accent side=accent side.w=4 use="IBM Cloud, or a cloud account: blue, a bar down its left side; always give WxH"',
        f'style region shape=rect {grp} fill=#ffffff stroke=soft side=soft side.w=4 use="a region or data centre: a grey frame with a bar down its left side; always give WxH"',
        f'style az shape=rect {grp} fill=none stroke=soft dash=1.5,2.5 use="an availability zone: dotted, no fill; always give WxH"',
        f'style subnet shape=rect {grp} fill=#edf5ff stroke=accent/0.6 side=accent side.w=4 use="a VPC or subnet: pale blue with a blue bar; always give WxH"',
        f'style security-group shape=rect {grp} fill=none stroke=rose dash=1.5,2.5 use="a security group or boundary: dotted Red 60; always give WxH"',
        f'style network-group shape=rect {grp} fill=#ffffff stroke=soft side=accent side.w=4 use="an outside network (public, enterprise): white with a blue bar; always give WxH"',
        'style security extends node icon.bg=rose use="a security service (firewall, VPN, gateway): Red 60"',
        'style compute extends focal fill=#ffffff stroke=#198038 icon.block=#198038 use="a compute resource with details (a server, VSI, cluster): a Green 60 colour block"',
        'style devops extends node icon.bg=#d02670 use="a DevOps or classic service: Magenta 60"',
        'style backend extends node icon.bg=#6f6f6f use="a backend or enterprise system: Gray 60"',
    ]
    head = ['Carbon: drawn the way IBM\'s technical diagram guidelines draw (ibm.com/design/language/infographics/technical-diagrams).',
            'Most things are small nodes: a 48px square in the category\'s colour with a white icon, the name in semibold under',
            'it (Blue 60 network, Teal 60 data, Purple 60 application; security, devops and backend add Red, Magenta and Gray).',
            'People are black circles. The subject, and a compute resource, are large colour-block nodes with their details',
            'left-aligned. Groups are frames with a bar down the left side: cloud-group and subnet blue, region grey, az dotted.',
            'Connectors are black, 1px, with square elbows. IBM Plex Sans, text always black. Needs FastDraw\'s icon.bg=, side=',
            'and icon.block=. Same style names as the built-in look.']
    guidance = ['Give every node an icon: a small node is its coloured square and the name under it; without an icon only the name is drawn.',
                'Small nodes are 144x104 boxes: leave their height free under the square for one or two lines of name.',
                'focal and compute are large nodes (192x96): put the details in sub=, one per line, such as sub="Type: Dedicated\\nvCPUs: 2".',
                'Colour means category (network, data, application, security); text is always black. Always finish with a legend, as IBM asks.',
                'Nest groups as IBM does: cloud-group > region > az > subnet, with security-group dotted round what it protects.']
    return look(base, head, 'canvas paper=paper dots=none', c, fonts('IBM Plex Sans', 'IBM Plex Mono'), edits, extra, guidance)

# ---- Vercel -----------------------------------------------------------------------------------------------
# The diagrams in Vercel's docs (vercel.com/docs/fundamentals/infrastructure): boxes of words only, in regular Geist
# at 13px, white with a light grey hairline; an outer panel hatched with fine diagonal lines, grey inner panels, each
# captioned in bold Geist Mono capitals; dashed boxes for alternatives; a browser-window box for the user; black
# hairline connectors with rounded elbows, labelled in mono on pill plates, black badges on the lines.
def vercel(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#171717', 'muted': '#666666', 'soft': '#a1a1a1',
         'accent': '#0070f3', 'link': '#0f9d8a', 'teal': '#0f9d8a', 'amber': '#f5a623', 'rose': '#e5484d', 'violet': '#7c3aed'}
    plain = {'title.color': 'ink', 'title.weight': '400', 'title.size': '13', 'sub.color': 'muted', 'sub.font': 'sans', 'sub.size': '11',
             'tag.color': 'muted', 'tag.border': 'ink/0.2', 'tag.font': 'mono', 'icon.color': 'ink', 'icon.fill': 'none', 'icon.size': '18'}
    # a browser window: a rounded box with three dots at its top-left (in a 160x64 box; other sizes stretch the dots)
    def dot(cx, cy, rx, ry):
        return (f'M{cx - rx:.4f},{cy:.4f} C{cx - rx:.4f},{cy - ry:.4f} {cx + rx:.4f},{cy - ry:.4f} {cx + rx:.4f},{cy:.4f} '
                f'C{cx + rx:.4f},{cy + ry:.4f} {cx - rx:.4f},{cy + ry:.4f} {cx - rx:.4f},{cy:.4f} Z')
    rx, ry = 6 / 160, 6 / 64
    window = (f'M{rx:.4f},0 L{1 - rx:.4f},0 Q1,0 1,{ry:.4f} L1,{1 - ry:.4f} Q1,1 {1 - rx:.4f},1 L{rx:.4f},1 Q0,1 0,{1 - ry:.4f} '
              f'L0,{ry:.4f} Q0,0 {rx:.4f},0 Z ' + ' '.join(dot((12 + 8 * i) / 160, 12 / 64, 2.2 / 160, 2.2 / 64) for i in range(3)))
    edits = {
        'node': {'radius': '6', 'size': '160x64', 'fill': '#ffffff', 'stroke': 'ink/0.16', 'sw': '1', **plain},
        # the subject: a blue hairline on a blue wash, as the docs mark the edge network
        'focal': {'fill': '#eef6ff', 'stroke': 'accent/0.7', 'sw': '1', **plain, 'icon.color': 'accent',
                  'tag.color': 'accent', 'tag.border': 'accent/0.4', 'ghost.color': 'accent/0.08'},
        # Vercel draws data as a plain box too: here a grey one
        'store': {'shape': 'rect', 'path': 'none', 'fill': '#fafafa', 'stroke': 'ink/0.16', **plain},
        'cloud': {'fill': '#f2f2f2', 'stroke': 'ink/0.12', **plain},
        'external': {'shape': 'path', 'path': f'"{window}"', 'fill': '#ffffff', 'stroke': 'ink/0.16', 'dash': 'none', **plain},
        # dashed hairlines, as the docs draw what happens in one case of several
        'optional': {'fill': '#ffffff', 'stroke': 'ink/0.25', 'dash': '3,3', **plain},
        'sticky': {'radius': '6', 'fill': '#fff8e6', 'stroke': 'amber/0.5', 'title.weight': '400', 'tag.color': 'ink', 'tag.border': 'ink/0.2'},
        'sticky-orange': {'fill': '#fff0f0', 'stroke': 'rose/0.5'},
        'sticky-violet': {'fill': '#f5f0ff', 'stroke': 'violet/0.5'},
        'terminal': {'fill': '#ffffff', 'stroke': 'ink/0.2', 'title.weight': '400', 'title.size': '13'},
        'terminal-focal': {'fill': '#eef6ff', 'stroke': 'accent/0.7', 'sw': '1', 'title.color': 'ink', 'title.weight': '400'},
        'decision': {'fill': '#ffffff', 'stroke': 'ink/0.2', 'title.weight': '400', 'title.size': '13'},
        # the outer panel: white with fine diagonal hatching, a hairline, the caption in bold mono capitals inside
        'zone': {'radius': '4', 'fill': '#ffffff', 'hatch': 'ink/0.12', 'hatch.gap': '6', 'hatch.sw': '0.6', 'stroke': 'ink/0.14', 'sw': '1',
                 'title.font': 'mono', 'title.size': '10', 'title.weight': '700', 'title.color': 'ink', 'title.spacing': '0.04',
                 'title.dy': '12', 'title.fill': 'none'},
        'bar': {'radius': '2', 'fill': 'accent/0.10', 'stroke': 'accent/0.6'},
        'table': {'radius': '6', 'stroke': 'ink/0.16', 'head.fill': '#f2f2f2', 'rule': 'ink/0.08'},
        'chart': {'stroke': 'ink/0.4'},
        'arrow': {'stroke': 'ink', 'sw': '1', 'radius': '8', 'head': 'arrow', 'head.size': '0.75',
                  'label.font': 'mono', 'label.size': '10', 'label.color': 'ink',
                  'label.fill': '#ffffff', 'label.border': 'ink/0.8', 'label.radius': '10', 'label.pad': '7', 'label.sw': '1'},
        # a coloured line carries a meaning and its pill is tinted to match, as the docs' Hit and Miss
        'primary': {'stroke': 'accent', 'label.color': 'accent', 'label.fill': '#eef6ff', 'label.border': 'accent'},
        'link': {'stroke': 'link', 'label.color': 'link', 'label.fill': '#e9f7f4', 'label.border': 'link'},
        'return': {'dash': '4,3'},
        'relation': {'stroke': 'ink/0.7'},
        'lifeline': {'stroke': 'ink/0.2'},
        'rule': {'stroke': 'ink/0.1'},
        'h1': {'size': '26', 'weight': '600', 'spacing': '-0.04'},
        'kicker': {'color': 'muted', 'weight': '700', 'spacing': '0.04'},
        'legend': {'rule': 'ink/0.1'},
    }
    cap = "radius=4 sw=1 layer=back title.pos=top title.align=left title.font=mono title.size=10 title.weight=700 title.color=ink title.spacing=0.04 title.caps=1 title.dy=12 title.fill=none"
    extra = [
        f'style panel shape=rect {cap} fill=#f2f2f2 stroke=ink/0.12 use="a grey inner panel, as the docs draw Routing inside a region; always give WxH"',
        f'style region shape=rect {cap} fill=#ffffff stroke=ink/0.14 use="a plain white panel, as the docs draw a region (LHR1) inside the hatched one; always give WxH"',
        'style badge shape=ellipse size=24x24 fill=ink stroke=none sw=0 icon.color=#ffffff icon.size=12 use="a small black badge sitting on a line, holding one icon (a shield where a firewall checks the request)"',
        'style chip extends node size=56x56 radius=6 icon.size=20 use="a small square box holding one icon and no words, as the docs draw the anycast cloud or a function"',
        'style miss extends arrow stroke=rose label.font=mono label.size=10 label.caps=0 label.spacing=0 label.color=rose label.fill=#fdeeee label.border=rose label.radius=10 label.pad=7 label.sw=1 use="a line for a failure or a cache miss: red, its pill tinted"',
    ]
    head = ['Vercel: drawn the way Vercel\'s docs draw (vercel.com/docs/fundamentals/infrastructure). Boxes of words only, in',
            'regular Geist at 13px, white with a light grey hairline and a 6px radius. The outer panel (zone) is hatched with fine',
            'diagonal lines; region is a plain panel and panel a grey one inside it, each captioned in bold Geist Mono capitals.',
            'external is a browser window, optional a dashed box, chip a small square holding an icon, badge a black circle on',
            'a line. Connectors are black hairlines with rounded elbows, labelled in mono on pill plates; primary, link and miss',
            'are blue, teal and red with pills to match. Same style names as the built-in look.']
    guidance = ['Boxes hold words, not icons: write names on one or two lines (Global\\nAnycast Load Balancing) and leave icon= off, except on chip and badge.',
                'Keep colour for meaning: primary blue for the request, link teal for a hit, miss red. Everything else stays black on white.',
                'Line labels sit on pill plates: keep them short, one or two words or a method and path such as GET /api.',
                'Nest panels as the docs do: a hatched zone, a region inside it, grey panels inside that.']
    return look(base, head, 'canvas paper=paper dots=none', c, fonts('Geist'), edits, extra, guidance)

# ---- FigJam -----------------------------------------------------------------------------------------------
# A FigJam board (figma.com/figjam): grey dots on white; flat shapes in FigJam's colours with square corners and no
# outline (circles where a flow starts, squares for steps, diamonds for questions); sticky notes that sit a little
# off the page; sections as pale panels with their name on a tag above the corner; black connectors; the cursors
# and name tags of the people on the board. Inter.
def figjam(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#1e1e1e', 'muted': '#4a4a4a', 'soft': '#8a8a8a',
         'accent': '#14ae5c', 'link': '#0d99ff', 'teal': '#14ae5c', 'amber': '#ffcd29', 'rose': '#f24822', 'violet': '#9747ff'}
    flat = {'stroke': 'none', 'sw': '0', 'dash': 'none', 'title.color': 'ink', 'title.weight': '500', 'title.size': '12',
            'sub.color': 'ink/0.7', 'sub.font': 'sans', 'sub.size': '10', 'tag.color': 'ink', 'tag.border': 'ink/0.35',
            'icon.color': 'ink', 'icon.fill': 'none'}
    sticky = {'radius': '0', 'size': '144x144', 'stroke': 'none', 'sw': '0', 'depth': '4', 'depth.fill': 'ink/0.08', 'depth.stroke': 'none',
              'title.weight': '400', 'title.size': '12', 'title.color': 'ink', 'title.align': 'left', 'tag.color': 'ink', 'tag.border': 'ink/0.35'}
    edits = {
        'node': {'radius': '0', 'size': '120x72', 'fill': '#ffd966', **flat},
        # the subject: full FigJam green, as a board's highlighted step
        'focal': {'radius': '0', 'size': '120x72', 'fill': '#14ae5c', **flat, 'title.weight': '600', 'tag.border': 'ink/0.5', 'ghost.color': 'ink/0.12'},
        'store': {'shape': 'path', 'fill': '#7fd1a6', **flat},
        'cloud': {'radius': '0', 'size': '120x72', 'fill': '#8fd3ff', **flat},
        # where a flow starts, or a person: a circle, as FigJam boards draw entry points
        'external': {'shape': 'ellipse', 'size': '96x96', 'fill': '#e2a5f8', **flat},
        'optional': {'radius': '0', 'size': '120x72', 'fill': '#fff4d6', 'stroke': 'ink/0.35', 'sw': '1.5', 'dash': '6,4', 'title.color': 'ink', 'title.weight': '500',
                     'sub.color': 'ink/0.7', 'sub.font': 'sans', 'icon.color': 'ink', 'icon.fill': 'none', 'tag.color': 'ink', 'tag.border': 'ink/0.35'},
        'sticky': {**sticky, 'fill': '#fff0a1'},
        'sticky-orange': {'fill': '#ffc9a8'},
        'sticky-violet': {'fill': '#e1dbff'},
        'step': {'radius': '0', 'size': '120x72', 'fill': '#ffd966', **flat},
        'terminal': {'shape': 'ellipse', 'radius': '0', 'size': '96x96', 'fill': '#e2a5f8', **flat},
        'terminal-focal': {'shape': 'ellipse', 'size': '96x96', 'fill': '#14ae5c', **flat, 'title.weight': '600'},
        'decision': {'size': '120x104', 'fill': '#e8825f', **flat},
        # a section: a pale panel with a hairline, its name on a yellow tag above the top-left corner
        'zone': {'radius': '2', 'fill': '#fff6e5', 'stroke': '#f5c26b', 'sw': '1',
                 'title.font': 'sans', 'title.size': '11', 'title.weight': '600', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0',
                 'title.dy': '-22', 'title.fill': 'amber'},
        'bar': {'radius': '0', 'fill': '#8fd3ff', 'stroke': 'none'},
        'table': {'radius': '0', 'stroke': 'ink', 'sw': '1.5', 'head.fill': '#ffd966', 'rule': 'ink/0.15', 'cell.font': 'sans'},
        'chart': {'stroke': 'ink/0.6'},
        'arrow': {'stroke': 'ink', 'sw': '1.5', 'radius': '4', 'head': 'arrow', 'head.size': '1', 'label.color': 'ink', 'label.size': '9', 'label.weight': '500'},
        'primary': {'stroke': 'ink', 'sw': '2.5', 'label.color': 'ink', 'label.weight': '600'},
        'link': {'stroke': 'link', 'label.color': 'ink'},
        'return': {'dash': '6,4'},
        'relation': {'stroke': 'ink', 'sw': '1.5'},
        'lifeline': {'stroke': 'ink/0.3', 'dash': '6,4'},
        'rule': {'stroke': 'ink/0.15'},
        'h1': {'size': '28', 'weight': '700', 'spacing': '-0.02'},
        'kicker': {'color': 'violet', 'font': 'sans', 'weight': '600', 'spacing': '0', 'caps': '0'},
        'eyebrow': {'font': 'sans', 'spacing': '0', 'caps': '0', 'size': '10'},
        'legend': {'rule': 'ink/0.12', 'title.font': 'sans', 'title.caps': '0', 'title.spacing': '0'},
    }
    cursor = '"M0,0 L0,1 L0.3,0.72 L0.52,1 L0.68,0.9 L0.47,0.63 L0.9,0.6 Z"'
    extra = [
        'style section extends zone fill=#f3f0ff stroke=#c7b9ff title.fill=#c7b9ff use="a violet section, for a second group beside a zone; always give WxH"',
        f'style cursor shape=path path={cursor} size=16x22 fill=violet stroke=#ffffff sw=1.2 use="a collaborator\'s pointer on the board; put a name-tag beside it"',
        'style name-tag shape=rect radius=2 size=48x20 fill=violet stroke=none sw=0 title.color=#ffffff title.size=10 title.weight=500 use="the name beside a cursor; set fill= to the cursor\'s colour"',
        'style shape-red extends node fill=#ff8f80 use="a red shape: a problem or a stop"',
        'style shape-blue extends node fill=#8fd3ff use="a blue shape"',
        'style shape-violet extends node fill=#e2a5f8 use="a violet shape"',
    ]
    head = ['FigJam: drawn like a FigJam board. Grey dots on white; flat shapes in FigJam\'s colours with square corners and no',
            'outline: yellow steps, a violet circle where a flow starts (external, terminal), a terracotta diamond for a question,',
            'the subject in full green. Sticky notes are squares that sit a little off the page; sections are pale panels named',
            'on a yellow tag above their corner; connectors are black, 1.5px. cursor and name-tag draw the people on the board.',
            'Inter. Same style names as the built-in look.']
    guidance = ['A zone\'s name sits on a tag above its top edge: leave 28px clear above every zone.',
                'Write on shapes the way people do on a board: a word or two, no sub= lines on circles and diamonds.',
                'A cursor and a name-tag together show someone on the board: put the tag 4px right and 12px below the cursor, in its colour.']
    return look(base, head, 'canvas paper=paper dots=ink/0.18 dotgap=20', c, fonts('Inter'), edits, extra, guidance)

if __name__ == '__main__':
    base = base_styles()
    for name, make in [('carbon', carbon), ('vercel', vercel), ('figjam', figjam)]:
        write(name, make(base))
    print('wrote carbon.look, vercel.look, figjam.look')
