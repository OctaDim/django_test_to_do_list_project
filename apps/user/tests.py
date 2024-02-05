from django.test import TestCase

import re
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import status

from apps.user.models import User



class AppsUserListUsersGenericList(TestCase):
    # check, if permissions is working (admin, not admin)
    # check, if data displaying (every field is corresponding to the field type)
    # check, that returns empty list of the users, if no users
    def setUp(self):
        # defining settings for creating fake test User before executing test case
        self.user = User.objects.create_user(
            email="UserTestCase@testcase.email",
            username="UserTestCase",
            first_name="UserTest",
            last_name="UserCase",
            password="qwe3",
            )

        # defining settings for creating fake SuperUser before executing test case
        self.admin = User.objects.create_superuser(
            email="AdminTestCase@testcase.email",
            username="AdminTestCase",
            first_name="AdminTest",
            last_name="AdminCase",
            password="qwe3",
            is_staff=True,
            is_superuser=True,
            )

        # imitate front client, as if any front client (user) makes requests
        self.client = APIClient()


    # def get_all_users_by_admin(self):
    #     self.client.force_authenticate()  # Authorises fake user by force in our fake test system
    #
    #     response = self.client.get("http://127.0.0.1:8000/api/generics/user/all_users-v2/")
    #     assert
