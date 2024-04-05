from django.shortcuts import render, redirect
from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
# from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
# Create your views here.
import os
from django.http import JsonResponse, HttpResponse
import PyPDF2


def home(request):
    return render(request, 'index.html')

# def doc_view(request):
#     return render(request, 'doc.html')

def doc_view(request):

    return render(request, 'doc.html')
def process_file(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        # Handle the uploaded file here
        # For example, you can save it to a folder or process it in some way
        pdf_file = request.FILES['pdf_file']
        # Process the file...

        # Redirect to the doc_chat.html page
        return redirect('doc_chat')
    else:
        return HttpResponse('Invalid request or no file provided')

def doc_chat(request):
    return render(request, 'doc_chat.html')


# def split_pdf(request):
#     if request.method == 'POST' and request.FILES.get('pdf_file'):
#         pdf_file = request.FILES['pdf_file']
#         output_folder = 'output_folder1'
#
#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)
#
#         try:
#             split_pdf_by_page(pdf_file, output_folder)
#             return JsonResponse({'message': 'PDF splitting successful'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#
#     return JsonResponse({'error': 'Invalid request or no PDF file provided'}, status=400)
#
# def split_pdf_by_page(pdf_file, output_folder):
#     pdf_reader = PyPDF2.PdfFileReader(pdf_file)
#     num_pages = pdf_reader.numPages
#
#     for page_num in range(num_pages):
#         pdf_writer = PyPDF2.PdfFileWriter()
#         pdf_writer.add_page(pdf_reader.getPage(page_num))
#         output_file_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
#         with open(output_file_path, 'wb') as output_pdf:
#             pdf_writer.write(output_pdf)
#
# def split_pdf(request):
#     pdf_file_path = 'example.pdf'  # Path to the existing PDF file in the project directory
#     output_folder = 'output_folder1'
#
#     if not os.path.exists(pdf_file_path):
#         return JsonResponse({'error': 'PDF file not found'}, status=404)
#
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     try:
#         split_pdf_by_page(pdf_file_path, output_folder)
#         return JsonResponse({'message': 'PDF splitting successful'})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
#
#
# def split_pdf_by_page(pdf_path, output_folder):
#     with open(pdf_path, 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         num_pages = len(pdf_reader.pages)
#
#         for page_num in range(num_pages):
#             pdf_writer = PyPDF2.PdfWriter()
#             pdf_writer.add_page(pdf_reader.pages[page_num])
#             output_file_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
#             with open(output_file_path, 'wb') as output_pdf:
#                 pdf_writer.write(output_pdf)