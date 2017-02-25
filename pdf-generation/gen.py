#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from PIL import Image

images = [
    'Test_Image1.png',
    'Test_Image2.png',
    'Test_Image3.png',
    'Test_Image4.png',
    'Test_Image5.png',
]

canvas = Canvas('fill_image.pdf')
for path in images:
    image = Image.open(path)
    image_width, image_height = image.size

    canvas.setPageSize((image_width, image_height))

    canvas.drawImage(path, 0, 0, width=image_width, height=image_height,
                     preserveAspectRatio=True)

    # Misnomer... Actually gets a new page.
    canvas.showPage()
canvas.save()
