import numpy as np

a = np.array([[[0, 1, -1], [1, 1, 0], [-1, -1, 1]],
              [[-1, 0, -1], [0, 1, 0], [0, 0, 0]],
              [[-1, 0, -1], [0, 1, 0], [0, 0, 0]]
              ])
nop = np.sum(np.absolute(a), 0).astype(int)
indices = np.where(nop < 3)
next = [(coords[0], coords[1]) for coords in zip(indices[0], indices[1])]
print(nop, next)
