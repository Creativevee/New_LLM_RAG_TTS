from rag import index_document, search_docs

index_document()

query = "How does the system answer questions?"
results = search_docs(query)

print(results)
