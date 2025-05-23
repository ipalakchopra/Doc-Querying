from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from dotenv import load_dotenv
import os
load_dotenv()

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
loader = FireCrawlLoader(
    api_key=firecrawl_api_key, url="https://www.freeipa.org/", mode="crawl"
)
print(loader)
docs = []
docs_lazy = loader.load_and_split()

print(docs_lazy)
# async variant:
# docs_lazy = await loader.alazy_load()

# for doc in docs_lazy:
#     docs.append(doc)
# print(docs[0].page_content[:100])
# print(docs[0].metadata)
