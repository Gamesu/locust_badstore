from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = 'https://www.google.com.co'

    @task
    def MyTask(self):
        self.client.get('/')