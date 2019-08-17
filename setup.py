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
    'coverage==4.*', # coverage 5.* has SQLite output and is not compatible with coveralls 
    'pytest-cov',
)

setup(
    name="pybeautymaps",
    version="0",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
