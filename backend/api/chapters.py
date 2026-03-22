from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.database import get_connection

router = APIRouter()

# --- Models ---

class ChapterCreate(BaseModel):
    chapter_number: Optional[float] = None
    page_number: Optional[int] = None
    duration_minutes: Optional[int] = None
    read_at: Optional[datetime] = None

# --- Routes ---

@router.get("/")
def get_chapters(title_id: int):
    """Get all chapters logged for a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chapters 
        WHERE title_id = ? 
        ORDER BY read_at DESC
    """, (title_id,))
    chapters = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return chapters


@router.post("/{title_id}")
def log_chapter(title_id: int, data: ChapterCreate):
    """Log a chapter/page/duration entry for a title."""
    conn = get_connection()
    cursor = conn.cursor()

    # Verify title exists
    cursor.execute("SELECT id FROM titles WHERE id = ?", (title_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Title not found")

    # Must provide at least one progress field
    if not any([data.chapter_number, data.page_number, data.duration_minutes]):
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Must provide at least one of: chapter_number, page_number, duration_minutes"
        )

    cursor.execute("""
        INSERT INTO chapters (title_id, chapter_number, page_number, duration_minutes, read_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title_id,
        data.chapter_number,
        data.page_number,
        data.duration_minutes,
        data.read_at or datetime.now()
    ))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": "Chapter logged successfully"}


@router.delete("/{chapter_id}")
def delete_chapter(chapter_id: int):
    """Delete a chapter log entry."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    conn.close()
    return {"message": "Chapter deleted successfully"}


@router.get("/latest/{title_id}")
def get_latest_chapter(title_id: int):
    """Get the most recent chapter logged for a title."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chapters 
        WHERE title_id = ? 
        ORDER BY read_at DESC 
        LIMIT 1
    """, (title_id,))
    chapter = cursor.fetchone()
    conn.close()

    if not chapter:
        raise HTTPException(status_code=404, detail="No chapters logged for this title")
    return dict(chapter)
