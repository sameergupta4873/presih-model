# FASTAPI REQ
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# CUSTOM REQ
# TODO: stuff -> change to actual name of module which reads from database
import stuff
from inference_sdk import InferenceHTTPClient
import uvicorn

# Initialize database collections
img_collection = stuff.db["images"]

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


@app.get("/check_forgery")
async def check_forgery(image_id: str):
    # TODO: change as per database schema
    image_data = img_collection.find_one({"_id": image_id})
 
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")

    # Get the image URL (assuming it's always present)
    image_url = image_data["image_url"]

    # Perform forgery detection
    result = CLIENT.infer(image_url, model_id="document-forgery-detection/2")

    # Determine if there is forgery
    if not result['predictions']:
        return {"response": "No forgery detected"}
    else:
        confidence = result['predictions'][0]['confidence']
        return {"response": "Forgery detected", "confidence": confidence}
    
if __name__ == '__main__':
    uvicorn.run(app)

