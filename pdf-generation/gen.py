#!/usr/bin/env python


from PIL import Image
from reportlab.graphics.shapes import Rect
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle


title_text = '''
FreedomLink: Amrita (Taylor University)
'''

paragraph1 = '''
On December 28, 2016 Tiny Hands Nepal staff at Kakarvitta intercepted a 22 year
old woman named Tunshi who was traveling with 3 other people, 2 of which
appeared to be victims and one of which appeared to be a trafficker. Border and
transit monitoring staff are trained to observe people's manner, appearance and
actions for clues that something may be wrong. In this case the attention of our
staff was initially drawn to Tunshi because she appeared nervous or afraid. The
manner in which a person is behaving can raise suspicion and is one of the main
things to which our staff pay attention.
'''

paragraph2 = '''
When she was questioned by our border staff Tunshi said that she was on her way
to a country in the Persian Gulf for a job. Because the Government of Nepal has
made it illegal for Nepalis to travel to a Gulf country by any means other than
Kathmandu International Airport, our staff immediately knew that Tunshi was
either being trafficked or at high risk of being trafficked or exploited upon
her arrival. This law was created in an attempt to reduce exploitation of
Nepalis overseas by giving the government more oversight, but due to the open
border it seems to have increased the number of people migrating through India
without basic legal protections. In the end the staff person making the
interception reported that they felt absolutely sure that it was a trafficking
case. Such certainty is rare because of the deception used by traffickers, but
enough evidence was uncovered in this case to make it completely clear.
'''

paragraph3 = '''
Tunshi was intercepted as a result of your support. We believe that human
trafficking - what may have happened to Tunshi without your help - is the
greatest injustice in the world. Thank you for your support in helping to
prevent Tunshi from being trafficked.
'''

paragraph4 = '''
Thank you for your support in helping to prevent Amrita from being trafficked.
'''

texts = [
        title_text,
        paragraph1,
        paragraph2,
        paragraph3,
        paragraph4,
]

# Filenames for the images to use
images = [
    'Test_Image1.png',
    'Test_Image2.png',
    'Test_Image3.png',
    'Test_Image4.png',
    'Test_Image5.png',
]

box_width = 1000

# Page Dimensions   Lan.  Port.
# image_width       2560  1013
# image_height      1706  1453

# Dimensions: x, y, width, height
rectangle_dimensions = [
    ((2560-box_width)/2, 1706/2),  #, 1000, 500),
    ((2560-box_width)/2, 1706/2),  #, 1000, 500),
    ((2560-box_width)/2, 1706/2),  #, 1000, 500),
    ((2560-box_width)/2, 1706/2),  #, 1000, 500),
    ((2560-box_width)/2, 1706/2),  #, 1000, 500),
]

if not (len(images) == len(rectangle_dimensions) == len(texts)):
    raise RuntimeError('You must have an equal number of text rectangles and'
            + ' images.')


canvas = Canvas('fill_image.pdf')

backgroundColor = Color(1, 1, 1, alpha=0.65)

styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleN.fontName = 'Helvetica'
styleN.fontSize = 30
styleN.leading = styleN.fontSize * 1.5
styleN.leftIndent = 40
styleN.rightIndent = 40
#styleN.spaceBefore = 40,
#styleN.spaceAfter = 40,
#styleN.borderWidth = 20
#styleN.borderPadding = 14
#styleN.borderColor = backgroundColor

# page_info: [path, (x, y, width, height)]
for page_info in zip(images, rectangle_dimensions, texts):
    image = Image.open(page_info[0])
    image_width, image_height = image.size
    canvas.setPageSize((image_width, image_height))

    canvas.drawImage(page_info[0], 0, 0, width=image_width, height=image_height,
                     preserveAspectRatio=True)

    text = Paragraph(page_info[2], styleN)

    data = [[text]]
    table = Table(data, box_width)

    table.setStyle(TableStyle([('BACKGROUND', (0,0), (0,0), backgroundColor)]))

    # I can't figure out what this does, but it has to be here. :/
    #table.wrapOn(canvas, image_width, image_height)
    table.wrapOn(canvas, 0, 0)

    # Where to draw the table
    table.drawOn(canvas, page_info[1][0], page_info[1][1])

    # Misnomer... Actually gets a new page.
    canvas.showPage()

canvas.save()





    # canvas.setFillColor(rectColor)
    # canvas.rect(page_info[1][0],
                # page_info[1][1],
                # page_info[1][2],
                # page_info[1][3],
                # fill=True,
                # stroke=False)
