from pandas import DataFrame, json_normalize
from numpy import unique
from lightfm.data import Dataset
from lightfm import LightFM
from json import loads


def json_to_df(new_data) -> DataFrame:
    data = json_normalize(loads(new_data))
    return data

def df_to_dataset(new_data: DataFrame, old_data: Dataset) -> Dataset:
    old_data.fit_partial(new_data.user_id, new_data.track_id)
    (new_interactions, new_weights) = old_data.build_interactions(old_data.itertuples(False, None))
    return new_interactions, new_weights

def retrain_model(model: LightFM, new_interactions, new_weights) -> LightFM:
    model.fit_partial(interactions=new_interactions, sample_weight=new_weights)
    return model