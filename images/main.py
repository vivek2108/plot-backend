from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import cv2
import pytesseract
import numpy as np
import json
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store extracted plots in memory for now
plot_data = []

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    plots = []
    for i, contour in enumerate(contours):
        epsilon = 0.02 * cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, epsilon, True)

        area = cv2.contourArea(polygon)
        if area < 500:  # Skip small areas (likely text or noise)
            continue

        if len(polygon) < 4:  # Skip shapes that are not polygonal
            continue

        x, y, w, h = cv2.boundingRect(polygon)

        # ✅ Aspect ratio filtering
        aspect_ratio = w / h if h != 0 else 0
        if aspect_ratio < 0.5 or aspect_ratio > 2.0:
            continue  # Skip very tall or very wide shapes

        # Optionally skip near-square contours that are too small
        if w < 50 or h < 50:
            continue

        roi = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config="--psm 6")

        plots.append({
            "plot_number": f"Plot_{i}",
            "raw_text": text.strip(),
            "polygon_coordinates": polygon[:, 0].tolist()
        })

    global plot_data
    plot_data = plots

    return {"status": "success", "num_plots": len(plots)}

@app.get("/plots/")
def get_plots():
    return JSONResponse(content=plot_data)

@app.get("/")
def get_frontend():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
