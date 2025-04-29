from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

db_url = os.getenv('DATABASE_URL')
example_jwt_token = os.getenv('EXAMPLE_JWT_TOKEN')
algorithm = os.getenv('ALGORITHM')
secret_key = os.getenv('SECRET_KEY')
expire_minutes = os.getenv('EXPIRE_MINUTES_ACCESS_TOKEN')
expire_days = os.getenv('EXPIRE_DAYS_REFRESH_TOKEN')
example_uuid = os.getenv('EXAMPLE_UUID')