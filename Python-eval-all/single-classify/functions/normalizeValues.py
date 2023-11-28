import math


# Integer normalization
def normalizeSingleValueInt(val, a, b, x_min=0, x_max=1):
    new_val = math.floor(
        (val - x_min) * (b - a + 1) / (x_max - x_min)
    ) + a

    return new_val


# Float normalization
def normalizeSingleValueFloat(val, a, b, x_min=0, x_max=1):
    new_val = (val - x_min) * (b - a) / (x_max - x_min) + a

    return new_val


def normalizeValues(vals, a, b, isInt = True):
    """Normalizes 2D array of numerous values to specified range.

      Args:
        vals (2D arr of floats): 2D array of values to normalize
        a (double): new maximum value
        b (double):  new maximum value

      Returns:
        2D array of normalized values

      Raises:
    """
    x_min = vals.min().item()  # old minimum value
    x_max = vals.max().item()  # old maximum value

    new_vals = []

    normalizeFunctionToUse = normalizeSingleValueInt if isInt else normalizeSingleValueFloat

    if len(vals) > 0:
        rows = len(vals)
        cols = len(vals[0])
        new_vals = [[0] * cols for i in range(rows)]

        for i in range(rows):
            for j in range(cols):
                new_vals[i][j] = normalizeFunctionToUse(vals[i][j], a, b, x_min, x_max)

    return new_vals
