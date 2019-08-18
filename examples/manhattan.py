from pybeautymaps import Beautymap


def main():
    m = Beautymap.square_centered(center_latlon=(40.757667, -73.983715), width=8.0)
    m.render_square_png(
        filename='manhattan.png',
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
