import pandas as pd
from sklearn.model_selection import train_test_split


def make_subsample(n_users: int, n_items: int, random_state=42) -> pd.DataFrame:
    """
    Make a subsample from listening-counts.tsv with :n_users users
    and :n_items most popular items, make column rating based on count column
    :param random_state: seed for random generator
    :param n_users: number of users to keep
    :param n_items: number of items to keep
    :return: DataFrame with columns user_id, item_id, rating, count
    """
    listening_counts = pd.read_csv("listening-counts.tsv", sep="\t")
    users = pd.read_csv("users.tsv", sep="\t")
    users_sample = users[(users["age"] != -1) & (users["country"].notna())].sample(
        n_users, random_state=random_state
    )

    counts_sample = listening_counts[
        listening_counts["user_id"].isin(users_sample["user_id"])
    ]
    counts_sample["rating"] = counts_sample["count"] / counts_sample.groupby("user_id")[
        "count"
    ].transform("max")

    ratings_df = counts_sample[
        counts_sample["track_id"].isin(
            list(
                counts_sample.groupby("track_id")
                .sum()["rating"]
                .sort_values(ascending=False)[:n_items]
                .index
            )
        )
    ]
    ratings_df["tracks_count"] = ratings_df.groupby("user_id")["count"].transform(
        "count"
    )
    ratings_df = ratings_df[ratings_df["tracks_count"] >= 5]
    ratings_df.drop(columns=["tracks_count"], inplace=True)
    return ratings_df


def default_train_test_split(data: pd.DataFrame, test_size, random_state) -> dict:
    """
    Split data on train and test
    :param data: DataFrame with columns user_id, item_id, rating
    :param test_size: size of test dataset
    :param random_state: seed for random generator
    """
    train, test = train_test_split(
        data, stratify=data["user_id"], test_size=test_size, random_state=random_state
    )
    return {"train_df": train, "test_df": test, "full_df": data}


def default_interactions_df(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Build DataFrame with two columns that contain lists of
    train and test interactions
    :param train_df: DataFrame with train tracks
    :param test_df: DataFrame with test tracks
    :return: DataFrame with train and test interactions
    """
    interactions_df = (
        train_df.groupby("user_id")["track_id"]
        .agg(lambda x: list(x))
        .reset_index()
        .rename(columns={"track_id": "true_train"})
        .set_index("user_id")
    )

    interactions_df["true_test"] = test_df.groupby("user_id")["track_id"].agg(
        lambda x: list(x)
    )

    interactions_df.loc[pd.isnull(interactions_df.true_test), "true_test"] = [
        [""]
        for x in range(
            len(interactions_df.loc[pd.isnull(interactions_df.true_test), "true_test"])
        )
    ]

    return interactions_df
