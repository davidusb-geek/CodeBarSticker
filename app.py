import streamlit as st
from typing import Optional, Tuple
import json
import treepoem
from fitz import fitz
import pathlib


def get_root(file: str, num_parent: Optional[int] = 3) -> str:
    """
    Get the root absolute path of the working directory.

    :param file: The passed file path with __file__
    :return: The root path
    :rtype: str
    """
    if num_parent == 3:
        root = pathlib.Path(file).resolve().parent.parent.parent
    elif num_parent == 2:
        root = pathlib.Path(file).resolve().parent.parent
    elif num_parent == 1:
        root = pathlib.Path(file).resolve().parent
    else:
        raise ValueError("num_parent value not valid, must be between 1 and 3")
    return root

@st.cache
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
        image.save('tmp/'+elm+'.png')

def fill_pdf(pdf, x0, y0, x1, y1, img):
    rect = fitz.Rect(x0, y0, x1, y1)
    pdf[0].insert_image(rect, stream=img)

st.set_page_config(layout="wide")
st.title("CodeBarSticker v0.1.0")
st.markdown("This is a project to generate code bars on a given PDF template in order to print stickers...")

# the root folder
root = get_root(__file__, num_parent=1)

# Upload configuration file
config_file = st.file_uploader("Upload a JSON configuration file",type=['json'])
if config_file is not None:
    file_details = {"FileName":config_file.name,"FileType":config_file.type,"FileSize":config_file.size}
    config_path = str(root / config_file.name)
else:
    st.info("Upload a JSON configuration file to begin...")
    config_path = 'empty'

if config_path != 'empty':
    
    # Read the json file
    with open(config_path) as f:
        data = json.load(f)
    
    pdf_file = st.file_uploader("Upload the PDF template file",type=['pdf'])
    if pdf_file is not None:
        file_details = {"FileName":pdf_file.name,"FileType":pdf_file.type,"FileSize":pdf_file.size}
        pdf_path = str(root / pdf_file.name)
    else:
        st.info("Upload the PDF file: "+data["params"]["templateFilename"]+" to continue...")
        pdf_path = 'empty'
        
    if pdf_path != 'empty':
        # Create bar codes
        generate_bar_codes(data)
        
        # Put images inside the PDF
        doc = fitz.open(pdf_path)
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
        with open("template_file_with_codebar_tags.pdf", "rb") as file:
            st.download_button(
                label="Download the result PDF",
                data=file,
                file_name='template_file_with_codebar_tags.pdf',
                mime='application/pdf',
            )