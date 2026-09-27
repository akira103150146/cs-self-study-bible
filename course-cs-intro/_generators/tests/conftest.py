import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # _generators/
sys.path.insert(0, HERE)                    # tests/helpers.py
