# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
from multiprocessing import Pool
import time
# import math





# %%
ar = np.random.rand(1*10**8, 5)


# %%

with Pool(5) as p:
    ts = time.monotonic()
    u = p.map(
        np.mean,
        [ar[:,0], ar[:,1], ar[:,2]]
        )
    te = time.monotonic()
    print(te-ts)


# %%
ts2 = time.monotonic()
z = (np.mean(ar[:,0]), np.mean(ar[:,1]), np.mean(ar[:,2]))
te2 = time.monotonic()
print(te2-ts2)


# %%


