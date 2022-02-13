from montecarlo import MonteCarlo
from rectangle import Rectangle


def main():
    for i in [10, 100, 1000, 100000]: print(MonteCarlo(100, 30, [Rectangle(0, 0, 50, 30)]).area(i))


if __name__ == '__main__':
    main()
