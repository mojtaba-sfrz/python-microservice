from typing import List

from fastapi import APIRouter, HTTPException

from app.api.models import MovieIn, MovieOut, MovieUpdate

from app.api import db_manager
from app.api.service import is_cast_present

movies = APIRouter()


def look_for_casts(movie: MovieIn):

    for cast_id in movie.cast_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id {cast_id} not found.")


@movies.get('/', response_model=List[MovieOut])
async def get_movies():

    return await db_manager.get_all_movies()


@movies.get('/{id}', response_model=MovieOut)
async def get_movie(id: int):

    movie = await db_manager.get_movie(id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@movies.post('/', response_model=MovieOut, status_code=201)
async def add_movie(playload: MovieIn):

    look_for_casts(playload)

    movie_id = await db_manager.add_movie(playload)

    responce = {
        'id': movie_id,
        **playload.dict()
    }
    return responce


@movies.put('/{id}', response_model=MovieOut)
async def update_movie(id: int, playload: MovieUpdate):

    movie = await db_manager.get_movie(id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = playload.dict(exclude_unset=True)

    if playload.case_id:
        look_for_casts(playload)

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_movie(id, updated_movie)


@movies.delete('/{id}')
async def delete_movie(id: int):

    movie = await db_manager.get_movie(id)

    if not movie:
        raise HTTPException(
            status_code=404, detail=f"movie with id {id} not found")

    return await db_manager.delete_movie(id)
