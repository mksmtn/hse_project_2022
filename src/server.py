from fastapi import FastAPI
from init import predictions
from tracks import find_track_by_id

app = FastAPI()

@app.get('/')
def read_root():
    return '<h1>Welcome</h1><p>Get predictions for user</p><ul><li><a href="/users/1/predictions">User 1</a></li></ul>'


@app.get('/users/{user_id}/predictions')
def read_predictions_for_user(user_id: int, n: int = 5):
    user_predictions = predictions[user_id]
    best_n = sorted(enumerate(user_predictions[0]), key=lambda x: x[1])[:n]
    best_n_indices = map(lambda x: x[0], best_n)
    best_n_tracks = map(find_track_by_id, best_n_indices)
    return list(best_n_tracks)
