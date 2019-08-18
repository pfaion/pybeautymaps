from pathlib import Path

import pybeautymaps as pbm

def test_beautymap_general_workflow(tmp_path):
    file_path: Path = tmp_path / 'test.png'

    assert not file_path.exists()

    line_widths = dict(
        trunk=5,
        primary=4,
        secondary=3,
        tertiary=2,
    )
    m = pbm.Beautymap.square_centered(center_latlon=(37.030347, -93.473126), width=1.2)
    m.render_square_png(file_path, size=1000, padding=50, line_widths=line_widths)

    assert file_path.exists()
