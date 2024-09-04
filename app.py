# FASTAPI REQ
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
# import stuff  # Replace with actual module name if necessary
from inference_sdk import InferenceHTTPClient
import uvicorn
import os
import multipart

# Initialize database collections
# img_collection = stuff.db["images"]  # Update if needed

# init APP
app = FastAPI()
origins = [
    "*"
]

# Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="XHaFXRyw5dZyr6rSletk"
)

@app.post("/check_forgery")
async def check_forgery(image: UploadFile = File(...)):
    # Save the uploaded image to a temporary location
    temp_image_path = f"temp_{image.filename}"
    with open(temp_image_path, "wb") as temp_image_file:
        shutil.copyfileobj(image.file, temp_image_file)

    # Perform forgery detection
    try:
        result = CLIENT.infer(temp_image_path, model_id="document-forgery-detection/2")
    finally:
        # Clean up the temporary file
        os.remove(temp_image_path)

    # Determine if there is forgery
    if not result['predictions']:
        return {"response": "No forgery detected"}
    else:
        confidence = result['predictions'][0]['confidence']
        return {"response": "Forgery detected", "confidence": confidence}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
