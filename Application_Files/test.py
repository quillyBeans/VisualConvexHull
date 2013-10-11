from convexHull import convexHull

testPoints = []
testPoints.append((1, 1))
testPoints.append((1, 5))
testPoints.append((10, 10))
testPoints.append((2, 8))
testPoints.append((3, 3))

print 'testPoints', testPoints
newPoints = convexHull(testPoints)
print 'newPoints', newPoints
print 'point (3,3) should be excluded as it is inside of the convex hull'