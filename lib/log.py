from config.config import ENABLE_LOG


def log(content):
    if not ENABLE_LOG:
        return
    print("[X-Frame] {}".format(content))
