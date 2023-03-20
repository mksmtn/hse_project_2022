from abc import ABC, abstractmethod
import pandas as pd


class AbstractModel(ABC):
    """
    Abstract class to reduce operations performed on all models
    and define the structure of other models.
    """
    def __init__(self, hyperparams: dict, name: str) -> None:
        self.hyperparams = hyperparams
        self.name = name
        self.data = dict()

    @abstractmethod
    def preprocess_data(self, data: pd.DataFrame, test_size=0.2, random_state=42) -> None:
        """
        Split data on train and test, build CF matrix or perform other transformation
        :param data: DataFrame with columns user_id, item_id, count or rating
        :param test_size: size of test dataset
        :param random_state: seed for random generator
        """
        pass

    @abstractmethod
    def fit(self) -> None:
        """
        Fit train data
        """
        pass

    @abstractmethod
    def build_report(self) -> pd.DataFrame:
        """
        Calculate all metrics available for a model
        :return: DataFrame with columns metric, value
        """
        pass

    def show_report(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Show model performance
        :param data: DataFrame with columns user_id, item_id, count or rating
        :return: DataFrame with columns metric, value
        """
        self.preprocess_data(data)
        self.fit()
        return self.build_report()
