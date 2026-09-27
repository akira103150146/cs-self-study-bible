"""任務 1 參考解:和 sum.c 做一模一樣的事。"""
import sys


def main():
    print(sum(int(tok) for tok in sys.stdin.read().split()))


if __name__ == "__main__":
    main()
