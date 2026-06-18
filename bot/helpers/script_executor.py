import sys
import io
import traceback
from typing import Tuple

def execute_script_sync(code: str, url: str) -> Tuple[bool, str]:
    """
    Executes a python script string synchronously, injecting the 'url' variable.
    Returns (success, output/error)
    """
    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    import cloudscraper
    from bs4 import BeautifulSoup
    import re
    import requests
    import json
    import time

    namespace = {
        "url": url,
        "cloudscraper": cloudscraper,
        "BeautifulSoup": BeautifulSoup,
        "re": re,
        "requests": requests,
        "json": json,
        "time": time
    }

    success = True
    try:
        exec(code, namespace)
    except Exception:
        success = False
        print(traceback.format_exc())
    finally:
        sys.stdout = old_stdout

    return success, output.getvalue()
