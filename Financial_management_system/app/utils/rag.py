from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import chromadb

# Load model (good for semantic search)
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(name="documents")


# =================================================
# 1. Chunking function
# =================================================
def split_text(text, chunk_size=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# =================================================
# 2. Create embeddings
# =================================================
def create_embedding(text):
    return model.encode(text).tolist()


# =================================================
# 3. Store with chunking
# =================================================
def store_document(doc_id, text):

    chunks = split_text(text)

    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{doc_id}_{i}"]   # unique id per chunk
        )


# =================================================
# 4. Delete all chunks of document
# =================================================
def delete_document(doc_id):

    # get all stored ids
    all_items = collection.get()

    ids_to_delete = [
        id_ for id_ in all_items["ids"]
        if id_.startswith(str(doc_id))
    ]

    collection.delete(ids=ids_to_delete)
    
# =================================================
# 5. Search in vector DB
# =================================================
def search_documents(query, top_k=3):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

# =================================================
# 6. Get all chunks of a document
# =================================================
def get_document_chunks(doc_id):

    all_items = collection.get()

    chunks = [
        doc for id_, doc in zip(all_items["ids"], all_items["documents"])
        if id_.startswith(str(doc_id))
    ]

    return chunks



# load reranker model (very good for relevance)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# =================================================
# 7. Rerank results
# =================================================
def rerank_results(query, documents, top_k=5):

    # create (query, doc) pairs
    pairs = [(query, doc) for doc in documents]

    # get scores
    scores = reranker.predict(pairs)

    # combine docs + scores
    scored_docs = list(zip(documents, scores))

    # sort by score (highest first)
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # return top results
    top_results = [doc for doc, score in scored_docs[:top_k]]

    return top_results



def search_with_rerank(query):

    # Step 1: vector search (top 20)
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=20
    )

    documents = results["documents"][0]

    # Step 2: rerank → top 5
    top_results = rerank_results(query, documents, top_k=5)

    return top_results