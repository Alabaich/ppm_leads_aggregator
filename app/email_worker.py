import imaplib
import email
import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# 1. Logging Configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/worker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
load_dotenv("../.env")

# 2. Configuration
IMAP_SERVER = "outlook.office365.com"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS") 

def list_unread_emails():
    try:
        if not EMAIL_USER or not EMAIL_PASS:
            logger.error("Missing Credentials in .env file.")
            return

        logger.info(f"Attempting login for {EMAIL_USER}...")
        
        # Connect via SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        
        try:
            mail.login(EMAIL_USER, EMAIL_PASS)
        except imaplib.IMAP4.error as e:
            logger.error(f"Login Rejected: {e}")
            print("\n" + "!"*60)
            print("AUTHENTICATION FAILED")
            print("Your standard password was rejected by Microsoft.")
            print("This usually happens because Multi-Factor Authentication (MFA) is active.")
            print("Microsoft requires an 'App Password' for IMAP when MFA is enabled.")
            print("!"*60 + "\n")
            return

        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN)')
        
        if status != 'OK': 
            logger.error("Could not search inbox.")
            return

        ids = messages[0].split()
        if not ids:
            logger.info("Connection successful! No unread emails found.")
            mail.logout()
            return

        logger.info(f"Connected! Found {len(ids)} Unread Email(s):")
        
        for e_id in ids:
            res, msg_data = mail.fetch(e_id, "(RFC822.HEADER)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"] or "No Subject"
                    from_addr = msg["From"] or "Unknown"
                    print(f"[{e_id.decode()}] From: {from_addr} | Subject: {subject}")

        mail.logout()
        
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")

if __name__ == "__main__":
    logger.info("LIS Email Discovery started.")
    list_unread_emails()
    
    # Poll every 5 minutes for new mail
    while True:
        time.sleep(300)
        list_unread_emails()