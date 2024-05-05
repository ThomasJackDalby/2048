import pyautogui
import random
import time
from colours import COLOURS

VERBOSE = True
DIRECTIONS = ['left', 'up', 'right', 'down']

T_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
T_90 = [3, 7, 11, 15, 2, 6, 10, 14, 1, 5, 9, 13, 0, 4, 8, 12]
T_180 = [T_90[i] for i in T_90]
T_270 = [T_180[i] for i in T_90]
ROTATIONS = [T_0, T_90, T_180, T_270]

TOP = 450
LEFT = 188
X_OFFSET = 125 + 20
Y_OFFSET = 125 + 20

ANIMATION_DELAY = 0.6

SCORE_WEIGHTING = [1.5, 2, 1, 0.5]

def convert_pixel_to_number(pixel):
    try:
        index = COLOURS.index(pixel)
        return 0 if index == 0 else 2 ** index
    except:
        print("Unknown colour...")
        return -1

def read_grid():
    digits = [0] * 16
    image = pyautogui.screenshot(region=(LEFT, TOP, 4 * X_OFFSET, 4 * X_OFFSET))
    for y in range(0, 4):
        for x in range(0, 4):
            pixel = image.getpixel((20 + X_OFFSET * x, 20 + Y_OFFSET * y))
            number = convert_pixel_to_number(pixel)
            digits[y * 4 + x] = number
    return digits

def get_index(x, y):
    return y * 4 + x

def get_merge_score_for_number(number):
    return number ** 2

def get_layout_score(digits):
    score = 0
    total = 0
    for y in range(4):
        for x in range(4):
            digit = digits[get_index(x, y)] ** 2
            total += digit
            score += digit * (6 - x + y)
    score /= total
    return score

def get_merge_score(digits, rotation):
    rotation_matrix = ROTATIONS[rotation]
    rotated_digits = [digits[i] for i in rotation_matrix]
    collapsed_digits = [0] * 16

    merge_score = 0
    for y in range(4):
        row = [rotated_digits[get_index(x, y)] for x in range(4)]
        collapsed_row = [0] * 4
        # shunts every non-zero value to the left 
        j = 0
        for i in range(4):
            if row[i] != 0:
                collapsed_row[j] = row[i]
                collapsed_digits[get_index(j, y)] = row[i]
                j += 1

        row = [collapsed_row[x] for x in range(4)]
        if row[0] == 0: continue
        elif row[0] == row[1]:
            merged_value = 2 * row[0]
            merge_score += get_merge_score_for_number(merged_value)
            collapsed_row[0] = merged_value

            if row[2] != 0 and row[2] == row[3]:
                merged_value = 2 * row[2]
                merge_score += get_merge_score_for_number(merged_value)
                collapsed_row[1] = merged_value
            else:
                collapsed_row[1] = row[2]
                collapsed_row[2] = row[3]

        elif row[1] == 0: continue
        elif row[1] == row[2]:
            merged_value = 2 * row[1]
            merge_score += get_merge_score_for_number(merged_value)
            collapsed_row[1] = merged_value
            collapsed_row[2] = row[2]

        elif row[2] == 0: continue
        elif row[2] == row[3]:
            merged_value = 2 * row[2]
            merge_score += get_merge_score_for_number(merged_value)
            collapsed_row[2] = merged_value

    for i in range(4): collapsed_digits[get_index(i, y)] = collapsed_row[i]

    unrotation_matrix = ROTATIONS[3 - rotation]
    unrotated_digits = [collapsed_digits[i] for i in unrotation_matrix]

    return merge_score, unrotated_digits

def get_score(digits, rotation, level=0):

    merge_score, collapsed_digits = get_merge_score(digits, rotation)
    layout_score = get_layout_score(collapsed_digits)
    look_ahead_score = 0

    if level > 0:
        scores = [get_score(collapsed_digits, i, level-1) for i in range(4)]
        look_ahead_score += max(scores) * 0.5

    score = (merge_score + layout_score + look_ahead_score) * SCORE_WEIGHTING[rotation]
    return score 

last_digits = None
last_direction = None
random_direction_indexes = [0,1,2,3]

while True:
    digits = read_grid()
    mode = ""
    if (last_digits is not None
        and all((digits[i] == last_digits[i] for i in range(16)))):
        mode = "random"
        direction_index = random.choice(random_direction_indexes)
    else:
        mode = "score"
        # reset the random directions
        random_direction_indexes = [0,1,2,3]

        # calculate the scores for each rotation
        scores = [get_score(digits, i, 3) for i in range(4)]
        
        # get the maximum score, and if multiple directions have the same score, choose equally between them.
        max_score = max(scores)
        directions = [i for i, score in enumerate(scores) if score == max_score]
        direction_index = random.choice(directions)

    direction = DIRECTIONS[direction_index]

    if VERBOSE:
        if mode == "random": print(mode, direction)
        elif mode == "score": print(mode, direction, max_score, scores)
    last_direction = direction_index
    random_direction_indexes.remove(last_direction)

    if VERBOSE:
        for y in range(4): print(digits[y * 4:(y+1) * 4])
        print()

    last_digits = digits

    pyautogui.press(direction)
    time.sleep(ANIMATION_DELAY)