import argparse
import time
from multiprocessing import Pool

import fabio
import numpy as np
from scipy import ndimage


class Sample:
    """
    This defines the sample and its geometry.
    All dimensions given in [mm].
    """
    # mu = 3.42	#Absorption length [mm] for iron Fe at 100 keV
    # mu = 0.114	#Absorption length [mm] for gold Au at  60 keV
    # mu = 1.06	#Absorption length [mm] for gold Fe at  60 keV
    # mu = 0.344	#Absorption length [mm] for gold LaB6 at  60 keV
    # mu = 0.179	#Absorption length [mm] for gold CeO2 at  60 keV
    mu = 0.513  # Absorption length [mm] for 1.5 mm diameter Zr60Al15Ni25 BMG (MARC780 from Mihai) at 60 keV

    def __init__(self, length=10.0, radius=0.5):
        """
        here we initialize cylinder sample geometry,
        namely	its length and radius
        """
        self.length = length
        self.radius = radius
        self.xs = 0.0
        self.ys = 0.0
        self.zs = 0.0

    def sample_offset(self, xs_off, ys_off, zs_off):
        """
        here we apply offset to the sample position
        """
        self.xs += xs_off
        self.ys += ys_off
        self.zs += zs_off

    def generate_shape(self, N):
        """
        this generate N random points from the surface of the cylinder
        """
        p = np.random.rand(N, 2) - 0.5
        x = self.xs + self.length * p[:, 0]
        y = self.ys + self.radius * np.cos(2 * np.pi * p[:, 1])
        z = self.zs + self.radius * np.sin(2 * np.pi * p[:, 1])
        return x, y, z

    def only_point_from_sample(self, x, y, z):
        """
        here we check if given point (x,y,z) falls within the sample volume
        """
        k = np.sqrt((y - self.ys) ** 2 + (z - self.zs) ** 2) / self.radius
        i = np.where(k <= 1)
        return x[i], y[i], z[i]

    def generate_random_points_within_sample(self, N, slit_x, cdf_x, slit_y, cdf_y):
        """
        """
        xn = np.array([], dtype=np.float32)
        yn = np.array([], dtype=np.float32)
        zn = np.array([], dtype=np.float32)
        while True:
            x = np.interp(np.random.rand(N), cdf_x, slit_x)
            y = np.interp(np.random.rand(N), cdf_y, slit_y)
            [z] = self.zs + 2 * self.radius * (np.random.rand(1, N) - 0.5)
            xi, yi, zi = self.only_point_from_sample(x, y, z)
            xn = np.append(xn, xi)
            yn = np.append(yn, yi)
            zn = np.append(zn, zi)
            if len(xn) > N:
                break
        return xn[:N], yn[:N], zn[:N]

    def generate_normal_points_within_sample(self, N):
        """
        """
        xn = np.array([], dtype=np.float32)
        yn = np.array([], dtype=np.float32)
        zn = np.array([], dtype=np.float32)
        while True:
            x = np.random.normal(0, 0.2, N)
            y = np.random.normal(0, 0.2, N)
            [z] = self.zs + 2 * self.radius * (np.random.rand(1, N) - 0.5)
            xi, yi, zi = self.only_point_from_sample(x, y, z)
            xn = np.append(xn, xi)
            yn = np.append(yn, yi)
            zn = np.append(zn, zi)
            if len(xn) > N:
                break
        return xn[:N], yn[:N], zn[:N]


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
        self.data = np.zeros([ydim, xdim], dtype=np.float32)
        self.xd, self.yd = np.meshgrid(np.arange(0, xdim, 1) * self.pixel_size, np.arange(0, ydim, 1) * self.pixel_size)

    def detector_offset(self, xd_off, yd_off):
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


def save_as(data):
    """
    """
    p = time.localtime()
    param = '{0:d}x{1:d}px_{2:0f}mm_'.format(det.xdim, det.ydim, det.SDD)
    datestring = '{0:d}-{1:02d}-{2:02d}_{3:02d}-{4:02d}-{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                        p.tm_min, p.tm_sec)

    output = fabio.edfimage.EdfImage()
    header = {}
    header['DISTANCE'] = det.SDD
    header['PIXEL LENGTH'] = int(1e3 * det.pixel_size)
    header['PIXEL HEIGHT'] = int(1e3 * det.pixel_size)
    header['CENTER X'] = np.abs(xd_off)
    header['CENTER Y'] = np.abs(yd_off)
    header['sample_radius'] = sam.radius
    header['photons_per_pixel'] = N
    output.header = header
    output.data = data
    fileName = 'AbsCor_' + param + datestring + '.edf'
    output.write(fileName)
    return fileName


def init(det, sam, N, slit_x, cdf_x, slit_y, cdf_y):
    global detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG
    detG, samG, NG, slit_xG, cdf_xG, slit_yG, cdf_yG = det, sam, N, slit_x, cdf_x, slit_y, cdf_y


def calculateRowIntensity(j):
    intensity = []
    for i in range(detG.xdim):
        xB, yB, zB = samG.generate_random_points_within_sample(NG, slit_xG, cdf_xG, slit_yG, cdf_yG)
        xD, yD, zD = detG.generate_random_points_within_pixel(NG, j, i)
        beam_path = beam_path_within_sample(samG, xB, yB, zB, xD, yD, zD)
        intensity.append(np.mean(np.exp(-beam_path / samG.mu)))

    return j, intensity


def writeOutput(det, output):
    for value in output:
        row, output = value
        det.increase_intensity_of_pixel_row(row, output)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--detX", default=500)
    p.add_argument("--detY", default=500)
    p.add_argument("--N", default=1000)
    args = p.parse_args()

    slit_x, cdf_x = generate_photon_statistics('./slit_scan/slit_05x05_00001.fio', 1.1, True)
    slit_y, cdf_y = generate_photon_statistics('./slit_scan/slit_05x05_00002.fio', 2.3, True)

    det = Detector(args.detX, args.detY)
    det.SDD = 374.836
    xd_off = -1028.607
    yd_off = -1016.952
    det.detector_offset(xd_off, yd_off)
    sam = Sample(20, 0.75)
    # sam.sample_offset(0.0, 0.0, 0.0)
    N = args.N

    t = time.time()
    pool = Pool(initializer=init, initargs=(det, sam, N, slit_x, cdf_x, slit_y, cdf_y))
    pool.map_async(calculateRowIntensity, range(det.ydim), callback=lambda output, det=det: writeOutput(det, output))
    pool.close()
    pool.join()
    print(time.time() - t)

    Z2 = ndimage.gaussian_filter(1 / det.data, sigma=20, order=0)
    fname = save_as(Z2)