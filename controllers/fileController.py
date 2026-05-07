from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException
from models.file import File

from rag.pdf_extractor import extract_text_from_pdf
from rag.text_splitter import split_text_into_chunks
from rag.vector_store import store_chunks_in_vector_db

import shutil
import os

rag_router = APIRouter()


@rag_router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = FastAPIFile(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:
        os.makedirs("files", exist_ok=True)

        file_location = f"files/{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ext = os.path.splitext(file.filename)[1]

        extracted_text = extract_text_from_pdf(file_location)

        chunks = split_text_into_chunks(extracted_text)

        file_obj = await File.create(
            filename=file.filename,
            file_path=file_location,
            file_type=ext,
            extracted_text=extracted_text,
            is_active=False
        )
        vector_store = store_chunks_in_vector_db(chunks, file_obj.id)

        return {
            "message": "PDF uploaded and indexed successfully",
            "total_chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
# Activate File
@rag_router.post("/file/{file_id}/activate")
async def activate_file(file_id: int):
    file_obj = await File.get_or_none(id=file_id)
    if not file_obj:
        return {"error": "File not found"}
    await File.filter().update(is_active=False)

    file_obj.is_active = True
    await file_obj.save()
    return {
        "message": f"{file_obj.filename} activated"
    }

# Deactivate File
@rag_router.post("/file/{file_id}/deactivate")
async def deactivate_file(file_id: int):
    file_obj = await File.get_or_none(id=file_id)
    if not file_obj:
        return {"error": "File not found"}
    await File.filter().update(is_active=False)

    file_obj.is_active = False
    await file_obj.save()
    return {
        "message": f"{file_obj.filename} deactivated"
    }