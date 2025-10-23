from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/2025/10/20/texto-de-400kb/")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
