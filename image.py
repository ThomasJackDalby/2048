import pyautogui

top = 450  # location.top + 442 - 237 + 8
left = 188  # location.left + 20
tile_width = 125
tile_height = 125
x_offset = tile_width + 20
y_offset = tile_height + 20
print(f"Found anchor at {left} {top}")

def read_grid():
    digits = [0] * 16
    image = pyautogui.screenshot(
        region=(left, top, 4 * x_offset, 4 * x_offset))
    for y in range(0, 4):
        for x in range(0, 4):
            pixel = image.getpixel((20 + x_offset * x, 20 + y_offset * y))
            try:
                index = colours.index(pixel)
            except:
                colours.append(pixel)
                index = len(colours) - 1
                print(f"Found colour for {2 ** index}")
            digits[y * 4 + x] = 0 if index == 0 else 2 ** index
    return digits