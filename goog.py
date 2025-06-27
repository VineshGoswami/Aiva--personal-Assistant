from googlesearch import search
import webbrowser


def goog_search(query):
    try:
        search_results = list(search(query, num_results=5))
        if search_results:
            google_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(google_url)
            return f"Please check this: {google_url}"
        else:
            return "No results found."
    except Exception as e:
        return f"Error occurred: {e}"
