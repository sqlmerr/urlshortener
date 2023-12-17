from .models import Link

async def get_url(code: str):
    return await Link.find_one(Link.code == code)

async def get_url_by_link(link: str):
    return await Link.find_one(Link.link == link)
