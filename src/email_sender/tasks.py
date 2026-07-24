from celery import shared_task
from email_sender.models import Campaign
from email_sender.services.email_sender import send_campaign


#тестовое для проверки работоспособности
# @shared_task
# def test_celery_task():
#     print("Celery работает!")
#
#     return "Celery task completed"



@shared_task
def send_campaign_task(campaign_id):
    """
    фоновая отправка  рассылки
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:  #если рассылку удалили между постановкой и вып.
        return {
            "status": "error",
            "message": "рассылка не найдена",
        }

    try:
        result = send_campaign(campaign) #запуск ф-ии из services
    except ValueError as error:          #если статус рассылки не из allowed_statuses
        return {
            "status": "error",
            "message": str(error),
        }
    except Exception as error:          #для непредвиденных ошибок
        campaign.status = Campaign.SendingStatus.FAILED
        campaign.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        return {
            "status": "error",
            "message": str(error),
        }
    return {
        "status": "success",
        "campaign_id": campaign.id,
        "total": result["total"],
        "sent": result["sent"],
        "failed": result["failed"],
    }