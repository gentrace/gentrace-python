# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from gentrace.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V1_RUN = "/v1/run"
    V1_TESTCASE = "/v1/test-case"
    V1_TESTRESULT = "/v1/test-result"
    V1_TESTRESULT_ID = "/v1/test-result/{id}"
    V1_TESTRESULT_STATUS = "/v1/test-result/status"
    V1_TESTRESULTSIMPLE = "/v1/test-result-simple"
    V1_PIPELINES = "/v1/pipelines"
    V1_FILES_UPLOAD = "/v1/files/upload"
    V2_TESTRESULTS = "/v2/test-results"
    V2_TESTCASES = "/v2/test-cases"
    V2_PIPELINES = "/v2/pipelines"
