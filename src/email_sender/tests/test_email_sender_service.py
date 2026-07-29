from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from email_sender.models import Campaign, Contact, EmailLog, MessageTemplate, ContactGroup
from email_sender.services.email_sender import send_campaign


User = get_user_model()

class EmailSenderServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@gmail.com",
            password="testpass123"
        )
        self.template = MessageTemplate.objects.create(
            owner=self.user,
            title="шаблон",
            subject="тема",
            body="текст письма"
        )
        self.contact = Contact.objects.create(
            owner=self.user,
            name="Иван",
            email="ivan@gmail.com"
        )
        self.campaign = Campaign.objects.create(
            owner=self.user,
            title="рассылка",
            template=self.template,
            status=Campaign.SendingStatus.DRAFT
        )
        self.campaign.contacts.add(self.contact)



    @patch("email_sender.services.email_sender.send_mail")
    def test_send_campaign(self, mock_send_mail):
        send_campaign(self.campaign) #запуск отправки
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.total_count, 1)
        self.assertEqual(self.campaign.sent_count, 1)
        self.assertEqual(self.campaign.failed_count, 0)
        self.assertEqual(self.campaign.status,Campaign.SendingStatus.COMPLETED)
        self.assertIsNotNone(self.campaign.sent_at)
        mock_send_mail.assert_called_once()



    @patch("email_sender.services.email_sender.send_mail")
    def test_campaign_without_recipients(self,mock_send_mail):
        self.campaign.contacts.clear()
        send_campaign(self.campaign)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.total_count, 0)
        self.assertEqual(self.campaign.sent_count, 0)
        self.assertEqual(self.campaign.failed_count, 0)
        mock_send_mail.assert_not_called()
        self.assertEqual(EmailLog.objects.count(),0)



    @patch("email_sender.services.email_sender.send_mail")
    def test_campaign_with_completed_status(self,mock_send_mail):
        self.campaign.status = Campaign.SendingStatus.COMPLETED
        self.campaign.save(update_fields=["status"])
        with self.assertRaises(ValueError):
            send_campaign(self.campaign)
        mock_send_mail.assert_not_called()
        self.assertEqual(EmailLog.objects.count(),0)



    @patch("email_sender.services.email_sender.send_mail")
    def test_contact_is_not_sent_twice(self,mock_send_mail):
        group = ContactGroup.objects.create(owner=self.user,title="Группа контактов")
        group.contacts.add(self.contact)   #доб  ивана чз группу хотя он уже добавлен в setUp
        self.campaign.contact_group = group
        self.campaign.save(update_fields=["contact_group"])
        send_campaign(self.campaign)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.total_count, 1)
        self.assertEqual(self.campaign.sent_count, 1)
        self.assertEqual(self.campaign.failed_count, 0)
        mock_send_mail.assert_called_once()
        self.assertEqual(EmailLog.objects.filter(campaign=self.campaign,contact=self.contact,).count(),1)#создан 1 лог,а не 2