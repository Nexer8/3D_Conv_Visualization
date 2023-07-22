# Colors
ALPHA = "50"  # in hex
EDGE_COLOR = "#2c3e50"

INPUT_COLOR = f"#1abc9c{ALPHA}"
FILTER_COLOR = "#e67e22"
OUTPUT_COLOR = f"#3498db{ALPHA}"

# Convolution Parameters
INPUT_SHAPE = (5, 5, 5)
FILTER_SHAPE = (3, 3, 3)

PADDING = (0, 0, 0)
STRIDE = (1, 1, 1)

OUTPUT_SHAPE = (
    ((INPUT_SHAPE[0] - FILTER_SHAPE[0] + 2 * PADDING[0]) // STRIDE[0]) + 1,
    ((INPUT_SHAPE[1] - FILTER_SHAPE[1] + 2 * PADDING[1]) // STRIDE[1]) + 1,
    ((INPUT_SHAPE[2] - FILTER_SHAPE[2] + 2 * PADDING[2]) // STRIDE[2]) + 1,
)
