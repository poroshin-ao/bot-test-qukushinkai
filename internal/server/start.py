from internal.server.bot_init import *
from internal.handlers.register_handlers import register_routers, register_routers_memb
import asyncio

async def on_startup(_):
    print('Работаем!')

async def start_server():
    register_routers()
    register_routers_memb()
    await asyncio.gather(dp_memb.start_polling(bot_memb, skip_updates=True, on_startup = on_startup), dp.start_polling(bot, skip_updates=True, on_startup=on_startup))
    #asyncio.run(dp.start_polling(bot, skip_updates=True, on_startup=on_startup))
    #asyncio.run(dp_memb.start_polling(bot_memb, skip_updates=True, on_startup = on_startup))