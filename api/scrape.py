import ujson as json
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
    @staticmethod
    def news():
        article_list_url = "https://geegee.net/en/news"

        # bs4 for article list via NEXTJS props
        r = requests.get(article_list_url, headers=headers)
        articles = BeautifulSoup(r.content, "lxml")
        status = r.status_code

        data = articles.find("script", id="__NEXT_DATA__").text

        article_list_data = json.loads(data)
        article_base = article_list_data["props"]["pageProps"]["initialReduxState"]["news"]["getSubNewsListRes"]["res"]["news_list"]

        api = []
        for each in article_base:
            post_id = each["news_id"]
            post_url = f"https://geegee.net/en/news/detail?news_id={post_id}&display_type=sub"

            # bs4 for post detail via NEXTJS props
            r = requests.get(post_url, headers=headers)
            post = BeautifulSoup(r.content, "lxml")
            status = r.status_code

            post_scrape = post.find("script", id="__NEXT_DATA__").text

            post_scrape_data = json.loads(post_scrape)
            buildId = post_scrape_data["buildId"]
            post_url_json = f"https://geegee.net/_next/data/{buildId}/en/news/detail.json?news_id={post_id}&display_type=sub"
            post = requests.get(post_url_json, headers=headers)
            post_response = post.json()
            post_base = post_response["pageProps"]["initialReduxState"]["news"]["getDetailNewsRes"]["res"]["news"]

            summary = post_base["summary"]
            summary_full = post_base["detail_content"]
            title = post_base["title"]
            thumbnail = post_base["resource_list"]["resource_cdn_url"]
            published = post_base["created_ts"]

            api.append(
                {
                    "title": title,
                    "summary": summary,
                    "thumbnail": thumbnail,
                    "url": post_url,
                    "publishDate": published,
                    "summary_full": remove_tags(summary_full),
                }
            )
        #
        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    Sppl.news()
