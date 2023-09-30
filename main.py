import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.users import user_router


app = FastAPI()
app.title ="Mi primer API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind= engine)


@app.get("/", tags=['home'])
async def root():
    detalle_antes = {
                "mesage":"¡Hola FastAPI!",
                "servidor" : "Este es el servidos"
                }

    detalle = json.dumps(detalle_antes)
    return detalle

@app.get("/url", tags=['url'])
async def url():
    return { "url_curso":"https://moured.com/python" }

@app.get("/pru", tags=['HTML response'])
async def prueba_html():
    return HTMLResponse('<h1>Hello world</h1>')