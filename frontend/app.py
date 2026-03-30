import streamlit as st
from api_client import get_titles, get_chapters, get_latest_chapter

# Page config
st.set_page_config(
    page_title="Reading Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("📚 Reading Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📖 My Library", "➕ Add Title", "📝 Log Progress", "🔍 Search"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Phase 1 — Personal Tracker")

# --- Dashboard Page ---
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.markdown("---")

    titles = get_titles()

    if not titles:
        st.info("No titles in your library yet. Add your first title to get started.")
    else:
        total = len(titles)
        reading = len([t for t in titles if t["status"] == "reading"])
        completed = len([t for t in titles if t["status"] == "completed"])
        dropped = len([t for t in titles if t["status"] == "dropped"])
        plan_to_read = len([t for t in titles if t["status"] == "plan_to_read"])

        formats = {}
        for t in titles:
            fmt = t["format"]
            formats[fmt] = formats.get(fmt, 0) + 1

        rated = [t["rating"] for t in titles if t["rating"]]
        avg_rating = round(sum(rated) / len(rated), 1) if rated else None

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Titles", total)
        col2.metric("Reading", reading)
        col3.metric("Completed", completed)
        col4.metric("Plan to Read", plan_to_read)
        col5.metric("Dropped", dropped)

        st.markdown("---")

        col6, col7 = st.columns(2)

        with col6:
            st.subheader("📊 By Format")
            for fmt, count in sorted(formats.items(), key=lambda x: x[1], reverse=True):
                st.write(f"**{fmt.replace('_', ' ').title()}** — {count}")

        with col7:
            st.subheader("⭐ Average Rating")
            if avg_rating:
                st.metric("Average Rating", f"{avg_rating} / 5")
            else:
                st.write("No ratings yet")

        st.markdown("---")

        st.subheader("📖 Currently Reading")
        currently_reading = [t for t in titles if t["status"] == "reading"]
        if currently_reading:
            for title in currently_reading:
                with st.expander(f"{title['title']} ({title['format'].replace('_', ' ').title()})"):
                    latest = get_chapters(title["id"])
                    if latest:
                        last = latest[0]
                        if last.get("chapter_number"):
                            st.write(f"**Last logged:** Chapter {last['chapter_number']}")
                        elif last.get("page_number"):
                            st.write(f"**Last logged:** Page {last['page_number']}")
                        elif last.get("duration_minutes"):
                            st.write(f"**Last logged:** {last['duration_minutes']} minutes")
                        st.write(f"**Logged at:** {last['read_at']}")
                    else:
                        st.write("No progress logged yet")
        else:
            st.write("Nothing currently being read.")

elif page == "📖 My Library":
    st.title("📖 My Library")
    st.markdown("---")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "reading", "completed", "plan_to_read", "dropped"]
        )
    with col2:
        format_filter = st.selectbox(
            "Filter by Format",
            ["All", "manga", "manhwa", "manhua", "web_novel", "light_novel", "book", "comic", "audiobook"]
        )

    # Fetch titles
    status = None if status_filter == "All" else status_filter
    format = None if format_filter == "All" else format_filter
    titles = get_titles(status=status, format=format)

    st.markdown("---")

    if not titles:
        st.info("No titles found.")
    else:
        st.write(f"**{len(titles)} title(s) found**")
        for title in titles:
            with st.expander(f"{title['title']} — {title['format'].replace('_', ' ').title()} — {title['status'].replace('_', ' ').title()}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Status:** {title['status'].replace('_', ' ').title()}")
                    st.write(f"**Format:** {title['format'].replace('_', ' ').title()}")
                    st.write(f"**Rating:** {title['rating']}/5" if title['rating'] else "**Rating:** Not rated")
                with col2:
                    st.write(f"**Started:** {title['start_date'] or 'Not set'}")
                    st.write(f"**Finished:** {title['finish_date'] or 'Not set'}")
                    if title['notes']:
                        st.write(f"**Notes:** {title['notes']}")

elif page == "➕ Add Title":
    st.title("➕ Add Title")
    st.markdown("---")

    from api_client import create_title, get_genres, get_tags

    with st.form("add_title_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title *", placeholder="e.g. Solo Leveling")
            format = st.selectbox("Format *", [
                "manga", "manhwa", "manhua", "web_novel",
                "light_novel", "book", "comic", "audiobook"
            ])
            status = st.selectbox("Status *", [
                "plan_to_read", "reading", "completed", "dropped"
            ])
            rating = st.slider("Rating", 0, 5, 0)

        with col2:
            start_date = st.date_input("Start Date", value=None)
            finish_date = st.date_input("Finish Date", value=None)
            narrator = st.text_input("Narrator (audiobooks only)", placeholder="e.g. John Smith")
            source_url = st.text_input("Source URL", placeholder="e.g. https://mangadex.org/...")

        notes = st.text_area("Notes", placeholder="Any notes about this title...")

        submitted = st.form_submit_button("Add Title")

        if submitted:
            if not title:
                st.error("Title is required.")
            else:
                data = {
                    "title": title,
                    "format": format,
                    "status": status,
                    "rating": rating if rating > 0 else None,
                    "start_date": str(start_date) if start_date else None,
                    "finish_date": str(finish_date) if finish_date else None,
                    "narrator": narrator if narrator else None,
                    "source_url": source_url if source_url else None,
                    "notes": notes if notes else None
                }
                result = create_title(data)
                if result:
                    st.success(f"✅ '{title}' added successfully!")
                else:
                    st.error("Something went wrong. Make sure the API is running.")

elif page == "📝 Log Progress":
    st.title("📝 Log Progress")
    st.markdown("---")

    from api_client import log_chapter, get_latest_chapter

    # Get currently reading titles
    reading_titles = get_titles(status="reading")

    if not reading_titles:
        st.info("No titles currently being read. Add a title and set its status to 'Reading' first.")
    else:
        # Select title
        title_options = {t["title"]: t for t in reading_titles}
        selected_title_name = st.selectbox("Select Title", list(title_options.keys()))
        selected_title = title_options[selected_title_name]

        # Show latest progress
        latest = get_latest_chapter(selected_title["id"])
        if latest:
            st.markdown("**Last logged progress:**")
            col1, col2 = st.columns(2)
            with col1:
                if latest.get("chapter_number"):
                    st.metric("Last Chapter", latest["chapter_number"])
                elif latest.get("page_number"):
                    st.metric("Last Page", latest["page_number"])
                elif latest.get("duration_minutes"):
                    st.metric("Last Duration", f"{latest['duration_minutes']} mins")
            with col2:
                st.metric("Logged At", latest["read_at"][:10])

        st.markdown("---")

        # Log new progress based on format
        fmt = selected_title["format"]

        with st.form("log_progress_form"):
            if fmt in ["manga", "manhwa", "manhua", "web_novel", "light_novel", "comic"]:
                chapter_number = st.number_input(
                    "Chapter Number",
                    min_value=0.0,
                    step=0.5,
                    format="%.1f"
                )
                data = {"chapter_number": chapter_number if chapter_number > 0 else None}

            elif fmt == "book":
                page_number = st.number_input(
                    "Page Number",
                    min_value=0,
                    step=1
                )
                data = {"page_number": page_number if page_number > 0 else None}

            elif fmt == "audiobook":
                duration_minutes = st.number_input(
                    "Minutes Listened",
                    min_value=0,
                    step=5
                )
                data = {"duration_minutes": duration_minutes if duration_minutes > 0 else None}

            submitted = st.form_submit_button("Log Progress")

            if submitted:
                if not any(data.values()):
                    st.error("Please enter a valid progress value.")
                else:
                    result = log_chapter(selected_title["id"], data)
                    if result:
                        st.success(f"✅ Progress logged for '{selected_title_name}'!")
                    else:
                        st.error("Something went wrong. Make sure the API is running.")

elif page == "🔍 Search":
    st.title("🔍 Search")
    st.markdown("---")

    query = st.text_input("Search by title name", placeholder="e.g. Solo Leveling")

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "reading", "completed", "plan_to_read", "dropped"]
        )
    with col2:
        format_filter = st.selectbox(
            "Filter by Format",
            ["All", "manga", "manhwa", "manhua", "web_novel",
             "light_novel", "book", "comic", "audiobook"]
        )

    st.markdown("---")

    # Fetch and filter
    status = None if status_filter == "All" else status_filter
    format = None if format_filter == "All" else format_filter
    titles = get_titles(status=status, format=format)

    if query:
        titles = [t for t in titles if query.lower() in t["title"].lower()]

    if not titles:
        st.info("No titles found matching your search.")
    else:
        st.write(f"**{len(titles)} result(s) found**")
        for title in titles:
            with st.expander(
                f"{title['title']} — "
                f"{title['format'].replace('_', ' ').title()} — "
                f"{title['status'].replace('_', ' ').title()}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Status:** {title['status'].replace('_', ' ').title()}")
                    st.write(f"**Format:** {title['format'].replace('_', ' ').title()}")
                    st.write(f"**Rating:** {title['rating']}/5" if title['rating'] else "**Rating:** Not rated")
                with col2:
                    st.write(f"**Started:** {title['start_date'] or 'Not set'}")
                    st.write(f"**Finished:** {title['finish_date'] or 'Not set'}")
                    if title['notes']:
                        st.write(f"**Notes:** {title['notes']}")

                # Latest progress
                latest = get_latest_chapter(title["id"])
                if latest:
                    st.markdown("**Latest progress:**")
                    if latest.get("chapter_number"):
                        st.write(f"Chapter {latest['chapter_number']} — {latest['read_at'][:10]}")
                    elif latest.get("page_number"):
                        st.write(f"Page {latest['page_number']} — {latest['read_at'][:10]}")
                    elif latest.get("duration_minutes"):
                        st.write(f"{latest['duration_minutes']} mins — {latest['read_at'][:10]}")
