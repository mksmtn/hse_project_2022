import pandas as pd
import pickle
import csv
from src.config import tracks_path, pickle_directory_path

def _init():
    model = pickle.load(open(f'{pickle_directory_path}/model.pickle', 'rb'))
    user_features = pickle.load(open(f'{pickle_directory_path}/user_features.pickle', 'rb'))
    test_interactions = pickle.load(open(f'{pickle_directory_path}/test_interactions.pickle', 'rb'))
    train_interactions = pickle.load(open(f'{pickle_directory_path}/train_interactions.pickle', 'rb'))
    dataset = pickle.load(open(f'{pickle_directory_path}/dataset.pickle', 'rb'))
    predictions = pickle.load(open(f'{pickle_directory_path}/predictions.pickle', 'rb'))
    user_id_map, user_feature_map, item_id_map, _ = dataset.mapping()
    track_index_map = {v: k for k, v in  item_id_map.items()}
    tracks = pd.read_csv(tracks_path, sep='\t', na_values='', na_filter=False, error_bad_lines=False, quoting=csv.QUOTE_NONE)
    return predictions, user_id_map, track_index_map, tracks

predictions, user_id_map, track_index_map, tracks = _init()
