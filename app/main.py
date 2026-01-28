from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="PDF Automation API",
    description="""
    A FastAPI-based system that extracts text from images using OCR and fills PDF forms.

    ## Features
    - **PDF Field Discovery**: Upload a PDF to see all fillable form fields
    - **OCR Text Extraction**: Extract text from images (NID, passport, documents)
    - **Structured Parsing**: Automatically detect names, dates, IDs, emails, phones
    - **PDF Form Filling**: Fill PDF forms with extracted or provided data
    - **Complete Workflow**: All-in-one endpoint for the full pipeline
    """,
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
