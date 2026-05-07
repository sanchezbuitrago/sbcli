import decimal
import datetime
from typing import Optional
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class Book:
    id: str
    title: str
    author: str
    link: str
    min_price: decimal.Decimal
    max_price: decimal.Decimal
    average_price: decimal.Decimal
    current_price: decimal.Decimal
    price_history_items: int
    last_updated_at: datetime.datetime
    created_at: datetime.datetime
    price_score: Optional[decimal.Decimal] = None
    book_with_error: bool = False
    error_detail: str = ""

    @classmethod
    def from_dict(cls, data: dict):
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})
