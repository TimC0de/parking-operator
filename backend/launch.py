import logging
import asyncio
import signal

import click

from uvicorn import Config, Server

from dotenv import load_dotenv

from app.config.logging import setup_logging

load_dotenv('.env')

import config

logging.basicConfig(level=logging.INFO)  # should use singleton class that handles the logging with multiple channels
logger = logging.getLogger("Start")

try:
    import uvloop  # noqa f401
except ModuleNotFoundError:
    loop = asyncio.new_event_loop()
else:
    loop = uvloop.new_event_loop()

asyncio.set_event_loop(loop)

@click.group()
def cli():
    pass


@cli.command()
@click.option("-p", "--port", default=5000)
@click.option("-h", "--host", default="0.0.0.0")
def runserver(
        host: str, port: int
):
    """
    Run the FastAPI Server.

    :param host:        Host to run it on.
    :param port:        Port to run it on.
    """

    debug = bool(config.env_optional_param("DEBUG"))

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.info("Running in debug mode")

    async def start_server():
        server_config = Config("app.main:app", host=host, port=port, reload=debug)
        server = Server(config=server_config)
        logger.info("Starting server")
        await server.serve()
        logger.info("Server ended")

    def stop(*args) -> None:
        pass

    async def start():
        setup_logging()
        # async with engine.begin() as conn:
        #     await create_tables()
        #     await create_roles()
        #     await create_admin()

        await asyncio.gather(
            asyncio.create_task(start_server())
        )

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    asyncio.run(start())


if __name__ == "__main__":
    cli()
