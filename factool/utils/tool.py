import asyncio
from factool.knowledge_qa.google_serper import GoogleSerperAPIWrapper
from factool.utils.openai_wrapper import OpenAIEmbed
import json
import os
import numpy as np
import jsonlines
import pdb
import pickle
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class local_search():
    def __init__(self, snippet_cnt, data_link, embedding_link=None):
        self.snippet_cnt = snippet_cnt
        self.data_link = data_link
        self.embedding_link = embedding_link
        self.openai_embed = OpenAIEmbed()
        self.data = None
        self.embedding = None
        asyncio.run(self.init_async())
        
    
    async def init_async(self):
        if self.embedding_link is None:
            self.load_data_by_link()
            await self.calculate_embedding()
        else:
            self.load_embedding_by_link()

    def load_data_by_link(self):
        #load data from json link
        self.data = []
        #self.data = json.load(open(self.data_link, 'r'))
        with jsonlines.open(self.data_link) as reader:
            for obj in reader:
                try:
                    # self.data.append(os.path.splitext(self.data_link)[0].rsplit('/',1)[-1]+obj['text'])
                    self.data.append(obj['text'])
                except TypeError as e: # content in data_link is a list if strings
                    self.data.append(obj)

    def load_embedding_by_link(self):
        self.embedding = []
        #load embedding from self.embedding_link using pickle
        with open(self.embedding_link, "rb") as f:
            self.embedding = pickle.load(f)
    
    def save_embeddings(self):
        with open(self.data_link.replace(".jsonl",".pkl"), "wb") as f:
            pickle.dump(self.embedding, f)

    async def calculate_embedding(self):
        embedding = await self.openai_embed.async_run(self.data,retry=3)
        self.embedding = list(zip(self.data, embedding))
        self.save_embeddings()

    async def search(self, query, num = None):
        query_embed = await self.openai_embed.create_embedding(query)
        faiss = FAISS.from_embeddings(self.embedding, embedding=OpenAIEmbeddings(model="text-embedding-ada-002"))
        if(num is not None):
            related_docs = faiss.similarity_search_by_vector(query_embed, k=num)
        else:
            related_docs = faiss.similarity_search_by_vector(query_embed, k=self.snippet_cnt)
        related_docs = [{"content":doc.page_content,"source":"local"} for doc in related_docs]
        return related_docs
    
    async def run(self, queries):
        flattened_queries = []
        for sublist in queries:
            if sublist is None:
                sublist = ['None', 'None']
            for item in sublist:
                flattened_queries.append(item)
        
        snippets = await asyncio.gather(*[self.search(query) for query in flattened_queries])
        snippets_split = [snippets[i] + snippets[i+1] for i in range(0, len(snippets), 2)]
        return snippets_split

    def get_laws_from_index(self, index_list):
        result = []
        for index in index_list:
            try:
                result.append(self.embedding[index][0])
            except IndexError as e:
                result.append("不存在第{}条法律".format(index+1))
        return result
    