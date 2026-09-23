"""Ken Burns, in full: six photographs made for the Farm Security Administration,
1936–38, each given a slow move authored to the picture — in on the father and
sons walking into the storm, across the buried fence to the house, up from a
collar to a stare, out from a mother's face to her children.

A move is two focus points and two scales: the picture is cover-fitted, its
object-position and transform-origin sit on the focus, and the scale pushes in
or pulls out about it. Covering the frame holds at any shape of screen.
"""
import html

TITLE = 'Slower than attention'
LEDE = ('Six photographs made for the Farm Security Administration, 1936–38, run as a film. Each gets the slow push, '
        'pull or drift of a documentary, authored to what is in the picture — and slow enough that you never see it begin. '
        'Rest the pointer on the film to hold a picture.')

# label in assets/curated.json, photographer, the Library of Congress caption, place, date,
# focus at the start and end (x%, y% of the picture), scale at the start and end
SHOTS = [
    ('Dust storm', 'Arthur Rothstein', 'Farmer and sons walking in the face of a dust storm', 'Cimarron County, Oklahoma', 'April 1936',
     (46, 46), (62, 56), 1.08, 1.18),   # the scan includes the print's edge: never show it
    ('Coldwater farm', 'Dorothea Lange', 'Dust Bowl farm. This house is occupied; most of the houses in this district have been abandoned',
     'Coldwater District, north of Dalhart, Texas', 'June 1938', (28, 48), (72, 40), 1.2, 1.2),
    ('Tractored out', 'Dorothea Lange', '“Tractored out.” Power farming displaces tenants from the land in the western dry cotton area',
     'Childress County, Texas', 'June 1938', (50, 72), (60, 34), 1.0, 1.22),
    ('Steer skull', 'Arthur Rothstein', 'The bleached skull of a steer on the dry sun-baked earth of the South Dakota Badlands',
     'South Dakota Badlands', 'May 1936', (52, 48), (30, 62), 1.0, 1.18),
    ('Allie Mae Burroughs', 'Walker Evans', 'Allie Mae Burroughs', 'Hale County, Alabama', '1936',
     (50, 62), (50, 34), 1.0, 1.1),
    ('Migrant Mother', 'Dorothea Lange', 'Destitute pea pickers in California. Mother of seven children. Age thirty-two',
     'Nipomo, California', 'March 1936', (52, 29), (50, 40), 1.3, 1.0),
]

HOW = """@property --fx { syntax: '<percentage>'; inherits: false; initial-value: 50% }   /* and --fy */
.shot img { object-fit: cover; object-position: var(--fx) var(--fy);
            transform-origin: var(--fx) var(--fy);                   /* the focus */
            animation: kb 54s linear infinite; animation-delay: calc(var(--i) * 9s) }
@keyframes kb { from { --fx: var(--fx0); --fy: var(--fy0); scale: var(--s0) }
                20%  { --fx: var(--fx1); --fy: var(--fy1); scale: var(--s1) } }"""

NOTE = ('Each move is two focus points and two scales. The picture is cover-fitted with its <code>object-position</code> '
        'and <code>transform-origin</code> on the focus, so it fills the frame at any shape of screen, and the scale pushes '
        'in or pulls out around what matters. Nine seconds a picture, two more to dissolve; nothing is scripted.')

MATERIAL = 'Material — photographs for the Farm Security Administration, 1936–38, Library of Congress · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'fsa'}
    shots, marks = [], []
    for i, (label, who, caption, place, date, f0, f1, s0, s1) in enumerate(SHOTS):
        w = by[label]
        style = f'--i:{i};--fx0:{f0[0]}%;--fy0:{f0[1]}%;--fx1:{f1[0]}%;--fy1:{f1[1]}%;--s0:{s0};--s1:{s1}'
        alt = html.escape(f'{who}: {caption}. {place}, {date}', quote=True)
        shots.append(
            f'<figure class="shot" style="{style}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="100vw" width="{w["w"]}" height="{w["h"]}" alt="{alt}" '
            f'decoding="async"{" fetchpriority=\"high\"" if i == 0 else ""}>\n'
            f'  <figcaption><span class="who">{html.escape(who)}</span><span class="what">{html.escape(caption)}</span>'
            f'<span class="where">{html.escape(place)} · {html.escape(date)}</span></figcaption>\n'
            f'</figure>')
        marks.append(f'<i style="--i:{i}"></i>')
    return ('<section class="film stage" data-material aria-label="Six Farm Security Administration photographs, run as a film">\n'
            + '\n'.join(shots) +
            f'\n<div class="reel" aria-hidden="true">{"".join(marks)}</div>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'fsa'}
    links = ', '.join(f'<a href="{by[s[0]]["descurl"]}">{html.escape(s[1])}, {html.escape(s[4])}</a>' for s in SHOTS)
    return ('Photographs — Arthur Rothstein, Dorothea Lange and Walker Evans for the Farm Security Administration, '
            f'Library of Congress, Prints and Photographs Division, public domain, via Wikimedia Commons: {links}. '
            'The captions follow the Library’s records.')
