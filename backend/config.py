from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

db_url = os.getenv('DATABASE_URL')
secret_key = "SECRET"#os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')

example_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzM1OTIxMzg5LCJ0eXBlIjoicmVmcmVzaCJ9.SDZcJf2hmbnYYer5R-VZKyQL2ztSu3WgzcZ6tFojx38"