from fastapi import FastAPI
from backend.api.titles import router as titles_router
from backend.api.chapters import router as chapters_router
from backend.api.genres_tags import router as genres_tags_router

app = FastAPI(
    title="Reading Tracker API",
    description="Personal reading tracker for manga, manhwa, manhua, novels, books, comics and audiobooks",
    version="0.1.0"
)

# Include routers
app.include_router(titles_router, prefix="/titles", tags=["Titles"])
app.include_router(chapters_router, prefix="/chapters", tags=["Chapters"])
app.include_router(genres_tags_router, prefix="/library", tags=["Genres & Tags"])

@app.get("/")
def root():
    return {"message": "Reading Tracker API is running"}
