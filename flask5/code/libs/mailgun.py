from requests import Response, post
from typing import List
import os



class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")

    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    
    @classmethod
    def send_confirmation_email(cls, email: List[str], subject: str, text:str) -> Response:
     return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={"from": f"Excited User cool <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text
                },)