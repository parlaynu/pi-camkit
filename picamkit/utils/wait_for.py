import time


def wait_for(seconds: float) -> bool:
    print(f"Waiting for {seconds} seconds")
    time.sleep(seconds)

    return True
