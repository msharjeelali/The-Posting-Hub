def load_draft(draft_id):
    print(f"Loading draft with ID: {draft_id}")
    return {"id": draft_id, "title": "Draft Title", "content": "Draft Content"}

def edit_draft(draft, new_title=None, new_content=None):
    if new_title:
        draft['title'] = new_title
    if new_content:
        draft['content'] = new_content
    print(f"Edited Draft: {draft}")
    return draft

# Example usage
draft = load_draft(1)
edit_draft(draft, new_title="Updated Draft Title", new_content="Updated content here.")
