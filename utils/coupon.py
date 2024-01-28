"""Coupon creator."""
from dataclasses import dataclass
from datetime import date, timedelta
from uuid import uuid4

from transliterate import translit


@dataclass
class Coupon:
    """Coupon dataclass."""

    code: str
    date_expires: str
    amount: int = 10
    discount_type: str = "percent"
    individual_use: bool = True
    usage_limit: int = 1


@dataclass
class CouponCreator:
    """Create coupon from message."""

    message: str
    days: int = 7

    def __call__(self) -> Coupon:
        """Create coupon."""
        splitted_message: list[str] = self.message.split()
        amount: int = 10
        if splitted_message[-1].isdigit():
            amount = int(splitted_message.pop())
        return Coupon(
            code=self._get_coupon_name(splitted_message),
            date_expires=self._count_date_expires(),
            amount=amount,
        )

    def _get_coupon_name(self, splitted_message: list[str]) -> str:
        first_name_part = translit(
            "_".join(splitted_message),
            "ru",
            reversed=True,
        )
        second_name_part = str(uuid4()).split("-", maxsplit=1)[0]
        coupon_name = f"{first_name_part}_{second_name_part}"
        return coupon_name

    def _count_date_expires(
        self,
    ) -> str:
        end_date = date.today() + timedelta(days=self.days)
        return end_date.strftime("%Y-%m-%d")
