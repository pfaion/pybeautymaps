from setuptools import setup, find_packages

install_requires = (
    'pycairo',
    'numpy',
    'overpy',
    'pyproj',
)

setup_requires = [
    'pytest-runner',
]

tests_require = (
    'pytest',
)

setup(
    name="pybeautymaps",
    version="0",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)