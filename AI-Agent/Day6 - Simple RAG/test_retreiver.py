from retriever import load_documents, retriever

# result=load_documents()

# for file_name,detail in result.items():
#     print('-'*80)
#     print(file_name)
#     print(detail)

filename,content = retriever(input("\nProvide the search term: "))
print(filename)
print(content)

