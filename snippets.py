# -*- coding: utf-8 -*-
import numpy as np


def generate_photon_statistics(slitscan, xo=0, mirror=False):
    """
    this generates photon statistics based on slitscan stored in respective file
    """
    if mirror == True:
        sign = -1
    else:
        sign = 1
    data = np.loadtxt(slitscan, skiprows=15, usecols=(0, 3))
    x = sign * (data[:, 0] - xo)
    y = data[:, 1] - data[0, 1]
    dx = np.mean(np.diff(x))
    cdf = []
    sum = 0
    for i in range(len(x)):
        sum += dx * y[i]
        cdf.append(sum)

    # xo = dx*np.sum(x*y)/sum
    cdf = cdf / sum
    return x, cdf


def beam_path_within_sample(sam, xB, yB, zB, xD, yD, zD):
    """
    """
    ### path_in
    zA = sam.zs - sam.radius * np.sin(np.arccos((yB - sam.ys) / sam.radius))
    path_in = np.abs(zA - zB)
    ### path_out
    path_out = np.sqrt((xD - xB) ** 2 + (yD - yB) ** 2 + (zD - zB) ** 2)
    a = (yD - yB) ** 2 + (zD - zB) ** 2
    b = 2 * ((yB - sam.ys) * (yD - yB) + (zB - sam.zs) * (zD - zB))
    c = (yB - sam.ys) ** 2 + (zB - sam.zs) ** 2 - sam.radius ** 2
    pom = np.sqrt(b ** 2 - 4 * a * c) / (2 * a)
    k1 = -b / (2 * a) + pom
    # k2 = -b/(2*a) - pom
    [path_out] = np.abs(k1) * path_out
    return path_in + path_out