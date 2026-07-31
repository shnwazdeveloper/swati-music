# Copyright (c) 2025 shnwazdeveloper
# Licensed under the MIT License.
# This file is part of Swati Music

import os
from aiohttp import web
from anony import logger

async def health_check(request: web.Request) -> web.Response:
    return web.json_response({
        "status": "online",
        "bot": "Swati Music",
        "health": "ok"
    })

async def apikey_handler(request: web.Request) -> web.Response:
    return web.json_response({
        "status": "active",
        "service": "Swati Music API",
        "api_url": "https://shnwazdev-ytmusicapi.vercel.app/",
        "key": "shnwazdev-public-access"
    })

async def start_server() -> None:
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    app.router.add_get("/apikey", apikey_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Web server successfully started on port {port} for Render health checks.")
