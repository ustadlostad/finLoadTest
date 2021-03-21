import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.api_key = "cc0a3effd7990f9a45633e52080005a8"
        self.guest_session_id = ""

    wait_time = between(1, 2)

    def on_start(self):
        with self.client.get(url="/3/authentication/guest_session/new?api_key=" + self.api_key) as response:
            self.guest_session_id = response.json()["guest_session_id"]

    @task(1)
    def getMovies(self):
        self.client.get(url="/3/trending/movie/day?api_key=" + self.api_key)

    @task(2)
    def rateMovie(self):
        self.client.post(url="3/movie/791373/rating?api_key=" +
                         self.api_key + "&guest_session_id=" + self.guest_session_id, json={"value": 8.5})

    @task(3)
    def deleteRate(self):
        self.client.delete(url="3/movie/791373/rating?api_key=" +
                           self.api_key + "&guest_session_id=" + self.guest_session_id)
