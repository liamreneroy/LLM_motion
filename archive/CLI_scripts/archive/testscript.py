import numpy as np

a = np.arange(6).reshape(2,3) + 10
print(a)

ind = np.unravel_index(np.argmax(a, axis=None), a.shape)
print(ind)
print(a[ind])