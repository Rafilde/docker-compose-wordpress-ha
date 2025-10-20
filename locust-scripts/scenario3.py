from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/imagem-de-300kb")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
    wait_time = between(1, 5) 