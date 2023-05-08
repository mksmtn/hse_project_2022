import pandas as pd

from models.abstract_model import AbstractModel
from metrics import calc_precision_at_k, calc_recall_at_k, calc_roc_auc
from utils import default_train_test_split, default_interactions_df


class BaselineModel(AbstractModel):
    """
    Top n items for all users
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

    def add_prediction(self) -> None:
        """
        Add predictions to interactions_df
        """
        predictions = []
        sorted_tracks = (
            self.data["train_df"]
            .groupby("track_id")
            .sum()["rating"]
            .sort_values(ascending=False)
            .reset_index()
        )

        for user_id in self.data["interactions_df"].index:
            prediction = (
                sorted_tracks[
                    ~sorted_tracks["track_id"].isin(  # убираем треки из трейна
                        self.data["train_df"][
                            self.data["train_df"]["user_id"] == user_id
                        ]["track_id"]
                    )
                ]
                .head(self.hyperparams["top_k"])["track_id"]
                .tolist()
            )

            predictions.append(prediction)

        self.data["interactions_df"]["prediction_baseline"] = predictions

    def fit(self) -> None:
        self.build_interactions_df()
        self.add_prediction()

    def build_report(self) -> pd.DataFrame:
        """
        Calculate all metrics available for the baseline model
        :return: DataFrame with columns metric, value
        """
        return pd.DataFrame(
            {
                "metric": ["precision@10", "recall@10", "ROC AUC"],
                "value": [
                    calc_precision_at_k(
                        self.data["interactions_df"], "prediction_baseline", 10
                    ),
                    calc_recall_at_k(
                        self.data["interactions_df"], "prediction_baseline", 10
                    ),
                    calc_roc_auc(
                        self.data["interactions_df"], "prediction_baseline", 10
                    ),
                ],
            }
        )
