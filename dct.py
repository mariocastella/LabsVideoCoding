from scipy.fft import dct, idct
import matplotlib.pyplot as plt


def dct2d(data):
    return dct(dct(data.T, norm='ortho').T, norm='ortho')
    # the function execute first the dft of colums by making traspose and then dct of the result trasposed to compute
    # the other axis


def idct2d(data):
    return idct(idct(data.T, norm='ortho').T, norm='ortho')
    # Follows the same idea as dct2d()


def main():
    while True:
        uim = str(input("Select a gray scale image by writing its route or pres Enter to load default image: "))
        if uim:
            im = plt.imread(uim)
        else:
            im = plt.imread('Lenna_gs.png')
        dctim = dct2d(im)
        idctim = idct2d(dctim)

        plt.gray()
        plt.subplot(121), plt.imshow(im), plt.axis('off'), plt.title('original image', size=15)
        plt.subplot(122), plt.imshow(idctim), plt.axis('off'), plt.title('reconstructed image', size=15)
        plt.savefig('DCT+IDCT')


main()
