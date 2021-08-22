from pdf2image import convert_from_path
import sys
import os
import shutil

BASE_DIR = 'in_pdfs'
EXTENSION = '.pdf'
OUT_DIR = 'images'
IMG_EXT = '.jpg'
sep = "/" # TODO: use os.sep instead of hardcoded /

def extractImagesFromPdf(args):

    fileName = args.inPDF

    print("Extracting images from: " + BASE_DIR + sep + fileName + EXTENSION);
    pages = convert_from_path(BASE_DIR + sep + fileName + EXTENSION)

    #delete all contents of images/ and create an empty folder again
    shutil.rmtree(OUT_DIR)
    os.mkdir(OUT_DIR)
    
    page_num = 1
    for page in pages:
        page.save(OUT_DIR + sep + str(page_num) + IMG_EXT, 'JPEG')
        page_num = page_num + 1


if __name__ == "__main__":
    extractImagesFromPdf()
