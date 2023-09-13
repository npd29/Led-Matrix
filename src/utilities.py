def rgb_to_hex(r, g, b) -> str:
    return '0x'+'{:02x}{:02x}{:02x}'.format(r, g, b).upper()


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return rgb


def convert_brightness(color: str, brightness: float) -> int:
    rgb_color = hex_to_rgb(color.lstrip('0x'))
    for i in range(len(rgb_color)):
        rgb_color[i] = int(rgb_color[i] * brightness)
    return int(rgb_to_hex(rgb_color[0], rgb_color[1], rgb_color[2]))