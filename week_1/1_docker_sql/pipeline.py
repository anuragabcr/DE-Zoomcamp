import sys
import pandas as pd

print(sys.argv)
print("Pandas Version:- ", pd.__version__)
day = sys.argv[1]
print(f"Day passed in the argument: {day}")

print("Pipeline completed")