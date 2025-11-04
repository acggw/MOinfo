class notificaton:
    def __init__(self, msg: str):
        self.message = msg
    def __str__(self):
        return self.message
    pass

def send_email(email_address: str, bill_notification: notificaton) -> bool:
    pass