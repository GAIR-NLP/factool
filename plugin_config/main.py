import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from factool.factool import Factool

foundation_model = 'gpt-4'
factool_instance = Factool(foundation_model)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FactCheckRequest(BaseModel):
    prompt: str
    response: str
    entry_point: Optional[str]

class FactCheckResponse(BaseModel):
    fact_check_result: List[Dict[str, Union[str, List[str]]]]

fact_checks = {}

@app.post("/fact_check_kbqa")
async def fact_check_kbqa(request_data: FactCheckRequest):
    request_obj = FactCheckRequest(**request_data.dict())
    fact_check_result = await factool_instance.run_for_plugin([{'prompt': request_obj.prompt, 'response': request_obj.response, 'category': 'kbqa'}])
    fact_check_id = len(fact_checks) + 1
    fact_checks[fact_check_id] = fact_check_result
    return JSONResponse(content={"fact_check_id": fact_check_id, "fact_check_result": fact_check_result})

@app.post("/fact_check_code")
async def fact_check_code(request_data: FactCheckRequest):
    request_obj = FactCheckRequest(**request_data.dict())
    fact_check_result = await factool_instance.run_for_plugin([{'prompt': request_obj.prompt, 'response': request_obj.response, 'category': 'code', 'entry_point': request_obj.entry_point}])
    fact_check_id = len(fact_checks) + 1
    fact_checks[fact_check_id] = fact_check_result
    return JSONResponse(content={"fact_check_id": fact_check_id, "fact_check_result": fact_check_result})

@app.post("/fact_check_math")
async def fact_check_math(request_data: FactCheckRequest):
    request_obj = FactCheckRequest(**request_data.dict())
    fact_check_result = await factool_instance.run_for_plugin([{'prompt': request_obj.prompt, 'response': request_obj.response, 'category': 'math'}])
    fact_check_id = len(fact_checks) + 1
    fact_checks[fact_check_id] = fact_check_result
    return JSONResponse(content={"fact_check_id": fact_check_id, "fact_check_result": fact_check_result})

@app.post("/fact_check_scientific_literature")
async def fact_check_scientific_literature(request_data: FactCheckRequest):
    request_obj = FactCheckRequest(**request_data.dict())
    fact_check_result = await factool_instance.run_for_plugin([{'prompt': request_obj.prompt, 'response': request_obj.response, 'category': 'scientific'}])
    fact_check_id = len(fact_checks) + 1
    fact_checks[fact_check_id] = fact_check_result
    return JSONResponse(content={"fact_check_id": fact_check_id, "fact_check_result": fact_check_result})

@app.get("/get_fact_check/{fact_check_id}")
async def get_fact_check(fact_check_id: int):
    if fact_check_id in fact_checks:
        fact_check_result = fact_checks[fact_check_id]
        return JSONResponse(content={"fact_check_id": fact_check_id, "fact_check_result": fact_check_result})
    else:
        return JSONResponse(content={"error": "Fact check not found"})

@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return FileResponse(filename, media_type="image/png")

@app.get("/.well-known/ai-plugin.json")
async def read_plugin_manifest():
    return FileResponse(".well-known/ai-plugin.json")

@app.get("/openapi.yaml")
async def openapi_spec():
    return FileResponse("./openapi.yaml")

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003, log_level="info")

if __name__ == "__main__":
    main()