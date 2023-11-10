from internal.server.bot_init import dp 
from internal.server.bot_init import dp_memb
from internal.handlers.set_new_turnir import router as set_new_tur_router
from internal.handlers.tunrir_manage import router as tur_manage_router
from internal.handlers.start_handler import router as start_router
from internal.handlers.turnir_memb import router as memb_router

def register_routers():
    dp.include_router(start_router)
    dp.include_router(tur_manage_router)
    dp.include_router(set_new_tur_router)

def register_routers_memb():
    dp_memb.include_router(memb_router)