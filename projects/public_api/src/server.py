import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from pickle import dump, load
import numpy as np
from src.init import predictions, dataset
from src.tracks import find_track_by_id
from src.logger import logger
from src.config import pickle_directory_path
from src.data_processing import json_to_df, df_to_dataset, retrain_model

router = APIRouter(prefix='')

@router.get('/', response_class=HTMLResponse)
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

@router.post('/users/')
def retrain_with_new_data(request: Request):
    data = request.json()
    data = json_to_df(new_data=data)
    data = df_to_dataset(new_data=data, old_data=dataset)
    logger.info('Dataset has been updated with (num_users, num_items) = %s', data.interactions_shape())
    model_old = load(open(f'{pickle_directory_path}/model.pickle', 'rb'))
    model = retrain_model(model=model_old, new_interactions=data[0], new_weights=data[1])
    dump(model, f'{pickle_directory_path}/model.pickle')
    logger.info('The model is retrained and saved')
    return model

def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app=app)
