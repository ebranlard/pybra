[![Build Status](https://travis-ci.org/ebranlard/pybra.svg?branch=master)](https://travis-ci.org/ebranlard/pybra)

# pybra

My small python library. Pybra stands from "python" and "ebra" (E. Branlard)

- `colors.py`: colors and color tools
- `compare.py`: compare two python variables (classes, arrays,..) and provides a listing of the differences (e.g. property missing, different values)
- `figlib.py`: tools to place figures on the screen
- `galib.py`:  tools for genetic algorithms (based on deap)
- `pandalib.py`: convenient functions tomanipulate pandas data (interpolation, etc.)
- `signal.py`: signal processing tools (detection of zero\_crossing, etc.)
- `tictoc.py`: timing tools, provides a context manager to time functions or piece of code


# Installation and testing
```bash
git clone http://github.com/ebranlard/pybra
cd pybra
python -m pip install -r requirements.txt
python -m pip install -e .
pytest
```
