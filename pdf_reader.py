from pdf2image import convert_from_path

def pdf_to_images(pdf_path):

    images = convert_from_path(

        pdf_path,

        dpi=120,          # lower DPI = faster
        fmt="jpeg",
        thread_count=4
    )

    return images