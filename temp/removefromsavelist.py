# Simulated in-memory bookmark database
# Format: {user_id: set of bookmarked post_ids}
bookmarks_db = {
    "user_001": {101, 102, 105},
    "user_002": {103},
    "user_003": {104, 105},
}

def get_user_bookmarks(user_id):
    """Retrieve all bookmarked post IDs for a user."""
    return bookmarks_db.get(user_id, set())

def unbookmark_post(user_id, post_id):
    """Unbookmark a post for a user if it exists in their bookmarks."""
    print(f"\nAttempting to unbookmark Post {post_id} for User '{user_id}'...")
    bookmarked_posts = get_user_bookmarks(user_id)

    if post_id in bookmarked_posts:
        bookmarked_posts.remove(post_id)
        bookmarks_db[user_id] = bookmarked_posts
        print(f"✅ Post {post_id} has been removed from {user_id}'s bookmarks.")
        return True
    else:
        print(f"❌ Post {post_id} is not in {user_id}'s bookmarks. Nothing to remove.")
        return False

def display_user_bookmarks(user_id):
    """Print all bookmarked posts for a user."""
    bookmarks = get_user_bookmarks(user_id)
    if bookmarks:
        print(f"\n📌 {user_id}'s bookmarked posts: {sorted(bookmarks)}")
    else:
        print(f"\n📌 {user_id} has no bookmarked posts.")

# Example usage
display_user_bookmarks("user_001")
unbookmark_post("user_001", 102)
display_user_bookmarks("user_001")

# Trying to unbookmark a post that doesn't exist
unbookmark_post("user_001", 200)
