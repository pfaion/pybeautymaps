from pybeautymaps import Beautymap


def main():
    m = Beautymap.square_centered(center_latlon=(48.873768, 2.295046), width=4.0)
    m.render_square_png(
        filename='paris.png',
        size=2000,
        padding=50,
        line_widths={
            'trunk': 5,
            'primary': 4,
            'secondary': 3,
            'tertiary': 2,
        }
    )


if __name__ == "__main__":
    main()
