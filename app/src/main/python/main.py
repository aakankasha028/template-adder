from PIL import Image
import PIL
from fpdf import FPDF
import os
import shutil
import glob
import sys
import argparse
from pdf2Img import extractImagesFromPdf

""" # parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--inPDF", help="Input pdf name")
parser.add_argument("--outPDF", help="Output pdf name")
parser.add_argument("--extractImages", help="Extract images if None. Else, use the image in the images directory and use them to create the pdf")

args = parser.parse_args() """

""" if args.extractImages is None:
    extractImagesFromPdf(args)
else:
    print("Finding images in folder 'static_images'")
    IMAGES_DIR = 'static_images' """

def createPDFWithTemplate(inPDF, outPDF):
    IMAGES_DIR = 'images'
    sep = "/"
    RESULTS_DIR = 'results'
    OUT_PDFS_DIR = 'out_pdfs'
    OUT_PDF_NAME = os.path.join(OUT_PDFS_DIR, outPDF+".pdf")

    num_files = len(glob.glob(IMAGES_DIR + sep + '*')) + 1
    shutil.rmtree(RESULTS_DIR)
    os.mkdir(RESULTS_DIR)

    pdf = FPDF()
    imgs = []

    for i in range(1,num_files):
        image = Image.open(IMAGES_DIR + sep + str(i)+ '.jpg').convert('RGB')
        base = Image.open('base.jpg').convert('RGB')
        image_w, image_h = image.size

        #scale base to size of image
        #base = base.resize((int(image_w*1.1), int(image_h*1.1)))
        base = base.resize((1819, 2572))

        base_w, base_h = base.size

        # just in case you want to rotate an image
        # image = image.rotate(-90, PIL.Image.NEAREST, expand = 1);

        #scale image down to 80%
        image = image.resize((int(base_w*0.8), int(base_h*0.8)))
        #image = image.resize((int(image_w*1.2), int(image_h*1.2)))

        base_w, base_h = base.size
        image_w, image_h = image.size

        print("base " + str(base_w) + "," + str(base_h))
        print("image " + str(image_w) + "," + str(image_h))

        x = int(base_w/2 - image_w/2 )
        y = int(base_h/2 - image_h/2 + 100)

        base.paste(image.copy(), (x,y))
        base.save(RESULTS_DIR + sep + str(i) + '.jpg')
        if i != 1:
            imgs += [Image.open(RESULTS_DIR + sep + str(i) + '.jpg')]

        img1 = Image.open(RESULTS_DIR + sep + '1.jpg')
        img1.save(OUT_PDF_NAME, "PDF", save_all=True, append_images=imgs)
        return img1