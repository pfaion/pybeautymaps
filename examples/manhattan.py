from pybeautymaps import Beautymap

def main():
    m = Beautymap.square_centered((40.757667, -73.983715), 8.0)
    m.render_square_png('manhattan.png', 2000, 50,
        line_widths={
            'trunk': 5,
            'primary': 4,
            'secondary': 3,
            'tertiary': 2,
        }
    )

if __name__ == "__main__":
    main()
