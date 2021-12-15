import re

import requests

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
        article_list_url = (
            "https://geegee.net/_next/data/-KK8Sf5jQy0DpZ-l3tmo3/en/news.json"
        )

        # https://geegee.net/_next/data/-KK8Sf5jQy0DpZ-l3tmo3/en/news/detail.json?news_id=b68jai9qpqf4&display_type=sub
        response = requests.get(article_list_url, headers=headers)
        responseJSON = response.json()
        status = response.status_code

        base = responseJSON["pageProps"]["initialReduxState"]["news"]["getSubNewsListRes"]["res"]["news_list"]

        api = []
        for each in base:
            post_id = each["news_id"]
            post_url = f"https://geegee.net/en/news/detail?news_id={post_id}&display_type=sub"
            post_api = f"https://geegee.net/_next/data/-KK8Sf5jQy0DpZ-l3tmo3/en/news/detail.json?news_id={post_id}&display_type=sub"
            post_response = requests.get(post_api, headers=headers)
            post_response_json = post_response.json()
            post_details = post_response_json["pageProps"]["initialReduxState"]["news"]["getDetailNewsRes"]["res"][
                "news"]

            excerpt = post_details["detail_content"]
            summary = post_details["summary"]
            thumbnail = post_details["resource_list"]["resource_cdn_url"]
            title = post_details["title"]
            published = post_details["created_ts"]

            api.append(
                {
                    "title": title,
                    "summary": summary,
                    # "body": remove_tags(excerpt),
                    "thumbnail": thumbnail,
                    "url": post_url,
                    "publishDate": published,
                }
            )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
