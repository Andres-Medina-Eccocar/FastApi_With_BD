from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from config.database import session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jsw_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie
movie_router = APIRouter()


@movie_router.get("/movies", tags=['Movies'], response_model = List[Movie], status_code=200 )
async def get_movies() -> List[Movie]:
    db = session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/{id}", tags=['Movies'], response_model=Movie)
async def get_movies_id(id: int = Path(ge=1, le=2000)) -> Movie:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=['Movies'], response_model = List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db =session()
    result = MovieService(db).get_movie_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def created_movie(movie: Movie) -> dict:
    db = session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"Mensaje": "Se ha registrado la pelicula."})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado la pelicula'})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'NO encontrado'})
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"Mensaje": "Se ha eliminado la pelicula."})