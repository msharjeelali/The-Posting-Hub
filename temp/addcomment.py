def add_comment(post_id, user, comment_text):
    print(f"Adding comment to Post ID {post_id}")
    comment = {
        "user": user,
        "text": comment_text,
        "status": "added"
    }
    print(f"Comment Added: {comment}")
    return comment

# Example usage
add_comment(101, "Noor", "Great post! Thanks for sharing.")
