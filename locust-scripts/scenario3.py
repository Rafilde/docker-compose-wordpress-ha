from locust import HttpUser, TaskSet, task, between

class WordpressUserBehavior(TaskSet):
    @task
    def load_post(self):
        self.client.get("/wp-content/uploads/2025/10/300kb-img.jpg")

class WebsiteUser(HttpUser):
    tasks = [WordpressUserBehavior]
