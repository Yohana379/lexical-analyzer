from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from lexer import tokenize_source_code
from docx import Document
import io
import uvicorn

app = FastAPI(title="Lexical Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

@app.post("/tokenize")
async def tokenize_endpoint(code: str = Form(...)):
    try:
        tokens = tokenize_source_code(code)
        return {
            "status": "success",
            "tokens": tokens,
            "count": len(tokens)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "tokens": []
        }

@app.post("/tokenize-file")
async def tokenize_file_endpoint(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith('.docx'):
            code_text = extract_text_from_docx(file_content)
        else:
            code_text = file_content.decode('utf-8')
        
        tokens = tokenize_source_code(code_text)
        
        return {
            "status": "success",
            "filename": filename,
            "tokens": tokens,
            "count": len(tokens)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "tokens": []
        }

@app.get("/")
async def root():
    return {"message": "Lexical Analyzer API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)