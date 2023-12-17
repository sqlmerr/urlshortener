from beanie import Document, Indexed

class Link(Document):
    code: str
    link: str
