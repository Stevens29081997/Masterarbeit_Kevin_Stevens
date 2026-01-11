"""
pdf2txt
~~~~~~~~~~~~~~~~~

This module provides the functionality to process pdf files down to a plain
text file. The resulting file will be cleaned and structured in a standardized
way:
<Header>
<Empty line>
<Text paragraph>
<Empty line>

... and so on
"""

from io import StringIO
import os
from os import listdir
from os.path import isfile, join
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def delete_file(filepath:str)->None:
    """
    delete_file is a function that deletes an unnecessary file.
    Input argument is the full path to the file including it's name.
    E.g.: 'src/project_package/data/file.pdf'.
    """
    if os.path.isfile(filepath) or os.path.islink(filepath):
        os.unlink(filepath)

def save_file(filepath:str, content:str)->None:
    """
    save_file is a function that saves a given file.
    Input argument is the full path to the file including it's name.
    E.g.: 'src/project_package/data/file.pdf'.
    """
    with open(filepath, 'w', encoding='utf-8') as outstream:
        outstream.write(content)

def read_file(filepath:str)->str:
    """
    read_file is a function that reads out a given file and returns it as a string.
    Input argument is the full path to the file including it's name.
    E.g.: 'src/project_package/data/file.pdf'.
    """
    with open(filepath, "r") as inStream:
        data = inStream.read()

    return ''.join(data)


def clean_paragraphs(raw_paragraphs: 'list[str]')->str:
    """
    clean_paragraphs is a function for cleaning text files in a standardized
    manner.
    * input: list of text paragraphs (strings)
    * output: single, cleaned string with all paragraphs combined
    """
    # convert non str elements to a str
    raw_paragraphs = [str(p) for p in raw_paragraphs]
    # # remove duplicated sentences from the entire text
    # sentences = " ". join(raw_paragraphs).split(".")
    # raw_paragraphs = [sentence for sentence in sentences if sentences.count(sentence) < 2]
    # # delete unnecessary data again
    # del sentences
    # remove clutter symbols (+, =, <, >, –, •, |, Ώ),
    # uncommon combinations (-\n, //_)
    # and line breaks inside a paragraph
    paragraphs = [
                    re.sub(r'[+=<>•|Ώ]', ' ', p)
                    .replace('-\n', '').replace('\n', ' ')
                    # .replace('–', '')#.replace('// ', '')
                    .replace('—', ' ').replace('....', '')
                    for p in raw_paragraphs
                 ]
    del raw_paragraphs
    # remove paragraphs that only consist of dots and numbers or are repeated
    paragraphs = [p for p in paragraphs if not re.compile(r'^[0-9\.]+$').match(p) and (paragraphs.count(p) < 2)]

    for idx, p in enumerate(paragraphs):
        # remove all non standard symbols
        p = re.sub(r"[^a-zA-Z0-9\s\n.;:#(){}'`´/\\^-äöüÄÖÜß]", ' ', p)
        # get each line inside a paragraph
        lines = p.splitlines()
        # stript whitespaces from every line in paragrpahs and remove repeated sentences
        lines = [" ".join([word for word in line.split()]) for line in lines if (lines.count(line) < 2)]
        # combine the paragraph to a single string again
        paragraphs[idx] = ''.join(lines)

    # remove empty paragraphs (paragraphs with images only will become "\n\n" otherwise)
    paragraphs = [p for p in paragraphs if p]
    
    # combine all paragraphs, separated by two newlines
    return '\n\n'.join(paragraphs)


def pdf_to_text(pdf_filepath: str, out_path:str)->int:
    """
    pdf_to_text is a function for converting pdf files to plain text.
    The resulting file will keep the original name and
    path as given in the input argument, only changing the file type.
    The original file can be deleted afterwards.
    """
    try:
        # extract all paragraphs from the given pdf as a list of strings
        raw_paragraphs = extract_text_by_paragraph(pdf_filepath)
        # clean every paragraph and combine all to a single string
        text = clean_paragraphs(raw_paragraphs)
        # save the text file in the same directory and with it's original name
        save_file(filepath=out_path, content=text)

    except Exception as e:
        # catch some unexpected errors
        print(f"|[Error]|: unable to convert pdf {pdf_filepath} with error: {e}")
        return 1
    
    finally:
        return 0

    
def extract_text_by_paragraph(pdf_path: str)->'list[str]':
    """
    extract_text_by_paragraph is a function for extracting every text paragraph
    of a given pdf via the PDF Miner library.
    This function will return a list with each paragraph of the pdf as a string.
    """
    # Create a PDF parser object
    parser = PDFParser(open(pdf_path, 'rb'))
    # Create a PDF document object
    document = PDFDocument(parser)
    # Connect the parser and document objects
    parser.set_document(document)
    
    # Create a PDF resource manager object
    resource_manager = PDFResourceManager()
    # Create a string buffer
    string_buffer = StringIO()
    # Set the parameter for text extraction
    laparams = LAParams()
    # Create a PDF page aggregator object
    device = TextConverter(resource_manager, string_buffer, laparams=laparams)
    # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(resource_manager, device)
    
    # Extract the text from each page
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    # Get the text from the string buffer
    text = string_buffer.getvalue()
    # Close the string buffer and the device
    string_buffer.close()
    device.close()
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')
    
    # Return the list of paragraphs
    return paragraphs


if __name__ == '__main__':

    # pdf_filepath = "path/to/file" # e.g. "data/raw/filename.pdf"

    # output_txt_path = "path/to/save" # e.g. "data/preprocessed/filename.txt"

    # pdf_to_text(pdf_filepath, output_txt_path)

    # alternatively: process all files inside a folder at once:
    path = "data/raw_programme/"
    files: list[str] = [f for f in listdir(path) if isfile(join(path, f))
                            and not (f.endswith('.dvc')
                            or f.endswith('.gitignore'))]
    for file in files:
        party = file.split(".pdf")[0]
        out_path = f"data/{party}/Parteiprogramm/"

        pdf_to_text(join(path, file), join(out_path, file.split(".")[0]+".txt"))
