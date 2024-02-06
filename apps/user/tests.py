from django.test import TestCase

import re
from datetime import datetime, timedelta, time
from rest_framework.test import APIClient
from rest_framework import status

from apps.user.models import User



class AppsUserListUsersExceptCurrentGenericListTest(TestCase):
    # check, if permissions is working (admin, not admin)
    # check, if data displaying (every field is corresponding to the field type)
    # check, that returns empty list of the users, if no users
    datetime_regex = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z')  # 2024-02-02 15:02:33.874252+03

    def setUp(self):
        # defining settings for creating fake test User before executing test case
        self.user = User.objects.create_user(
            email="user1@email.com",
            username="user1",
            first_name="user1first",
            last_name="user1last",
            password="qwe3",
            )

        # defining settings for creating fake SuperUser before executing test case
        self.admin = User.objects.create_superuser(
            email="admin1@email.com",
            username="admin1",
            first_name="admin1first",
            last_name="admin1last",
            password="qwe3",
            is_staff=True,
            is_superuser=True,
            )

        for user_number in range(2, 11):
            User.objects.create_user(
                email=f"user{user_number}@email.com",
                username=f"user{user_number}",
                first_name=f"user{user_number}first",
                last_name=f"user{user_number}last",
                password=f"qwe3")


        self.client = APIClient()  # imitate front client, as if any front client (user) makes requests


    def test_get_users_as_admin(self):
        self.client.force_authenticate(user=self.admin)  # Authorises fake user by force in our fake test system

        response = self.client.get("http://127.0.0.1:8000/api/generics/user/all_users-v2/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if status is status.HTTP_200_OK
        self.assertIsInstance(response.data["data"], list)  # Check if type is dict
        self.assertEqual(len(response.data["data"]), User.objects.count() - 1)  # Check if count=User.objects.count()-1

        for each_user in response.data["data"]:  # for user in response.data["data"] because I return data = "message" and "data" as keys
        # for user in response.data:  # for user in response.data should be if return in data = serializer.data only

            self.assertIsInstance(each_user['email'], str)  # Check if type is str
            self.assertIsInstance(each_user["first_name"], str)
            self.assertIsInstance(each_user["last_name"], str)
            self.assertIsInstance(each_user["username"], str)
            self.assertIsInstance(each_user["phone"], (str | None))  # Check if type is str or None

            self.assertIsInstance(each_user["is_staff"], bool)  # Check if type is bool
            self.assertIsInstance(each_user["is_superuser"], bool)
            self.assertIsInstance(each_user["is_verified"], bool)
            self.assertIsInstance(each_user["is_active"], bool)

            self.assertTrue(
                self.datetime_regex.match(each_user["date_joined"]), datetime)

            self.assertTrue(
                self.datetime_regex.match(each_user["last_login"]), datetime)


    def test_get_users_as_non_admin(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("http://127.0.0.1:8000/api/generics/user/all_users-v2/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
                        path=f"http://127.0.0.1:8000/api/generics/user/user_by_id-v2/{self.user.id}/",
                        data={"first_name": "UPDATED"},
                        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "user1@email.com")
        self.assertEqual(self.user.username, "user1")
        self.assertEqual(self.user.first_name, "UPDATED")
        self.assertEqual(self.user.last_name, "user1last")


    def test_delete_user(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            f"http://127.0.0.1:8000/api/generics/user/user_by_id-v2/{self.user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsInstance(response.data["data"], list)
        self.assertEqual(response.data["data"], [])


    def test_get_no_users(self):
        self.client.force_authenticate(user=self.admin)

        User.objects.all().delete()
        response = self.client.get("http://127.0.0.1:8000/api/generics/user/all_users-v2/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response.data["data"], list)  # for user in response.data["data"] because I return data = "message" and "data" as keys
        # self.assertIsInstance(response.data, list)  # for user in response.data should be if return in data = serializer.data only
        self.assertEqual(response.data["data"], [])
