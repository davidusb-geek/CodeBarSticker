import json
import treepoem
from fitz import fitz
import pathlib
import os
import sys
from os import chdir
from os.path import join
from os.path import dirname
from os import environ


def get_path(filename):   
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller >= 1.6
        chdir(sys._MEIPASS)
        filename = join(sys._MEIPASS, filename)
    elif '_MEIPASS2' in environ:
        # PyInstaller < 1.6 (tested on 1.5 only)
        chdir(environ['_MEIPASS2'])
        filename = join(environ['_MEIPASS2'], filename)
    else:
        chdir(dirname(sys.argv[0]))
        filename = join(dirname(sys.argv[0]), filename)
        
    return filename

def generate_bar_codes(data):
    for elm in data["TagList"]:
        # Generate the code bar image
        image = treepoem.generate_barcode(
            barcode_type=data["params"]["barcode_type"],  # One of the supported codes.
            data=elm, 
            options={"includetext":True, "alttext":elm, "guardwhitespace":True, 
                     "textsize":data["params"]["barcode_textsize"],
                     "version":data["params"]["barcode_version"]}
        ) 
        image.save(get_path('tmp/'+elm+'.png'))

def fill_pdf(pdf, x0, y0, x1, y1, img):
    rect = fitz.Rect(x0, y0, x1, y1)
    pdf[0].insert_image(rect, stream=img)

if __name__ == "__main__":

    # Read the json file
    with open(get_path('config.json')) as f:
        data = json.load(f)

    # Create bar codes
    generate_bar_codes(data)
    
    # Put images inside the PDF
    doc = fitz.open(data["params"]["templateFilename"])
    x0 = data["params"]["x0"]
    y0 = data["params"]["y0"]
    x1 = data["params"]["x_box_size"]
    y1 = data["params"]["y_box_size"]
    x_offset = data["params"]["x_offset"]
    y_offset = data["params"]["y_offset"]
    listPNG = list(pathlib.Path('tmp').glob('*.png'))
    count = 0
    for row in range(data["params"]["numRow"]):
        for col in range(data["params"]["numCol"]):
            if count >= len(listPNG):
                break
            img = open(listPNG[count], "rb").read()
            fill_pdf(doc, x0+x_offset*col, y0+y_offset*row, x1+x_offset*col, y1+y_offset*row, img)
            count += 1
    doc.save(get_path('template_file_with_codebar_tags.pdf'))
    