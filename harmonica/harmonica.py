from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

NOTES = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']
CIRCLE_MAJOR = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
CIRCLE_MINOR = ['A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D']

RICHTER_BLOW = [0, 4, 3, 5, 4, 3, 5, 4, 3, 5]
RICHTER_DRAW = [2, 5, 4, 3, 3, 4, 2, 3, 3, 4]
RICHTER_DRAW_BENDS = [[-1], [-1, -2], [-1, -2, -3], [-1], [], [-1], [], [], [], []]
RICHTER_BLOW_BENDS = [[], [], [], [], [], [], [], [-1], [-1], [-1, -2]]
RICHTER_OVERDRAW = [[], [], [], [], [], [], [1], [], [1], [1]]
RICHTER_OVERBLOW = [[1], [], [], [1], [1], [1], [], [], [], []]

MAJOR = [0, 2, 2, 1, 2, 2, 2]
MINOR = [0, 2, 1, 2, 2, 1, 2]
HARMONIC_MAJOR = [0, 2, 2, 1, 2, 1, 3]
HARMONIC_MINOR = [0, 2, 1, 2, 2, 1, 3]
MELODIC_MAJOR = [0, 2, 2, 1, 2, 1, 2]
MELODIC_MINOR = [0, 2, 1, 2, 2, 2, 2]
PENTATONIC_MAJOR = [0, 2, 2, 3, 2]
PENTATONIC_MINOR = [0, 3, 2, 2, 3]
BLUES_MAJOR = [0, 2, 1, 1, 3, 2]
BLUES_MINOR = [0, 3, 2, 1, 1, 3]
DORIAN = [0, 2, 1, 2, 2, 2, 1]
PHRYGIAN = [0, 1, 2, 2, 2, 1, 2]
PHRYGIAN_DOMINANT = [0, 1, 3, 1, 2, 1, 2]
LYDIAN = [0, 2, 2, 2, 1, 2, 2]
MIXOLYDIAN = [0, 2, 2, 1, 2, 2, 1]
LOCRIAN = [0, 1, 2, 2, 1, 2, 2]

SCALES = [('major', 'Major'), ('minor', 'Minor'), ('harmonic_major', 'Harmonic Major'), ('harmonic_minor', 'Harmonic Minor'), ('melodic_major', 'Melodic Major'), ('melodic_minor', 'Melodic Minor'), ('pentatonic_major', 'Pentatonic Major'), ('pentatonic_minor', 'Pentatonic Minor'), ('blues_major', 'Blues Major'), ('blues_minor', 'Blues Minor'), ('dorian', 'Dorian'), ('phrygian', 'Phrygian'), ('phrygian_dominant', 'Phrygian Dominant'), ('lydian', 'Lydian'), ('mixolydian', 'Mixolydian'), ('locrian', 'Locrian')]


def get_holes_notes(start_stage, note_map):
    row = []
    stage = start_stage
    for step in note_map:
        stage += step
        if stage > len(NOTES) - 1:
            stage -= len(NOTES)
        name_note = NOTES[stage]
        row.append((name_note, stage))
    return row


def get_effect_notes(notes, pattern):
    effect_notes = []
    for note, effect in zip(notes, pattern):
        effect_notes.append([])
        name_note, note_stage = note
        for step in effect:
            stage = note_stage + step
            if stage > len(NOTES) - 1:
                stage -= len(NOTES)
            elif stage < 0:
                stage += len(NOTES)
            name_note = NOTES[stage]
            effect_notes[-1].append((name_note, stage))
    return effect_notes


def get_scale(scale='major', tonic='C'):
    _tonic = tonic.capitalize()
    start_stage = NOTES.index(_tonic)

    if scale == 'major':
        scale_pattern = MAJOR
    elif scale == 'minor':
        scale_pattern = MINOR
    elif scale == 'harmonic_major':
        scale_pattern = HARMONIC_MAJOR
    elif scale == 'harmonic_minor':
        scale_pattern = HARMONIC_MINOR
    elif scale == 'melodic_major':
        scale_pattern = MELODIC_MAJOR
    elif scale == 'melodic_minor':
        scale_pattern = MELODIC_MINOR
    elif scale == 'pentatonic_major':
        scale_pattern = PENTATONIC_MAJOR
    elif scale == 'pentatonic_minor':
        scale_pattern = PENTATONIC_MINOR
    elif scale == 'blues_major':
        scale_pattern = BLUES_MAJOR
    elif scale == 'blues_minor':
        scale_pattern = BLUES_MINOR
    elif scale == 'dorian':
        scale_pattern = DORIAN
    elif scale == 'phrygian':
        scale_pattern = PHRYGIAN
    elif scale == 'phrygian_dominant':
        scale_pattern = PHRYGIAN_DOMINANT
    elif scale == 'lydian':
        scale_pattern = LYDIAN
    elif scale == 'mixolydian':
        scale_pattern = MIXOLYDIAN
    elif scale == 'locrian':
        scale_pattern = LOCRIAN

    scale = get_holes_notes(start_stage, scale_pattern)
    scale = [note[0] for note in scale]
    return scale


def get_harmonica(tonic='C', tune='richter', scale=[]):
    if tune == 'richter':
        blow_pattern = RICHTER_BLOW
        draw_pattern = RICHTER_DRAW
        draw_bends_pattern = RICHTER_DRAW_BENDS
        blow_bends_pattern = RICHTER_BLOW_BENDS
        overdraw_pattern = RICHTER_OVERDRAW
        overblow_pattern = RICHTER_OVERBLOW

    _tonic = tonic.capitalize()
    start_stage = NOTES.index(_tonic)

    blow = get_holes_notes(start_stage, blow_pattern)
    draw = get_holes_notes(start_stage, draw_pattern)
    draw_bends = get_effect_notes(draw, draw_bends_pattern)
    blow_bends = get_effect_notes(blow, blow_bends_pattern)
    overdraws = get_effect_notes(blow, overdraw_pattern)
    overblows = get_effect_notes(draw, overblow_pattern)

    harmonica_img = draw_harmonica(blow, draw, draw_bends, blow_bends, overdraws, overblows, _tonic, scale)
    _file = BytesIO()
    harmonica_img.save(_file, 'PNG')
    return _file.getvalue()


def write_square(text, hole, position, draw, font, main_color=(13, 13, 13), fill=(255, 255, 255), scale=[]):
    hole_size = (43, 43)
    start_point = (14, 229)

    _position = (
        start_point[0] + (hole_size[0]*hole),
        start_point[1] + position*hole_size[1],
        start_point[0] + (hole_size[0]*hole) + hole_size[0],
        start_point[1] + position*hole_size[1] + hole_size[1],
    )

    draw.rectangle(_position, outline=main_color, fill=fill)

    if text in scale:
        if text == scale[0]:
            draw.rectangle(_position, outline=main_color, fill=(242, 75, 89))
        draw.rectangle((
                _position[0]+5,
                _position[1]+5,
                _position[2]-5,
                _position[3]-5,
        ),
            fill=main_color
        )
        draw.text(
            (
                _position[0] + round((_position[2]-_position[0]-font.getlength(text))/2),
                _position[1] + round((_position[3]-_position[1]-font.size)/2)
            ),
            text,
            fill=fill,
            font=font
        )
    else:
        draw.text(
            (
                _position[0] + round((_position[2]-_position[0]-font.getlength(text))/2),
                _position[1] + round((_position[3]-_position[1]-font.size)/2)
            ),
            text,
            fill=main_color,
            font=font
        )


def draw_harmonica(blow, draw, draw_bends, blow_bends, overdraws, overblows, tonic, scale=[]):
    font = ImageFont.truetype('font.ttf', 18)
    harmonica_img = Image.new('RGB', (500, 500), (255, 255, 255))
    draws = ImageDraw.Draw(harmonica_img)
    draws.rectangle((14, 229, 487, 272), fill=(125, 125, 125))

    write_square(tonic, 0, 0, draws, font, main_color=(255, 255, 255), fill=(125, 125, 125))
    for i in range(1, 11):
        write_square(str(i), i, 0, draws, font, main_color=(255, 255, 255), fill=(125, 125, 125))
    draws.rectangle((486, 229, 487, 272), fill=(125, 125, 125))

    for i, blow_note in enumerate(blow):
        write_square(blow_note[0], i+1, -1, draws, font, scale=scale)
    for i, draw_note in enumerate(draw):
        write_square(draw_note[0], i+1, 1, draws, font, scale=scale)
    for i, overdraws_notes in enumerate(overdraws):
        for j, overdraws_note in enumerate(overdraws_notes):
            write_square(overdraws_note[0], i+1, 2+j, draws, font, main_color=(142, 108, 7), scale=scale)
    for i, overblows_notes in enumerate(overblows):
        for j, overblows_note in enumerate(overblows_notes):
            write_square(overblows_note[0], i+1, -2-j, draws, font, main_color=(142, 108, 7), scale=scale)
    for i, draw_bends_notes in enumerate(draw_bends):
        for j, draw_bends_note in enumerate(draw_bends_notes):
            write_square(draw_bends_note[0], i+1, 2+j, draws, font, main_color=(94, 110, 242), scale=scale)
    for i, blow_bends_notes in enumerate(blow_bends):
        for j, blow_bends_note in enumerate(blow_bends_notes):
            write_square(blow_bends_note[0], i+1, -2-j, draws, font, main_color=(94, 144, 242), scale=scale)
    return harmonica_img


def get_position(harp='C', tonic='C'):
    _tonic = tonic.capitalize()
    position_tonic = CIRCLE_MAJOR.index(_tonic)

    _harp = harp.capitalize()
    position_1 = CIRCLE_MAJOR.index(_harp)

    position = position_tonic - position_1 + 1
    if position <= 0:
        position += len(CIRCLE_MAJOR)

    return position
