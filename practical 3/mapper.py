import sys

for line in sys.stdin:
    for char in line.strip():
        if char != " ":
            print(f"{char}\t1")