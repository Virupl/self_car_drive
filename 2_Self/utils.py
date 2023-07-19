def lerp(A, B, t):
    return A + (B - A) * t


def getIntersection1(A, B, C, D):
    tTop = (D['x'] - C['x']) * (A['y'] - C['y']) - \
        (D['y'] - C['y']) * (A['x'] - C['x'])
    uTop = (C['y'] - A['y']) * (A['x'] - B['x']) - \
        (C['x'] - A['x']) * (A['y'] - B['y'])
    bottom = (D['y'] - C['y']) * (B['x'] - A['x']) - \
        (D['x'] - C['x']) * (B['y'] - A['y'])

    if bottom != 0:
        t = tTop / bottom
        u = uTop / bottom
        if t >= 0 and t <= 1 and u >= 0 and u <= 1:
            return {
                'x': lerp(A['x'], B['x'], t),
                'y': lerp(A['y'], B['y'], t),
                'offset': t
            }

    return None


def getIntersection2(A, B, C, D):
    tTop = (D[0] - C[0]) * (A[1] - C[1]) - (D[1] - C[1]) * (A[0] - C[0])
    uTop = (C[0] - A[0]) * (A[1] - B[1]) - (C[1] - A[1]) * (A[0] - B[0])
    bottom = (D[1] - C[1]) * (B[0] - A[0]) - (D[0] - C[0]) * (B[1] - A[1])

    if bottom != 0:
        t = tTop / bottom
        u = uTop / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = A[0] + t * (B[0] - A[0])
            y = A[1] + t * (B[1] - A[1])
            return x, y

    return None


def polysIntersect(poly1, poly2):
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            touch = getIntersection1(
                poly1[i],
                poly1[(i + 1) % len(poly1)],
                poly2[j],
                poly2[(j + 1) % len(poly2)]
            )
            if touch:
                return True

    return False


def getRGB(value):
    alpha = 255 - abs(value)
    R = 0 if value < 0 else 255
    G = R
    B = 0 if value > 0 else 255

    return (R, G, B, 100)

    # # Define the color with RGBA values
    # red = 255
    # green = 0
    # blue = 0
    # alpha = 110  # 0 (transparent) to 255 (opaque)
    # # RGBA values (Red: 255, Green: 0, Blue: 0, Alpha: 128)
    # color = (255, 0, 0, alpha)

    # return color
