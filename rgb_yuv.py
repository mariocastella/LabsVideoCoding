import numpy as np


# this is the method SDTV with BT.601 using normalized RGB values in the interval [0,1]

def rgb2yuv(rgb):
    #yuvm = np.array([[0.299, -0.14713, 0.615],
    #                 [0.587, -0.28886, -0.51499],
    #                 [0.114, 0.436, -0.10001]])
    #yuv = np.dot(rgb, yuvm)

    Y = 0.257 * rgb[0] + 0.504 * rgb[1] + 0.098 * rgb[2] + 16
    U = -0.148 * rgb[0] - 0.291 * rgb[1] + 0.439 * rgb[2] + 128
    V = 0.439 * rgb[0] - 0.368 * rgb[1] - 0.071 * rgb[2] + 128
    yuv = np.array([Y, U, V])

    return yuv


def yuv2rgb(yuv):
    #rgbm = np.array([[1., 1., 1.],
    #                 [0., -0.39465, 2.03211],
    #                 [1.14, -0.58060, 0.]])
    #rgb = np.dot(yuv, rgbm)
    # Note that for small values of Y' it is possible to get R, G, or B values
    # that are negative so in practice we clamp the RGB results to the interval [0,1].
    B = 1.164 * (yuv[0] - 16) + 2.018 * (yuv[1] - 128)
    G = 1.164 * (yuv[0] - 16) - 0.813 * (yuv[2] - 128) - 0.391 * (yuv[1] - 128)
    R = 1.164 * (yuv[0] - 16) + 1.596 * (yuv[2] - 128)
    rgb = np.array([R, G, B])

    return rgb


def main():
    while True:
        conversion = int(input("Select what conversion do you want to execute. Input '1' =  R2Y or '2' = Y2R: "))
        if conversion == 1:
            R, G, B = [float(x) for x in input("Input RGB value normalized between [0,1] and spaced each component "
                                             "(Example:1 1 1): ").split(" ")]
            rgb = np.array([R, G, B])
            print(rgb2yuv(rgb))

        elif conversion == 2:
            Y, U, V = [float(x) for x in
                       input("Input YUV with Y normalized between [0,1], UV a vector and spaced each component "
                             "(Example: 1 -1 1): ").split(" ")]
            yuv = np.array([Y, U, V])
            print(yuv2rgb(yuv))
        conversion == 0


main()
