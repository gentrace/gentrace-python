import os
import tempfile
from urllib.parse import urlparse

import gentrace
import requests
from dotenv import load_dotenv

temp_directory = tempfile.gettempdir()

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

GENTRACE_PIPELINE_SLUG = "main"

cases = gentrace.get_test_cases(pipeline_slug=GENTRACE_PIPELINE_SLUG)

for case in cases:
    image_url = case.get("inputs").get("imageUrl")

    if not image_url:
        continue

    headers = {
        'Authorization': 'Bearer {}'.format(os.getenv("GENTRACE_API_KEY"))
    }

    response = requests.get(image_url, headers=headers)

    # Get the image file name. The Gentrace URL includes it in the final part of
    # the path.
    path = urlparse(image_url).path
    final_part = path.rsplit('/', 1)[-1]

    full_path = os.path.join(temp_directory, final_part)

    print("Full path: ", full_path)

    with open(full_path, 'wb') as file:
        file.write(response.content)
