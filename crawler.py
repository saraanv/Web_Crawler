import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


BASE_URL = "https://miladhospital.com"

MAX_PAGES = 50

OUTPUT_FILE = "data/pages.json"


visited = set()
pages = []

IGNORE_PATHS = [
    "/login",
    "/logout",
    "/register",
    "/admin",
    "/me",
    "/manager",
    "/profile",
    "/dashboard"
]

IGNORE_EXTENSIONS = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".zip",
    ".rar",
    ".mp4",
    ".mp3"
]


def normalize_url(url):

    url = url.split("#")[0]

    if url.endswith("/"):
        url = url[:-1]

    return url



def is_valid_url(url):

    url = normalize_url(url)

    parsed = urlparse(url)


    if parsed.netloc != urlparse(BASE_URL).netloc:
        return False

    for path in IGNORE_PATHS:

        if parsed.path.startswith(path):
            return False


    for ext in IGNORE_EXTENSIONS:

        if url.lower().endswith(ext):
            return False


    return True




def extract_text(html):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav"
        ]
    ):
        tag.decompose()


    text = soup.get_text(
        separator=" ",
        strip=True
    )


    return text




def crawl():


    queue = deque()

    queue.append(BASE_URL)


    session = requests.Session()


    session.headers.update(
        {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )



    while queue and len(pages) < MAX_PAGES:


        current_url = normalize_url(
            queue.popleft()
        )


        if current_url in visited:
            continue


        visited.add(current_url)



        try:

            response = session.get(
                current_url,
                timeout=15
            )


            if response.status_code != 200:
                continue

            content_type = response.headers.get(
                "Content-Type",
                ""
            )


            if "text/html" not in content_type:
                continue



            text = extract_text(
                response.text
            )

            if len(text) < 300:
                continue



            pages.append(
                {
                    "url": current_url,
                    "text": text
                }
            )


            print(
                f"[{len(pages)}] {current_url}"
            )




            soup = BeautifulSoup(
                response.text,
                "lxml"
            )



            for link in soup.find_all("a"):


                href = link.get("href")


                if not href:
                    continue



                new_url = urljoin(
                    BASE_URL,
                    href
                )


                new_url = normalize_url(
                    new_url
                )



                if (
                    is_valid_url(new_url)
                    and new_url not in visited
                ):
                    queue.append(new_url)



        except Exception as e:


            print(
                "ERROR:",
                current_url
            )

            print(e)



    save_data()




def save_data():


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            pages,
            file,
            ensure_ascii=False,
            indent=2
        )



    print()
    print(
        "===================="
    )

    print(
        f"Saved Pages: {len(pages)}"
    )

    print(
        "Saved to:",
        OUTPUT_FILE
    )

    print(
        "===================="
    )




if __name__ == "__main__":

    crawl()