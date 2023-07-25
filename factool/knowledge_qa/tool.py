from factool.knowledge_qa.google_serper import GoogleSerperAPIWrapper

class google_search():
    def __init__(self, snippet_cnt):
        self.serper = GoogleSerperAPIWrapper(snippet_cnt=snippet_cnt)

    async def run(self, queries):
        return await self.serper.run(queries)

