from dotenv import load_dotenv

from fixtures.embedding import embedding_response


def pytest_configure():
    load_dotenv()
