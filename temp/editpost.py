def fetch_post(post_id):
    print(f"Fetching post ID: {post_id}")
    return {"id": post_id, "title": "Original Post", "body": "Original content"}

def update_post(post, title=None, body=None):
    if title:
        post["title"] = title
    if body:
        post["body"] = body
    print(f"Updated Post: {post}")
    return post

# Example usage
post = fetch_post(2)
update_post(post, title="New Post Title", body="New content for the post.")
