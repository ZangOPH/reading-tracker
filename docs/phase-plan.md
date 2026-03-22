# Reading Tracker — Phase Plan

## Phase 1: Personal Tracker (Current)

### Goal
A functional personal tracker I can actually use day to day.

### Features
- Add titles manually with full metadata (format, status, rating, dates, notes)
- Log chapter/page/duration progress per session
- Assign genres and tags to titles
- View reading history and basic stats (titles read, avg rating, most read format)
- Basic search and filter by format, status, genre, tag

### Tech
- FastAPI backend
- SQLite database (schema.sql)
- Streamlit frontend

### Data Sources
- MangaDex API (manga, manhwa, manhua metadata)
- Anilist GraphQL (anime/manga metadata)
- NovelUpdates (web novel metadata)
- Royal Road (web novel metadata)
- Manual entry (books, comics, audiobooks)

### Done
- [x] Repo created
- [x] Folder structure defined
- [x] Database schema designed

### To Do
- [ ] Initialise SQLite database from schema
- [ ] Build FastAPI backend with CRUD routes
- [ ] Build Streamlit frontend
- [ ] Integrate MangaDex API for metadata lookup
- [ ] Deploy locally and use daily

---

## Phase 2: Recommendation Engine

### Goal
Personalised recommendations based on reading history.

### Features
- Cluster analysis on genres, tags, formats and ratings
- Content-based filtering
- "If you liked X, try Y" recommendations
- Reading pattern insights

### Tech
- scikit-learn (clustering)
- pandas (data processing)
- Extended Streamlit UI

---

## Phase 3: Community Product

### Goal
Open the tracker up as a public multi-user product.

### Features
- User accounts and authentication
- Shared lists and social features
- Community recommendations
- Public web deployment

### Tech
- PostgreSQL (replacing SQLite)
- Proper auth (JWT or OAuth)
- Cloud deployment (Railway, Render or similar)
