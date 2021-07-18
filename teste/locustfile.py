import json
from locust import HttpUser, task, HttpUser


class LoadTesting(HttpUser):
    last_wait_time = 5

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time

    @task
    def ping(self):
        weight = 1
        self.client.get("/ping/", name="ping")

    @task
    def get_group(self):
        weight = 3
        teste_dict = json.dumps({
            "tam_class": 10,
            "tam_group": 5,
            "ppg": 2,
            "iterations": 5,
            "numcarac": 3,
            "carac": [[10.0, 0.8, 120.0],
                      [20.0, 0.6, 200.0],
                      [10.0, 0.9, 0.0],
                      [50.0, 0.0, 560.0],
                      [30.0, 0.3, 800.0],
                      [30.0, 0.9, 700.0],
                      [20.0, 0.8, 230.0],
                      [30.0, 0.7, 300.0],
                      [40.0, 1, 100.0],
                      [60.0, 0.1, 670.0]
                      ],
            "interations": []
        })

        self.client.post("/get_group", teste_dict, name="get_group")