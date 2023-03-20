import pandas as pd


def calc_precision_at_k(interactions_df: pd.DataFrame, prediction_column: str, k: int) -> float:
    """
    Precision@k = (# of recommended items @k that are relevant) / (# of recommended items @k)
    :param interactions_df: DataFrame with columns true_train, true_test, prediction_column
    :param prediction_column: name of column with prediction
    :param k: parameter of metric
    :return: precision@k
    """
    return (
        interactions_df
        .apply(
            lambda row:
            len(set(row['true_test']).intersection(
                set(row[prediction_column][:k]))) / len(row[prediction_column][:k]),
            axis=1)).mean()


def calc_recall_at_k(interactions_df: pd.DataFrame, prediction_column: str, k: int) -> float:
    """
        Recall@k = (# of recommended items @k that are relevant) / (total # of relevant items)
        :param interactions_df: DataFrame with columns true_train, true_test, prediction_column
        :param prediction_column: name of column with prediction
        :param k: parameter of metric
        :return: recall@k
        """
    return (
        interactions_df
        .apply(
            lambda row:
            len(set(row['true_test']).intersection(
                set(row[prediction_column][:k]))) / len(row['true_test']) + 0.001,
            axis=1)).mean()

