# -*- coding: utf-8 -*-
import numpy as np
import fabio
import time

from scipy import ndimage


class Detector:
    """
    This defines detector, its dimensions in [pixels] and pixel size in [mm]

       +Y"
        ^"
        |"
        |"
        |"
        |"
    [0,0]------------> +X

    [0,0] point is located in lower left corner
    """

    pixel_size = 0.2  # in [mm]
    SDD = 500.0  # sample to detector distance in [mm]

    def __init__(self, xdim=6, ydim=10):
        self.xdim = xdim
        self.ydim = ydim
        self.offset = (0, 0)
        self.data = np.zeros([ydim, xdim], dtype=np.float32)
        self.xd, self.yd = np.meshgrid(np.arange(0, xdim, 1) * self.pixel_size, np.arange(0, ydim, 1) * self.pixel_size)

    def detector_offset(self, xd_off, yd_off):
        self.offset = (xd_off, yd_off)
        self.xd += xd_off * self.pixel_size
        self.yd += yd_off * self.pixel_size

    def increase_intensity_of_pixel(self, r, s, value):
        self.data[r, s] += value

    def increase_intensity_of_pixel_row(self, r, value):
        self.data[r, :] += value

    def generate_random_points_within_pixel(self, N, r, s):
        """
        """
        x = self.xd[r, s] + np.random.rand(1, N) * self.pixel_size
        y = self.yd[r, s] + np.random.rand(1, N) * self.pixel_size
        z = np.ones([1, N]) * self.SDD
        return x, y, z

    def save_output(self, sample, numberOfPhotons, fileName=None):
        """
        """
        p = time.localtime()
        param = '{0:d}x{1:d}px_{2:0f}mm_'.format(self.xdim, self.ydim, self.SDD)
        datestring = '{0:d}-{1:02d}-{2:02d}_{3:02d}-{4:02d}-{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                            p.tm_min, p.tm_sec)

        savingData = ndimage.gaussian_filter(1 / self.data, sigma=20, order=0)
        output = fabio.edfimage.EdfImage()
        header = {}
        header['DISTANCE'] = self.SDD
        header['PIXEL LENGTH'] = int(1e3 * self.pixel_size)
        header['PIXEL HEIGHT'] = int(1e3 * self.pixel_size)
        header['CENTER X'] = np.abs(self.offset[0])
        header['CENTER Y'] = np.abs(self.offset[1])
        header['sample_radius'] = sample.radius
        header['photons_per_pixel'] = numberOfPhotons
        output.header = header
        output.data = savingData
        if fileName is None:
            fileName = 'AbsCor_' + param + datestring + '.edf'

        output.write(fileName)
        return fileName