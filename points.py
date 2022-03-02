from email.mime import base
from vectors import Vector as Vec
import math


class FlightPlan:
    def __init__(
        self, subject=Vec(0, 0, 0), camera=Vec(1, 1, 1), fov=Vec(5, 5), step=1, theta=0
    ):
        assert fov.x > 0 or fov.y > 0, "FOV must not have zero dimension"
        assert step < fov.x or step < fov.y, "Step must be smaller than the FOV"

        self.subject = subject
        self.camera = camera
        self.fov = fov
        self.step = step
        self.theta = theta


def split_points(array):
    x = [a.x for a in points]
    y = [a.y for a in points]
    z = [a.z for a in points]

    return x, y, z


def calculate(plan):
    offset = plan.camera - plan.subject
    theta = math.asin(offset.z / offset.size())
    heading = math.atan2(offset.y, offset.z)

    points = []

    Nx = math.floor(plan.fov.width / plan.step) + 1
    Nz = math.floor(plan.fov.height / plan.step) + 1

    for x in range(Nx):
        for z in range(Nz):
            posn = Vec(x, 0, z)
            if x % 2 != 0:
                posn.z = Nz - z - 1

            # Place point at origin
            posn *= plan.step
            posn.x -= plan.fov.width / 2
            posn.z -= plan.fov.height / 2

            # Adjust X rotation of plane
            dist = Vec(posn.z, posn.y).size()
            angle = math.atan2(posn.y, posn.z) + theta + (math.pi / 2)
            posn = Vec(posn.x, dist * math.sin(angle), dist * math.cos(angle))

            # Adjust Z rotation of plane
            dist = Vec(posn.x, posn.y).size()
            angle = math.atan2(posn.y, posn.x) + heading - (math.pi / 2)
            posn = Vec(dist * math.cos(angle), dist * math.sin(angle), posn.z)

            # Translate point to camera
            posn += plan.camera

            points.append(posn)

    return points


plan = FlightPlan(
    subject=Vec(0, 0, 0),
    camera=Vec(10, 15, 10),
    fov=Vec(12, 8),
    step=1,
    theta=math.radians(0),
)

points = calculate(plan)


import numpy as np
import matplotlib.pyplot as plt

x, y, z = split_points(points)

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection="3d")

ax.set_xlabel("x", fontsize=24)
ax.set_ylabel("y", fontsize=24)
ax.set_zlabel("z", fontsize=24)

ax.scatter(plan.subject.x, plan.subject.y, plan.subject.z, c="blue")
ax.scatter(plan.camera.x, plan.camera.y, plan.camera.z, c="blue", s=100)
ax.plot(x, y, z, ".r-")

plt.show()
