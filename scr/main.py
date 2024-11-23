from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import google.generativeai as genai
import io
import os


def remove_asterick(text):
    text = text.replace('*', '')
    text = text.replace('/n', '')
    return text

app = FastAPI()

# Configure Gemini API

KEY = os.getenv("API")
genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Define the analysis prompt
ANALYSIS_PROMPT = """
You are a seasoned and well experienced Crop Doctor. Analyze this crop image and provide:
- Possible Name of Disease:
- Observation:
- Cause:
- Cure step by step procedures
- Future Prevention
If the crops look healthy, describe their condition.
"""

@app.post("/analyze-crop")
async def analyze_crop(file: UploadFile = File(...)):
    try:
        # Read and validate image
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Please upload an image file")
            
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Get analysis from Gemini
        response = model.generate_content([ANALYSIS_PROMPT, image])
        
        return {
            "status": "success",
            "analysis": remove_asterick(response.text)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)