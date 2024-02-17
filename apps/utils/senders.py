from apps.accounts.models import SentSMS


class SendSMS:
    @staticmethod
    def send(phone_number: str, text: str, reason: str) -> None:
        # todo : add sms service api
        print("code sent")
        SentSMS(phone_number=phone_number, text=text, reason=reason).save()

    @staticmethod
    def send_otp(code: str, phone_number: str) -> None:
        text = f"کد ورود شما به سامانه : {code}"
        SendSMS.send(phone_number, text, "OTP")
