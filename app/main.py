from fastapi import FastAPI, Response, Request
from app.pdf_generator import generate_pdf

app = FastAPI()

@app.post("/generate-report")
async def generate_report(request: Request):
    # Leer el JSON enviado por el cliente
    data = await request.json()

    # Generar el PDF usando el módulo pdf_generator
    pdf_binary = generate_pdf(data)

    # Retornar el PDF como respuesta
    headers = {'Content-Disposition': 'inline; filename="Reporte.pdf"'}
    return Response(content=pdf_binary, media_type="application/pdf", headers=headers)

@app.post("/receive-data")
async def receive_data(request: Request):
    # Leer el JSON enviado por el cliente
    data = await request.json()

    # Retornar los datos recibidos como respuesta JSON
    return data