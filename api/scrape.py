import json
import re

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/74.0.3729.169 Safari/537.36",
}

# remove html elements from json output
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


class Sppl:
    def news(self):
        article_list_url = "https://geegee.net/en/news"

        # https://geegee.net/_next/data/-KK8Sf5jQy0DpZ-l3tmo3/en/news/detail.json?news_id=b68jai9qpqf4&display_type=sub
        r = requests.get(article_list_url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        status = r.status_code

        data = soup.find("script", id="__NEXT_DATA__").text

        jsondata = json.loads(data)
        base = jsondata["props"]["pageProps"]["initialReduxState"]["news"]["getSubNewsListRes"]["res"]["news_list"]

        api = []
        for each in base:
            post_id = each["news_id"]
            post_url = f"https://geegee.net/en/news/detail?news_id={post_id}&display_type=sub"
            r = requests.get(post_url, headers=headers)
            articles = BeautifulSoup(r.content, "lxml")

            title = articles.find("h2").text.strip()
            published = articles.find("span", {"class": "css-e9hs7k e1myrdfa3"}).text.strip()
            thumbnail = each["resource_list"]["resource_cdn_url"]

            summary = articles.findChildren('h3')

            try:
                for head in articles.select("h3:nth-of-type(1)"):
                    if head is not None:
                        summary = head.text.strip()
            except:
                summary = "nope"

            api.append(
                {
                    "title": title,
                    "summary": summary,
                    "thumbnail": thumbnail,
                    "url": post_url,
                    "publishDate": published,
                }
            )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
