import asyncio
import logging
import sys

from aiogram import Dispatcher, types, BaseMiddleware
from handlers import router, bot


dp = Dispatcher()


async def main() -> None:
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
