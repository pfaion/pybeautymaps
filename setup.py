from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'numpy',
    'overpy',
    'pycairo',
    'pyproj',
]

setup_requires = [
    'pytest-runner',
]

tests_require = [
    'pytest',
    # coverage 5.* has SQLite output and is not compatible with coveralls
    # pytest-cov will automatically install coverage 5.* though!
    'coverage==4.*',
    'pytest-cov',
]

setup(
    name="pybeautymaps",
    version="0",
    author="Patrick Faion",
    description="Beautiful images of street maps made with python.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="art beautiful maps street-maps openstreetmaps",
    urls="https://github.com/pfaion/pybeautymaps",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
