from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/wp-content/uploads/2025/10/foto-um-mega.jpg")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
