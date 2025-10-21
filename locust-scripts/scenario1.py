from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/2025/10/20/imagem-de-1mb/")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
    wait_time = between(1, 5) 