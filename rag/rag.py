import os

from decouple import config

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader # Biblioteca para ler PDF
from langchain_huggingface import HuggingFaceEmbeddings


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')
os.environ['HUGGINGFACE_API_KEY'] = config('HUGGINGFACE_API_KEY')


if __name__ == '__main__':
    file_path = '/app/rag/data/django_master.pdf' # Indica o caminho onde o seu arquivo PDF está guardado.
    loader = PyPDFLoader(file_path) # Prepara o "leitor" de PDF.
    docs = loader.load()  # Efetivamente abre o PDF e lê todo o conteúdo original.

    text_splitter = RecursiveCharacterTextSplitter( # Cria a "tesoura" que vai cortar o texto em pedaços menores (chunks).
        chunk_size=1000, # Cada "pedaço" de texto terá no máximo 1000 caracteres.
        chunk_overlap=200, # Os últimos 200 caracteres de um pedaço são repetidos no início do próximo. 
    )

    chunks = text_splitter.split_documents( # Executa o corte do PDF inteiro do text_splitter
        documents=docs,
    )

    persist_directory = '/app/chroma_data' # Define a pasta onde o banco de dados será salvo no computador.

    embedding = HuggingFaceEmbeddings() # Carrega o modelo que transforma palavras em números (vetores).

    vector_store = Chroma( # Cria o banco de dados Chroma
        embedding_function=embedding,
        persist_directory=persist_directory,
    ) 
    vector_store.add_documents( # Transfere os pedaços de texto para o banco de dados, convertendo-os em vetores.
        documents=chunks,
    )
