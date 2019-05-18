from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def news_categories():
    # Iterate through the news categories and search for articles
    # categories = ["neuroscience", "open-neuroscience-articles", "neurology", "brain-cancer", "brain-research", "psychology", "genetics", "artificial-intelligence-2", "robotics-2"]
    categories = ["neuroscience"]
    nsn_topics = "https://neurosciencenews.com/neuroscience-topics/"
    for a in categories:
        search_topic = nsn_topics + a
        raw_html = simple_get(search_topic)
        html = BeautifulSoup(raw_html, 'html.parser')
        for title in html.find_all("h2", class_="cb-post-title"):
            print (title.text)




news_categories()

# raw_html = simple_get("https://neurosciencenews.com/female-suicide-increase-14026/")
# html = BeautifulSoup(raw_html, 'html.parser')
# for p in html.select("div"):
#     print(p.text)