from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_doc(file_path):
    loader = PyPDFLoader(file_path)
    data = data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(data)

    return docs
