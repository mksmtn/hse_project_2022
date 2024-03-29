from models.baseline_model import BaselineModel
from models.svd_model import SVDModel

from models.lightfm_model import LightfmModel
from utils import make_subsample

import os
import warnings
import pandas as pd

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    if os.path.isfile("subsample.csv"):
        subsample = pd.read_csv("subsample.csv")
    else:
        subsample = make_subsample(2000, 3000)
        subsample.to_csv("subsample.csv", index=False)

    print(f"Subsample size: {subsample.shape}")
    svd_model = SVDModel({"n_factors": 30, "top_k": 10}, name="SVD")

    print(f"{svd_model.name} model metrics:")
    print(svd_model.show_report(subsample.drop(columns=["count"])))

    baseline_model = BaselineModel({"top_k": 10}, name="Baseline")
    print(f"{baseline_model.name} model metrics:")
    print(baseline_model.show_report(subsample.drop(columns=["count"])))

    lightfm_model = LightfmModel(
       {
           'no_components': 60,
           'learning_schedule': 'adadelta',
           'loss': 'warp',
           'learning_rate': 0.0035804710258826042,
           'item_alpha': 3.801716649932694e-08,
           'user_alpha': 3.3596022700403683e-09,
           'max_sampled': 15,
           'random_state': 42},
       name='Lightfm'
    )

    print(f'{lightfm_model.name} model metrics:')
    print(lightfm_model.show_report(subsample.drop(columns=['rating'])))
