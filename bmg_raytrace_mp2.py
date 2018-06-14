# -*- coding: utf-8 -*-
import argparse
from multiprocessing import Pool, cpu_count

import numpy as np
from detector import Detector
from sample import Sample
from scipy import ndimage
from snippets import generate_photon_statistics, beam_path_within_sample


def init(det, sam, N, slit_x, cdf_x, slit_y, cdf_y):
    global detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG
    detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG = det, sam, N, slit_x, cdf_x, slit_y, cdf_y


def calculateRowIntensity(row):
    intensity = []
    for column in range(detG.xdim):
        xB, yB, zB = samG.generate_random_points_within_sample(NG, slit_xG, cdf_xG, slit_yG, cdf_yG)
        xD, yD, zD = detG.generate_random_points_within_pixel(NG, row, column)
        beam_path = beam_path_within_sample(samG, xB, yB, zB, xD, yD, zD)
        intensity.append(np.mean(np.exp(-beam_path / samG.mu)))
    return row, intensity


def writeOutput(det, output):
    outputArray = np.zeros(det.xdim * det.ydim)
    for value in output:
        row, output = value

    # det.increase_intensity_of_pixel_row(row, output)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--detX", default=78)
    p.add_argument("--detY", default=93)
    p.add_argument("--N", default=1000)
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

    cpuNodes = cpu_count()

    numPixels = det.xdim * det.ydim
    arraySize, rest = numPixels / cpuNodes, numPixels % cpuNodes


    pool = Pool(initializer=init, initargs=(det, sam, N, slit_x, cdf_x, slit_y, cdf_y))
    pool.map_async(calculateRowIntensity, range(det.ydim), callback=lambda output, det=det: writeOutput(det, output))
    pool.close()
    pool.join()

    det.save_output(sam, N)