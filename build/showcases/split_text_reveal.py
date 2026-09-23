"""Split Text Reveal, in full: six of William Blake's Songs of Innocence and of Experience,
from copy Z (printed and painted in 1826; Library of Congress). Each poem is set beside its
plate, which holds still while the verse passes; every line of verse is a window, and its
words rise into it out of the page, a beat behind the line before. Innocence stands on paper,
Experience on night: the page turns dark at The Tyger.

The text is Blake's, with his spelling (chear, charter'd, sieze) and his ampersands, checked
against the plates. No script: each stanza triggers its own lines when it is mostly on screen.
"""
import html

TITLE = 'Two contrary states'
LEDE = ('Six of William Blake’s Songs of Innocence and of Experience, from a copy printed and painted in 1826, the year '
        'before he died. Scroll: each line of verse rises out of the page, a beat behind the last.')

INNOCENCE, EXPERIENCE = ('Songs of Innocence', '1789'), ('Songs of Experience', '1794')

# label in assets/curated.json, the book, the stanzas as Blake etched them, the plate described
POEMS = [
    ('Introduction', INNOCENCE, [
        ['Piping down the valleys wild', 'Piping songs of pleasant glee', 'On a cloud I saw a child.', 'And he laughing said to me.'],
        ['Pipe a song about a Lamb;', 'So I piped with merry chear,', 'Piper pipe that song again—', 'So I piped, he wept to hear.'],
        ['Drop thy pipe thy happy pipe', 'Sing thy songs of happy chear,', 'So I sung the same again', 'While he wept with joy to hear'],
        ['Piper sit thee down and write', 'In a book that all may read—', 'So he vanish’d from my sight.', 'And I pluck’d a hollow reed.'],
        ['And I made a rural pen,', 'And I stain’d the water clear,', 'And I wrote my happy songs', 'Every child may joy to hear'],
     ], 'the poem framed by two twining vines, small figures in their loops'),
    ('The Lamb', INNOCENCE, [
        ['Little Lamb who made thee', 'Dost thou know who made thee', 'Gave thee life & bid thee feed.', 'By the stream & o’er the mead;',
         'Gave thee clothing of delight,', 'Softest clothing wooly bright;', 'Gave thee such a tender voice,', 'Making all the vales rejoice!',
         'Little Lamb who made thee', 'Dost thou know who made thee'],
        ['Little Lamb I’ll tell thee,', 'Little Lamb I’ll tell thee!', 'He is called by thy name,', 'For he calls himself a Lamb:',
         'He is meek & he is mild,', 'He became a little child:', 'I a child & thou a lamb,', 'We are called by his name.',
         'Little Lamb God bless thee.', 'Little Lamb God bless thee.'],
     ], 'a child with a flock of sheep before a cottage, the poem in the sky between two slender trees'),
    ('Infant Joy', INNOCENCE, [
        ['I have no name', 'I am but two days old.—', 'What shall I call thee?', 'I happy am', 'Joy is my name,—', 'Sweet joy befall thee!'],
        ['Pretty joy!', 'Sweet joy but two days old,', 'Sweet joy I call thee;', 'Thou dost smile.', 'I sing the while', 'Sweet joy befall thee.'],
     ], 'a mother and child with a winged figure inside a great crimson flower'),
    ('The Tyger', EXPERIENCE, [
        ['Tyger Tyger, burning bright,', 'In the forests of the night;', 'What immortal hand or eye,', 'Could frame thy fearful symmetry?'],
        ['In what distant deeps or skies.', 'Burnt the fire of thine eyes?', 'On what wings dare he aspire?', 'What the hand, dare sieze the fire?'],
        ['And what shoulder, & what art,', 'Could twist the sinews of thy heart?', 'And when thy heart began to beat,', 'What dread hand? & what dread feet?'],
        ['What the hammer? what the chain,', 'In what furnace was thy brain?', 'What the anvil? what dread grasp,', 'Dare its deadly terrors clasp!'],
        ['When the stars threw down their spears', 'And water’d heaven with their tears:', 'Did he smile his work to see?', 'Did he who made the Lamb make thee?'],
        ['Tyger Tyger burning bright,', 'In the forests of the night:', 'What immortal hand or eye,', 'Dare frame thy fearful symmetry?'],
     ], 'the poem between the branches of a bare tree, the tyger walking beneath'),
    ('The Sick Rose', EXPERIENCE, [
        ['O Rose thou art sick.', 'The invisible worm,', 'That flies in the night', 'In the howling storm:'],
        ['Has found out thy bed', 'Of crimson joy:', 'And his dark secret love', 'Does thy life destroy.'],
     ], 'a thorny briar around the poem, and a crimson rose bent to the ground with a worm in it'),
    ('London', EXPERIENCE, [
        ['I wander thro’ each charter’d street,', 'Near where the charter’d Thames does flow.', 'And mark in every face I meet', 'Marks of weakness, marks of woe.'],
        ['In every cry of every Man,', 'In every Infants cry of fear,', 'In every voice: in every ban,', 'The mind-forg’d manacles I hear'],
        ['How the Chimney-sweepers cry', 'Every blackning Church appalls,', 'And the hapless Soldiers sigh', 'Runs in blood down Palace walls'],
        ['But most thro’ midnight streets I hear', 'How the youthful Harlots curse', 'Blasts the new-born Infants tear',
         'And blights with plagues the Marriage hearse'],
     ], 'an old man led through the streets by a child above the poem, and a child warming himself at a fire beside it'),
]
SOURCES = [('https://en.wikipedia.org/wiki/Songs_of_Innocence_and_of_Experience', 'Songs of Innocence and of Experience'),
           ('https://en.wikipedia.org/wiki/Etching#Variants', 'relief etching')]

HEAD = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/im-fell-english/index.css">\n'
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/im-fell-english/400-italic.css">\n')

HOW = """.stanza { timeline-trigger: --verse view() entry 70% exit 30% }  /* a stanza mostly on screen… */
.l { overflow: clip; animation: rise .95s both;                     /* …every line a window… */
     animation-trigger: --verse play-once;
     animation-delay: calc((sibling-index() - 1) * 85ms) }          /* …a beat behind the last */
.l > span { translate: 0 calc(var(--rise) * 105%) }                 /* its words come up from below */"""

NOTE = ('Each line of verse is a window with its words below the sill, so they come up out of the page instead of fading '
        'in on top of it. When a stanza is mostly on screen its lines rise, each a beat behind the one before; '
        'there is no script, and the poem is plain text from first to last. Blake’s words rose from their plates too: he '
        'etched each page in relief, so that the words stood up from the copper to take the ink, and painted it after '
        'printing.')

MATERIAL = ('Material — William Blake, Songs of Innocence and of Experience, copy Z, printed and painted 1826 · '
            'Library of Congress · public domain')


def _line(text, tag='span', attrs=''):
    return f'<{tag} class="l"{attrs}><span>{html.escape(text, quote=False)}</span></{tag}>'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'blake'}
    songs = []
    for i, (label, (book, year), stanzas, plate) in enumerate(POEMS, 1):
        w = by[label]
        state = 'innocence' if book == INNOCENCE[0] else 'experience'
        verse = '\n'.join('    <p class="stanza">' + '\n'.join(_line(t) for t in s) + '</p>' for s in stanzas)
        songs.append(
            f'<article class="song {state} {"left" if i % 2 else "right"}" aria-labelledby="song{i}">\n'
            f'  <figure class="leaf"><img src="{w["default"]}" srcset="{w["srcset"]}" '
            f'sizes="(max-width: 760px) 70vw, min(50svh, 460px)" width="{w["w"]}" height="{w["h"]}" style="--ar:{w["w"] / w["h"]:.4f}" '
            f'alt="{html.escape(f"Blake’s plate for {label}: {plate}", quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 1 else " loading=\"lazy\""}></figure>\n'
            f'  <div class="poem">\n'
            f'    <p class="book">{book} · {year}</p>\n'
            f'    {_line(label, "h2", f" id=\"song{i}\"")}\n'
            f'{verse}\n'
            f'  </div>\n'
            f'</article>')
    return ('<section class="songs stage" data-material aria-label="Six of Blake’s Songs of Innocence and of Experience">\n'
            + '\n'.join(songs) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'blake'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[0])}</a>' for p in POEMS)
    return ('Plates — William Blake, Songs of Innocence and of Experience, copy Z, printed and painted in 1826; Library of '
            f'Congress; public domain, via Wikimedia Commons: {links}. Text — Blake’s, with his spelling, read against the '
            'plates. Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
