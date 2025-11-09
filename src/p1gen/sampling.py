from rich import print
import numpy as np


def gen_normal(seed: int = 10):
    gen = np.random.default_rng(seed)
    inp = (1, 1, 3)  # loc, scale, size
    res = gen.normal(*inp)
    print(res)
    return res


seed = 20
gen = np.random.default_rng(seed)
inp = (1, 1, 3)  # loc, scale, size

# gen_normal("dog")
