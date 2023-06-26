import pandas as pd
import pickle
import csv
from src.config import tracks_path, pickle_directory_path

def _init():
    dataset = pickle.load(open(f'{pickle_directory_path}/dataset.pickle', 'rb'))
    predictions = pickle.load(open(f'{pickle_directory_path}/predictions.pickle', 'rb'))
    user_id_map, user_feature_map, item_id_map, _ = dataset.mapping()
    track_index_map = {v: k for k, v in  item_id_map.items()}
    tracks = pd.read_csv(tracks_path, sep='\t', na_values='', na_filter=False, error_bad_lines=False, quoting=csv.QUOTE_NONE)
    return predictions, user_id_map, track_index_map, tracks, dataset

predictions, user_id_map, track_index_map, tracks, dataset = _init()
