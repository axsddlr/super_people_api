import uvicorn
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.scrape import Sppl

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Unofficial Super People API",
    description="An Unofficial REST API for [Super People](https://geegee.net/en/news), Made by [Andre Saddler]("
                "https://github.com/axsddlr)",
    version="1.0.1",
    docs_url="/",
    redoc_url=None,
)

# init limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# init classes
super_people = Sppl()


@app.get("/news", tags=["News"])
@limiter.limit("250/minute")
def latest_super_people_news(request: Request, cat):
    """
    notice\n
    update\n
    news\n
    event\n
    tournament\n
    """
    return super_people.news(cat)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
