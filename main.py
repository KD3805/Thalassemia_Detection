# File: main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import logging

from ocr_utils import extract_text_from_file, extract_parameters_from_file
from ml_model import predict_thalassemia
from database import SessionLocal, BloodReport
from models import BloodReportModel  # Pydantic model for input validation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS (modify allowed_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-report/")
async def upload_report(file: UploadFile = File(...)):
    """
    Accept a blood report file (PDF or image), perform OCR, and extract parameters.
    Returns the extracted parameters for review.
    """
    try:
        suffix = file.filename.split(".")[-1]
        # Create a temporary file and write the content.
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}")
        contents = await file.read()
        temp_file.write(contents)
        temp_file.close()  # Ensure the file is closed so other processes can access it.
        logger.info(f"File saved to temporary path: {temp_file.name}")
    except Exception as e:
        logger.exception("Failed to save uploaded file.")
        raise HTTPException(status_code=500, detail="Failed to save file")

    if suffix.lower() in ["jpg", "jpeg", "png"]:
        file_type = "image"
    elif suffix.lower() == "pdf":
        file_type = "pdf"
    else:
        os.unlink(temp_file.name)
        logger.error("Unsupported file type encountered.")
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        # Process the temporary file to extract parameters.
        parameters = extract_parameters_from_file(temp_file.name, file_type)
        logger.info("Parameter extraction succeeded.")
    except Exception as e:
        logger.exception("Error during OCR processing or parameter extraction.")
        raise HTTPException(status_code=500, detail=f"Error during OCR processing: {str(e)}")
    finally:
        # Always delete the temporary file.
        try:
            os.unlink(temp_file.name)
            logger.info("Temporary file deleted.")
        except Exception as e:
            logger.warning(f"Could not delete temporary file: {e}")

    return JSONResponse(content={"extracted_parameters": parameters})

@app.post("/predict-report/")
async def predict_report(report: BloodReportModel):
    """
    Accept validated blood report parameters, perform prediction,
    store the record in the database, and return the prediction.
    """
    parameters = report.dict()
    
    try:
        prediction = predict_thalassemia(parameters)
        logger.info(f"Prediction completed: {prediction}")
    except Exception as e:
        logger.exception("Error during model prediction.")
        raise HTTPException(status_code=500, detail=f"Error during model prediction: {str(e)}")
    
    try:
        db = SessionLocal()
        blood_report_entry = BloodReport(
            sex=parameters.get("sex"),
            hb=parameters.get("hb"),
            pcv=parameters.get("pcv"),
            rbc=parameters.get("rbc"),
            mcv=parameters.get("mcv"),
            mch=parameters.get("mch"),
            mchc=parameters.get("mchc"),
            rdw=parameters.get("rdw"),
            wbc=parameters.get("wbc"),
            neut=parameters.get("neut"),
            lymph=parameters.get("lymph"),
            plt=parameters.get("plt"),
            hba=parameters.get("hba"),
            hba2=parameters.get("hba2"),
            hbf=parameters.get("hbf"),
            prediction=prediction,  # Stored as integer
        )
        db.add(blood_report_entry)
        db.commit()
        db.refresh(blood_report_entry)
        db.close()
        logger.info(f"Record saved with id: {blood_report_entry.id}")
    except Exception as e:
        logger.exception("Database error during record insertion.")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return JSONResponse(content={
        "prediction": prediction,
        "report_id": blood_report_entry.id,
        "parameters": parameters
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
