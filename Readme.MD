# CodeBarSticker

This is a project to generate code bars on a given PDF template in order to print stickers.

To do this the actions are configurable with a single `config.json` file.

The JSON file contains two main sections: `params` and `TagList`.

The `params` section contains the following configurable parameters:

- `barcode_type` with the type of code bar to generate. This defaults to `datamatrix`. The full list of options in the documentation of the treepoem Python module here: https://github.com/adamchainz/treepoem,
- `templateFilename` is the PDF file template that will be used to print the stickers,
- `numCol` is the number of columns in the PDF template,
- `numRow` is the number of rows in the PDF template,
- `x0` is the x coordinate of the first box containing the first code bar,
- `y0` is the x coordinate of the first box containing the first code bar,
- `x_box_size` is the x size of the box containing the code bar, for 20x20 `datamatrix` 100 is a good value,
- `y_box_size` is the y size of the box containing the code bar, for 20x20 `datamatrix` 100 is a good value,
- `x_offset` is the horizontal offset to place the code bars in the PDF template,
- `y_offset` is the vertical offset to place the code bars in the PDF template

The `TagList` contains the list of values that will be encoded in the code bars.

After launching the script with:
```
python3 main.py
```

The result is a new PDF file `template_file_with_codebar_tags.pdf` that contains the code bars added to the original template.
