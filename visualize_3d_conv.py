from types import MethodType

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from voxels import voxels

# Set label font size and family
plt.rcParams["font.size"] = 12
plt.rcParams["font.family"] = "sans-serif"

# Colors
ALPHA = 50  # in hex
INPUT_COLOR = f"#1abc9c{ALPHA}"
FILTER_COLOR = "#e67e22"
OUTPUT_COLOR = f"#3498db{ALPHA}"
EDGE_COLOR = "#2c3e50"
DARK_MODE = False

if DARK_MODE:
    plt.style.use("dark_background")

# Convolution parameters
INPUT_SHAPE = (5, 5, 5)
FILTER_SHAPE = (3, 3, 3)

PADDING = (0, 0, 0)
STRIDE = (1, 1, 1)

OUTPUT_SHAPE = (
    ((INPUT_SHAPE[0] - FILTER_SHAPE[0] + 2 * PADDING[0]) // STRIDE[0]) + 1,
    ((INPUT_SHAPE[1] - FILTER_SHAPE[1] + 2 * PADDING[1]) // STRIDE[1]) + 1,
    ((INPUT_SHAPE[2] - FILTER_SHAPE[2] + 2 * PADDING[2]) // STRIDE[2]) + 1,
)


# Create figure
fig = plt.figure(figsize=(10, 5))
# set title
fig.suptitle(
    "3D Convolution",
    fontsize=16,
    fontweight="bold",
    fontfamily="serif",
)
# add description
fig.text(
    0.5, 0.9, f"stride: {STRIDE}, padding: {PADDING}", ha="center", fontfamily="serif"
)
fig.tight_layout()

# Create subplot 1
ax1 = fig.add_subplot(121, projection="3d")
ax1.voxels = MethodType(voxels, ax1)

# Create subplot 2
ax2 = fig.add_subplot(122, projection="3d")
ax2.voxels = MethodType(voxels, ax2)

# add titles to subplots under the plots
ax1.set_title(
    f"Input Volume ({'x'.join(map(str, INPUT_SHAPE))})", y=0.95, fontweight="bold"
)
ax2.set_title(
    f"Output Volume ({'x'.join(map(str, OUTPUT_SHAPE))})", y=0.95, fontweight="bold"
)

if DARK_MODE:
    for ax in [ax1, ax2]:
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

for ax in [ax1, ax2]:
    # set 0,0 to be top left corner
    ax.invert_zaxis()
    ax.invert_xaxis()
    ax.invert_yaxis()

    # add labels
    ax.set_xlabel("width")
    ax.set_ylabel("height")
    ax.set_zlabel("depth")

    # initial view angle front
    ax.view_init(20, 110)

# Create data
x, y, z = np.indices(INPUT_SHAPE)

# Set the colors of each object
cube1 = (x < INPUT_SHAPE[0]) & (y < INPUT_SHAPE[1]) & (z < INPUT_SHAPE[2])
cube2 = (x < OUTPUT_SHAPE[0]) & (y < OUTPUT_SHAPE[1]) & (z < OUTPUT_SHAPE[2])

# create animation
def animate(i):
    # change color of cube 1
    colors = np.empty(cube1.shape, dtype=object)
    colors2 = np.empty(cube2.shape, dtype=object)
    colors[cube1] = INPUT_COLOR
    colors2[cube2] = OUTPUT_COLOR

    x = (i % OUTPUT_SHAPE[0]) * STRIDE[0]
    z = ((i // OUTPUT_SHAPE[0]) % OUTPUT_SHAPE[2]) * STRIDE[2]
    y = ((i // (OUTPUT_SHAPE[0] * OUTPUT_SHAPE[2])) %
         OUTPUT_SHAPE[1]) * STRIDE[1]

    colors[
        x: FILTER_SHAPE[0] + x, y: FILTER_SHAPE[1] + y, z: FILTER_SHAPE[2] + z
    ] = FILTER_COLOR
    colors2[
        x // STRIDE[0]: 1 + x // STRIDE[0],
        y // STRIDE[1]: 1 + y // STRIDE[1],
        z // STRIDE[2]: 1 + z // STRIDE[2],
    ] = FILTER_COLOR

    ax1.collections.clear()
    ax2.collections.clear()

    ax1.voxels(cube1, facecolors=colors, edgecolors=EDGE_COLOR,
               internal_faces=True, animated=True)
    ax2.voxels(cube2, facecolors=colors2, edgecolors=EDGE_COLOR,
               internal_faces=True, animated=True)

    # return the artists set
    return fig,


anim = FuncAnimation(
    fig,
    animate,
    frames=OUTPUT_SHAPE[0] * OUTPUT_SHAPE[1] * OUTPUT_SHAPE[2],
    # frames=16,
    interval=200,
    blit=True,
)
anim.save(f"animations/3d_convolution{'_dark' if DARK_MODE else ''}.gif",
          writer="ffmpeg", dpi=200, fps=4)
