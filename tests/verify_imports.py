import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

modules_to_test = [
    "bot.config",
    "bot.utils.logger",
    "bot.utils.health",
    "bot.database.mongo",
    "bot.database.models",
    "bot.filters.roles",
    "bot.helpers.rate_limiter",
    "bot.helpers.progress",
    "bot.modules.example_scraper",
    "bot.modules.tollyflix",
    "bot.handlers.commands",
    "bot.handlers.callbacks",
    "bot.bot",
]

def test_imports():
    failed = []
    # Mock environment variables for config loading
    os.environ["API_ID"] = "12345"
    os.environ["API_HASH"] = "hash"
    os.environ["BOT_TOKEN"] = "token"

    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ Successfully imported {module}")
        except Exception as e:
            print(f"❌ Failed to import {module}: {e}")
            failed.append(module)

    if failed:
        print(f"\nImport verification FAILED for {len(failed)} modules.")
        sys.exit(1)
    else:
        print("\nAll modules imported successfully!")

if __name__ == "__main__":
    test_imports()
