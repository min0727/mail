import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging

# 環境変数を読み込む
load_dotenv()

# ログ設定
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
log_level = logging.INFO if DEBUG else logging.WARNING
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# SMTP設定
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
TO_ADDRESS = os.getenv("TO_ADDRESS")


def send_email(subject: str, body: str) -> None:
    """
    メールを送信する関数

    :param subject: メールの件名
    :param body: メールの本文
    """
    logger.info("メール送信を開始します")
    try:
        # メールメッセージを作成
        message = MIMEMultipart()
        message["From"] = FROM_ADDRESS
        message["To"] = TO_ADDRESS
        message["Subject"] = subject

        # 本文を追加
        message.attach(MIMEText(body, "plain"))

        # SMTPサーバーに接続
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # TLSセッションを開始
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_ADDRESS, TO_ADDRESS, message.as_string())
        logger.info("メール送信に成功しました")
    except Exception as e:
        logger.error(f"メール送信中にエラーが発生しました: {e}")


if __name__ == "__main__":
    subject = "テストメール"
    body = "これはPythonから送信されたテストメールです。"
    send_email(subject, body)
