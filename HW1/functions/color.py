import re

from .base import normalizer, build_question

all_colors = []

with open("colors.txt", encoding="utf-8") as f:
    for color in f:
        color = color.strip()
        normalizer.normalize(color)
        if len(color) > 2:
            # add before the simple color to have priority
            all_colors.append(f'رنگ {color}')
            all_colors.append(f'{color} رنگ')
            all_colors.append(color)

all_colors_group = "|".join(all_colors)
color_pattern = f' ({all_colors_group})(( و|،) ({all_colors_group}))* '


def color(input: str):
    a = re.search(color_pattern, input)
    if a is not None:
        qu = build_question(re.sub(color_pattern, " چه رنگی ", input, 1))
        return qu, a.group(), True
    else:
        return None, None, False

