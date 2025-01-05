import aiopg
import os
import logging as log
from aiohttp.web import Application

log.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

def setup_database(app: Application):
    # create connection to the database
    
    log.debug (">>> Database setup")
    app.on_startup.append(_init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(_close_pg)


async def _init_pg(app: Application):
    conf = app['config']['db']

    log.debug (">>> Database Initialization")
    log.debug (conf)

    dsn = (
        'dbname={database} user={user} password={password} host={host} port={port}'
        .format(**conf)
    )
    log.debug ("getting connection")
    db = await aiopg.create_pool(dsn)
    log.debug ("saving db connection")
    app['db'] = db


async def _close_pg(app: Application):
    log.debug (">>> Datapool cleanup")
    app['db'].close()
    await app['db'].wait_closed()
