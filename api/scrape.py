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
    def news(cat):
        new_article_url = f"https://api.geegee.net/v1/public/news/b02t0wwj4t8g/sub/type/{cat}/0/list?project_id=b02t0wwj4t8g&display_type=sub&last_news_id=0&news_type={cat}&lang_code=en"

        r = requests.get(new_article_url, headers=headers)
        status = r.status_code

        data_base = r.json()["res"]["news_list"]

        api = []
        for each in data_base:
            post_id = each["news_id"]
            post_url = f"https://api.geegee.net/v1/public/news/b02t0wwj4t8g/sub/{post_id}"

            summary = each["summary"]
            summary_full = each["detail_content"]
            title = each["title"]
            thumbnail = each["resource_list"]["resource_cdn_url"]
            published = each["created_ts"]

            api.append(
                {
                    "title": title,
                    "summary": summary,
                    "thumbnail": thumbnail,
                    "url": post_url,
                    "publishDate": published,
                }
            )
        #
        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    Sppl.news("update")
