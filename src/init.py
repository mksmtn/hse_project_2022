import pandas as pd
import pickle
import csv
from config import tracks_path

def _init():
    model = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.model.pickle', 'rb'))
    user_features = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.user_features.pickle', 'rb'))
    test_interactions = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.test_interactions.pickle', 'rb'))
    train_interactions = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.train_interactions.pickle', 'rb'))
    dataset = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.dataset.pickle', 'rb'))
    predictions = pickle.load(open('../pickle/lightfm-filtered-split-userfeatures.predictions.pickle', 'rb'))
    user_id_map, user_feature_map, item_id_map, _ = dataset.mapping()
    track_index_map = {v: k for k, v in  item_id_map.items()}
    tracks = pd.read_csv(tracks_path, sep='\t', na_values='', na_filter=False, error_bad_lines=False, quoting=csv.QUOTE_NONE)
    return predictions.todense(), user_id_map, track_index_map, tracks

predictions, user_id_map, track_index_map, tracks = _init()
