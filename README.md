This script monitors the Resident Advisor (RA) event page for resell tickets and sends an email notification when any of the desired tickets become available. Uses Gmail's SMTP server.

## Usage

1. Clone this repository.
2. Install the required packages.
3. Edit the following variables in the `ra-ticket-watcher.py` file or set them as environment variables:
- `URL`: The URL of the RA event page.
- `TICKETS_WANTED`: Price of currently soldout ticket (or a list of tickets) you are interested in. (e.g.,`"£15.00"` or `["£15.00", "£17.00", "£20.00"]`)
- `TARGET_EMAIL`: The email address (or a list of addresses) to send the notification to.
- `GMAIL_CLIENT_EMAIL`: 
- `GMAIL_CLIENT_PASS`: Generate an App password for Gmail SMTP authentication.
4. Create a cron job to run `ra_ticket_scraper.py` automatically. 

## GitHub Actions

This repository includes a GitHub Actions pipeline that runs the script as a cron job. To use the pipeline:

1. Fork this repository.
2. Add your Gmail credentials and target emails as secrets in your GitHub repository: `GMAIL_CLIENT_EMAIL`, `GMAIL_CLIENT_PASS`, `TARGET_EMAILS`.
3. Set the rest of the variables inside `ra-ticket-watcher.py` file or add them as secrets.
4. Uncomment and edit the schedule part in the `.github/workflows/ra-ticket-watcher.yml` file.

