import requests

for x in range(3, 10):
            course = {"invalid": "Sel" + str(x), "teacher": "user1"}
            response = requests.post("http://localhost:5000/courses?uid=Bart", json=course)  # valid user
            assert response.status_code == 201