import pandas as pd


def make_subsample(n_users: int, n_items: int, random_state=42) -> pd.DataFrame:
    """
    Make a subsample from listening-counts.tsv with :n_users users
    and :n_items most popular items, make column rating based on count column
    :param random_state: seed for random generator
    :param n_users: number of users to keep
    :param n_items: number of items to keep
    :return: DataFrame with columns user_id, item_id, rating, count
    """
    listening_counts = pd.read_csv('listening-counts.tsv', sep='\t')
    users = pd.read_csv('users.tsv', sep='\t')
    users_sample = users[(users['age'] != -1) & (users['country'].notna())].sample(n_users,
                                                                                   random_state=random_state)

    counts_sample = listening_counts[listening_counts['user_id'].isin(users_sample['user_id'])]
    counts_sample['rating'] = counts_sample['count'] / counts_sample.groupby('user_id')['count'].transform('max')

    ratings_df = counts_sample[counts_sample['track_id'].isin(
        list(counts_sample.groupby('track_id').sum()['rating'].sort_values(ascending=False)[:n_items].index))]
    ratings_df['tracks_count'] = ratings_df.groupby('user_id')['count'].transform('count')
    ratings_df = ratings_df[ratings_df['tracks_count'] >= 5]
    ratings_df.drop(columns=['tracks_count'], inplace=True)
    return ratings_df

