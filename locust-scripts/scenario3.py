from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/2025/10/20/imagem-de-300kb/")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
