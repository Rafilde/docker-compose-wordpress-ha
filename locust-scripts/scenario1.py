from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/imagem-de-1mb")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
    wait_time = between(1, 5) 