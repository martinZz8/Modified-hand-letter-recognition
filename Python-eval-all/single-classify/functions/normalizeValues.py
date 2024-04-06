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


def normalizeValues(vals,
                    a,
                    b,
                    x_min,
                    x_max,
                    isInt = True,
                    usetwoDecimalPoints = True):
    """Normalizes 2D array of numerous values to specified range.

      Args:
        vals (2D arr of floats): 2D array of values to normalize
        a (double): new maximum value
        b (double):  new maximum value

      Returns:
        2D array of normalized values

      Raises:
    """
    new_vals = []

    normalizeFunctionToUse = normalizeSingleValueInt if isInt else normalizeSingleValueFloat

    if len(vals) > 0:
        rows = len(vals)
        cols = len(vals[0])
        new_vals = [[0] * cols for i in range(rows)]

        for i in range(rows):
            for j in range(cols):
                new_vals[i][j] = normalizeFunctionToUse(vals[i][j], a, b, x_min, x_max)

                if usetwoDecimalPoints:
                    new_vals[i][j] = round(new_vals[i][j], 2)

    return new_vals


def normalizeValuesOwnRowCol(vals,
                             a_fir,
                             b_fir,
                             a_sec,
                             b_sec,
                             x_min_fir,
                             x_max_fir,
                             x_min_sec,
                             x_max_sec,
                             isInt = True,
                             useTwoDecimalPoints = True):
    """Normalizes 2D array of numerous values to specified range.

      Args:
        vals (2D arr of floats): 2D array of values to normalize
        a_fir (double): new minimum value of first element in row
        b_fir (double): new maximum value of first element in row
        a_sec (double): new minimum value of second (or further) element in row
        b_sec (double): new maximum value of second (or further) element in row
        x_min_fir (double): old minimum value of first element in row
        x_max_fir (double): old maximum value of first element in row
        x_min_sec (double): old minimum value of second (or further) element in row
        x_max_sec (double): old maximum value of second (or further) element in row

      Returns:
        2D array of normalized values

      Raises:
    """
    new_vals = []

    normalizeFunctionToUse = normalizeSingleValueInt if isInt else normalizeSingleValueFloat

    if len(vals) > 0:
        rows = len(vals)
        cols = len(vals[0])
        new_vals = [[0] * cols for i in range(rows)]

        for i in range(rows):
            for j in range(cols):
                a_to_pass, b_to_pass = (a_fir, b_fir) if j == 0 else (a_sec, b_sec)
                x_min_to_pass, x_max_to_pass = (x_min_fir, x_max_fir) if j == 0 else (x_min_sec, x_max_sec)

                new_vals[i][j] = normalizeFunctionToUse(vals[i][j],
                                                        a_to_pass,
                                                        b_to_pass,
                                                        x_min_to_pass,
                                                        x_max_to_pass)

                if useTwoDecimalPoints:
                    new_vals[i][j] = round(new_vals[i][j], 2)

    return new_vals
