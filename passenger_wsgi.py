import sys
import os

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)
path = os.environ.get("PASSENGER_BASE_PATH")
sys.path.append(path)

# import app must come after sys.path.append
from app import create_app

application = create_app()
