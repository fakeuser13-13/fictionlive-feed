import json
import html
from datetime import datetime, timezone

with open("stories.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stories = data.get("stories", [])

def date_text(timestamp):
    if not timestamp:
        return ""
    try:
        return datetime.fromtimestamp(
            timestamp / 1000, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return ""

rows = []

for story in stories:
    title = html.escape(str(story.get("t", "Untitled")))
    story_id = html.escape(str(story.get("_id", "")))

    authors = story.get("u", [])
    author_names = ", ".join(
        str(author.get("n", ""))
        for author in authors
        if author.get("n")
    )
    author_names = html.escape(author_names)

    description = html.escape(str(story.get("d", "")))
    rating = html.escape(str(story.get("contentRating", "")))
    tags = html.escape(", ".join(str(x) for x in story.get("ta", [])))

    is_live = story.get("isLive", False)
    live_text = "LIVE NOW" if is_live else "Not live"

    next_live = date_text(story.get("nextLive"))
    updated = date_text(story.get("ut"))

    story_url = f"https://fiction.live/stories/{story_id}"

    rows.append(f"""
    <article>
        <h2><a href="{story_url}">{title}</a></h2>
        <p><strong>QM:</strong> {author_names}</p>
        <p><strong>Status:</strong> {live_text}</p>
        <p><strong>Next live:</strong> {next_live}</p>
        <p><strong>Rating:</strong> {rating}</p>
        <p><strong>Tags:</strong> {tags}</p>
        <p><strong>Description:</strong> {description}</p>
        <p><strong>Last activity:</strong> {updated}</p>
        <p><strong>Story ID:</strong> {story_id}</p>
    </article>
    """)

page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Fiction.live Feed</title>
</head>
<body>
    <h1>Fiction.live Story Feed</h1>
    <p>Automatically updated from Fiction.live.</p>
    <p>Total stories in current feed: {len(stories)}</p>
    {''.join(rows)}
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)
