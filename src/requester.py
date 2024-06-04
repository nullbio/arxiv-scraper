import time
from requests import Session


class Requester(Session):
    def __init__(self, session, logger, sleep_seconds=3, max_retries=5):
        self.session = session
        self.logger = logger
        self.sleep_seconds = sleep_seconds
        self.max_retries = max_retries

    def get(self, url, params=None, headers=None):
        self.logger.debug(f"Requesting {url}")
        counter = 0
        result = None
        while counter < self.max_retries:
            try:
                result = self.session.get(url, params=params, headers=headers)
                if result.status_code != 200:
                    raise Exception(
                        f"failed with status code {result.status_code}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Error while requesting {url}: {e}, status code: {result.status_code}. Trying again in {counter} seconds"
                )
                if counter == self.max_retries:
                    raise Exception(
                        f"Error while requesting {url}: {e}, status code: {result.status_code}. Max retries reached"
                    )
                    exit(1)
                time.sleep(self.sleep_seconds * counter)
                counter += 1
            return result
