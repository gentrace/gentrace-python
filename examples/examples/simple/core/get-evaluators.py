import os

import gentrace
from dotenv import load_dotenv

load_dotenv()


def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api",
    )

    # example pipeline slug
    pipeline_slug = "guess-the-year"
    evaluators_from_slug = gentrace.get_evaluators(pipeline_slug = pipeline_slug)

    print(evaluators_from_slug)

    # example pipeline ID
    pipeline_id = "c10408c7-abde-5c19-b339-e8b1087c9b64"
    evaluators_from_id = gentrace.get_evaluators(pipeline_id = pipeline_id)

    print(evaluators_from_id)

    # get evaluator templates
    evaluator_templates = gentrace.get_evaluators()
    print(evaluator_templates)


main()
