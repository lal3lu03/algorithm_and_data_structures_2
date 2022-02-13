from random import random


class MonteCarlo:

    def __init__(self, length, width, rectangles):
        """constructor

        Keyword arguments:
        :param length -- length of the enclosing rectangle
        :param width -- width of the enclosing rectangle
        :param rectangles -- array that contains the embedded rectangles
        """
        self.length, self.width, self.rectangles = length, width, rectangles

    def area(self, num_of_shots):
        """Method to estimate the area of the enclosing rectangle that is not covered by the embedded rectangles

        Keyword arguments:
        :param num_of_shots -- Number of generated random points whose location (inside/outside) is analyzed
        :return float -- the area of the enclosing rectangle not covered.
        :raises ValueError if any of the parameters is None
        """
        if self.length is None or self.width is None or num_of_shots is None or self.rectangles is None: raise ValueError
        total = []
        for strike in range(num_of_shots): x = random() * self.length; y = random() * self.width; total.append((x, y))

        enumeration = 0
        shots = 0
        score = False

        for strike in total:
            for hit in self.rectangles:
                if self.inside(strike[0], strike[1], hit): score = True; break
            if score is True: shots += 1
            else: enumeration += 1; shots += 1
            score = False

        field = self.length * self.width
        return field * (enumeration / shots)

    def inside(self, x, y, rect):
        """Method to determine if a given point (x,y) is inside a given rectangle

        Keyword arguments:
        :param x,y -- coordinates of the point to check
        :param rect -- given rectangle
        :return bool
        :raises ValueError if any of the parameters is None
        """
        if x is None or y is None or rect is None: raise ValueError

        org_x, org_y = rect.origin_x, rect.origin_y

        if org_x <= x <= org_x + rect.length and org_y <= y <= org_y + rect.width: return True
        else: return False