# pybeautymaps


[![Travis Build](https://travis-ci.org/pfaion/pybeautymaps.svg?branch=master)](https://travis-ci.org/pfaion/pybeautymaps)
[![Coveralls Coverage](https://coveralls.io/repos/github/pfaion/pybeautymaps/badge.svg?branch=master)](https://coveralls.io/github/pfaion/pybeautymaps?branch=master)

This is a library for creating beautyful map images with python.

![Example Image](examples/manhattan.png)


## Installation

```bash
pip install git+https://github.com/pfaion/pybeautymaps
```


## Quick-Start

Take a look at the [examples](examples) folder for different renderings.

```python
from pybeautymaps import Beautymap

m = Beautymap.square_centered(
    center_latlon=(40.757667, -73.983715),
    width=8.0
)

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
```

## TODO
A brief list of what additional features are planned:

- [ ] Add option to show rivers
- [ ] Add option to use custom colors
- [ ] Add more rendering shapes (rectangular, circular, ...)
- [ ] Add more output formats (jpg, pdf, svg, ...)
- [ ] Add debugging support via iPython

  - [ ] Return image as iPython image
  - [ ] Plot different road types in different colors
  - [ ] Cache data for every road type separately
