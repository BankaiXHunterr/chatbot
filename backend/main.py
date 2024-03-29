from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from modules.read_content import FileProcessor
from modules.llm import ConversationHandler
import os
# Load environment variables from .env file (if any)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))



class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/predict", response_model=Response)
async def predict(file: UploadFile = File(...), question: str = Form(...)) -> Any:
  # Check if file is a CSV file

    print("Received question:", question)
    print("Received file:", file.filename)

    file_extension = file.filename.split('.')[-1]
    allowed_ext = ["txt",'csv','pdf','docx']
    if  file_extension not in allowed_ext:
        return JSONResponse(status_code=400, content={"error": "Only CSV files are allowed."})

    try:
        # Read file content
        file_content = await file.read()
        fileProcessor = FileProcessor()
        file_content = await fileProcessor.process_file_by_extension(file_content=file_content,file_extension=file_extension)

        conversation_handler = ConversationHandler()
        text_chunks = await conversation_handler.get_text_chunks(file_content)
        await conversation_handler.get_vector_store(text_chunks)
        user_question = question
        res = await conversation_handler.user_input(user_question)

        return {"result": res}
    except Exception as e:  # Catch any unexpected errors
        print(f"Error processing file: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error."})