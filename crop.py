import os

from PyPDF2 import PdfReader, PdfWriter

def crop_pdfs(output_path):
    pdfs = sorted([f for f in os.listdir(output_path) if f.endswith('.pdf')])

    for idx, pdf in enumerate(pdfs):
        file = PdfReader(open(f'{output_path}/{pdf}', "rb"))
        page = file.pages[0]

        # print(page.mediabox.lower_left)
        # print(page.mediabox.lower_right)
        # print(page.mediabox.upper_left)
        # print(page.mediabox.upper_right)

        output = PdfWriter()
        page.mediabox.lower_left = (
            page.mediabox.left + 50, page.mediabox.bottom + 25)
        page.mediabox.lower_right = (
            page.mediabox.right - 20, page.mediabox.bottom + 25)
        page.mediabox.upper_left = (
            page.mediabox.left + 50, page.mediabox.top - 40)
        page.mediabox.upper_right = (
            page.mediabox.right - 20, page.mediabox.top - 40)

        output.add_page(page)
        with open(f'{output_path}/3d_conv_{str(idx).zfill(2)}.pdf', 'wb') as output_stream:
            output.write(output_stream)
