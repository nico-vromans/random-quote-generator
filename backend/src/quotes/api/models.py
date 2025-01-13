from typing import Optional

from pydantic import BaseModel, HttpUrl


class Quote(BaseModel):
    author: str
    category: str
    image_search_query: Optional[str] = None
    origin: HttpUrl
    quote_text: str

    class Config:
        # Optional configuration for serialization, validation, etc.
        json_schema_extra = {
            'example': {
                'author': 'Albert Einstein',
                'category': 'Zen',
                'image_search_query': 'code,programming,programmer',
                'origin': 'https://zenquotes.io/api/',
                'quote_text': 'Life is like riding a bicycle. To keep your balance, you must keep moving.',
            }
        }
