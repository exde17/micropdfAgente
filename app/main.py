
from fastapi import Depends, FastAPI, Response, Request,  HTTPException
from sqlalchemy import text
from app.pdf_generator import generate_pdf
from fastapi.middleware.cors import CORSMiddleware
# from app.db import get_db
from sqlalchemy.orm import Session
from app.db_connection import get_db_connection
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://tudominio.com"] en vez de "*" por seguridad
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.post("/generate-report")
async def generate_report(data: dict):
    """
    Genera un reporte en PDF basado en los datos recibidos.
    """
    # Generar el PDF usando el módulo pdf_generator
    pdf_binary = generate_pdf(data)

    # Retornar el PDF como respuesta
    headers = {'Content-Disposition': 'inline; filename="Reporte.pdf"'}
    return Response(content=pdf_binary, media_type="application/pdf", headers=headers)

@app.post("/receive-data")
async def receive_data(request: Request):
    """
    Recibe datos en formato JSON y decide si debe generar un reporte o devolver una respuesta natural.
    """
    # Leer el JSON enviado por el cliente
    data = await request.json()

    # Verificar si la clave "tipo" está en el JSON
    tipo = data.get("tipo", "").lower()

    if tipo == "reporte":
        # Si el tipo es "reporte", llamar a generate_report con data como parámetro directamente
        # return await generate_report(data)
        return data
    elif tipo == "natural":
        # Si el tipo es "natural", devolver una respuesta en JSON con el texto adecuado
        respuesta = data.get("respuesta", "¡Hola! ¿En qué puedo ayudarte hoy?")
        return {"output": {"tipo": "natural", "respuesta": respuesta}}
    else:
        # Si el tipo no es válido, devolver un mensaje de error
        return {"error": "Tipo de solicitud no reconocido. Usa 'reporte' o 'natural'."}

# -------------------- NUEVOS ENDPOINTS --------------------

@app.get("/usuarios")
async def get_usuarios():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM security.users;")  # Asegúrate de que esta tabla exista

        # Obtiene los nombres de las columnas
        column_names = [desc[0] for desc in cur.description]

        # Convierte cada fila en un diccionario
        # usuarios = [dict(zip(column_names, row)) for row in cur.fetchall()]
        # Convierte cada fila en un diccionario y excluye el campo "password"
        usuarios = [
            {key: value for key, value in zip(column_names, row) if key != "password"}
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return {"usuarios": usuarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/usuarios/count")
async def get_total_usuarios():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")

    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM security.users;")  # Contar el total de usuarios
        total_usuarios = cur.fetchone()[0]  # Obtener el resultado

        cur.close()
        conn.close()

        return {"total_usuarios": total_usuarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

#creamos el endpoint para obtener las calificaciones
@app.get("/calificaciones")
async def get_calificaciones():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.calificacion;")  # Asegúrate de que esta tabla exista

        # Obtiene los nombres de las columnas
        column_names = [desc[0] for desc in cur.description]

        # Convierte cada fila en un diccionario
        calificaciones = [dict(zip(column_names, row)) for row in cur.fetchall()]

        cur.close()
        conn.close()

        return {"calificaciones": calificaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))       
    
#promedio de calificaciones
# @app.get("/promedio-calificaciones")
# async def get_calificaciones():
#     conn = get_db_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")

#     try:
#         cur = conn.cursor()
#         cur.execute('SELECT "usuarioId", puntaje FROM public.calificacion;')

#         # Procesar los resultados para calcular el promedio por usuario
#         calificaciones_raw = cur.fetchall()

#         # Diccionario para acumular los puntajes por usuario
#         usuarios_calificaciones = {}

#         for usuario_id, puntaje in calificaciones_raw:
#             if usuario_id in usuarios_calificaciones:
#                 usuarios_calificaciones[usuario_id]['suma_puntaje'] += puntaje
#                 usuarios_calificaciones[usuario_id]['cantidad'] += 1
#             else:
#                 usuarios_calificaciones[usuario_id] = {'suma_puntaje': puntaje, 'cantidad': 1}

#         # Calcular el promedio para cada usuario
#         calificaciones = [
#             {
#                 "usuarioId": usuario_id,
#                 "promedio_puntaje": round(data['suma_puntaje'] / data['cantidad'], 2)
#             }
#             for usuario_id, data in usuarios_calificaciones.items()
#         ]

#         cur.close()
#         conn.close()

#         return {"calificaciones": calificaciones}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))    

@app.get("/promedio-calificaciones")
async def get_calificaciones():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # JOIN entre calificacion y users para obtener el nombre del proyecto
        query = """
            SELECT c."usuarioId", c.puntaje, u."nombre-proyecto"
            FROM public.calificacion c
            JOIN security.users u ON c."usuarioId" = u.id;
        """
        cur.execute(query)

        calificaciones_raw = cur.fetchall()

        # Diccionario para acumular los puntajes por usuario
        usuarios_calificaciones = {}

        for row in calificaciones_raw:
            usuario_id = row['usuarioId']
            puntaje = row['puntaje']
            nombre_proyecto = row['nombre-proyecto']

            if usuario_id in usuarios_calificaciones:
                usuarios_calificaciones[usuario_id]['suma_puntaje'] += puntaje
                usuarios_calificaciones[usuario_id]['cantidad'] += 1
            else:
                usuarios_calificaciones[usuario_id] = {
                    'suma_puntaje': puntaje,
                    'cantidad': 1,
                    'nombre-proyecto': nombre_proyecto
                }

        # Calcular el promedio para cada usuario
        calificaciones = [
            {
                # "usuarioId": usuario_id,
                "nombre-proyecto": data['nombre-proyecto'],
                "promedio_puntaje": round(data['suma_puntaje'] / data['cantidad'], 2)
            }
            for usuario_id, data in usuarios_calificaciones.items()
        ]

        cur.close()
        conn.close()

        return {"calificaciones": calificaciones}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
