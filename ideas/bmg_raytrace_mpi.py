# -*- coding: utf-8 -*-
from __future__ import print_function

import itertools
from mpi4py import MPI
import argparse
from time import time
import numpy as np

from detector import Detector
from sample import Sample
from snippets import generate_photon_statistics, beam_path_within_sample

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

a = time()
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


def calculateIntensity(input):
    i, j = input
    intensity = []
    for detPixel in range(i, i + j):
        row, column = detPixel / det.xdim, detPixel % det.xdim
        xB, yB, zB = sam.generate_random_points_within_sample(N, slit_x, cdf_x, slit_y, cdf_y)
        xD, yD, zD = det.generate_random_points_within_pixel(N, row, column)
        beam_path = beam_path_within_sample(sam, xB, yB, zB, xD, yD, zD)
        intensity.append(np.mean(np.exp(-beam_path / sam.mu)))
    return intensity


if rank == 0:
    procCount = comm.Get_size()
    batchSize = size - 1
    numPixels = det.xdim * det.ydim
    arraySize, rest = numPixels / batchSize, numPixels % batchSize

    ranges = zip([cpuNode * arraySize for cpuNode in range(batchSize)], (arraySize,) * batchSize)
    if rest > 0:
        ranges[-1] = ((batchSize - 1) * arraySize, arraySize + rest)

    for index, range in enumerate(ranges):
        comm.send(range, dest=index + 1)

    recieveCount = len(ranges)
    output = np.zeros([det.xdim * det.ydim])
    a = time()
    while recieveCount != 0:
        pixelRange, intensities = comm.recv(source=MPI.ANY_SOURCE)
        output[pixelRange[0]:sum(pixelRange)] += intensities
        recieveCount -= 1

        det.data = np.reshape(output, [det.xdim, det.ydim])

    print(time() - a)
    det.save_output(sam, N)

    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D, axes3d
    # from scipy import ndimage
    # Z2 = ndimage.gaussian_filter(1 / det.data, sigma=20, order=0)
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1, projection='3d')
    # cset = ax.plot_surface(det.xd, det.yd, Z2, cmap='jet')
    # plt.show()


else:
    pixelRange = comm.recv(source=0)
    output = calculateIntensity(pixelRange)
    comm.send((pixelRange, output), dest=0)
