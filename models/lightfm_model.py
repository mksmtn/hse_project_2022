from lightfm.data import Dataset
from lightfm.evaluation import auc_score, precision_at_k, recall_at_k, reciprocal_rank
from lightfm.cross_validation import random_train_test_split
from lightfm import LightFM
import dask.dataframe as dd

from models.abstract_model import AbstractModel


class LightfmModel(AbstractModel):
    """
    CF model using lightfm lib
    """

    def __init__(self, hyperparams: dict, name: str) -> None:
        super().__init__(hyperparams, name)
        self.model = LightFM(**self.hyperparams)

    def preprocess_data(self, data: pd.DataFrame, test_size=0.2, random_state=42) -> None:
        """
        Split data on train and test and create interactions and weights
        :param data: DataFrame with columns user_id, item_id, rating
        :param test_size: size of test dataset
        :param random_state: seed for random generator
        """
        dataset = Dataset()
        dataset.fit(data.user_id, data.track_id)
        (interactions, weights) = dataset.build_interactions(data.itertuples(False, None))
        (train_interactions, test_interactions) = random_train_test_split(
            interactions,
            test_percentage=test_size,
            random_state=random_state,
        )

        (train_weights, test_weights) = random_train_test_split(
            weights,
            test_percentage=test_size,
            random_state=random_state,
        )

        self.data['interactions'] = {'train': train_interactions,
                                     'test': test_interactions}

        self.data['weights'] = {'train': train_weights,
                                'test': test_weights}

    def fit(self) -> None:
        """
        Fit train data
        """
        self.model.fit(
            self.data['interactions']['train'],
            sample_weight=self.data['weights']['train'],
            epochs=50,
            num_threads=12,
            verbose=True,
        )

    def build_report(self) -> pd.DataFrame:
        """
        Calculate metrics available for the Lightfm model
        :return: DataFrame with columns metric, value
        """
        return pd.DataFrame({'metric': ['precision@10',
                                        'recall@10',
                                        'auc_score',
                                        'reciprocal_rank'],
                             'value': [precision_at_k(
                                             self.model,
                                             self.data['interactions']['test'],
                                             self.data['interactions']['train'],
                                             k=10,
                                             num_threads=12,
                                         ).mean(),
                                       recall_at_k(
                                           self.model,
                                           self.data['interactions']['test'],
                                           self.data['interactions']['train'],
                                           k=10,
                                           num_threads=12,
                                       ).mean(),
                                       auc_score(
                                           self.model,
                                           self.data['interactions']['test'],
                                           self.data['interactions']['train'],
                                           num_threads=12,
                                       ).mean(),
                                       reciprocal_rank(
                                           self.model,
                                           self.data['interactions']['test'],
                                           self.data['interactions']['train'],
                                           num_threads=12,
                                       ).mean()
                                       ]
                             })
