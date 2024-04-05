from django.shortcuts import render
from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
# from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
# Create your views here.
import os
from django.http import JsonResponse
import PyPDF2


def home(request):
    return render(request, 'index.html')

def doc_view(request):
    return render(request, 'doc_chat.html')

# def summarize_file(request):
#     # File path in the project directory
#     file_path = 'path/to/your/file.txt'  # Update this with the actual file path
#
#     # Check if the file exists
#     if os.path.exists(file_path):
#         # Perform document summarization using Llama index
#         # try:
#         #     llama_index = LlamaIndex()
#         #     summary = llama_index.summarize(file_path)  # Assuming 'summarize' method exists in Llama index
#         except Exception as e:
#             # Handle any errors that may occur during document summarization
#             # For example, if Llama index encounters an error or the file format is not supported
#             return render(request, 'summary.html', {'error': str(e)})
#
#         # Return the summary to the user
#         return render(request, 'summary.html', {'summary': summary})
#
#     # If the file does not exist, return an error response
#     return render(request, 'summary.html', {'error': 'File not found'})

# views.py



def split_pdf(request):
    # Assuming the PDF file is present in the current directory
    pdf_file_path = 'Tax-Transparency-Report.pdf'  # Update with your PDF file name

    # Output folder to save split PDF pages
    output_folder = 'output_folder1'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Call the function to split the PDF by each page
        split_pdf_by_page(pdf_file_path, output_folder)
        return JsonResponse({'message': 'PDF splitting successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def split_pdf_by_page(pdf_path, output_folder):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages

        for page_num in range(num_pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.add_page(pdf_reader.getPage(page_num))
            output_file_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
            with open(output_file_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
