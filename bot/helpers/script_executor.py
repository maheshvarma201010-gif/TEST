import io
import traceback
import cloudscraper
from bs4 import BeautifulSoup
import re
import requests
import json
import time
import urllib.parse
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def execute_script_sync(code: str, url: str) -> Tuple[bool, str]:
    """
    Executes a python script string synchronously with its own captured output.
    """
    output_buffer = io.StringIO()

    def custom_print(*args, **kwargs):
        # Handle file argument if provided
        if 'file' not in kwargs:
            kwargs['file'] = output_buffer
        print(*args, **kwargs)

    namespace = {
        "url": url,
        "cloudscraper": cloudscraper,
        "BeautifulSoup": BeautifulSoup,
        "re": re,
        "requests": requests,
        "json": json,
        "time": time,
        "urllib": urllib.parse,
        "print": custom_print,
        "__name__": "__main__",
        "name": "__main__"
    }

    success = True
    try:
        # Using a fresh namespace for each execution
        exec(code, namespace)
    except Exception:
        success = False
        custom_print(traceback.format_exc())

    return success, output_buffer.getvalue()

async def execute_script_with_timeout(code: str, url: str, timeout: int = 60) -> Tuple[bool, str]:
    import asyncio
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            # We use the executor to run the synchronous code
            return await loop.run_in_executor(executor, execute_script_sync, code, url)
        except TimeoutError:
            return False, f"❌ Execution timed out after {timeout} seconds."
        except Exception as e:
            return False, f"❌ Execution error: {e}"
