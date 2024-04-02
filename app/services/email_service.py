from fastapi_mail import FastMail, MessageSchema
from app.core.config import mail_config


async def send_invitation_email(
    recipient_email: str, project_name: str, sender_name: str
):
    html = f"""
    <p>Hi,</p>
    <p>You have been invited by {sender_name} to join the project {project_name}.</p>
    <p>Please log in to your account to accept the invitation.</p>
    """

    message = MessageSchema(
        subject=f"Invitation to join the project: {project_name}",
        recipients=[recipient_email],  # FastAPI-Mail expects a list of recipients
        body=html,
        subtype="html",
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)


async def send_invitation_response_email(
    creator_email: str, project_name: str, responder_name: str, response: str
):
    response_msg = "accepted" if response == "accepted" else "refused"
    html = f"""
    <p>Hi,</p>
    <p>{responder_name} has {response_msg} the invitation to join the project {project_name}.</p>
    """

    message = MessageSchema(
        subject=f"Project invitation {response_msg}: {project_name}",
        recipients=[creator_email],
        body=html,
        subtype="html",
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)
