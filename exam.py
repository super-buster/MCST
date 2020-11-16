import numpy as np

a = np.array([[[0, 1, -1], [1, 1, 0], [-1, -1, 1]],
              [[-1, 0, -1], [0, 1, 0], [0, 0, 0]]])
b = [[0, 1, -1], [1, 1, 0], [-1, -1, 1]]
indices = np.where(a < 5)
result = [(x, y) for x, y in zip(indices[0], indices[1])]


def whowin(*unknow):
    if any(unknow == 1):
        return 1
    elif any(unknow == -1):
        return -1
    else:
        return None


print(whowin([1, 2, 3]))
