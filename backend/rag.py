import os
import json
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

import chromadb
from chromadb.config import Settings


# function to read JSON Q&A files
def load_json_documents():

    documents = []

    folder = "documents"

    for file in os.listdir(folder):

        if file.endswith(".json"):

            with open(f"{folder}/{file}", "r", encoding="utf-8") as f:

                data = json.load(f)

                for item in data:

                    text = f"""
                    Question:
                    {item['question']}

                    Answer:
                    {item['answer']}
                    """

                    documents.append(text)

    return documents




# function to read PDF files
def load_pdf_documents():

    documents = []

    folder = "documents"

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            reader = PdfReader(f"{folder}/{file}")

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            documents.append(text)

    return documents

# split large text into smaller chunks

def split_text(text, chunk_size=300):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i+chunk_size])

        chunks.append(chunk)

    return chunks


# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# convert text list into embeddings
def create_embeddings(text_list):

    embeddings = model.encode(text_list)

    return embeddings


# create vector database client
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(

    name="legal_documents"

)


# store embeddings in vector DB
def store_embeddings(text_list):

    embeddings = create_embeddings(text_list)

    for i, text in enumerate(text_list):

        collection.add(

            documents=[text],

            embeddings=[embeddings[i]],

            ids=[str(i)]

        )


# search relevant documents
def search_documents(query):

    # convert user question to embedding
    query_embedding = create_embeddings([query])

    # search similar text
    results = collection.query(

        query_embeddings=query_embedding,

        n_results=3

    )

    return results["documents"][0]
