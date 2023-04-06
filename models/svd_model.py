import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

from models.abstract_model import AbstractModel
from metrics import calc_precision_at_k, calc_recall_at_k


class SVDModel(AbstractModel):
    """
    CF model based on SVD
    """

    def __init__(self, hyperparams: dict, name: str) -> None:
        super().__init__(hyperparams, name)

    def preprocess_data(self, data: pd.DataFrame, test_size=0.2, random_state=42) -> None:
        """
        Split data on train and test
        :param data: DataFrame with columns user_id, item_id, rating
        :param test_size: size of test dataset
        :param random_state: seed for random generator
        """
        train, test = train_test_split(data,
                                       stratify=data['user_id'],
                                       test_size=test_size,
                                       random_state=random_state)
        self.data['train_df'] = train.set_index('user_id')
        self.data['test_df'] = test.set_index('user_id')
        self.data['full_df'] = data.set_index('user_id')

    def build_interactions_df(self) -> None:
        """
        Build DataFrame with two columns that contain lists of
        train and test interactions
        """
        interactions_df = (self.data['train_df']
                           .reset_index()
                           .groupby('user_id')['track_id']
                           .agg(lambda x: list(x)).reset_index()
                           .rename(columns={'track_id': 'true_train'})
                           .set_index('user_id'))

        interactions_df['true_test'] = (
            self.data['test_df']
            .reset_index()
            .groupby('user_id')['track_id'].agg(lambda x: list(x))
        )

        interactions_df.loc[pd.isnull(interactions_df.true_test), 'true_test'] = [
            [''] for x in range(len(interactions_df.loc[pd.isnull(interactions_df.true_test), 'true_test']))]

        self.data['interactions_df'] = interactions_df

    def add_prediction(self, cf_preds_df: pd.DataFrame):
        """
        Add predictions to interactions_df
        """
        cf_preds_df_t = cf_preds_df.transpose()

        predictions = []

        for user_id in self.data['interactions_df'].index:
            prediction = (
                cf_preds_df_t
                .loc[user_id]
                .sort_values(ascending=False)
                .index.values
            )

            predictions.append(
                list(prediction[~np.in1d(
                    prediction,
                    self.data['interactions_df'].loc[user_id, 'true_train'])])[:self.hyperparams['top_k']])

        self.data['interactions_df']['prediction_svd'] = predictions

    def fit(self):
        """
        Fit train data
        """
        pivot_train = self.data['full_df'].pivot_table(index='user_id', columns='track_id', values='rating').fillna(0)
        csr_coll_matrix_train = csr_matrix(pivot_train)
        u, sigma, v = svds(csr_coll_matrix_train, k=self.hyperparams['n_factors'])
        sigma = np.diag(sigma)

        predicted_ratings_train = np.dot(np.dot(u, sigma), v)
        predicted_ratings_train_norm = (predicted_ratings_train -
                                        predicted_ratings_train.min()) / (predicted_ratings_train.max()
                                                                          - predicted_ratings_train.min())

        cf_preds_df = pd.DataFrame(predicted_ratings_train_norm,
                                   columns=pivot_train.columns,
                                   index=list(pivot_train.index)).transpose()

        self.build_interactions_df()
        self.add_prediction(cf_preds_df)

    def build_report(self) -> pd.DataFrame:
        """
        Calculate all metrics available for the SVD model
        :return: DataFrame with columns metric, value
        """
        return pd.DataFrame({'metric': ['precision@10',
                                        'recall@10'],
                             'value': [calc_precision_at_k(self.data['interactions_df'],
                                                           'prediction_svd',
                                                           10),
                                       calc_recall_at_k(self.data['interactions_df'],
                                                        'prediction_svd',
                                                        10)
                                       ]
                             })
