def publish_draft(draft):
    post = {
        "id": draft['id'],
        "title": draft['title'],
        "body": draft['content'],
        "status": "published"
    }
    print(f"Draft converted to Post: {post}")
    return post

# Example usage
draft = {"id": 3, "title": "My Draft", "content": "This is a draft."}
publish_draft(draft)
