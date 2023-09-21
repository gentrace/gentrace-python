# Changelog

## [0.17.1](https://github.com/gentrace/gentrace-python/compare/v0.17.0...v0.17.1) (2023-09-21)


### Bug Fixes

* Add context ([#150](https://github.com/gentrace/gentrace-python/issues/150)) ([c9fd8ff](https://github.com/gentrace/gentrace-python/commit/c9fd8ff910886c16c132072e52b26247eec4efd4))
* Add render key, rename "context" to "gentrace" to match Node ([#152](https://github.com/gentrace/gentrace-python/issues/152)) ([a864fd2](https://github.com/gentrace/gentrace-python/commit/a864fd2c730217b2fe939d761c0b8488dad5a1f6))

## [0.17.0](https://github.com/gentrace/gentrace-python/compare/v0.16.0...v0.17.0) (2023-09-21)


### Features

* Add test result simple route, include step run flattening ([#148](https://github.com/gentrace/gentrace-python/issues/148)) ([daaa0c5](https://github.com/gentrace/gentrace-python/commit/daaa0c5528c632d60b6e8316362f57a9645ac59b))

## [0.16.0](https://github.com/gentrace/gentrace-python/compare/v0.15.6...v0.16.0) (2023-09-19)


### Features

* Add evaluation routes, deprecate set ID a few calls ([#146](https://github.com/gentrace/gentrace-python/issues/146)) ([7d6fd9b](https://github.com/gentrace/gentrace-python/commit/7d6fd9b5445b1cb7a39ee085287ee680362e19ac))

## [0.15.6](https://github.com/gentrace/gentrace-python/compare/v0.15.5...v0.15.6) (2023-08-28)


### Bug Fixes

* Fix slug not accepted in Python invocation ([#144](https://github.com/gentrace/gentrace-python/issues/144)) ([660e7f7](https://github.com/gentrace/gentrace-python/commit/660e7f7b7ac5143f5d0c03592d12ecfc10b485b9))

## [0.15.5](https://github.com/gentrace/gentrace-python/compare/v0.15.4...v0.15.5) (2023-08-28)


### Bug Fixes

* Add inputs and templates for chat completion rendering ([#142](https://github.com/gentrace/gentrace-python/issues/142)) ([dee4360](https://github.com/gentrace/gentrace-python/commit/dee43607485030742a50ce33b7c31e03d2290018))

## [0.15.4](https://github.com/gentrace/gentrace-python/compare/v0.15.3...v0.15.4) (2023-08-10)


### Bug Fixes

* Ensure that run_test flushes at the end ([#139](https://github.com/gentrace/gentrace-python/issues/139)) ([255b813](https://github.com/gentrace/gentrace-python/commit/255b8133bc7e8e7b3f436fe0734431173868917e))

## [0.15.3](https://github.com/gentrace/gentrace-python/compare/v0.15.2...v0.15.3) (2023-07-31)


### Bug Fixes

* Add collection method ([#134](https://github.com/gentrace/gentrace-python/issues/134)) ([4cbe774](https://github.com/gentrace/gentrace-python/commit/4cbe77438b819f2c0784af929a81e49c0ee0108a))
* Add test counter ([#136](https://github.com/gentrace/gentrace-python/issues/136)) ([84172d7](https://github.com/gentrace/gentrace-python/commit/84172d73d7b5193ee9fa8d806d053cf6f8dece73))

## [0.15.2](https://github.com/gentrace/gentrace-python/compare/v0.15.1...v0.15.2) (2023-07-26)


### Bug Fixes

* Fix issue with stale connection in pool ([#132](https://github.com/gentrace/gentrace-python/issues/132)) ([252a666](https://github.com/gentrace/gentrace-python/commit/252a66661845d5abe8904ef6ad9ae6a173eb235a))

## [0.15.1](https://github.com/gentrace/gentrace-python/compare/v0.15.0...v0.15.1) (2023-07-26)


### Bug Fixes

* Do not use built-in type subscripting  ([#130](https://github.com/gentrace/gentrace-python/issues/130)) ([b825cf8](https://github.com/gentrace/gentrace-python/commit/b825cf832631c502bc17d939ffc1a9273f606da0))

## [0.15.0](https://github.com/gentrace/gentrace-python/compare/v0.14.0...v0.15.0) (2023-07-26)


### Features

* Merge evaluate and observe ([#127](https://github.com/gentrace/gentrace-python/issues/127)) ([8529582](https://github.com/gentrace/gentrace-python/commit/85295823a807d8c02ca0f038316dadf301809454))

## [0.14.0](https://github.com/gentrace/gentrace-python/compare/v0.13.0...v0.14.0) (2023-07-20)


### Features

* when ingesting test runs, support outputs (a JSON blob) and deprecate output / outputSteps ([#124](https://github.com/gentrace/gentrace-python/issues/124)) ([c63e23c](https://github.com/gentrace/gentrace-python/commit/c63e23cc1cd4bd87ef1f9bfbeb8525e5bfc9d832))

## [0.13.0](https://github.com/gentrace/gentrace-python/compare/v0.12.1...v0.13.0) (2023-07-18)


### Features

* Accept output steps ([#119](https://github.com/gentrace/gentrace-python/issues/119)) ([673b453](https://github.com/gentrace/gentrace-python/commit/673b45307be8d1f8e809b8b5eac99b8fd546d5e0))
* add TestSet routes and testing ([#123](https://github.com/gentrace/gentrace-python/issues/123)) ([39b7b44](https://github.com/gentrace/gentrace-python/commit/39b7b44cdc7f88055482414e9565fb07178d095a))

## [0.12.1](https://github.com/gentrace/gentrace-python/compare/v0.12.0...v0.12.1) (2023-06-23)


### Bug Fixes

* Add typings for get test cases ([#115](https://github.com/gentrace/gentrace-python/issues/115)) ([dbf8cd4](https://github.com/gentrace/gentrace-python/commit/dbf8cd4539979c78eab60166e6066c432bbeff91))

## [0.12.0](https://github.com/gentrace/gentrace-python/compare/v0.11.1...v0.12.0) (2023-06-17)


### Features

* Add TestRun name ([#113](https://github.com/gentrace/gentrace-python/issues/113)) ([e99fe69](https://github.com/gentrace/gentrace-python/commit/e99fe69d9578d58e3d403b833c912aa345f0c2c3))

## [0.11.1](https://github.com/gentrace/gentrace-python/compare/v0.11.0...v0.11.1) (2023-06-15)


### Bug Fixes

* Read `GENTRACE_API_KEY` from the environment  (109) ([755a907](https://github.com/gentrace/gentrace-python/commit/755a907db6568986e4cd0fdf19112a2a19950784))

## [0.11.0](https://github.com/gentrace/gentrace-python/compare/v0.10.0...v0.11.0) (2023-06-15)


### Features

* Allow passing in `GENTRACE_BRANCH` and `GENTRACE_COMMIT` as env variables ([4f2327d](https://github.com/gentrace/gentrace-python/commit/4f2327da14a71c78c712f08faa65bc3a30d76cd8))

## [0.10.0](https://github.com/gentrace/gentrace-python/compare/v0.9.1...v0.10.0) (2023-06-15)


### Features

* Simplify SDK for evaluation ([#105](https://github.com/gentrace/gentrace-python/issues/105)) ([ae605c1](https://github.com/gentrace/gentrace-python/commit/ae605c156489ca2913ec0bc3e2f35fbb5e57ba99))

## [0.9.1](https://github.com/gentrace/gentrace-python/compare/v0.9.0...v0.9.1) (2023-06-06)


### Bug Fixes

* add evaluation tests ([#103](https://github.com/gentrace/gentrace-python/issues/103)) ([173dd00](https://github.com/gentrace/gentrace-python/commit/173dd002a158ec2a0f7e04da6bcf2218d518636e))

## [0.9.0](https://github.com/gentrace/gentrace-python/compare/v0.8.1...v0.9.0) (2023-06-05)


### Features

* add the branch commit logic, init() function ([#99](https://github.com/gentrace/gentrace-python/issues/99)) ([2f6dd2c](https://github.com/gentrace/gentrace-python/commit/2f6dd2c80ffb68bc0e2685b4ec444d75268f9723))

## [0.8.1](https://github.com/gentrace/gentrace-python/compare/v0.8.0...v0.8.1) (2023-06-01)


### Bug Fixes

* updating OpenAI generated Python logic to "0.6.0" ([#94](https://github.com/gentrace/gentrace-python/issues/94)) ([2511ab5](https://github.com/gentrace/gentrace-python/commit/2511ab5b57b26ac46b9dfcfe9b882136ecddde8b))

## [0.8.0](https://github.com/gentrace/gentrace-python/compare/v0.7.4...v0.8.0) (2023-05-31)


### Features

* add evaluation routes ([#91](https://github.com/gentrace/gentrace-python/issues/91)) ([f967745](https://github.com/gentrace/gentrace-python/commit/f967745a9dd3a4233c60b1cf32aab6a13f08bf16))

## [0.7.4](https://github.com/gentrace/gentrace-python/compare/v0.7.3...v0.7.4) (2023-05-19)


### Bug Fixes

* wrap streamed output correctly for the ChatCompletion endpoint ([#89](https://github.com/gentrace/gentrace-python/issues/89)) ([8cb0518](https://github.com/gentrace/gentrace-python/commit/8cb0518e7b07298bb3832954d1da4039f1c098bc))

## [0.7.3](https://github.com/gentrace/gentrace-python/compare/v0.7.2...v0.7.3) (2023-05-01)


### Bug Fixes

* remove python-dotenv from mandatory requirements ([#82](https://github.com/gentrace/gentrace-python/issues/82)) ([b035bd7](https://github.com/gentrace/gentrace-python/commit/b035bd7300c871247ac3dd44242397abb7f0265b))

## [0.7.2](https://github.com/gentrace/gentrace-python/compare/v0.7.1...v0.7.2) (2023-04-28)


### Bug Fixes

* make sure that not applying a host is fine ([#79](https://github.com/gentrace/gentrace-python/issues/79)) ([0708570](https://github.com/gentrace/gentrace-python/commit/0708570500869b6db9763ec2db52c9939cbc15d1))

## [0.7.1](https://github.com/gentrace/gentrace-python/compare/v0.7.0...v0.7.1) (2023-04-28)


### Bug Fixes

* input for prompt just the entire prompt string ([#77](https://github.com/gentrace/gentrace-python/issues/77)) ([6c5fceb](https://github.com/gentrace/gentrace-python/commit/6c5fceb2166dfa53dff9184360f8aa706b39ad95))

## [0.7.0](https://github.com/gentrace/gentrace-python/compare/v0.6.1...v0.7.0) (2023-04-28)


### Features

* add chat completion templating ([#76](https://github.com/gentrace/gentrace-python/issues/76)) ([9ef50d2](https://github.com/gentrace/gentrace-python/commit/9ef50d24745fe5659aa3b17d119fc5ec8bd82c96))


### Bug Fixes

* add chat completion tests ([#74](https://github.com/gentrace/gentrace-python/issues/74)) ([b0ffcf8](https://github.com/gentrace/gentrace-python/commit/b0ffcf88130cc9392642062f1a115558354f5e36))

## [0.6.1](https://github.com/gentrace/gentrace-python/compare/v0.6.0...v0.6.1) (2023-04-27)


### Bug Fixes

* datetime invalidity in Python ([#72](https://github.com/gentrace/gentrace-python/issues/72)) ([e67d4b8](https://github.com/gentrace/gentrace-python/commit/e67d4b8fcf94db1a65014f60e4ac89c32e30384f))

## [0.6.0](https://github.com/gentrace/gentrace-python/compare/v0.5.6...v0.6.0) (2023-04-27)


### Features

* add in log levels for library ([#70](https://github.com/gentrace/gentrace-python/issues/70)) ([8e6d8fa](https://github.com/gentrace/gentrace-python/commit/8e6d8fad14e93b3a62e5372b92d3165518e78103))

## [0.5.6](https://github.com/gentrace/gentrace-python/compare/v0.5.5...v0.5.6) (2023-04-27)


### Bug Fixes

* allow prompt, change to pipelineRunId ([#68](https://github.com/gentrace/gentrace-python/issues/68)) ([8d449cf](https://github.com/gentrace/gentrace-python/commit/8d449cf557965d7992cfbc8f5208bd4f8ec32705))

## [0.5.5](https://github.com/gentrace/gentrace-python/compare/v0.5.4...v0.5.5) (2023-04-25)


### Bug Fixes

* add validity check for Pinecone ([#67](https://github.com/gentrace/gentrace-python/issues/67)) ([22fd42c](https://github.com/gentrace/gentrace-python/commit/22fd42c954e74291f005ef91913cbb3eabd411cf))
* check hostname validity, throw exception if not correct ([#65](https://github.com/gentrace/gentrace-python/issues/65)) ([6429350](https://github.com/gentrace/gentrace-python/commit/6429350c32a11304749213de6951702ec771c111))

## [0.5.4](https://github.com/gentrace/gentrace-python/compare/v0.5.3...v0.5.4) (2023-04-24)


### Bug Fixes

* add Pinecone tests ([#61](https://github.com/gentrace/gentrace-python/issues/61)) ([5828612](https://github.com/gentrace/gentrace-python/commit/58286129fa46fae4bf08ff73413cc0141f7932f5))
* don't throw if pipeline ID isn't specified ([#63](https://github.com/gentrace/gentrace-python/issues/63)) ([6a06ed3](https://github.com/gentrace/gentrace-python/commit/6a06ed3d3ebcbb672c8103eeaa1273a9d01c971d))

## [0.5.3](https://github.com/gentrace/gentrace-python/compare/v0.5.2...v0.5.3) (2023-04-24)


### Bug Fixes

* add more tests around proper usage patterns ([#60](https://github.com/gentrace/gentrace-python/issues/60)) ([fe8970c](https://github.com/gentrace/gentrace-python/commit/fe8970cf4539bedddf74fa1f6956ef24f93c13e4))
* store old create/acreate functions ([#58](https://github.com/gentrace/gentrace-python/issues/58)) ([b7414c6](https://github.com/gentrace/gentrace-python/commit/b7414c65071b061f560f5e2ec351bdc9237309b4))

## [0.5.2](https://github.com/gentrace/gentrace-python/compare/v0.5.1...v0.5.2) (2023-04-23)


### Bug Fixes

* many proper tests and bug fixes ([#56](https://github.com/gentrace/gentrace-python/issues/56)) ([97ab284](https://github.com/gentrace/gentrace-python/commit/97ab28496cd88b6921ae2f10163789bb31551edf))

## [0.5.1](https://github.com/gentrace/gentrace-python/compare/v0.5.0...v0.5.1) (2023-04-21)


### Bug Fixes

* add in simple SDK refactors ([#52](https://github.com/gentrace/gentrace-python/issues/52)) ([94a2ab9](https://github.com/gentrace/gentrace-python/commit/94a2ab98846956970230f84323fdc0d80fa77152))

## [0.5.0](https://github.com/gentrace/gentrace-python/compare/v0.4.1...v0.5.0) (2023-04-20)


### Features

* simplify the OpenAI interface syntax ([#50](https://github.com/gentrace/gentrace-python/issues/50)) ([0932029](https://github.com/gentrace/gentrace-python/commit/0932029f84600326326f846ca698916ce0f527f6))

## [0.4.1](https://github.com/gentrace/gentrace-python/compare/v0.4.0...v0.4.1) (2023-04-20)


### Bug Fixes

* make stream work with returned pipeline_run_id ([#48](https://github.com/gentrace/gentrace-python/issues/48)) ([ffa60ad](https://github.com/gentrace/gentrace-python/commit/ffa60ada5023d0ee32e8ad5b4407c4f05979d218))

## [0.4.0](https://github.com/gentrace/gentrace-python/compare/v0.3.0...v0.4.0) (2023-04-19)


### Features

* add in gentrace.flush ([#44](https://github.com/gentrace/gentrace-python/issues/44)) ([f896cc2](https://github.com/gentrace/gentrace-python/commit/f896cc295cc59d3c525748bb2700bb5f70b0b967))

## [0.3.0](https://github.com/gentrace/gentrace-python/compare/v0.2.2...v0.3.0) (2023-04-16)


### Features

* add asubmit (async submit) ([#39](https://github.com/gentrace/gentrace-python/issues/39)) ([dc3253f](https://github.com/gentrace/gentrace-python/commit/dc3253f2c74204df069f309f9aecdddc9701ddc9))

## [0.2.2](https://github.com/gentrace/gentrace-python/compare/v0.2.1...v0.2.2) (2023-04-14)


### Bug Fixes

* modify prompt templating to be more Pythonic ([#37](https://github.com/gentrace/gentrace-python/issues/37)) ([0c96b84](https://github.com/gentrace/gentrace-python/commit/0c96b847e10cfa2ec1f4d5eac425d1d6bc78776a))

## [0.2.1](https://github.com/gentrace/gentrace-python/compare/v0.2.0...v0.2.1) (2023-04-14)


### Bug Fixes

* elapsed time is computed in the correct way ([#34](https://github.com/gentrace/gentrace-python/issues/34)) ([88bdf0c](https://github.com/gentrace/gentrace-python/commit/88bdf0c074fae1ab8829d144b440bd8e947cf8e5))

## [0.2.0](https://github.com/gentrace/gentrace-python/compare/v0.1.7...v0.2.0) (2023-04-14)


### Features

* add ChatCompletion async streaming coverage ([#30](https://github.com/gentrace/gentrace-python/issues/30)) ([7128f53](https://github.com/gentrace/gentrace-python/commit/7128f5369652c39ed9b1d825f5eb57c58bcf10ca))


### Bug Fixes

* create OpenAI embedding ([#32](https://github.com/gentrace/gentrace-python/issues/32)) ([13f0917](https://github.com/gentrace/gentrace-python/commit/13f0917eaba6dbb50d5fe65f35ec0446b2feb2b2))

## [0.1.7](https://github.com/gentrace/gentrace-python/compare/v0.1.6...v0.1.7) (2023-04-14)


### Miscellaneous Chores

* release 0.1.7 ([#28](https://github.com/gentrace/gentrace-python/issues/28)) ([bedc759](https://github.com/gentrace/gentrace-python/commit/bedc7599fc2f620ef12a8603f314328f8a41f1ed))

## [0.1.6](https://github.com/gentrace/gentrace-python/compare/v0.1.5...v0.1.6) (2023-04-14)


### Bug Fixes

* modify README ([#22](https://github.com/gentrace/gentrace-python/issues/22)) ([6f399c4](https://github.com/gentrace/gentrace-python/commit/6f399c44b21f2f6f24356a1a4f60ee013a280d62))

## [0.1.5](https://github.com/gentrace/gentrace-python/compare/v0.1.4...v0.1.5) (2023-04-12)


### Bug Fixes

* change name to gentrace-py ([#18](https://github.com/gentrace/gentrace-python/issues/18)) ([0bb41d0](https://github.com/gentrace/gentrace-python/commit/0bb41d00789cd2511febb744dbb121632096ee00))

## [0.1.4](https://github.com/gentrace/gentrace-python/compare/v0.1.3...v0.1.4) (2023-04-12)


### Bug Fixes

* hopefully final test ([#16](https://github.com/gentrace/gentrace-python/issues/16)) ([bf8ec1e](https://github.com/gentrace/gentrace-python/commit/bf8ec1e28be359a40f8b42092c9def7d05aed010))

## [0.1.3](https://github.com/gentrace/gentrace-python/compare/v0.1.2...v0.1.3) (2023-04-12)


### Bug Fixes

* workflow deploys to PyPI ([#12](https://github.com/gentrace/gentrace-python/issues/12)) ([89df6c1](https://github.com/gentrace/gentrace-python/commit/89df6c136bd7d51ce788053f189bff1f09dac444))

## [0.1.2](https://github.com/gentrace/gentrace-python/compare/v0.1.1...v0.1.2) (2023-04-12)


### Bug Fixes

* add another test fix ([#10](https://github.com/gentrace/gentrace-python/issues/10)) ([d65c520](https://github.com/gentrace/gentrace-python/commit/d65c520817ef405d1995f9ea52fb6b342719d28b))

## [0.1.1](https://github.com/gentrace/gentrace-python/compare/v0.1.0...v0.1.1) (2023-04-12)


### Bug Fixes

* add test fix ([#7](https://github.com/gentrace/gentrace-python/issues/7)) ([42cc414](https://github.com/gentrace/gentrace-python/commit/42cc414cc0467bb83f8840031ab880523c4fb0a7))
* test fix behavior ([#9](https://github.com/gentrace/gentrace-python/issues/9)) ([2da4313](https://github.com/gentrace/gentrace-python/commit/2da4313d8baacca3cc428b87e535c2b839db55de))

## 0.1.0 (2023-04-12)


### Bug Fixes

* add in Pinecone PipelineHandler ([cc47d6e](https://github.com/gentrace/gentrace-python/commit/cc47d6e8aad7948af26329edf0ba02465153f4c7))
* add in the OpenAI StepRuns ([0b47b60](https://github.com/gentrace/gentrace-python/commit/0b47b60d9e49503595e18335a68822f35d22f0ed))
* add work on providing custom functionality ([9604ccd](https://github.com/gentrace/gentrace-python/commit/9604ccd60b60be7bcc8e1f5e3ac93f1ec9675dcc))
* adding in base generator assets ([d0d0984](https://github.com/gentrace/gentrace-python/commit/d0d0984c673ac4b8e7897893393e3002b1eff5ec))
* define Makefile and poetry config/deps ([dc40e06](https://github.com/gentrace/gentrace-python/commit/dc40e0608da8cacb326ea375e9e9fde327d768a4))
* include ruff, black, mypy formatters/linters ([8ffdfe4](https://github.com/gentrace/gentrace-python/commit/8ffdfe405a474d688034b7fc04df6ef99684d394))
* intercept chat completion and embedding ([50c9d1a](https://github.com/gentrace/gentrace-python/commit/50c9d1adc57fdf068c6350196d3857e490e15136))
* make sure that lint works ([80af76a](https://github.com/gentrace/gentrace-python/commit/80af76a9ab634ce41f801997c306b013ae3a90d2))
* modify Pinecone usage to include dynamic assignment on module ([4056b0e](https://github.com/gentrace/gentrace-python/commit/4056b0e59681bb82ca3c91caae98d99fb625c2b4))
* simplify OpenAPI generator ([4fce65c](https://github.com/gentrace/gentrace-python/commit/4fce65cf39285fa88e4590c7ffe0848ff39b6687))
* update to pystache ([a44dbab](https://github.com/gentrace/gentrace-python/commit/a44dbabcbcb49cb680a7469fd1ce70b97cc3403d))
