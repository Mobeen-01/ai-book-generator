import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def _build_html(subject: str, message: str) -> str:
    heading = subject.split(" ", 1)[-1] if subject[0] in "📘✍️📕⚠️" else subject

    parts    = message.split("\n\nDetails: ", 1)
    main_msg = parts[0]
    details  = parts[1] if len(parts) > 1 else None

    details_block = f"""
        <div style="margin-top:20px;background:#0f0e0c;border-left:3px solid #b8a97a;
                    border-radius:6px;padding:14px 18px;font-size:13px;
                    color:#a8a098;line-height:1.7;">
            <span style="font-size:10px;letter-spacing:0.14em;text-transform:uppercase;
                         color:#b8a97a;display:block;margin-bottom:6px;">Details</span>
            {details}
        </div>
    """ if details else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#0f0e0c;font-family:'Helvetica Neue',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background:#0f0e0c;padding:48px 16px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" border="0"
             style="background:#1a1916;border:1px solid rgba(232,228,220,0.1);
                    border-radius:16px;overflow:hidden;max-width:560px;width:100%;">

        <!-- gold accent bar -->
        <tr><td style="height:3px;background:linear-gradient(90deg,#b8a97a,#cfc08e);"></td></tr>

        <!-- header -->
        <tr>
          <td style="padding:36px 40px 28px;border-bottom:1px solid rgba(232,228,220,0.08);">
            <p style="margin:0 0 10px;font-size:10px;letter-spacing:0.18em;
                      text-transform:uppercase;color:#b8a97a;font-family:'Courier New',monospace;">
              AI Book Generator
            </p>
            <h1 style="margin:0;font-size:22px;font-weight:600;color:#f5f0e6;
                       line-height:1.2;letter-spacing:-0.01em;">
              {heading}
            </h1>
          </td>
        </tr>

        <!-- body -->
        <tr>
          <td style="padding:28px 40px 36px;">
            <p style="margin:0;font-size:15px;color:#c8c4bc;line-height:1.7;">
              {main_msg}
            </p>
            {details_block}
          </td>
        </tr>

        <!-- footer -->
        <tr>
          <td style="padding:20px 40px;border-top:1px solid rgba(232,228,220,0.06);
                     background:#131210;">
            <p style="margin:0;font-size:11px;color:#4a4844;
                      font-family:'Courier New',monospace;letter-spacing:0.06em;">
              This is an automated notification &mdash; please do not reply.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


class EmailNotificationService:

    def __init__(self):
        self.smtp_server  = os.getenv("SMTP_SERVER")
        self.port         = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.password     = os.getenv("SENDER_PASSWORD")

    def send_email(self, subject: str, message: str, receiver_email: str):

        msg = MIMEMultipart("alternative")
        msg["From"]    = self.sender_email
        msg["To"]      = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))
        msg.attach(MIMEText(_build_html(subject, message), "html"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            server.quit()

            return {"status": "success", "message": "Email sent"}

        except Exception as e:
            return {"status": "error", "message": str(e)}