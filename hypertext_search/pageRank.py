import os
import time
import numpy as np
from .constants import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HypertextSearch.settings")


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))
        return ret

    return wrap


def pagerankPowerMethod(H, a, eps=EPSILON, alpha=0.85, iterations=ITERATIONS):
    n = H.shape[1]
    # initial vector
    v = np.ones((n, 1)) / n
    last_v = np.ones((n, 1)) * 100
    cnt = 0
    while True:
        if np.linalg.norm(v - last_v, 2) < eps or cnt == iterations:
            break
        last_v = v
        x = alpha * np.matmul(H, v)
        v = x + (np.matmul(x, a) + 1 - alpha) * np.ones((n, 1)) / n
        cnt += 1

    return v


# @timing
def pageRank(H, a, eps=EPSILON, iterations=ITERATIONS):
    n = H.shape[1]
    # initial vector
    v = np.ones((n, 1)) / n
    last_v = np.ones((n, 1)) * 100
    cnt = 0
    while True:
        if np.linalg.norm(v - last_v, 2) < eps or cnt == iterations:
            break
        last_v = v
        v = np.matmul(H, v) + np.matmul(a, np.ones((n, 1))) / n
        cnt += 1
    return v


def calculateDanglingVector(H):
    a = H.shape[0] * [0]
    for i in range(H.shape[0]):
        if np.count_nonzero(H[i]) == 0:
            a[i] = 1
    return np.asmatrix(a)


def replaceZeros(a, H, num=EPSILON):
    a = np.array(a)
    M = H
    for i in range(H.shape[0]):
        if a.item(i) == 0:
            M[i, :] = np.where(M[i, :] == 0, num, M[i, :])
    return M


