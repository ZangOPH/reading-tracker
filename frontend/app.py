import streamlit as st
import pandas as pd
from api_client import *

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
    ["🏠 Dashboard", "📖 My Library", "➕ Add Title", "📝 Log Progress", "🔍 Search", "📊 Statistics"]
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
                    
                    log_next_chapter = st.button("Log Progress", key=f"log_{title['id']}")
                    if log_next_chapter:
                        if latest:
                            last_entry = latest[0]
                            if last_entry.get("chapter_number") is not None:
                                data = {"chapter_number": last_entry["chapter_number"] + 1}
                            elif last_entry.get("page_number") is not None:
                                data = {"page_number": last_entry["page_number"] + 1}
                            elif last_entry.get("duration_minutes") is not None:
                                data = {"duration_minutes": last_entry["duration_minutes"]}
                        else:
                            data = {"chapter_number": 1.0}

                        result = log_chapter(title["id"], data)
                        if result:
                            st.success(f"✅ Progress logged for '{title['title']}'!")
                            st.rerun()
                        else:
                            st.error(f"Failed to log progress for '{title['title']}'!")
        else:
            st.write("Nothing currently being read.")

elif page == "📖 My Library":
    st.title("📖 My Library")
    st.markdown("---")

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

    status = None if status_filter == "All" else status_filter
    format = None if format_filter == "All" else format_filter
    titles = get_titles(status=status, format=format)

    st.markdown("---")
    with st.expander("⚙️ Manage Genres & Tags", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Genres**")
            existing_genres = get_genres()
            if existing_genres:
                st.write(", ".join([g["name"] for g in existing_genres]))
            else:
                st.write("No genres yet")
            
            new_genre_name = st.text_input("Add new genre", placeholder="e.g. Isekai")
            if st.button("➕ Add Genre"):
                if new_genre_name:
                    result = create_genre(new_genre_name)
                    if result:
                        st.success(f"✅ Genre '{new_genre_name}' created!")
                        st.rerun()
                    else:
                        st.error("Genre already exists or something went wrong.")

            if existing_genres:
                st.markdown("**Remove Genre**")
                genre_to_remove = st.selectbox(
                    "Select genre to remove",
                    options=[g["name"] for g in existing_genres],
                    key="remove_genre_select"
                )
                if st.button("🗑️ Remove Genre"):
                    genre_id = next(g["id"] for g in existing_genres if g["name"] == genre_to_remove)
                    result = delete_genre(genre_id)
                    if result:
                        st.success(f"✅ Genre '{genre_to_remove}' removed!")
                        st.rerun()
                    else:
                        st.error("Something went wrong.")
        with col2:
            st.markdown("**Tags**")
            existing_tags = get_tags()
            if existing_tags:
                st.write(", ".join([t["name"] for t in existing_tags]))
            else:
                st.write("No tags yet")

            new_tag_name = st.text_input("Add new tag", placeholder="e.g. Overpowered MC")
            if st.button("➕ Add Tag"):
                if new_tag_name:
                    result = create_tag(new_tag_name)
                    if result:
                        st.success(f"✅ Tag '{new_tag_name}' created!")
                        st.rerun()
                    else:
                        st.error("Tag already exists or something went wrong.")

            if existing_tags:
                st.markdown("**Remove Tag**")
                tag_to_remove = st.selectbox(
                    "Select tag to remove",
                    options=[t["name"] for t in existing_tags],
                    key="remove_tag_select"
                )
                if st.button("🗑️ Remove Tag"):
                    tag_id = next(t["id"] for t in existing_tags if t["name"] == tag_to_remove)
                    result = delete_tag(tag_id)
                    if result:
                        st.success(f"✅ Tag '{tag_to_remove}' removed!")
                        st.rerun()
                    else:
                        st.error("Something went wrong.")
                                
    st.markdown("---")
    if not titles:
        st.info("No titles found.")
    else:
        st.write(f"**{len(titles)} title(s) found**")
        for title in titles:
            with st.expander(
                f"{title['title']} — "
                f"{title['format'].replace('_', ' ').title()} — "
                f"{title['status'].replace('_', ' ').title()}"
            ):
                # Display current details
                col1, col2 = st.columns(2)
                genres = get_title_genres(title["id"])
                tags = get_title_tags(title["id"])
                with col1:
                    st.write(f"**Status:** {title['status'].replace('_', ' ').title()}")
                    st.write(f"**Format:** {title['format'].replace('_', ' ').title()}")
                    st.write(f"**Genres:** {', '.join([g['name'] for g in genres]) or 'None'}")
                    st.write(f"**Tags:** {', '.join([t['name'] for t in tags]) or 'None'}")
                    st.write(f"**Chapters Logged:** {len(get_chapters(title['id']))}")
                    st.write(f"**Rating:** {title['rating']}/5" if title['rating'] else "**Rating:** Not rated")
                with col2:
                    st.write(f"**Started:** {title['start_date'] or 'Not set'}")
                    st.write(f"**Finished:** {title['finish_date'] or 'Not set'}")
                    if title['notes']:
                        st.write(f"**Notes:** {title['notes']}")

                st.markdown("---")

                # Edit form
                with st.form(f"edit_{title['id']}"):
                    st.markdown("**Edit Title**")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox(
                            "Status",
                            ["reading", "completed", "plan_to_read", "dropped"],
                            index=["reading", "completed", "plan_to_read", "dropped"].index(title["status"])
                        )
                        new_genres = st.multiselect(
                            "Genres",
                            options=[g["name"] for g in get_genres()],
                            default=[g["name"] for g in genres]
                        )
                        new_tags = st.multiselect(
                            "Tags",
                            options=[t["name"] for t in get_tags()],
                            default=[t["name"] for t in tags]
                        )

                        new_rating = st.slider("Rating", 0, 5, title["rating"] or 0)
                    with col2:
                        new_start_date = st.date_input(
                            "Start Date",
                            value=pd.to_datetime(title["start_date"]).date() if title["start_date"] else None
                        )
                        new_finish_date = st.date_input(
                            "Finish Date",
                            value=pd.to_datetime(title["finish_date"]).date() if title["finish_date"] else None
                        )
                        new_narrator = st.text_input(
                            "Narrator (audiobooks only)",
                            value=title["narrator"] or ""
                        )
                        new_source_url = st.text_input(
                            "Source URL",
                            value=title["source_url"] or ""
                        )
                        new_notes = st.text_area(
                            "Notes",
                            value=title["notes"] or ""
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        save = st.form_submit_button("💾 Save Changes")
                    with col2:
                        delete = st.form_submit_button("🗑️ Delete Title")

                    if save:
                        result = update_title(title["id"], {
                            "status": new_status,
                            "rating": new_rating if new_rating > 0 else None,
                            "notes": new_notes if new_notes else None,
                            "start_date": str(new_start_date) if new_start_date else None,
                            "finish_date": str(new_finish_date) if new_finish_date else None,
                            "narrator": new_narrator if new_narrator else None,
                            "source_url": new_source_url if new_source_url else None
                        })

                        if result:
                            # Update genres
                            current_genre_ids = {g["id"] for g in genres}
                            new_genre_ids = {g["id"] for g in get_genres() if g["name"] in new_genres}
                            for gid in new_genre_ids - current_genre_ids:
                                assign_genre_to_title(gid, title["id"])
                            for gid in current_genre_ids - new_genre_ids:
                                remove_genre_from_title(gid, title["id"])

                            # Update tags
                            current_tag_ids = {t["id"] for t in tags}
                            new_tag_ids = {t["id"] for t in get_tags() if t["name"] in new_tags}
                            for tid in new_tag_ids - current_tag_ids:
                                assign_tag_to_title(tid, title["id"])
                            for tid in current_tag_ids - new_tag_ids:
                                remove_tag_from_title(tid, title["id"])

                            st.success("✅ Changes saved.")
                            st.rerun()
                        else:
                            st.error("Something went wrong.")

                    if delete:
                        result = delete_title(title["id"])
                        if result:
                            st.success("🗑️ Title deleted.")
                            st.rerun()
                        else:
                            st.error("Something went wrong.")

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

elif page == "📊 Statistics":
    st.title("📊 Statistics")
    st.markdown("---")

    import plotly.express as px
    import pandas as pd

    titles = get_titles()

    if not titles:
        st.info("No data yet. Add some titles to see your statistics.")
    else:
        df = pd.DataFrame(titles)

        # --- Row 1 — Key metrics ---
        st.subheader("📈 Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Titles", len(df))
        col2.metric("Completed", len(df[df["status"] == "completed"]))
        col3.metric("Currently Reading", len(df[df["status"] == "reading"]))
        col4.metric("Plan to Read", len(df[df["status"] == "plan_to_read"]))

        st.markdown("---")

        # --- Row 2 — Format and Status charts ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📚 Titles by Format")
            format_counts = df["format"].value_counts().reset_index()
            format_counts.columns = ["Format", "Count"]
            format_counts["Format"] = format_counts["Format"].str.replace("_", " ").str.title()
            fig = px.bar(format_counts, x="Format", y="Count", color="Format")
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📊 Titles by Status")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            status_counts["Status"] = status_counts["Status"].str.replace("_", " ").str.title()
            fig2 = px.pie(status_counts, names="Status", values="Count")
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # --- Row 3 — Ratings ---
        st.subheader("⭐ Ratings Analysis")
        rated_df = df[df["rating"].notna()]

        if rated_df.empty:
            st.write("No ratings yet.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                avg_by_format = rated_df.groupby("format")["rating"].mean().reset_index()
                avg_by_format.columns = ["Format", "Average Rating"]
                avg_by_format["Format"] = avg_by_format["Format"].str.replace("_", " ").str.title()
                avg_by_format["Average Rating"] = avg_by_format["Average Rating"].round(2)
                fig3 = px.bar(avg_by_format, x="Format", y="Average Rating", color="Format")
                fig3.update_layout(showlegend=False, height=350, yaxis_range=[0, 5])
                st.plotly_chart(fig3, use_container_width=True)

            with col2:
                st.subheader("🏆 Top Rated Titles")
                top_rated = rated_df.nlargest(5, "rating")[["title", "format", "rating"]]
                top_rated["format"] = top_rated["format"].str.replace("_", " ").str.title()
                top_rated.columns = ["Title", "Format", "Rating"]
                st.dataframe(top_rated, use_container_width=True, hide_index=True)

        st.markdown("---")

        # --- Row 4 — Chapter activity ---
        st.subheader("📖 Reading Activity")
        all_chapters = []
        for _, title in df.iterrows():
            chapters = get_chapters(title["id"])
            for chapter in chapters:
                chapter["title_name"] = title["title"]
                chapter["format"] = title["format"]
                all_chapters.append(chapter)

        if all_chapters:
            chapters_df = pd.DataFrame(all_chapters)
            chapters_df["read_at"] = pd.to_datetime(chapters_df["read_at"])
            chapters_df["date"] = chapters_df["read_at"].dt.date

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Chapter Logs", len(chapters_df))
            with col2:
                most_active = chapters_df.groupby("title_name").size().idxmax()
                st.metric("Most Logged Title", most_active)

            daily_activity = chapters_df.groupby("date").size().reset_index()
            daily_activity.columns = ["Date", "Chapters Logged"]
            fig4 = px.line(daily_activity, x="Date", y="Chapters Logged", title="Daily Reading Activity")
            fig4.update_layout(height=350)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.write("No chapter logs yet.")