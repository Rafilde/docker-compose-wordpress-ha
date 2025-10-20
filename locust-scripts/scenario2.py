from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/texto-de-400kb")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
    wait_time = between(1, 5) 