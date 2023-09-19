from gentrace.paths.test_case.get import ApiForget
from gentrace.paths.test_case.patch import ApiForpatch
from gentrace.paths.test_case.post import ApiForpost


class TestCase(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
