from concurrent.futures import ThreadPoolExecutor

from requests_futures.sessions import FuturesSession
from maya import when


def requests_multiple(*args):
    args_len = len(args)
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=args_len))
    # Kick off requests in parallel and store it next to the URL requested
    urls_futures = {
        url: session.get(url)
        for url in args
    }
    # Build a new dictionary waiting for all of them
    return {
        url: future.result()
        for url, future in urls_futures.items()
    }

if __name__ == '__main__':
    start = when('now').datetime()
    res = requests_multiple(
        'http://httpbin.org/delay/8',
        'http://httpbin.org/delay/9',
        'http://httpbin.org/delay/7',
        'http://httpbin.org/delay/5',
        'http://httpbin.org/delay/2'
    )
    end = when('now').datetime()

    print(f"Completed in {end - start} results: {res}")
