from fastapi import FastAPI
import uvicorn
from api.scrape import Sppl
from ratelimit import limits

app = FastAPI(
    title="Unofficial Super People API",
    description="An Unofficial REST API for [Super People](https://geegee.net/en/news), Made by [Andre Saddler]("
                "https://github.com/axsddlr)",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
)

# init classes
super_people = Sppl()

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news", tags=["News"])
def latest_super_people_news():
    return super_people.news()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
