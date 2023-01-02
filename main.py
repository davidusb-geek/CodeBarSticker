import json
import treepoem
from fitz import fitz
import pathlib


def generate_bar_codes(data):
    for elm in data["TagList"]:
        # Generate the code bar image
        image = treepoem.generate_barcode(
            barcode_type=data["params"]["barcode_type"],  # One of the supported codes.
            data=elm, 
            options={"includetext":True, "alttext":elm, "guardwhitespace":True, "textsize":3,
                     "version":"20x20"}
        ) 
        image.save('tmp/'+elm+'.png')

def fill_pdf(pdf, x0, y0, x1, y1, img):
    rect = fitz.Rect(x0, y0, x1, y1)
    pdf[0].insert_image(rect, stream=img)

if __name__ == "__main__":

    # Read the json file
    with open('config.json') as f:
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
    doc.save('template_file_with_codebar_tags.pdf')
    