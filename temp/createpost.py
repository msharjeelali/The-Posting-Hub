# Simulated in-memory post storage
post_db = []
post_id_counter = 1

def generate_post_id():
    global post_id_counter
    post_id = post_id_counter
    post_id_counter += 1
    return post_id

def create_post(title, body, author, tags=None):
    if tags is None:
        tags = []

    post = {
        "id": generate_post_id(),
        "title": title,
        "body": body,
        "author": author,
        "tags": tags,
        "status": "draft",
        "comments": [],
        "likes": 0
    }

    post_db.append(post)
    print("Post successfully created!\n")
    display_post(post)
    return post

def display_post(post):
    print(f"Post ID: {post['id']}")
    print(f"Title: {post['title']}")
    print(f"Author: {post['author']}")
    print(f"Tags: {', '.join(post['tags']) if post['tags'] else 'None'}")
    print(f"Status: {post['status']}")
    print(f"Body: {post['body']}")
    print("-" * 40)

def list_all_posts():
    print("\nAll Posts:")
    for post in post_db:
        print(f"- {post['id']}: {post['title']} by {post['author']}")

# Example usage
create_post("How to Cook Pasta", "Start with boiling water...", "Noor", tags=["cooking", "recipe"])
create_post("Learning Python", "Let's explore functions and loops.", "Ali", tags=["programming", "python"])
list_all_posts()
