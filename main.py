from fastapi import FastAPI, Path, Query, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import json
from fastapi.security import HTTPBearer
from config.database import session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jsw_bearer import JWTBearer

app = FastAPI()
app.title ="Mi primer API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind= engine)

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 5, max_length =15)
    overview: str = Field(min_length = 15, max_length =50)
    year: int = Field(le = 2022)
    rating: float = Field(ge = 1, le = 10.0)
    category: str = Field(min_length = 5, max_length =15)

    class Config:
        schema_extra={
            "example":{
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 9.1,
                "category": "Acción"
            }
        }


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

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)

@app.get("/movies", tags=['Movies'], response_model = List[Movie], status_code=200 )
async def get_movies() -> List[Movie]:
    db = session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/{id}", tags=['Movies'], response_model=Movie)
async def get_movies_id(id: int = Path(ge=1, le=2000)) -> Movie:
    bd = session()
    result = bd.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get("/movies/", tags=['Movies'], response_model = List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    bd =session()
    result = bd.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def created_movie(movie: Movie) -> dict:
    db = session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"Mensaje": "Se ha registrado la pelicula."})

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    else:
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()
        return JSONResponse(status_code=200, content={'message': 'Se ha modificado la pelicula'})

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"Mensaje": "Se ha eliminado la pelicula."})