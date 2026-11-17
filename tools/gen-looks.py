# Writes five of the looks in this repository (engraved, keys, transit, offset, listing); headline is written by hand.
# They share every style name with FastDraw's built-in look, so one generator keeps them in step:
# each look below gives its colours, fonts and the lines that differ; the rest is common.
#   python3 tools/gen-looks.py
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CYL = 'path="M0,0.1 C0,-0.035 1,-0.035 1,0.1 L1,0.9 C1,1.035 0,1.035 0,0.9 Z M0,0.1 C0,0.235 1,0.235 1,0.1 C1,0.235 0,0.235 0,0.1"'
USE = {
    'node': 'default box: a backend, service, component or step', 'focal': 'the one or two elements the diagram is about',
    'store': 'something that holds data or state', 'cloud': 'a hosted or third-party platform', 'external': 'a person or system outside what you own',
    'optional': 'optional or asynchronous participant', 'sticky': 'a yellow sticky note: an idea, comment or open question',
    'sticky-orange': 'an orange sticky note: a risk or issue', 'sticky-violet': 'a violet sticky note: a decision or note',
    'step': 'flowchart action', 'terminal': 'flowchart start or end', 'terminal-focal': 'the flowchart outcome that matters most',
    'decision': 'flowchart yes/no question; put the text on two short lines', 'zone': 'a labelled region drawn behind a group of boxes; always give WxH',
    'bar': 'sequence diagram activation bar, centred on a lifeline; always give WxH',
    'table': 'an entity, class or database table: a header and rows. One line per row: | id \\"name\\" \\"type\\" \\"key\\". Arrows can end on a row: orders.user_id -> users.id',
    'matrix': 'a grid of values: first row with |= for the column headings, first cell of each row is its name',
    'chart': 'axes with your numbers drawn for you: chart at x,y WxH x=\\"Q1,Q2,Q3\\" y=0..100, then a line per series: | bars \\"Revenue\\" 42 61 75',
    'arrow': 'default arrow', 'primary': 'the main path; at most two per diagram', 'link': 'an HTTP or API request crossing a boundary',
    'return': 'a response, or something optional or asynchronous', 'lifeline': 'sequence diagram lifeline', 'rule': 'thin separator, e.g. above a legend',
    'h1': 'diagram title', 'kicker': 'optional: a short category above the title, e.g. PROCESS', 'dek': 'optional: one line under the title saying what the diagram shows',
    'eyebrow': 'small caps label, e.g. LEGEND', 'caption': 'small explanatory text', 'note': 'a short aside; at most two', 'small': 'technical detail: a port, path or command',
}
GUIDANCE = [
    'focal, terminal-focal and primary are the accent. Use the accent on at most two things in one diagram.',
    'Never fill a shape with ink to make it stand out; use focal.',
    'tag= is a 3 or 4 letter type marker in the corner of a box (EXT, EDGE, API, DB). Use it on architecture boxes, not flowchart shapes.',
    'sub= is a short second line of detail: a product name, path, port or protocol. Names of things go in the main text.',
    'kicker and dek are optional. Add a kicker only when the diagram belongs to a named category, and a dek only when there is one clear message; most diagrams need neither.',
    "Finish with a legend: one statement, 'legend at x,y' followed by style=\\\"what it means\\\" for each style you used.",
]
ORDER = [('boxes', ['node', 'focal', 'store', 'cloud', 'external', 'optional', 'sticky', 'sticky-orange', 'sticky-violet']),
         ('flowchart shapes', ['step', 'terminal', 'terminal-focal', 'decision']),
         ('regions and markers', ['zone', 'bar', 'table', 'matrix', 'chart']),
         ('lines', ['arrow', 'primary', 'link', 'return', 'relation', 'lifeline', 'rule']),
         ('text', ['h1', 'kicker', 'dek', 'eyebrow', 'caption', 'legend', 'note', 'small'])]

def write(name, head, canvas, colors, fonts, styles, extra_guidance=()):
    out = ['// ' + l for l in head] + ['', 'canvas ' + canvas, '']
    out += [f'color {k.ljust(8)} {v}' for k, v in colors.items()] + ['']
    out += [f'font {k.ljust(5)} "{v}"' for k, v in fonts.items()]
    for title, names in ORDER:
        out += ['', f'// ---- {title} ' + '-' * (70 - len(title))]
        for n in names:
            use = f' use="{USE[n]}"' if n in USE else ''
            out.append(f'style {n} {styles[n]}{use}')
    out += [''] + [f'guidance "{g}"' for g in list(GUIDANCE) + list(extra_guidance)]
    open(os.path.join(ROOT, name + '.look'), 'w').write('\n'.join(out) + '\n')

TEXT_LINES = 'label.spacing=0 label.caps=0'

# ---------------------------------------------------------------------------------------------
write('engraved',
      ['Engraved: a plate from an old technical book. Double rules round every box, shadows cut in fine lines,',
       'a tall serif title and italic notes on the lines, a black plate for the subject and a red double line',
       'for the main path. Same style names as the built-in look.'],
      'paper=paper',
      dict(paper='#f3eee2', card='#fbf8f0', block='#e7dfcd', ink='#1c1814', muted='#5d554a', soft='#9a8f7f', accent='#b3261a', link='#1c1814', teal='#2f6f62', amber='#a8742a', rose='#b3261a', violet='#5b4a8a'),
      dict(sans='Newsreader', mono='Geist Mono', serif='Instrument Serif'),
      {
          'node': 'shape=rect radius=0 size=144x64 fill=card stroke=ink sw=1.2 inner=ink inner.gap=3.5 inner.sw=0.5 shade=ink shade.gap=3 shade.sw=0.7\n    title.size=12.5 sub.font=serif sub.italic=1 sub.size=11.5 sub.color=ink/0.8 tag.color=ink tag.border=ink/0.5 tag.font=mono icon.color=ink',
          'focal': 'extends node fill=ink inner=paper shade.gap=2.2 shade.sw=0.9 title.color=paper sub.color=paper/0.85\n    tag.color=paper tag.border=paper/0.6 icon.color=paper ghost.color=paper/0.14',
          'store': f'extends node shape=path {CYL} inner=none',
          'cloud': 'extends node fill=block',
          'external': 'extends node fill=paper sw=0.9 dash=1.2,3 inner=none shade=none',
          'optional': 'extends node fill=paper sw=0.9 dash=4,3 inner=none shade=none',
          'sticky': 'extends node size=120x120 fill=#ead9a0 title.font=serif title.italic=1 title.size=15 title.weight=400',
          'sticky-orange': 'extends sticky fill=#e9c4b0', 'sticky-violet': 'extends sticky fill=#d9d0e6',
          'step': 'extends node size=160x48', 'terminal': 'extends node radius=24 size=160x48',
          'terminal-focal': 'extends terminal fill=ink inner=paper title.color=paper sub.color=paper/0.85',
          'decision': 'shape=diamond size=200x96 fill=card stroke=ink sw=1.2 shade=ink shade.gap=3 shade.sw=0.7 title.size=12.5',
          'zone': 'shape=rect radius=0 fill=none hatch=ink/0.4 hatch.gap=5 hatch.sw=0.45 stroke=ink sw=0.8 corners=square layer=back\n    title.pos=top title.dy=-11 title.font=sans title.size=11 title.weight=500 title.color=ink title.spacing=0.2 title.caps=1',
          'bar': 'shape=rect radius=0 size=8x80 fill=ink stroke=ink sw=1',
          'table': 'shape=table radius=0 fill=card stroke=ink sw=1.2 shade=ink shade.gap=3 shade.sw=0.7 head.fill=block rule=ink/0.18\n    title.size=12.5 cell.font=mono cell.size=10 detail.color=muted',
          'matrix': 'extends table align=center grid=1 cell.font=sans',
          'chart': 'shape=chart fill=none stroke=ink sw=1 mask=0 bar.radius=0 grid.color=ink/0.12\n    tick.font=mono tick.size=9 tick.color=muted',
          'arrow': f'line stroke=ink sw=0.95 route=ortho radius=0 head.size=1.15 label.font=sans label.italic=1 label.size=10 label.color=ink {TEXT_LINES}',
          'primary': 'extends arrow stroke=accent sw=4.2 double=paper double.sw=1.8 head.size=1.5 label.color=accent',
          'link': 'extends arrow', 'return': 'extends arrow dash=1.2,3.2',
          'relation': f'extends relation stroke=ink label.font=sans label.italic=1 label.size=10 {TEXT_LINES}',
          'lifeline': 'line head=none stroke=ink/0.5 sw=0.8 dash=1.2,3 route=straight', 'rule': 'line head=none stroke=ink/0.45 sw=0.7 route=straight',
          'h1': 'text font=serif size=36 weight=400 color=ink', 'kicker': 'text font=sans size=10 weight=500 color=accent spacing=0.2 caps=1',
          'dek': 'text font=serif italic=1 size=16 color=ink', 'eyebrow': 'text font=sans size=9 weight=500 color=ink spacing=0.18 caps=1',
          'caption': 'text font=sans size=10 color=muted', 'legend': 'extends legend rule=ink/0.4 title.font=sans title.size=9 item.font=sans item.size=10.5 item.color=ink',
          'note': 'text font=serif italic=1 size=15 color=ink', 'small': 'text font=mono size=9 color=muted',
      })

# ---------------------------------------------------------------------------------------------
write('keys',
      ['Keys: every box is a solid key you could press, with a face and a coloured side for its depth. Lines',
       'are thick cables and their labels are tags clipped onto them. Same style names as the built-in look.'],
      'paper=paper',
      dict(paper='#f4f5fa', card='#ffffff', side='#c3c8d8', ink='#1c1a2e', muted='#6b6f86', soft='#a3a7bb', accent='#6d4aff', accentside='#4326c9', link='#2f7de1', teal='#0f9d83', amber='#d18a00', rose='#e5484d', violet='#6d4aff'),
      dict(sans='Geist', mono='Geist Mono', serif='Newsreader'),
      {
          'node': 'shape=rect radius=12 size=144x64 fill=card stroke=ink sw=2 depth=7 depth.fill=side title.size=12.5 sub.font=sans sub.size=9.5 sub.color=muted\n    tag.color=muted tag.border=ink/0.3 tag.font=mono icon.color=ink',
          'focal': 'extends node fill=accent depth.fill=accentside title.color=#ffffff sub.color=#ffffff/0.85\n    tag.color=#ffffff tag.border=#ffffff/0.6 icon.color=#ffffff ghost.color=#ffffff/0.16',
          'store': 'extends node radius=32 fill=#bff0df depth.fill=#6fcab0',
          'cloud': 'extends node fill=#cfe3ff depth.fill=#8db5ee',
          'external': 'extends node fill=none dash=2,6 cap=round depth=0 icon.color=muted',
          'optional': 'extends node fill=none stroke=ink/0.6 dash=2,6 cap=round depth=0',
          'sticky': 'extends node radius=10 size=120x120 fill=#ffe27a depth.fill=#e0b93a',
          'sticky-orange': 'extends sticky fill=#ffc2ad depth.fill=#e58a6c', 'sticky-violet': 'extends sticky fill=#ddd3ff depth.fill=#a996ee',
          'step': 'extends node size=160x48', 'terminal': 'extends node radius=24 size=160x48 fill=#e9ebf3',
          'terminal-focal': 'extends terminal fill=accent depth.fill=accentside title.color=#ffffff sub.color=#ffffff/0.85',
          'decision': 'shape=diamond size=200x96 fill=card stroke=ink sw=2 depth=7 depth.fill=side title.size=12.5',
          'zone': 'shape=rect radius=18 fill=#e9ebf3 stroke=none sw=0 layer=back\n    title.pos=top title.dy=4 title.fill=none title.align=left title.font=sans title.size=12 title.weight=600 title.color=muted title.spacing=0 title.caps=0',
          'bar': 'shape=rect radius=4 size=8x80 fill=accent stroke=ink sw=1.5',
          'table': 'shape=table radius=10 fill=card stroke=ink sw=2 depth=7 depth.fill=side head.fill=accent/0.12 rule=ink/0.1\n    cell.font=mono cell.size=10 detail.color=muted',
          'matrix': 'extends table align=center grid=1 cell.font=sans',
          'chart': 'shape=chart fill=none stroke=ink sw=2 mask=0 bar.radius=4 grid.color=ink/0.08\n    tick.font=mono tick.size=9 tick.color=muted',
          'arrow': f'line stroke=ink sw=3 cap=round route=ortho radius=10 head.size=1.5 label.font=sans label.size=9.5 label.weight=600 label.color=ink\n    label.fill=card label.border=ink label.sw=1.5 label.radius=12 label.pad=4 {TEXT_LINES}',
          'primary': 'extends arrow stroke=accent sw=5 label.color=accent label.border=accent',
          'link': 'extends arrow stroke=link label.color=link label.border=link', 'return': 'extends arrow dash=1,8',
          'relation': f'extends relation stroke=ink sw=2 label.font=sans label.size=10 {TEXT_LINES}',
          'lifeline': 'line head=none stroke=ink/0.35 sw=2 dash=1,7 cap=round route=straight', 'rule': 'line head=none stroke=ink/0.18 sw=1.5 route=straight',
          'h1': 'text font=sans size=30 weight=600 color=ink spacing=-0.02', 'kicker': 'text font=sans size=11 weight=600 color=accent',
          'dek': 'text font=sans size=14 color=muted', 'eyebrow': 'text font=sans size=10 weight=600 color=muted',
          'caption': 'text font=sans size=10 color=muted', 'legend': 'extends legend rule=ink/0.14 title.font=sans title.caps=0 title.size=10 item.size=10',
          'note': 'text font=sans size=13 color=muted', 'small': 'text font=mono size=9 color=muted',
      })

# ---------------------------------------------------------------------------------------------
write('transit',
      ['Transit: a transit map. The lines are the picture: thick coloured routes with sweeping bends and a ring',
       'where each one starts; the boxes are stations along them. Same style names as the built-in look.'],
      'paper=paper',
      dict(paper='#ffffff', card='#ffffff', ink='#14213d', muted='#5c677d', soft='#8a94a8', accent='#e4002b', link='#0072ce', teal='#00857c', amber='#f2a900', rose='#e4002b', violet='#6a3fa0'),
      dict(sans='Geist', mono='Geist Mono', serif='Newsreader'),
      {
          'node': 'shape=rect radius=32 size=144x64 fill=card stroke=ink sw=3.5 title.size=12.5 sub.font=sans sub.size=9.5 sub.color=muted\n    tag.color=muted tag.border=ink/0.35 tag.font=mono icon.color=ink',
          'focal': 'extends node fill=ink title.color=#ffffff sub.color=#ffffff/0.8 tag.color=#ffffff tag.border=#ffffff/0.6 icon.color=#ffffff ghost.color=#ffffff/0.14',
          'store': 'extends node inner=ink inner.gap=5.5 inner.sw=1.2',
          'cloud': 'extends node stroke=link icon.color=link',
          'external': 'extends node sw=2 dash=6,5 icon.color=muted', 'optional': 'extends node sw=2 stroke=ink/0.6 dash=2,5',
          'sticky': 'extends node radius=4 size=120x120 fill=#ffe9a8 stroke=none sw=0',
          'sticky-orange': 'extends sticky fill=#ffd2c2', 'sticky-violet': 'extends sticky fill=#e6dcf7',
          'step': 'extends node size=160x48', 'terminal': 'extends node size=160x48 fill=#eef2f7',
          'terminal-focal': 'extends terminal fill=ink title.color=#ffffff sub.color=#ffffff/0.8',
          'decision': 'shape=diamond size=200x96 fill=card stroke=ink sw=3.5 title.size=12.5',
          'zone': 'shape=rect radius=26 fill=#eef2f7 stroke=none sw=0 layer=back\n    title.pos=top title.dy=6 title.fill=none title.align=left title.font=sans title.size=11 title.weight=600 title.color=soft title.spacing=0.1 title.caps=1',
          'bar': 'shape=rect radius=4 size=8x80 fill=ink stroke=ink sw=1',
          'table': 'shape=table radius=10 fill=card stroke=ink sw=3 head.fill=ink/0.07 rule=ink/0.12\n    cell.font=mono cell.size=10 detail.color=muted',
          'matrix': 'extends table align=center grid=1 cell.font=sans',
          'chart': 'shape=chart fill=none stroke=ink sw=2 mask=0 bar.radius=3 grid.color=ink/0.08\n    tick.font=mono tick.size=9 tick.color=muted',
          'arrow': 'line stroke=ink sw=6 cap=round route=ortho radius=22 casing=paper casing.width=2.5 tail=stop stop.color=ink head.size=1.7\n    label.font=sans label.size=9 label.weight=600 label.spacing=0.05 label.color=#ffffff label.fill=ink label.radius=3 label.pad=4',
          'primary': 'extends arrow stroke=accent sw=9 label.fill=accent', 'link': 'extends arrow stroke=link label.fill=link',
          'return': 'extends arrow stroke=#8a94a6 dash=1,11 label.fill=#8a94a6',
          'relation': f'extends relation stroke=ink sw=3 label.font=sans label.size=10 {TEXT_LINES}',
          'lifeline': 'line head=none stroke=ink/0.3 sw=2 dash=1,7 cap=round route=straight', 'rule': 'line head=none stroke=#c9ced8 sw=1.5 route=straight',
          'h1': 'text font=sans size=32 weight=600 color=ink spacing=-0.025', 'kicker': 'text font=sans size=10 weight=600 color=accent spacing=0.1 caps=1',
          'dek': 'text font=sans size=14 color=muted', 'eyebrow': 'text font=sans size=9 weight=600 color=muted spacing=0.1 caps=1',
          'caption': 'text font=sans size=10 color=muted', 'legend': 'extends legend rule=ink/0.14 title.font=sans title.size=9 item.size=10',
          'note': 'text font=sans size=13 color=muted', 'small': 'text font=mono size=9 color=muted',
      })

# ---------------------------------------------------------------------------------------------
write('offset',
      ['Offset: printed in two spot inks, a little out of register, the way a small press prints a poster.',
       'There is no black: blue is the ink, red is the subject, and tints are fields of dots.',
       'Same style names as the built-in look.'],
      'paper=paper grain=0.5',
      dict(paper='#f6f2e9', card='#f6f2e9', ink='#2a3fd0', muted='#2a3fd0', soft='#7d8be0', accent='#ff5a4f', link='#2a3fd0', teal='#2a3fd0', amber='#ffcf33', rose='#ff5a4f', violet='#2a3fd0'),
      dict(sans='Libre Franklin', mono='Geist Mono', serif='Newsreader'),
      {
          'node': 'shape=rect radius=0 size=144x64 fill=card stroke=ink sw=2 title.size=12.5 title.weight=700 sub.font=sans sub.size=9.5 sub.color=ink\n    tag.color=ink tag.border=ink/0.6 tag.font=mono icon.color=ink',
          'focal': 'extends node fill=accent offset=5,5 blend=multiply title.color=paper sub.color=paper tag.color=paper tag.border=paper/0.7 icon.color=paper ghost.color=paper/0.2',
          'store': 'extends node radius=32 fill=amber offset=5,5 blend=multiply',
          'cloud': 'extends node halftone=ink/0.4 halftone.gap=5 offset=5,5',
          'external': 'extends node fill=none dash=7,5', 'optional': 'extends node fill=none dash=2,4',
          'sticky': 'extends node size=120x120 halftone=accent/0.55 halftone.gap=5 halftone.r=1 offset=5,5',
          'sticky-orange': 'extends sticky halftone=accent/0.85', 'sticky-violet': 'extends sticky halftone=ink/0.4',
          'step': 'extends node size=160x48', 'terminal': 'extends node radius=24 size=160x48',
          'terminal-focal': 'extends terminal fill=accent offset=5,5 blend=multiply title.color=paper sub.color=paper',
          'decision': 'shape=diamond size=200x96 fill=card stroke=ink sw=2 title.size=12.5 title.weight=700',
          'zone': 'shape=rect radius=0 fill=none halftone=ink/0.3 halftone.gap=6 offset=5,5 stroke=none sw=0 layer=back\n    title.pos=top title.dy=8 title.fill=none title.align=left title.font=sans title.size=11 title.weight=700 title.color=ink title.spacing=0.14 title.caps=1',
          'bar': 'shape=rect radius=0 size=8x80 fill=accent stroke=ink sw=1.5',
          'table': 'shape=table radius=0 fill=card stroke=ink sw=2 head.fill=amber rule=ink/0.25\n    title.weight=700 cell.font=mono cell.size=10 cell.color=ink detail.color=ink',
          'matrix': 'extends table align=center grid=1 cell.font=sans',
          'chart': 'shape=chart fill=none stroke=ink sw=2 mask=0 bar.radius=0 grid.color=ink/0.15\n    tick.font=mono tick.size=9 tick.color=ink',
          'arrow': 'line stroke=ink sw=1.8 route=ortho radius=0 blend=multiply label.font=sans label.size=8.5 label.weight=700 label.spacing=0.09 label.color=ink',
          'primary': 'extends arrow stroke=accent sw=4.5 head.size=1.4 label.color=accent', 'link': 'extends arrow', 'return': 'extends arrow dash=5,4',
          'relation': f'extends relation stroke=ink sw=1.8 label.font=sans label.size=9 {TEXT_LINES}',
          'lifeline': 'line head=none stroke=ink/0.6 sw=1.2 dash=2,4 route=straight', 'rule': 'line head=none stroke=ink/0.5 sw=1 route=straight',
          'h1': 'text font=sans size=34 weight=700 color=ink spacing=-0.03 echo=accent blend=multiply', 'kicker': 'text font=sans size=10 weight=700 color=accent spacing=0.14 caps=1',
          'dek': 'text font=sans size=14 weight=600 color=ink', 'eyebrow': 'text font=sans size=9 weight=700 color=ink spacing=0.14 caps=1',
          'caption': 'text font=sans size=10 color=ink', 'legend': 'extends legend rule=ink/0.5 title.font=sans title.color=ink item.color=ink item.size=10',
          'note': 'text font=sans size=13 weight=600 color=ink', 'small': 'text font=mono size=9 color=ink',
      })

# ---------------------------------------------------------------------------------------------
write('listing',
      ['Listing: the diagram as a line printer would put it on green-bar paper, sprocket holes and all.',
       'One typewriter face, names in capitals, plus signs on the corners, the subject printed in reverse.',
       'A FastDraw diagram is a text file; in this look the picture says so. Same style names as the built-in look.'],
      'paper=paper bars=#e3f1e4 bargap=32 feed=#b9cdbb',
      dict(paper='#f6fbf6', card='#f6fbf6', ink='#1d2b24', muted='#4a5d52', soft='#8fa697', accent='#2f8f5f', link='#1d2b24', teal='#1d6b4f', amber='#8a6d00', rose='#a33a2a', violet='#4a3f8a'),
      dict(sans='Geist Mono', mono='Geist Mono', serif='Geist Mono'),
      {
          'node': 'shape=rect radius=0 size=144x64 fill=card stroke=ink sw=1.4 corners=plus shade=ink/0.55 shade.size=6 shade.gap=2 shade.sw=0.8\n    title.size=11 title.weight=500 title.caps=1 sub.font=mono sub.size=9 sub.color=ink tag.color=ink tag.border=ink/0.5 tag.font=mono icon.color=ink',
          'focal': 'extends node fill=ink inner=paper inner.sw=1.2 title.color=paper sub.color=paper tag.color=paper tag.border=paper/0.6 icon.color=paper ghost.color=paper/0.14',
          'store': 'extends node inner=ink inner.gap=3.5 inner.sw=1.2',
          'cloud': 'extends node dash=1,3',
          'external': 'extends node dash=6,5 shade=none', 'optional': 'extends node dash=2,4 shade=none',
          'sticky': 'extends node size=120x120 fill=#fff6c9 title.caps=0', 'sticky-orange': 'extends sticky fill=#ffe3d6', 'sticky-violet': 'extends sticky fill=#e8e4fb',
          'step': 'extends node size=160x48', 'terminal': 'extends node size=160x48 inner=ink inner.gap=3.5 inner.sw=0.8',
          'terminal-focal': 'extends terminal fill=ink inner=paper title.color=paper sub.color=paper',
          'decision': 'shape=diamond size=200x96 fill=card stroke=ink sw=1.4 title.size=11 title.weight=500 title.caps=1',
          'zone': 'shape=rect radius=0 fill=none halftone=#9fc2a4 halftone.gap=4 halftone.r=0.7 stroke=none sw=0 layer=back\n    title.pos=top title.dy=-11 title.fill=ink title.align=left title.font=mono title.size=10 title.weight=500 title.color=paper title.spacing=0.06 title.caps=1',
          'bar': 'shape=rect radius=0 size=8x80 fill=ink stroke=ink sw=1',
          'table': 'shape=table radius=0 fill=card stroke=ink sw=1.4 corners=plus head.fill=ink/0.1 rule=ink/0.25\n    title.size=11 title.weight=500 title.caps=1 cell.font=mono cell.size=10 detail.color=ink',
          'matrix': 'extends table align=center grid=1',
          'chart': 'shape=chart fill=none stroke=ink sw=1.4 mask=0 bar.radius=0 grid.color=ink/0.15\n    tick.font=mono tick.size=9 tick.color=ink',
          'arrow': 'line stroke=ink sw=1.4 route=ortho radius=0 label.font=mono label.size=9 label.color=ink label.spacing=0.02',
          'primary': 'extends arrow sw=3.4 double=paper double.sw=1 head.size=1.3', 'link': 'extends arrow', 'return': 'extends arrow dash=6,5',
          'relation': 'extends relation stroke=ink sw=1.4 label.font=mono label.size=9',
          'lifeline': 'line head=none stroke=ink/0.6 sw=1 dash=1,4 route=straight', 'rule': 'line head=none stroke=ink/0.5 sw=1 dash=1,4 route=straight',
          'h1': 'text font=mono size=22 weight=500 color=ink spacing=0.05 caps=1', 'kicker': 'text font=mono size=10 weight=500 color=ink spacing=0.1 caps=1',
          'dek': 'text font=mono size=11 color=ink', 'eyebrow': 'text font=mono size=9 color=ink spacing=0.1 caps=1',
          'caption': 'text font=mono size=9.5 color=ink', 'legend': 'extends legend rule=ink/0.5 title.font=mono title.color=ink item.font=mono item.size=9 item.color=ink',
          'note': 'text font=mono size=11 color=ink', 'small': 'text font=mono size=9 color=ink',
      })
print('wrote 5 looks')
