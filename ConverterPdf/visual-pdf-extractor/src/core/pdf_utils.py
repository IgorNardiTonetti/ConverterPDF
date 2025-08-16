def extract_pages_from_pdf(pdf_path, page_numbers):
    from PyPDF2 import PdfReader, PdfWriter
    import os

    
    pdf_writer = PdfWriter()

   
    pdf_reader = PdfReader(pdf_path)

   
    for page_number in page_numbers:
        if page_number < len(pdf_reader.pages):
            pdf_writer.add_page(pdf_reader.pages[page_number])
        else:
            raise ValueError(f"Page number {page_number + 1} is out of range.")

   
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}_extracted.pdf")

    
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    return output_path

def get_total_pages(pdf_path):
    from PyPDF2 import PdfReader

    
    pdf_reader = PdfReader(pdf_path)

    
    return len(pdf_reader.pages)

def validate_page_input(page_input, total_pages):
    
    page_ranges = page_input.split(',')
    page_numbers = set()

    for part in page_ranges:
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start) - 1, int(end) - 1  
            if start < 0 or end >= total_pages or start > end:
                raise ValueError("Invalid page range.")
            page_numbers.update(range(start, end + 1))
        else:
            page_number = int(part) - 1 
            if page_number < 0 or page_number >= total_pages:
                raise ValueError("Invalid page number.")
            page_numbers.add(page_number)

    return sorted(page_numbers)