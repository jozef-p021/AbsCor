import argparse

import fabio
import matplotlib.pyplot as plt
from bmg_raytrace import Detector

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--image", default="AbsCor_2048x2048px_374.836000mm_2018-06-19_14-47-18.edf")
    args = p.parse_args()

    output = fabio.openimage.openimage(args.image)
    detX, detY = output.data.shape
    det = Detector(detX, detY)
    
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    cset = ax.plot_surface(det.xd, det.yd, output.data, cmap='jet')
    plt.show()