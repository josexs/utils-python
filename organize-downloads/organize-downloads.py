import os
from PIL import Image


downloadsFolder = "/Users/josexs/Downloads/"
docsFolder = "/Users/josexs/Downloads/docs/"
devFolder = "/Users/josexs/Downloads/dev/"
imagesFolder = "/Users/josexs/Downloads/images/"
appsFolder = "/Users/josexs/Downloads/apps/"

appsExt = [".dmg"]
docsExt = [".pdf", ".doc", ".xls"]
devExt = [".json", ".html", ".csv"]
imagesExt = [".jpg", ".png", ".svg", ".jpeg"]


if os.path.isdir(appsFolder) == False:
    os.mkdir(appsFolder)
if os.path.isdir(docsFolder) == False:
    os.mkdir(docsFolder)
if os.path.isdir(devFolder) == False:
    os.mkdir(devFolder)
if os.path.isdir(imagesFolder) == False:
    os.mkdir(imagesFolder)


if __name__ == "__main__":
    for filename in os.listdir(downloadsFolder):
        name, extension = os.path.splitext(filename)

        if extension in appsExt:
            os.rename(downloadsFolder + filename, appsFolder + filename)
        if extension in devExt:
            os.rename(downloadsFolder + filename, devFolder + filename)
        if extension in imagesExt:
            os.rename(downloadsFolder + filename, imagesFolder + filename)
        if extension in docsExt:
            os.rename(downloadsFolder + filename, docsFolder + filename)
