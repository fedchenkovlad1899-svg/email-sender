import io
from django.contrib.auth import get_user_model
from django.urls import reverse                     #url по имени
from openpyxl import Workbook                       #для созд exel ф-ла в памяти
from rest_framework import status
from rest_framework.test import APITestCase         #позволяет отправлять запросы self.client.post/get...
from email_sender.models import Contact, ContactGroup


User = get_user_model()

class ContactImportTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(        #create_user чтобы пароль сохр в виде хэша
            username="user1",
            email="user1@gmail.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@gmail.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)  #forceauth за user1
        self.url = reverse("contact_import")            #contacts/import/


    def test_import_csv(self):
        csv_content = (
            "name,email,description\n"
            "Ivan Ivanov,ivan@gmail.com,Client\n"
            "Anna Petrova,anna@gmail.com,VIP\n"
        )
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "contacts.csv"
        response = self.client.post(self.url,{"file": file},format="multipart")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.filter(owner=self.user).count(),2)  # проврка что у user1 2 контакта
        self.assertEqual(response.data["created"],2)                         #2-created
        self.assertEqual(response.data["errors_count"],0)

    def test_import_xlsx(self):
        workbook = Workbook()           # созд в памяти exel-книгу
        worksheet = workbook.active     # активный лист
        worksheet.append(               # строка1
            [
                "name",
                "email",
                "description",
            ]
        )
        worksheet.append(              # строка2
            [
                "Ivan Ivanov",
                "ivan@gmail.com",
                "Client",
            ]
        )
        worksheet.append(              # строка3
            [
                "Anna Petrova",
                "anna@gmail.com",
                "VIP",
            ]
        )
        file = io.BytesIO()           #созд вирт файл
        workbook.save(file)
        file.seek(0)                  #курсор в начало документа для чтения данных
        file.name = "contacts.xlsx"
        response = self.client.post(self.url,{"file": file},format="multipart")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.filter(owner=self.user).count(),2)
        self.assertEqual(response.data["created"],2)

    def test_skipp_duplicate_(self):
        Contact.objects.create(        #созд Ивана вручную
            owner=self.user,
            name="Ivan",
            email="ivan@gmail.com",
        )
        csv_content = (                #созд того же ивана через импорт csv
            "name,email,description\n"
            "Ivan Ivanov,ivan@gmail.com,duplicate\n"
        )
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "contacts.csv"
        response = self.client.post(self.url,{"file": file},format="multipart")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["created"],0)
        self.assertEqual(response.data["skipped"],1)
        self.assertEqual(Contact.objects.filter(owner=self.user,email="ivan@gmail.com",).count(),1)



    def test_invalid_email(self):
        csv_content = (
            "name,email,description\n"
            "Bad Contact,idsivgmail,Test\n"
        )
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "contacts.csv"
        response = self.client.post(self.url,{"file": file},format="multipart")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["created"],0)
        self.assertEqual(response.data["errors_count"], 1)
        self.assertEqual(Contact.objects.filter(owner=self.user).count(),0)

    def test_import_only_own_group(self):
        group = ContactGroup.objects.create(
            owner=self.other_user,
            title="user2 group",
        )
        csv_content = (
            "name,email,description\n"
            "Ivan Ivanov,ivan@gmail.com,test\n"
        )
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "contacts.csv"
        response = self.client.post(self.url,{"file": file,"group_id": group.id}, format="multipart")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Contact.objects.filter(owner=self.user).count(),0)