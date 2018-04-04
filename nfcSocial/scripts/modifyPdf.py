from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

c = canvas.Canvas('QR_file.pdf')
c.drawImage('qr.png', 100, 720)


c.save()

watermark = PdfFileReader(open("QR_file.pdf", "rb"))

# Get our files ready
output_file = PdfFileWriter()
input_file = PdfFileReader(open("test.pdf", "rb"))

# Number of pages in input document
page_count = input_file.getNumPages()

# Go through all the input file pages to add a watermark to them
for page_number in range(page_count):
    print "Watermarking page {} of {}".format(page_number, page_count)
    # merge the watermark with the page
    input_page = input_file.getPage(page_number)
    input_page.mergePage(watermark.getPage(0))
    # add page from input file to output document
    output_file.addPage(input_page)

# finally, write "output" to document-output.pdf
with open("document-output.pdf", "wb") as outputStream:
    output_file.write(outputStream)



