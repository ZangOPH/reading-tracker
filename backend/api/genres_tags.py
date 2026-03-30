from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_connection

router = APIRouter()

# --- Models ---

class GenreCreate(BaseModel):
    name: str

class TagCreate(BaseModel):
    name: str

# --- Genre Routes ---

@router.get("/genres")
def get_genres():
    """Get all genres."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genres ORDER BY name")
    genres = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return genres


@router.post("/genres")
def create_genre(data: GenreCreate):
    """Add a new genre."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO genres (name) VALUES (?)", (data.name,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, "message": "Genre added successfully"}
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Genre already exists")


@router.post("/genres/{genre_id}/titles/{title_id}")
def assign_genre_to_title(genre_id: int, title_id: int):
    """Assign a genre to a title."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO title_genres (title_id, genre_id) VALUES (?, ?)
        """, (title_id, genre_id))
        conn.commit()
        conn.close()
        return {"message": "Genre assigned to title successfully"}
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Genre already assigned to this title")


@router.delete("/genres/{genre_id}/titles/{title_id}")
def remove_genre_from_title(genre_id: int, title_id: int):
    """Remove a genre from a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM title_genres WHERE title_id = ? AND genre_id = ?
    """, (title_id, genre_id))
    conn.commit()
    conn.close()
    return {"message": "Genre removed from title successfully"}


@router.get("/titles/{title_id}/genres")
def get_title_genres(title_id: int):
    """Get all genres for a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.* FROM genres g
        JOIN title_genres tg ON g.id = tg.genre_id
        WHERE tg.title_id = ?
        ORDER BY g.name
    """, (title_id,))
    genres = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return genres


# --- Tag Routes ---

@router.get("/tags")
def get_tags():
    """Get all tags."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags ORDER BY name")
    tags = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tags


@router.post("/tags")
def create_tag(data: TagCreate):
    """Add a new tag."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tags (name) VALUES (?)", (data.name,))
        conn.commit()
        new_id = cursor.lastrowid
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, "message": "Tag added successfully"}
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Tag already exists")


@router.post("/tags/{tag_id}/titles/{title_id}")
def assign_tag_to_title(tag_id: int, title_id: int):
    """Assign a tag to a title."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO title_tags (title_id, tag_id) VALUES (?, ?)
        """, (title_id, tag_id))
        conn.commit()
        conn.close()
        return {"message": "Tag assigned to title successfully"}
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="Tag already assigned to this title")


@router.delete("/tags/{tag_id}/titles/{title_id}")
def remove_tag_from_title(tag_id: int, title_id: int):
    """Remove a tag from a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM title_tags WHERE title_id = ? AND tag_id = ?
    """, (title_id, tag_id))
    conn.commit()
    conn.close()
    return {"message": "Tag removed from title successfully"}


@router.get("/titles/{title_id}/tags")
def get_title_tags(title_id: int):
    """Get all tags for a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.* FROM tags t
        JOIN title_tags tt ON t.id = tt.tag_id
        WHERE tt.title_id = ?
        ORDER BY t.name
    """, (title_id,))
    tags = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tags

@router.delete("/genres/{genre_id}")
def delete_genre(genre_id: int):
    """Delete a genre entirely."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM genres WHERE id = ?", (genre_id,))
    conn.commit()
    conn.close()
    return {"message": "Genre deleted successfully"}

@router.delete("/tags/{tag_id}")
def delete_tag(tag_id: int):
    """Delete a tag entirely."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    conn.commit()
    conn.close()
    return {"message": "Tag deleted successfully"}
