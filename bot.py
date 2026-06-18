import asyncio
import signal
from bot.bot import bot
from bot.utils.health import start_health_server
from bot.config import settings
from bot.utils.logger import logger

async def main():
    # Start the bot
    bot_task = asyncio.create_task(bot.start())

    # Start the health check server
    health_task = asyncio.create_task(start_health_server(port=settings.PORT))

    # Handle termination signals
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("Termination signal received. Shutting down...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Wait for the bot to start properly or for a stop signal
    try:
        # Keep the application running until stop signal
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        # Stop everything
        logger.info("Cleaning up...")
        await bot.stop()
        # Health server is stopped when the task is cancelled or process exits

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
