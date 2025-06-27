import wikipedia
import webbrowser


def wiki_search(query):
    try:
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=4)
        page_url = wikipedia.page(query).url
        webbrowser.open(page_url)

        return result
    except Exception as e:
        print(f"could not find anything about on this topic{e}")
