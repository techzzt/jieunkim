"""Write data/latest-post.json from the newest Medium post that is not the pinned one.

Run daily by .github/workflows/latest-post.yml. Leaves the file untouched if the
feed cannot be read, so the homepage keeps showing the last known post.
"""
import html
import json
import re
import sys
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://medium.com/feed/@techzzt0"
PINNED_ID = "ee42d385854c"  # the Think-Act-React post shown in the fixed card
OUT = Path(__file__).resolve().parent.parent / "data" / "latest-post.json"


def text_of(fragment):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def excerpt(body, limit=150):
    """First sentences of the post body, cut at a word boundary."""
    paragraphs = re.findall(r"<p>(.*?)</p>", body, re.S)
    words = text_of(" ".join(paragraphs[:3])).split()
    out = ""
    for w in words:
        if len(out) + len(w) + 1 > limit:
            return out.rstrip(".,;:") + "…"
        out = f"{out} {w}".strip()
    return out


def main():
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (homepage feed reader)"})
    try:
        feed = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    except Exception as err:  # keep the previous post on any network problem
        print(f"feed unavailable, keeping previous file: {err}")
        return 0

    for item in re.findall(r"<item>(.*?)</item>", feed, re.S):
        link = re.search(r"<link>(.*?)</link>", item).group(1).split("?")[0]
        if PINNED_ID in link:
            continue
        title = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item, re.S).group(1)
        date = parsedate_to_datetime(re.search(r"<pubDate>(.*?)</pubDate>", item).group(1))
        body = (re.search(r"<content:encoded><!\[CDATA\[(.*?)\]\]>", item, re.S) or [None, ""])[1]
        post = {"title": html.unescape(title.strip()), "url": link,
                "date": date.strftime("%b %Y"), "excerpt": excerpt(body)}
        new = json.dumps(post, ensure_ascii=False, indent=2) + "\n"
        if OUT.exists() and OUT.read_text() == new:
            print("latest post unchanged")
        else:
            OUT.write_text(new)
            print(f"latest post: {post['title']}")
        return 0

    print("no post other than the pinned one; keeping previous file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
