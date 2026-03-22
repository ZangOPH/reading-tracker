from fastapi import FastAPI
from backend.api.titles import router as titles_router

app = FastAPI(
    title="Reading Tracker API",
    description="Personal reading tracker for manga, manhwa, manhua, novels, books, comics and audiobooks",
    version="0.1.0"
)

# Include routers
app.include_router(titles_router, prefix="/titles", tags=["Titles"])

@app.get("/")
def root():
    return {"message": "Reading Tracker API is running"}
