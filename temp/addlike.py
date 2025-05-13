def like_post(post_id, user_id):
    print(f"User {user_id} liked Post {post_id}")
    return {"post_id": post_id, "user_id": user_id, "status": "liked"}

# Example usage
like_post(42, "user_007")
