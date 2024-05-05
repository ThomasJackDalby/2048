COLOURS_HEX = [  
    "#eee4da",
    "#ede0c8",
    "#f2b179",
    "#f59563", 
    "#f67c5f",
    "#f65e3b",
    "#edcf72",
    "#edcc61",
    "#edc850",
    "#edc53f",
    "#edc22e"
]

def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

COLOURS = [(205, 193, 180)] + [hex_to_rgb(hex) for hex in COLOURS_HEX]