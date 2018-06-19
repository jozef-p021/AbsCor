# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse

import numpy as np
from mpi4py import MPI

from detector import Detector
from sample import Sample
from snippets import beam_path_within_sample

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

p = argparse.ArgumentParser()
p.add_argument("--detX", default=500)
p.add_argument("--detY", default=500)
p.add_argument("--N", default=1000)
args = p.parse_args()

det = Detector(int(args.detX), int(args.detY))
det.SDD = 374.836
xd_off = -1028.607
yd_off = -1016.952
det.detector_offset(xd_off, yd_off)
sam = Sample(20, 0.75)
N = int(args.N)


if rank == 0:
    from snippets import generate_photon_statistics
    batchSize = size - 1
    numPixels = det.xdim * det.ydim
    arraySize, rest = numPixels / batchSize, numPixels % batchSize
    output = np.zeros([det.xdim * det.ydim])

    ranges = zip([cpuNode * arraySize for cpuNode in range(batchSize)], (arraySize,) * batchSize)
    if rest > 0:
        ranges[-1] = ((batchSize - 1) * arraySize, arraySize + rest)

    recieveCount = len(ranges)

    def storeData(data):
        global output, recieveCount
        pixelRange, intensities = data
        output[pixelRange[0]:sum(pixelRange)] += intensities
        recieveCount -= 1

    slit_x, cdf_x = generate_photon_statistics('./slit_scan/slit_05x05_00001.fio', 1.1, True)
    slit_y, cdf_y = generate_photon_statistics('./slit_scan/slit_05x05_00002.fio', 2.3, True)
    zD = np.ones([1, N], dtype=np.float32) * det.SDD
    pack = (slit_x, cdf_x, slit_y, cdf_y, zD)

    while len(ranges) != 0:
        dest = comm.recv(source=MPI.ANY_SOURCE)
        if isinstance(dest, tuple):
            storeData(dest)
        else:
            comm.isend((ranges.pop(0), pack), dest=dest)

    while recieveCount != 0:
        data = comm.recv(source=MPI.ANY_SOURCE)
        if isinstance(data, tuple):
            storeData(data)
        else:
            comm.isend(False, dest=data)

    det.data = np.reshape(output, [det.xdim, det.ydim])
    det.save_output(sam, N)

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D, axes3d
    from scipy import ndimage
    Z2 = ndimage.gaussian_filter(1 / det.data, sigma=20, order=0)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    cset = ax.plot_surface(det.xd, det.yd, Z2, cmap='jet')
    plt.show()
else:
    import time
    # Handshake with master, ask for pixel range
    comm.send(rank, dest=0)
    # Receive pixel range to count on
    input  = comm.recv(source=0)
    # If output is not pixel range, exit
    a = time.time()

    def calculateIntensity(input, zD):
        i, j = input
        intensity = []
        a = time.time()

        randomPoints = np.random.rand(N * j * 2) * det.pixel_size
        randomPointsOffset = 0

        xB, yB, zB = sam.generate_random_points_within_sample(N * j, slit_x, cdf_x, slit_y, cdf_y)

        for index, detPixel in enumerate(range(i, i + j)):
            row, column = detPixel / det.xdim, detPixel % det.xdim
            xD, randomPointsOffset = det.xd[row, column] + randomPoints[randomPointsOffset*N:randomPointsOffset*N + N], randomPointsOffset + 1
            yD, randomPointsOffset = det.yd[row, column] + randomPoints[randomPointsOffset*N:randomPointsOffset*N + N], randomPointsOffset + 1

            beam_path = beam_path_within_sample(sam, xB[N * index:(index + 1) * N], yB[N * index:(index + 1) * N],
                                                zB[N * index:(index + 1) * N], xD, yD, zD)
            intensity.append(np.mean(np.exp(-beam_path / sam.mu)))

        print(time.time() - a)
        return intensity

    if input is not False:
        pixelRange, (slit_x, cdf_x, slit_y, cdf_y, zD) = input
        output = calculateIntensity(pixelRange, zD)
        # Send computed pixel intensities
        comm.send((pixelRange, output), dest=0)
