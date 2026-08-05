from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from email_sender.models import Campaign, MessageTemplate,Contact


User = get_user_model()

class CampaignApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@gmail.com",
            password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@gmail.com",
            password="testpass123"
        )
        self.template = MessageTemplate.objects.create(
            owner=self.user,
            title=" шаблон юзера1",
            subject=" тема юзера1",
            body=" письмо юзера1"
        )
        self.other_template = MessageTemplate.objects.create(
            owner=self.other_user,
            title=" шаблон юзера2",
            subject="тема юзера2",
            body=" письмо юзера2"
        )
        self.contact = Contact.objects.create( #тк в сериалайзере проверка чтобы была группа или контакт
            owner=self.user,
            name="Ivan",
            email="ivan@gmail.com",
        )
        self.client.force_authenticate(user=self.user)


    def test_create_campaign(self):
        url = reverse("campaign_create")
        data = {
            "title": "Новая рассылка",
            "template": self.template.id,
            "contacts": [self.contact.id], #список.тк может быть несколько контактов у пользователя
        }
        response = self.client.post(url, data, format="json") #отпр POST запрос
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.filter(owner=self.user).count(),1)
        campaign = Campaign.objects.get(owner=self.user)
        self.assertEqual(campaign.title, "Новая рассылка")
        self.assertEqual(campaign.template, self.template)




    @patch("api.v1.views.campaigns.send_campaign_task.delay") #тк.delay() вызывается во views.task=send_campaign_task.delay(campaign.id)
    def test_send_campaign(self, mock_delay):
        campaign = Campaign.objects.create(
            owner=self.user,
            title="рассылка",
            template=self.template,
            status=Campaign.SendingStatus.DRAFT
        )
        mock_delay.return_value.id = "test_task_id" # id возвращенного объекта заглушки
        url = reverse("campaign_send",kwargs={"pk": campaign.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["campaign_id"],campaign.id)  #прорверка что API вернул id нужной рассылки
        self.assertEqual(response.data["task_id"],"test_task_id")  # что вернулся id который настроили в заглушке
        mock_delay.assert_called_once_with(campaign.id)  #что был вызов ровно1 раз с нужным id



    @patch("api.v1.views.campaigns.send_campaign_task.delay")
    def test_send_only_own_campaign(self,mock_delay):
        campaign = Campaign.objects.create(
            owner=self.other_user,
            title="чужая рассылка ",
            template=self.other_template,
            status=Campaign.SendingStatus.DRAFT
        )
        url = reverse("campaign_send",kwargs={"pk": campaign.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        mock_delay.assert_not_called() #проверка что задача не была вызвана



    def test_create_with_only_own_template(self):
        url = reverse("campaign_create")
        data = {
            "title": "рассылка",
            "template": self.other_template.id,
            "contacts": [self.contact.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Campaign.objects.count(), 0)




    def test_cancel_scheduled_campaign(self):
        campaign = Campaign.objects.create(
            owner=self.user,
            title="рассылка",
            template=self.template,
            status=Campaign.SendingStatus.SCHEDULED,
        )
        url = reverse("campaign_cancel",kwargs={"pk": campaign.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        campaign.refresh_from_db() #загрузка актуал данных из бд
        self.assertEqual(campaign.status,Campaign.SendingStatus.CANCELED)