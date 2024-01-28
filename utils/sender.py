"""Coupon sender."""
from dataclasses import asdict, dataclass
from pathlib import Path

import aiofiles
import httpx

from utils.coupon import Coupon
from utils.settings import WoocommerceSettings

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
}


@dataclass
class CouponSender:
    """Coupon sender."""

    coupon: Coupon
    wc_settings: WoocommerceSettings

    async def __call__(self) -> str:
        """Send coupon."""
        url = f"{self.wc_settings.url}/wp-json/wc/v3/coupons"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=url,
                auth=(
                    self.wc_settings.user_key,
                    self.wc_settings.secret_key,
                ),
                params=asdict(self.coupon),
                headers=HEADERS,
            )
            response.raise_for_status()
        return await self._get_user_message()

    async def _get_user_message(
        self,
        file_name="message_template.txt",
    ) -> str:
        async with aiofiles.open(
            Path(".") / file_name,
            mode="r",
            encoding="UTF-8",
        ) as f:
            contents = await f.read()
            return contents.format(
                **asdict(self.coupon),
            )
