filepath = "enter your filepath here"
with open(filepath, "rb") as file:
    file.seek(0x1c)
    color_depth = file.read(1)[0] | file.read(1)[0] << 8
    print("Color depth:", color_depth)

    file.seek(0x1e)
    compression = file.read(1)[0] | file.read(1)[0] << 8
    print("Compression:", compression)

    file.seek(0x2e)
    colors = file.read(1)[0] | file.read(1)[0] << 8 | file.read(1)[0] << 16 | file.read(1)[0] << 24
    print("Colors:", colors)

    print("Is true color BMP: ", colors == 0 and color_depth >= 16)
