from vectors import Vector as Vec
import plotly.graph_objects as go
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
    offset = plan.subject - plan.camera
    theta = math.asin(offset.z / offset.size())
    heading = math.atan2(offset.y, offset.x)

    points = []

    Nx = math.floor(plan.fov.width / plan.step) + 1
    Ny = math.floor(plan.fov.height / plan.step) + 1

    for x in range(Nx):
        for y in range(Ny):
            posn = Vec(x, y, 0)
            if x % 2 != 0:
                posn.y = Ny - y - 1

            # Place point at origin
            posn *= plan.step
            posn.x -= plan.fov.width / 2
            posn.y -= plan.fov.height / 2

            # Adjust X rotation of plane
            dist = Vec(posn.z, posn.y).size()
            angle = math.atan2(posn.y, posn.z) + theta + (math.pi / 2)
            posn = Vec(posn.x, dist * math.sin(angle), dist * math.cos(angle))

            # Adjust Z rotation of plane
            dist = Vec(posn.x, posn.y).size()
            angle = math.atan2(posn.y, posn.x) + heading + (math.pi / 2)
            posn = Vec(dist * math.cos(angle), dist * math.sin(angle), posn.z)

            # Translate point to camera
            posn += plan.camera

            points.append(posn)

    return points


def plot(plan, points):
    x, y, z = split_points(points)

    flight_path = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        marker=dict(
            size=1,
            color=list(range(len(x))),
        ),
        line=dict(color="darkblue", width=1),
    )

    x0, y0, z0 = plan.camera.x, plan.camera.y, plan.camera.z
    x1, y1, z1 = plan.subject.x, plan.subject.y, plan.subject.z

    subject_arrow = go.Scatter3d(
        x=[x0, x1],
        y=[y0, y1],
        z=[z0, z1],
        mode="lines",
        line=dict(width=2, color="red"),
    )

    fig = go.Figure(data=[flight_path, subject_arrow])

    # https://stackoverflow.com/questions/66789390/draw-an-arrow-between-two-specific-points-in-a-scatter-plot-with-plotly-graph-ob
    arrow_tip_ratio = 0.05
    arrow_starting_ratio = 0.98

    fig.add_trace(
        go.Cone(
            x=[x0 + arrow_starting_ratio * (x1 - x0)],
            y=[y0 + arrow_starting_ratio * (y1 - y0)],
            z=[z0 + arrow_starting_ratio * (z1 - z0)],
            u=[arrow_tip_ratio * (x1 - x0)],
            v=[arrow_tip_ratio * (y1 - y0)],
            w=[arrow_tip_ratio * (z1 - z0)],
            showlegend=False,
            showscale=False,
            colorscale=[[0, "red"], [1, "red"]],
        )
    )

    return fig


plan = FlightPlan(
    subject=Vec(0, 5, 0),
    camera=Vec(30, 40, 10),
    fov=Vec(12, 8),
    step=0.5,
    theta=math.radians(0),
)

points = calculate(plan)
figure = plot(plan, points)

figure.show()
