from http.client import responses

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from app.models import Projects, Task
from users.models import Users


class APITestSetup(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            email='test@info.com',
            username='testname',
            password='TestAPI1234'
        )
        self.login_url = reverse('token_obtain_pair')
        self.project = Projects.objects.create(name='Test', owner=self.user)
        self.task = Task.objects.create(title="Initial Title", description='Something', project=self.project)

        self.login_url = reverse('token_obtain_pair')
        login_response = self.client.post(self.login_url, {
            "email": "test@info.com",
            "password": "TestAPI1234"
        })
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # def test_user_login_and_get_token(self):
    #     response = self.client.post(self.login_url, {
    #         "email" : "test@info.com",
    #         "password" : "TestAPI1234"
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('refresh', response.data)
    #     self.assertIn('access', response.data)
    #
    #
    # def test_create_task_validation_error(self):
    #     token_response = self.client.post(self.login_url, {
    #         "email": "test@info.com",
    #         "password": "TestAPI1234"
    #     })
    #     token = token_response.data['access']
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    #
    #     response = self.client.post(reverse('task-list'), {
    #         'description' : "No Title",
    #         'project' : self.project.id
    #     })
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('title', response.data)

    def test_get_task_detail(self):
        response = self.client.get(reverse('task-detail', kwargs={"pk": self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Initial Title")

    def test_update_task(self):
        url = reverse('task-detail', kwargs={"pk" : self.task.id})
        data = {
            'title' : 'Updated',
            'description' : 'Updated',
            'status' : 'to do',
            'priority' : 'low',
            'project' : self.project.id,
        }
        response = self.client.put(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated")

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', kwargs={"pk": self.task.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get('task-detail', kwargs={"pk": self.task.id})
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
