# -*- coding: utf-8 -*-
import argparse
from multiprocessing import Pool, cpu_count

import itertools
import numpy as np
import time
from detector import Detector
from sample import Sample
from scipy import ndimage
from snippets import generate_photon_statistics, beam_path_within_sample

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, axes3d
from scipy import ndimage


def init(det, sam, N, slit_x, cdf_x, slit_y, cdf_y):
    global detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG
    detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG = det, sam, N, slit_x, cdf_x, slit_y, cdf_y


def calculateIntensity(input):
    i, j = input
    intensity = []
    for detPixel in range(i, i + j):
        row, column = detPixel / detG.xdim, detPixel % detG.xdim
        xB, yB, zB = samG.generate_random_points_within_sample(NG, slit_xG, cdf_xG, slit_yG, cdf_yG)
        xD, yD, zD = detG.generate_random_points_within_pixel(NG, row, column)
        beam_path = beam_path_within_sample(samG, xB, yB, zB, xD, yD, zD)
        intensity.append(np.mean(np.exp(-beam_path / samG.mu)))
    return intensity


def writeOutput(det, output):
    det.data = np.reshape(np.array(list(itertools.chain.from_iterable(output)), dtype=np.float32), [det.xdim, det.ydim])

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--detX", default=50)
    p.add_argument("--detY", default=50)
    p.add_argument("--N", default=1000)
    p.add_argument("--batchSize", default=50)
    args = p.parse_args()

    slit_x, cdf_x = generate_photon_statistics('./slit_scan/slit_05x05_00001.fio', 1.1, True)
    slit_y, cdf_y = generate_photon_statistics('./slit_scan/slit_05x05_00002.fio', 2.3, True)

    det = Detector(int(args.detX), int(args.detY))
    det.SDD = 374.836
    xd_off = -1028.607
    yd_off = -1016.952
    det.detector_offset(xd_off, yd_off)
    sam = Sample(20, 0.75)
    N = int(args.N)

    batchSize = int(args.batchSize)
    numPixels = det.xdim * det.ydim
    arraySize, rest = numPixels / batchSize, numPixels % batchSize

    ranges = zip([cpuNode * arraySize for cpuNode in range(batchSize)], (arraySize,) * batchSize)
    if rest > 0:
        ranges[-1] = ((batchSize-1) * arraySize, arraySize + rest)

    pool = Pool(initializer=init, initargs=(det, sam, N, slit_x, cdf_x, slit_y, cdf_y), processes=cpu_count())
    pool.map_async(calculateIntensity, ranges, callback=lambda output, det=det: writeOutput(det, output))
    pool.close()
    pool.join()

    det.save_output(sam, N)
    Z2 = ndimage.gaussian_filter(1 / det.data, sigma=20, order=0)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    cset = ax.plot_surface(det.xd, det.yd, Z2, cmap='jet')
    plt.show()