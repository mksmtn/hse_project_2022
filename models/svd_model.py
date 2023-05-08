import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

from models.abstract_model import AbstractModel
from metrics import calc_precision_at_k, calc_recall_at_k, calc_roc_auc
from utils import default_train_test_split, default_interactions_df


class SVDModel(AbstractModel):
    """
    CF model based on SVD
    """

    def preprocess_data(
        self, data: pd.DataFrame, test_size=0.2, random_state=42
    ) -> None:
        """
        Split data on train and test
        :param data: DataFrame with columns user_id, item_id, rating
        :param test_size: size of test dataset
        :param random_state: seed for random generator
        """
        self.data.update(default_train_test_split(data, test_size, random_state))

    def build_interactions_df(self) -> None:
        """
        Build DataFrame with two columns that contain lists of
        train and test interactions
        """
        self.data["interactions_df"] = default_interactions_df(
            self.data["train_df"], self.data["test_df"]
        )

    def add_prediction(self, cf_preds_df: pd.DataFrame):
        """
        Add predictions to interactions_df
        """
        cf_preds_df_t = cf_preds_df.transpose()

        predictions = []

        for user_id in self.data["interactions_df"].index:
            prediction = (
                cf_preds_df_t.loc[user_id].sort_values(ascending=False).index.values
            )

            predictions.append(
                list(
                    prediction[
                        ~np.in1d(
                            prediction,
                            self.data["interactions_df"].loc[user_id, "true_train"],
                        )
                    ]
                )[: self.hyperparams["top_k"]]
            )

        self.data["interactions_df"]["prediction_svd"] = predictions

    def fit(self):
        """
        Fit train data
        """
        pivot_train = (
            self.data["full_df"]
            .pivot_table(index="user_id", columns="track_id", values="rating")
            .fillna(0)
        )
        csr_coll_matrix_train = csr_matrix(pivot_train)
        u, sigma, v = svds(csr_coll_matrix_train, k=self.hyperparams["n_factors"])
        sigma = np.diag(sigma)

        predicted_ratings_train = np.dot(np.dot(u, sigma), v)
        predicted_ratings_train_norm = (
            predicted_ratings_train - predicted_ratings_train.min()
        ) / (predicted_ratings_train.max() - predicted_ratings_train.min())

        cf_preds_df = pd.DataFrame(
            predicted_ratings_train_norm,
            columns=pivot_train.columns,
            index=list(pivot_train.index),
        ).transpose()

        self.build_interactions_df()
        self.add_prediction(cf_preds_df)

    def build_report(self) -> pd.DataFrame:
        """
        Calculate all metrics available for the SVD model
        :return: DataFrame with columns metric, value
        """
        return pd.DataFrame(
            {
                "metric": ["precision@10", "recall@10", "ROC AUC"],
                "value": [
                    calc_precision_at_k(
                        self.data["interactions_df"], "prediction_svd", 10
                    ),
                    calc_recall_at_k(
                        self.data["interactions_df"], "prediction_svd", 10
                    ),
                    calc_roc_auc(self.data["interactions_df"], "prediction_svd", 10),
                ],
            }
        )
