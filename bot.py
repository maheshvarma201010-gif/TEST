import asyncio
import signal
import sys
from bot.bot import bot
from bot.utils.health import start_health_server
from bot.config import settings
from bot.utils.logger import logger

async def main():
    logger.info("Application starting...")

    # Start the bot
    try:
        await bot.start()
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
        sys.exit(1)

    # Start the health check server in background
    asyncio.create_task(start_health_server(port=settings.PORT))

    # Handle termination signals
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("Termination signal received.")
        stop_event.set()

    # Use try-except for signal handlers as they might not be available on all platforms
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)
    except NotImplementedError:
        pass

    logger.info("Bot is active. Waiting for messages...")

    try:
        await stop_event.wait()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
