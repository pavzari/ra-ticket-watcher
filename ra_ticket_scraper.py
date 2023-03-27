"""
Resident Advisor resell ticket watcher. Collects the prices of currently
soldout tickets and checks them against a list of wanted tickets. Notifies via 
Gmail if any become available. 
"""
# TODO:
# 1. Remove hardcoding of URL, TARGET_EMAIL, TICKETS_WANTED, TICKET_WANTED
# 2. Add support for multiple events
# 3. Add support for multiple target emails
# 4. Requirements.txt
# 5. Update actions pipeline.

import os
import ssl
import smtplib
import requests
from bs4 import BeautifulSoup

EVENT_URL = os.environ["EVENT_URL"]
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}
REQUEST_TIMEOUT = 15
EMAIL_SUBJECT = "RA tickets are available"
EMAIL_CONTENT = f"Quick, tickets are now available here: {EVENT_URL}"
TICKETS_WANTED = os.environ["TICKETS_WANTED"] #['£15.00', '£17.00', '£20.00']
TARGET_EMAIL = os.environ["TARGET_EMAIL"]
GMAIL_CLIENT_EMAIL = os.environ["GMAIL_CLIENT_EMAIL"]
GMAIL_CLIENT_PASS = os.environ["GMAIL_CLIENT_PASS"]


class GmailClient:
  def __init__(self):
      self.port = 465
      self.smtp_server_domain_name = "smtp.gmail.com"
      self.sender_email = GMAIL_CLIENT_EMAIL
      self.password = GMAIL_CLIENT_PASS

  def send(self, target_email, email_subject, email_content):
    try:
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=context) as connection:
        connection.login(self.sender_email, self.password)
        connection.sendmail(self.sender_email, target_email, f"Subject: {email_subject}\n\n{email_content}")
        connection.quit()
    except smtplib.SMTPException as e:
        raise SystemExit(e)
    

def scrape_tickets():
  soldout_tickets = []
  try:
    page = requests.get(EVENT_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    page.raise_for_status()
  except requests.exceptions.RequestException as e: 
    raise SystemExit(e)

  soup = BeautifulSoup(page.content, "html.parser")   
  for ticket in soup.find_all("li", class_= "closed"):
      price = ticket.find("div", class_="type-price")
      soldout_tickets.append(price.text)
  return soldout_tickets


def check_tickets_and_notify():
  soldout_tickets = scrape_tickets()
  for ticket in TICKETS_WANTED:
    if ticket not in soldout_tickets:
      email = GmailClient()
      email.send(TARGET_EMAIL, EMAIL_SUBJECT, EMAIL_CONTENT)

if __name__ == '__main__':
  check_tickets_and_notify()

