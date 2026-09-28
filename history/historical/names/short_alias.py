import re, math
import numpy as np

def candidate_matches(text, actors, suffixes):
    found = []
    for actor in actors:
        name = r'\s*'.join(map(re.escape, actor['given_name']))
        pattern = r'(?<![가-힣])(?P<name>' + name + r')(?P<gap>\s*)(?P<suffix>' + '|'.join(map(re.escape, suffixes)) + r')(?=$|[^가-힣])'
        for m in re.finditer(pattern, text):
            found.append({'start': m.start('name'), 'end': m.end('name'), 'quote': m.group('name'),
                          'suffix': m.group('suffix'), 'staff_id': actor['staff_id'], 'token': actor['token'],
                          'canonical_name': actor['name'], 'name_form': 'given_name', 'action': 'erase_and_existing_token'})
    return found

def runs(values):
    edges = np.diff(np.r_[False, values, False].astype(np.int8))
    return list(zip(np.flatnonzero(edges == 1).tolist(), np.flatnonzero(edges == -1).tolist()))

def locate_prefix(im, candidate):
    """Measured ink/gaps, not proportional subdivision of the OCR line box.

    This route requires a horizontal initial two-syllable name + one honorific.
    It finds the first ink word, drops punctuation from its measured outline,
    and locates a blank-column seam before the suffix. Ambiguous layouts stop.
    """
    w, h = im.size; b = candidate['line_box']
    rh = b['height'] * h
    if b['width'] * w < rh or len(candidate['quote'].replace(' ', '')) != 2:
        raise ValueError('UNSUPPORTED_ORIENTATION_OR_NAME_FORM')
    x0 = max(0, math.floor(b['x'] * w) - 8)
    y0 = max(0, math.floor(b['y'] * h) - 3)
    x1 = min(w, x0 + max(220, math.ceil(rh * 7)))
    y1 = min(h, math.ceil((b['y'] + b['height']) * h) + 3)
    gray = np.array(im.convert('L'))[y0:y1, x0:x1]
    binary = gray < 170
    rule_rows = np.flatnonzero(binary.sum(axis=1) > gray.shape[1] * .55)
    for y in rule_rows:
        binary[max(0, y - 2):min(binary.shape[0], y + 3)] = False
    bands = runs(binary.any(axis=0))
    if len(bands) < 3:
        raise ValueError('NAME_AND_SUFFIX_NOT_SEGMENTED')
    word = [bands[0]]
    for band in bands[1:]:
        if band[0] - word[-1][1] > rh * .85:
            break
        word.append(band)
    while len(word) > 1:
        yy, xx = np.where(binary[:, word[-1][0]:word[-1][1]])
        if len(yy) and yy.max() - yy.min() + 1 < rh * .45:
            word.pop()
        else:
            break
    if len(word) < 2:
        raise ValueError('NO_BLANK_SEAM_BEFORE_SUFFIX')
    yy, xx = np.where(binary[:, word[0][0]:word[-1][1]])
    glyph_h = int(yy.max() - yy.min() + 1)
    choices = []
    for i in range(1, len(word)):
        prefix_width = word[i-1][1] - word[0][0]
        suffix_width = word[-1][1] - word[i][0]
        # The preserved 씨 starts with substantial consonant ink. A narrow
        # detached vertical stroke is not a new suffix start; it can belong
        # to the final vowel of the second name syllable. This adds evidence, not a lower threshold.
        if word[i][1] - word[i][0] < .28 * glyph_h:
            continue
        if not (.9 * glyph_h <= prefix_width <= 3.0 * glyph_h and .45 * glyph_h <= suffix_width <= 1.5 * glyph_h):
            continue
        gap = word[i][0] - word[i-1][1]
        score = abs(suffix_width / glyph_h - .85) + .4 * abs(prefix_width / glyph_h - 1.75) - .01 * min(gap, 6)
        choices.append((score, i, gap))
    choices.sort()
    if not choices:
        raise ValueError('NO_PLAUSIBLE_SUFFIX_BOUNDARY')
    best = choices[0]
    margin = choices[1][0] - best[0] if len(choices) > 1 else 99.0
    if margin < .10:
        raise ValueError('AMBIGUOUS_SUFFIX_BOUNDARY')
    i = best[1]; seam = (word[i-1][1] + word[i][0]) // 2
    yy, xx = np.where(binary[:, word[0][0]:word[i-1][1]])
    ink = [x0 + word[0][0] + int(xx.min()), y0 + int(yy.min()),
           x0 + word[0][0] + int(xx.max()) + 1, y0 + int(yy.max()) + 1]
    erase = [max(0, ink[0]-1), max(0, ink[1]-1), min(x0+seam, ink[2]+1), min(h, ink[3]+1)]
    suffix = [x0 + word[i][0], y0, x0 + word[-1][1], y1]
    return {'ink_box': ink, 'erase_box': erase, 'protected_suffix_box': suffix,
            'method': 'saved_ocr_anchor_measured_word_ink_and_suffix_seam',
            'geometry_evidence': {'seam_x': x0+seam, 'blank_gap_px': best[2],
                                  'score_margin': round(margin, 4), 'removed_rule_rows': len(rule_rows)}}
