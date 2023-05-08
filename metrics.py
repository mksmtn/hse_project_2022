import pandas as pd
import numpy as np


def calc_precision_at_k(
    interactions_df: pd.DataFrame, prediction_column: str, k: int
) -> float:
    """
    Precision@k = (# of recommended items @k that are relevant) / (# of recommended items @k)
    :param interactions_df: DataFrame with columns true_train, true_test, prediction_column
    :param prediction_column: name of column with prediction
    :param k: parameter of metric
    :return: precision@k
    """
    return (
        interactions_df.apply(
            lambda row: len(
                set(row["true_test"]).intersection(set(row[prediction_column][:k]))
            )
            / len(row[prediction_column][:k]),
            axis=1,
        )
    ).mean()


def calc_recall_at_k(
    interactions_df: pd.DataFrame, prediction_column: str, k: int
) -> float:
    """
    Recall@k = (# of recommended items @k that are relevant) / (total # of relevant items)
    :param interactions_df: DataFrame with columns true_train, true_test, prediction_column
    :param prediction_column: name of column with prediction
    :param k: parameter of metric
    :return: recall@k
    """
    return (
        interactions_df.apply(
            lambda row: len(
                set(row["true_test"]).intersection(set(row[prediction_column][:k]))
            )
            / len(row["true_test"])
            + 0.001,
            axis=1,
        )
    ).mean()


def roc_auc_user(row: pd.Series, prediction_column: str, k: int) -> float:
    mask = np.in1d(row[prediction_column][:k], row["true_test"]).astype(int)
    true_ind = mask.nonzero()[0]
    n = len(mask)
    r = len(true_ind)
    if r == 0:
        return 0.5
    s = 0
    for i in true_ind:
        if i + 1 != n:
            s += np.sum(1 - mask[i + 1 :])
    return s / (r * (n - r))


def calc_roc_auc(
    interactions_df: pd.DataFrame, prediction_column: str, k: int
) -> float:
    """
    Calculate ROC AUC
    :param interactions_df: DataFrame with columns true_train, true_test, prediction_column
    :param prediction_column: name of column with prediction
    :param k: parameter of metric
    :return: ROC AUC
    """
    return (
        interactions_df.apply(roc_auc_user, args=(prediction_column, k), axis=1)
    ).mean()
