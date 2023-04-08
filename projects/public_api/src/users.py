from src.init import user_id_map

def get_user_index(user_id: str) -> int:
    return user_id_map[user_id]
