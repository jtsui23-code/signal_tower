import math
from itertools import pairwise
class Path:
    def __init__(self, points):

        # A list of (x,y) tuples for the path
        self.positions = points


        # Long form:
        # for i in range(len(self.positions) - 1):
        #     a = self.positions[i]
        #     b = self.positions[i + 1]
        #     self.totalLength += math.dist(a, b)

        # Calculates the total distance of the path based off of the way points of the path
        self.totalLength = sum(math.dist(a,b) for a,b in pairwise(points))

    def calculatePosition(self,distance):
        # Pairs position tuples i & i+1
        for start, end in pairwise(self.positions):
            segmentLength = math.dist(start, end)

            if distance <= segmentLength:

                # Calculate how far along the enemy is on on the segment
                ratio = distance/segmentLength

                # Return position of enemy
                return (start[0] + (end[0] - start[0])*ratio, start[1] + (end[1] - start[1])*ratio)

            # If the Enemy is not at this point then subtract the left over distance and check the next point
            distance -= segmentLength
        # If the enemy is not found then they already passed the finish line
        return self.positions[-1]

if __name__ == "__main__":

    path = Path([(0, 60), (200, 60), (200, 250)])
    assert path.totalLength == 390
    assert path.calculatePosition(0) == (0, 60)
    assert path.calculatePosition(260) == (200, 120)
    assert path.calculatePosition(9999) == (200, 250)
    print("Path checks passed.")

