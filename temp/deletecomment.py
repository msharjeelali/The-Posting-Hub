def delete_comment(comment_id):
    print(f"Attempting to delete comment with ID: {comment_id}")
    success = True  # Simulating deletion
    if success:
        print(f"Comment ID {comment_id} deleted successfully.")
    else:
        print(f"Failed to delete comment ID {comment_id}.")
    return success

# Example usage
delete_comment(55)
