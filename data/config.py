# api id, hash
API_ID = 21421214
API_HASH = 'asafasfasf'

DELAYS = {
    'ACCOUNT': [5, 15],  # delay between connections to accounts (the more accounts, the longer the delay)
    'TASK':  [5, 10],  # delay after complete task
}

# For example 'FUOM_I_3mNrbplFo4EUEj'
REFS = ['M1o0iuj']

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": "http",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "http"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
