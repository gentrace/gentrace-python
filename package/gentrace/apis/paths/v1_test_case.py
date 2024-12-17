from gentrace.paths.v1_test_case.get import ApiForget
from gentrace.paths.v1_test_case.post import ApiForpost
from gentrace.paths.v1_test_case.patch import ApiForpatch


class V1TestCase(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
