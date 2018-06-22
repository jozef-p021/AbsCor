# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse

import numpy as np
from mpi4py import MPI

from AbsCor.detector import Detector
from AbsCor.sample import Sample
from AbsCor.snippets import beam_path_within_sample

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

p = argparse.ArgumentParser()
p.add_argument("--detX", default=50)
p.add_argument("--detY", default=50)
p.add_argument("--detOffsetX", default=-1028.607)
p.add_argument("--detOffsetY", default=-1016.952)
p.add_argument("--sdd", default=374.836)
p.add_argument("--samLength", default=20)
p.add_argument("--samRadius", default=0.75)
p.add_argument("--N", default=1000)
p.add_argument("--o", default=None)
args = p.parse_args()

det = Detector(int(args.detX), int(args.detY))
det.SDD = float(args.sdd)
xd_off = float(args.detOffsetX)
yd_off = float(args.detOffsetY)
det.detector_offset(xd_off, yd_off)
sam = Sample(float(args.samLength), float(args.samRadius))
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

    while len(ranges) != 0:
        dest = comm.recv(source=MPI.ANY_SOURCE)
        if isinstance(dest, tuple):
            storeData(dest)
        else:
            pack = (ranges.pop(0), slit_x, cdf_x, slit_y, cdf_y)
            comm.isend(pack, dest=dest)

    while recieveCount != 0:
        data = comm.recv(source=MPI.ANY_SOURCE)
        if isinstance(data, tuple):
            storeData(data)
        else:
            comm.isend(False, dest=data)

    det.data = np.reshape(output, [det.xdim, det.ydim])
    det.save_output(sam, N, fileName=args.o)
else:
    # Handshake with master, ask for pixel range
    comm.send(rank, dest=0)
    # Receive pixel range to count on
    input = comm.recv(source=0)


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


    if input is not False:
        pixelRange, slit_x, cdf_x, slit_y, cdf_y = input
        output = calculateIntensity(pixelRange)
        comm.send((pixelRange, output), dest=0)
