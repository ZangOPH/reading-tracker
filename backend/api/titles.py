from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from backend.database import get_connection

router = APIRouter()

# --- Models ---

class TitleCreate(BaseModel):
    title: str
    format: str
    status: str = "plan_to_read"
    cover_url: Optional[str] = None
    source_url: Optional[str] = None
    external_id: Optional[str] = None
    external_source: Optional[str] = None
    rating: Optional[int] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None
    narrator: Optional[str] = None
    notes: Optional[str] = None

class TitleUpdate(BaseModel):
    title: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    cover_url: Optional[str] = None
    source_url: Optional[str] = None
    rating: Optional[int] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None
    narrator: Optional[str] = None
    notes: Optional[str] = None

# --- Routes ---

@router.get("/")
def get_titles(status: Optional[str] = None, format: Optional[str] = None):
    """Get all titles, optionally filtered by status or format."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM titles WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if format:
        query += " AND format = ?"
        params.append(format)

    query += " ORDER BY updated_at DESC"
    cursor.execute(query, params)
    titles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return titles


@router.get("/{title_id}")
def get_title(title_id: int):
    """Get a single title by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM titles WHERE id = ?", (title_id,))
    title = cursor.fetchone()
    conn.close()

    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return dict(title)


@router.post("/")
def create_title(data: TitleCreate):
    """Add a new title."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO titles (
            title, format, status, cover_url, source_url,
            external_id, external_source, rating,
            start_date, finish_date, narrator, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.title, data.format, data.status, data.cover_url,
        data.source_url, data.external_id, data.external_source,
        data.rating, data.start_date, data.finish_date,
        data.narrator, data.notes
    ))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": "Title added successfully"}


@router.patch("/{title_id}")
def update_title(title_id: int, data: TitleUpdate):
    """Update a title's details."""
    conn = get_connection()
    cursor = conn.cursor()

    # Only update fields that were actually provided
    fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join([f"{k} = ?" for k in fields])
    set_clause += ", updated_at = CURRENT_TIMESTAMP"
    values = list(fields.values()) + [title_id]

    cursor.execute(f"UPDATE titles SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return {"message": "Title updated successfully"}


@router.delete("/{title_id}")
def delete_title(title_id: int):
    """Delete a title and all associated data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM titles WHERE id = ?", (title_id,))
    conn.commit()
    conn.close()
    return {"message": "Title deleted successfully"}
