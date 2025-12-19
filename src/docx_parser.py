import os
from docx import Document
from docx.oxml.ns import qn
from PIL import Image
from io import BytesIO


def is_paragraph_list_item(paragraph):
    """Check if a paragraph is part of a list (bullet or numbered)."""
    style_name = paragraph.style.name.lower() if paragraph.style else ""
    return 'list bullet' in style_name or 'list number' in style_name

def get_paragraph_list_level(paragraph):
    p = paragraph._p
    numPr = p.find(qn('w:numPr'))
    if numPr is not None:
        ilvl = numPr.find(qn('w:ilvl'))
        if ilvl is not None:
            val = ilvl.get(qn('w:val'))
            if val is not None:
                return int(val)

    style_name = paragraph.style.name.lower() if paragraph.style else ""
    if 'list bullet' in style_name or 'list number' in style_name:
        for word in style_name.split():
            if word.isdigit():
                return int(word) - 1
    return 0

def generate_markdown_from_docx(docx_filename):
    docx_basename = os.path.splitext(os.path.basename(docx_filename))[0]
    images_dir = f'images/{docx_basename}/'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    document = Document(docx_filename)
    markdown_content = ''
    image_counter = 1

    for para in document.paragraphs:
        style = para.style.name if para.style else "Normal"
        text = para.text.strip() if para.text else ''

        if not text and not para.runs:
            continue

        is_heading = 'Heading' in style
        is_title = style == 'Title'
        is_list = is_paragraph_list_item(para)
        list_level = get_paragraph_list_level(para) if is_list else 0

        if is_title:
            heading_level = 1
        elif is_heading:
            heading_level = int(style.replace('Heading', '')) + 1
        else:
            heading_level = None

        for run in para.runs:
            drawings = run.element.findall('.//w:drawing', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            for drawing in drawings:
                blips = drawing.findall('.//a:blip', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
                for blip in blips:
                    rId = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    if rId is not None and rId in document.part.related_parts:
                        image_part = document.part.related_parts[rId]
                        image_bytes = image_part.blob
                        image_filename = f'{image_counter}.png'
                        image_path = os.path.join(images_dir, image_filename)

                        image = Image.open(BytesIO(image_bytes))
                        if image.mode in ('RGBA', 'P', 'LA'):
                            image = image.convert('RGB')
                        image.save(image_path, 'PNG')

                        markdown_content += f'![image{image_counter}]({image_path})\n\n'
                        image_counter += 1

        if heading_level:
            markdown_content += f'{"#" * heading_level} {text}\n\n'
        elif is_list:
            markdown_content += f'{"  " * list_level}- {text}\n'
        elif text:
            markdown_content += f'{text}\n\n'

    return markdown_content

if __name__ == "__main__":
    docx_filename = 'inputs/docx/multimodal_llm_overview.docx'
    docx_basename = os.path.splitext(os.path.basename(docx_filename))[0]

    markdown_content = generate_markdown_from_docx(docx_filename)

    with open(f'{docx_basename}.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)