import io
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api/v1"
)

file = io.FileIO("examples/files/icon.png", "r")
url = gentrace.upload_file(file)
print('url', url)
