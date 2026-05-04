import decimal
import datetime
from dataclasses import dataclass


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
    book_with_error: bool = False
    error_detail: str = ""
