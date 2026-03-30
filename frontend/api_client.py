import requests

BASE_URL = "http://127.0.0.1:8000"

def get_titles(status=None, format=None):
    """Get all titles with optional filters."""
    params = {}
    if status:
        params["status"] = status
    if format:
        params["format"] = format
    response = requests.get(f"{BASE_URL}/titles/", params=params)
    return response.json() if response.status_code == 200 else []

def get_title(title_id):
    """Get a single title by ID."""
    response = requests.get(f"{BASE_URL}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def create_title(data):
    """Add a new title."""
    response = requests.post(f"{BASE_URL}/titles/", json=data)
    return response.json() if response.status_code == 200 else None

def update_title(title_id, data):
    """Update a title."""
    response = requests.patch(f"{BASE_URL}/titles/{title_id}", json=data)
    return response.json() if response.status_code == 200 else None

def delete_title(title_id):
    """Delete a title."""
    response = requests.delete(f"{BASE_URL}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def log_chapter(title_id, data):
    """Log a chapter entry."""
    response = requests.post(f"{BASE_URL}/chapters/{title_id}", json=data)
    return response.json() if response.status_code == 200 else None

def get_chapters(title_id):
    """Get all chapters for a title."""
    response = requests.get(f"{BASE_URL}/chapters/", params={"title_id": title_id})
    return response.json() if response.status_code == 200 else []

def get_latest_chapter(title_id):
    """Get the latest chapter for a title."""
    response = requests.get(f"{BASE_URL}/chapters/latest/{title_id}")
    return response.json() if response.status_code == 200 else None

def get_genres():
    """Get all genres."""
    response = requests.get(f"{BASE_URL}/library/genres")
    return response.json() if response.status_code == 200 else []

def get_tags():
    """Get all tags."""
    response = requests.get(f"{BASE_URL}/library/tags")
    return response.json() if response.status_code == 200 else []

def get_title_genres(title_id):
    """Get genres for a title."""
    response = requests.get(f"{BASE_URL}/library/titles/{title_id}/genres")
    return response.json() if response.status_code == 200 else []

def get_title_tags(title_id):
    """Get tags for a title."""
    response = requests.get(f"{BASE_URL}/library/titles/{title_id}/tags")
    return response.json() if response.status_code == 200 else []

def assign_genre_to_title(genre_id, title_id):
    """Assign a genre to a title."""
    response = requests.post(f"{BASE_URL}/library/genres/{genre_id}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def remove_genre_from_title(genre_id, title_id):
    """Remove a genre from a title."""
    response = requests.delete(f"{BASE_URL}/library/genres/{genre_id}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def assign_tag_to_title(tag_id, title_id):
    """Assign a tag to a title."""
    response = requests.post(f"{BASE_URL}/library/tags/{tag_id}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def remove_tag_from_title(tag_id, title_id):
    """Remove a tag from a title."""
    response = requests.delete(f"{BASE_URL}/library/tags/{tag_id}/titles/{title_id}")
    return response.json() if response.status_code == 200 else None

def create_genre(name):
    """Create a new genre."""
    response = requests.post(f"{BASE_URL}/library/genres", json={"name": name})
    return response.json() if response.status_code == 200 else None

def create_tag(name):
    """Create a new tag."""
    response = requests.post(f"{BASE_URL}/library/tags", json={"name": name})
    return response.json() if response.status_code == 200 else None

def delete_genre(genre_id):
    """Delete a genre entirely."""
    response = requests.delete(f"{BASE_URL}/library/genres/{genre_id}")
    return response.json() if response.status_code == 200 else None

def delete_tag(tag_id):
    """Delete a tag entirely."""
    response = requests.delete(f"{BASE_URL}/library/tags/{tag_id}")
    return response.json() if response.status_code == 200 else None