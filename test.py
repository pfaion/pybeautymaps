# %%

import pybeautymaps as pbm

m = pbm.Beautymap(bbox=(51.272611, 9.463197, 51.299340, 9.524970))
m.render_square_png(
    filename='test.png',
    size=2000,
    padding=50,
    line_widths={
        'trunk': 5,
        'primary': 4,
        'secondary': 3,
        'tertiary': 2,
    }
)

# %%