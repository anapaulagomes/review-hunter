import requests
import os
from .endpoints import *


class UnauthorizedToken(Exception):
    pass


class ReviewsAPI:

    def __init__(self):
        token = os.environ['UDACITY_AUTH_TOKEN']
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def execute(self, request):
        try:
            raw_response = request()
            response = raw_response.json()

            raw_response.raise_for_status()

            return response
        except requests.exceptions.HTTPError:
            raise UnauthorizedToken('Maybe it\'s time to change your token!')

    def certifications(self):
        return self.execute(lambda: requests.get(CERTIFICATIONS, headers=self.headers))

    def certified_languages(self):
        return self.execute(lambda: requests.get(REVIEWER, headers=self.headers))

    def request_reviews(self, projects):
        return self.execute(lambda: requests.post(NEW_SUBMISSION_REQUESTS, headers=self.headers, json=projects))

    def assigned_count(self):
        return self.execute(lambda: requests.get(ASSIGNED_COUNT, headers=self.headers))

    def submission_requests(self):
        return self.execute(lambda: requests.get(SUBMISSION_REQUESTS, headers=self.headers))
