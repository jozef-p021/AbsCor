# -*- coding: utf-8 -*-
import numpy as np


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
        genN = int(N *1.05)
        while True:
            x = np.interp(np.random.rand(genN), cdf_x, slit_x)
            y = np.interp(np.random.rand(genN), cdf_y, slit_y)
            [z] = self.zs + 2 * self.radius * (np.random.rand(1, genN) - 0.5)
            xi, yi, zi = self.only_point_from_sample(x, y, z)
            xn = np.append(xn, xi)
            yn = np.append(yn, yi)
            zn = np.append(zn, zi)
            if len(xn) >= N:
                break
            else:
                print("now")
                genN = int((N - len(xn)) * 1.05)
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