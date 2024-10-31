import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file into environment variables

config = {
    "DATABASE_URL": os.getenv("DATABASE_URL", "data/users.db"),
    "SMTP_SERVER": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "SMTP_PORT": int(os.getenv("SMTP_PORT", "587")),
    "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
}
