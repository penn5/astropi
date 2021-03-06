import os, atexit
dirname = os.path.dirname(os.path.realpath(__file__))

# Initialize the project
def init():
    initLog()
    initCamera()
    initProcessor()

# Load camera and start the preview
def initCamera():
    picn = 1
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (1296,972)
    camera.start_preview()

# Prepare the logger and add handler to close file safely on exit
def initLog():
    logn = 1
    logfile = open(os.path.join(dirname, 'data{:02d}'.format(logn)), 'wb')
    atexit.register(closeLog)

# Import graphics processing libs
def initProcessor():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import ndimage as ndi
    from skimage import feature, io

# Close the log file
def closeLog():
    try:
        logfile.write('S') # End of log
        logfile.close()
    except:
        pass # We don't care.

# This escapes `\`s and `,`s so we can find the end of csv fields
def sanitizeForLog(data):
    return data.replace('\\', '\\\\').replace(',', '\\,')

# Store a picture to the log
def storeData(data, location):
    if f.tell() + len(data) > 1000000*35:
        if logn < 5:
            logn += 1
            closeLog()
            logfile = open(os.path.join(dirname, 'data{:02d}'.format(logn)), 'wb')
        else:
            raise RuntimeException("Out of storage!!!")
    logfile.write('M'+sanitizeForLog(data)+',L'+sanitizeForLog(location)+',')

# Take a photo and store it to the disk, returning the absolute path
def takePhoto():
    camera.capture(dir_path+"/image_{:03d}.jpg".format(picn))
    picn += 1
    return dir_path+"/image_{:03d}.jpg".format(picn-1)

# Process the photo, currently just an example. It finds the edges in the photo and draws them onto a plot
def processPhoto(path):
    im = io.imread(path)
    im = ndi.rotate(im, 15, mode='constant')
    im = ndi.gaussian_filter(im, 4)
    im += 0.2 * np.random.random(im.shape)

    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(im)
    edges2 = feature.canny(im, sigma=3)

    # display results
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                        sharex=True, sharey=True)

    ax1.imshow(im, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('noisy image', fontsize=20)

    ax2.imshow(edges1, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

    ax3.imshow(edges2, cmap=plt.cm.gray)
    ax3.axis('off')
    ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

    fig.tight_layout()

    plt.show()

# See how much storage our program is using
def checkStorage():
    return sum(os.path.getsize(f) for f in os.listdir(dirname) if os.path.isfile(f))

# Cleanup storage if we are over 2G
def cleanStorage():
    s = checkStorage()
    if s > 1000000000*2:
        cleanEveryOtherPhoto()

# Removes every other photo from the disk.
def cleanEveryOtherPhoto():
    x = 0
    for f in os.listdir(dirname):
        if os.path.isfile(f) and f[:6] == 'image_':
            x += 1
            if x % 2 == 0:
                os.remove(f)



if __name__ == "__main__":
    init()
    x = takePhoto()
    print(x)
    processPhoto(x)
