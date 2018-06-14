import time

import fabio
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D, axes3d
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
        xn = np.array([])
        yn = np.array([])
        zn = np.array([])
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
        xn = np.array([])
        yn = np.array([])
        zn = np.array([])
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
        self.data = np.zeros([ydim, xdim])
        self.xd, self.yd = np.meshgrid(np.arange(0, xdim, 1) * self.pixel_size, np.arange(0, ydim, 1) * self.pixel_size)

    def detector_offset(self, xd_off, yd_off):
        self.xd += xd_off * self.pixel_size
        self.yd += yd_off * self.pixel_size

    def increase_intensity_of_pixel(self, r, s, value):
        self.data[r, s] += value

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


def beam_path_within_sample(xB, yB, zB, xD, yD, zD):
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
    output.write('AbsCor_' + param + datestring + '.edf')


if __name__ == '__main__':

    slit_x, cdf_x = generate_photon_statistics('./slit_scan/slit_05x05_00001.fio', 1.1, True)
    slit_y, cdf_y = generate_photon_statistics('./slit_scan/slit_05x05_00002.fio', 2.3, True)

    det = Detector(50, 50)
    det.SDD = 374.836
    xd_off = -1028.607
    yd_off = -1016.952
    det.detector_offset(xd_off, yd_off)
    sam = Sample(20, 0.75)
    # sam.sample_offset(0.0, 0.0, 0.0)

    N = 1000
    t0 = time.time()
    for j in range(det.ydim):
        t1 = time.time()
        for i in range(det.xdim):
            xB, yB, zB = sam.generate_random_points_within_sample(N, slit_x, cdf_x, slit_y, cdf_y)
            # xB, yB, zB = sam.generate_normal_points_within_sample(N)
            xD, yD, zD = det.generate_random_points_within_pixel(N, j, i)
            beam_path = beam_path_within_sample(xB, yB, zB, xD, yD, zD)
            value = np.mean(np.exp(-beam_path / sam.mu))
            det.increase_intensity_of_pixel(j, i, value)
        t2 = time.time()
        print '{0:04d}.\t{1:.2f}% done in {2:.2f} min, (total {3:.2f} min), remaining {4:.2f} min\n'.format((j + 1),
                                                                                                            1e2 * (
                                                                                                                        j + 1) / det.ydim,
                                                                                                            (
                                                                                                                        t2 - t0) / 60.0,
                                                                                                            det.ydim * (
                                                                                                                        t2 - t0) / (
                                                                                                                        60.0 * (
                                                                                                                            j + 1)),
                                                                                                            det.ydim * (
                                                                                                                        t2 - t0) / (
                                                                                                                        60.0 * (
                                                                                                                            j + 1)) - (
                                                                                                                        t2 - t0) / 60.0)

    print(det.data)
    Z2 = ndimage.gaussian_filter(1 / det.data, sigma=20, order=0)
    save_as(np.float32(Z2))

    fig = plt.figure()
    # ax = Axes3D(fig)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # X, Y, Z = axes3d.get_test_data(0.05)
    # cset = ax.plot_surface(X, Y, Z, 16, extend3d=True)
    # ax.clabel(cset, fontsize=9, inline=1)
    cset = ax.plot_surface(det.xd, det.yd, Z2, cmap='jet')
    # ax.clabel(cset, fontsize=9, inline=1)
    # ax1 = fig.add_subplot(111, extend3d=True)
    # ax1.plot_surface(det.xd, det.yd, Z2, cmap='jet')
    # ax1.contour(X, Y, Z, zorder=10)

    # j = 0
    # i = 1023
    # xB, yB, zB = sam.generate_random_points_within_sample(N, slit_x, cdf_x, slit_y, cdf_y)
    # xD, yD, zD = det.generate_random_points_within_pixel(N, j, i)
    # beam_path = beam_path_within_sample(xB, yB, zB, xD, yD, zD)
    # print beam_path

    # x, y, z = sam.generate_shape(200)

    # plt.scatter(zB, yB)
    # plt.scatter(z, y, marker='.')

    # xi, yi, zi = sam.generate_random_points_within_sample(N, slit_x, cdf_x, slit_y, cdf_y)
    # plt.hist2d(zB,yB, 40, cmap='jet')
    plt.show()
