from django.shortcuts import render, redirect
from django.urls import reverse
from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage,MessageRole
from django.conf import settings
from llama_index.llms.together import TogetherLLM
import os
from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexLLMRetriever,
)
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
import PyPDF2
import shutil
from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext





def home(request):
    return render(request, 'index.html')

# def doc_view(request):
#     return render(request, 'doc.html')

def doc_view(request):


    return render(request, 'doc.html')

def split_pdf_by_page(pdf_file, output_folder):
    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create the output folder
    os.makedirs(output_folder)

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    pdf_names = []

    for page_num in range(num_pages):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])
        output_file_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
        pdf_names.append(f'page_{page_num + 1}')
        with open(output_file_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

    return pdf_names
# def build_document_summary_index(city_docs):
#     # Initialize the embedding model
#     lc_embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
#     embed_model = LangchainEmbedding(lc_embed_model)
#     Settings.embed_model = embed_model
#     splitter = SentenceSplitter(chunk_size=1000)
#     response_synthesizer = get_response_synthesizer(
#         response_mode="tree_summarize", use_async=True
#     )
#
#     # Initialize the LLM model
#     llm = TogetherLLM(
#         model="togethercomputer/llama-2-70b-chat",
#         api_key="96557b956acf6073510ee7e4abadc1c7863626e75278a0eaf9a747875af30604"
#     )
#     Settings.llm = llm
#     # Settings.llm = TogetherLLMSettings(
#     #     model="togethercomputer/llama-2-70b-chat",
#     #     api_key="your_api_key_here"
#     # )
#     # from llama_index.core import Settings
#     Settings.context_window = 4000
#
#     # Build the document summary index from the city_docs list
#     doc_summary_index = DocumentSummaryIndex.from_documents(
#         city_docs,
#         llm=llm,
#         transformations=[splitter],
#         response_synthesizer=response_synthesizer,
#         show_progress=True
#     )
#
#     return doc_summary_index
# def build_document_summary_index(city_docs):
#     # Initialize the embedding model
#     embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=settings.SENTENCE_EMBEDDING_MODEL))
#     settings.Settings.embed_model = embed_model
#
#     # Initialize the LLM model
#     llm = TogetherLLM(model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY)
#     settings.Settings.llm = llm
#
#     # Set context window size
#     settings.Settings.context_window = settings.CONTEXT_WINDOW_SIZE
#
#     # Initialize the splitter
#     splitter = SentenceSplitter(chunk_size=settings.SPLITTER_CHUNK_SIZE)
#
#     # Initialize the response synthesizer
#     response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)
#
#     # Build the document summary index
#     doc_summary_index = DocumentSummaryIndex.from_documents(
#         city_docs,
#         llm=llm,
#         transformations=[splitter],
#         response_synthesizer=response_synthesizer,
#         show_progress=True
#     )
#
#     return doc_summary_index

def build_document_summary_index(city_docs):
    # Initialize the embedding model
    embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=settings.SENTENCE_EMBEDDING_MODEL))
    settings.embed_model = embed_model

    # Initialize the LLM model
    llm = TogetherLLM(model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY)
    settings.llm = llm

    # Set context window size
    settings.context_window = settings.CONTEXT_WINDOW_SIZE

    # Initialize the splitter
    splitter = SentenceSplitter(chunk_size=settings.SPLITTER_CHUNK_SIZE)

    # Initialize the response synthesizer
    response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)

    # Build the document summary index
    doc_summary_index = DocumentSummaryIndex.from_documents(
        city_docs,
        llm=llm,
        transformations=[splitter],
        response_synthesizer=response_synthesizer,
        show_progress=True
    )

    return doc_summary_index

def process_user_input(user_input, doc_summary_index):
    if user_input:
        # Prepare chat message template and query
        print(user_input)
        chat_text_qa_msgs = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=(
                    "Summarize the documents.\n"
                    "Always answer the query using the provided context information, "
                ),
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=(
                    "Context information is below.\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n"
                    f"Given the context information, Provide a summary to the document {user_input} .\n"
                ),
            ),
        ]
        text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
        query_2 = "summarize the   message from CFO section with the context relevant for Financial Performance"  # Use user input as part of the query

        # Get response from document summary index
        response__2 = doc_summary_index.as_query_engine(text_qa_template=text_qa_template).query(query_2)
        print(response__2)

        return response__2
    else:
        return None

def process_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Redirect to the process_file view function while passing the user_input as a query parameter
        return redirect('process_file', user_input=user_input)
def process_file(request):
    doc_summary_index = None
    user_input = None

    if request.method == 'POST':
        if request.FILES.get('pdf_file'):
            # Handle PDF file upload
            pdf_file = request.FILES['pdf_file']
            output_folder = 'output_folder'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            city_docs = []
            output_folder = 'output_folder'
            pdf_names = split_pdf_by_page(pdf_file, output_folder)
            for wiki_title in pdf_names:
                docs = SimpleDirectoryReader(
                    input_files=[f"{output_folder}/{wiki_title}.pdf"]
                ).load_data()
                for doc in docs:
                    doc.doc_id = wiki_title
                city_docs.extend(docs)
            doc_summary_index = build_document_summary_index(city_docs)
            doc_summary_index.storage_context.persist("index")
            storage_context = StorageContext.from_defaults(persist_dir="index")
            doc_summary_index = load_index_from_storage(storage_context)



        elif request.POST.get('user_input'):
            # Handle user input
            user_input = request.POST.get('user_input', '')


            # Now you have access to the user_input variable, you can print it or use it as needed
            print("User input:", user_input)
            print(doc_summary_index)
            if user_input:
                doc_summary_index = build_document_summary_index(city_docs)
                doc_summary_index.storage_context.persist("index")
                storage_context = StorageContext.from_defaults(persist_dir="index")
                doc_summary_index = load_index_from_storage(storage_context)
                retriever = DocumentSummaryIndexLLMRetriever(
                    doc_summary_index,
                    choice_top_k=1,
                )
                response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")

                chat_text_qa_msgs = [
                    ChatMessage(
                        role=MessageRole.SYSTEM,
                        content=(
                            "Summarize the documents.\n"
                            "Always answer the query using the provided context information, "
                        ),
                    ),
                    ChatMessage(
                        role=MessageRole.USER,
                        content=(
                            "Context information is below.\n"
                            "---------------------\n"
                            "{context_str}\n"
                            "---------------------\n"
                            "Given the context information, Provide a summary to the document .\n"
                        ),
                    ),
                ]


                text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)
                query_2 = f"""{user_input}
                   list:list any 5 important points
                   background:Explain background with financial context
                   provide data points with milestone"""
                query_engine = RetrieverQueryEngine(
                    retriever=retriever,
                    response_synthesizer=response_synthesizer
                )
                response__2 = doc_summary_index.as_query_engine(text_qa_template=text_qa_template).query(query_2)
                print(response__2,"response")

                # Get response from document summary index
                return render(request, 'doc_chat.html', {'response_2': response__2})

    # Render the HTML template without response data if the request method is not POST or if no file or user input is provided

    return render(request, 'doc_chat.html')


def doc_chat(request,response__2=None):
    # return render(request, 'doc_chat.html')
    print("Response:", response__2)
    return render(request, 'doc_chat.html', {'response_2': response__2})


