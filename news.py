import sys
import json
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='your Api key')


def fetch_news():
    news = newsapi.get_everything(q="technology", language="en", sort_by="publishedAt")

    if "articles" not in news or not news["articles"]:
        print(json.dumps({"error": "No articles found"}, ensure_ascii=False))
        return

    articles = news["articles"][:5]
    top_news = [{"title": article.get("title", "No title"), "description": article.get("description", "No description")} for article in articles]

    json_output = json.dumps(top_news, ensure_ascii=False)
    sys.stdout.buffer.write(json_output.encode('utf-8'))
    sys.stdout.flush()


if __name__ == "__main__":
    fetch_news()

