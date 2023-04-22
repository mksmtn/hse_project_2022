import uvicorn
from fastapi import FastAPI, APIRouter
import numpy as np
from src.init import predictions
from src.tracks import find_track_by_id
from src.logger import logger

router = APIRouter(prefix='')

@router.get('/')
def read_root():
    return '<h1>Welcome</h1><p>Get predictions for user</p><ul><li><a href="/users/1/predictions">User 1</a></li></ul>'


@router.get('/users/{user_id}/predictions')
def read_predictions_for_user(user_id: int, n: int = 5):
    if n > 100:
        raise ValueError('That, sir, would be too bold.')
    logger.info('Getting %d predictions for user %s', n, user_id)
    user_predictions = predictions.getrow(user_id)
    every_item = list(zip(user_predictions.indices, user_predictions.data))
    best_n = map(lambda x: x[0], sorted(every_item, key=lambda x: x[1])[:n])
    best_n_tracks = map(find_track_by_id, best_n)
    return list(best_n_tracks)

def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app=app)
