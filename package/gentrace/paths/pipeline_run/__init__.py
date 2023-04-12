# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from gentrace.paths.pipeline_run import Api

from gentrace.paths import PathValues

path = PathValues.PIPELINERUN
