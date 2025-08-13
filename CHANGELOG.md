# Changelog

## 1.5.1 (2025-08-13)

Full Changelog: [v1.5.0...v1.5.1](https://github.com/gentrace/gentrace-python/compare/v1.5.0...v1.5.1)

### Bug Fixes

* **eval_dataset:** raise limit to 100 concurrency ([#371](https://github.com/gentrace/gentrace-python/issues/371)) ([c7b5db8](https://github.com/gentrace/gentrace-python/commit/c7b5db838f10ead8fc2ed214dd7d3799528488b5))

## 1.5.0 (2025-08-12)

Full Changelog: [v1.4.1...v1.5.0](https://github.com/gentrace/gentrace-python/compare/v1.4.1...v1.5.0)

### Features

* **progress:** show experiment URL in reporters ([#369](https://github.com/gentrace/gentrace-python/issues/369)) ([5a48f44](https://github.com/gentrace/gentrace-python/commit/5a48f445af2131ceb2d758efff95826b24c8ac57))

## 1.4.1 (2025-08-11)

Full Changelog: [v1.4.0...v1.4.1](https://github.com/gentrace/gentrace-python/compare/v1.4.0...v1.4.1)

### Bug Fixes

* **progress:** improve Rich progress bar display ([#367](https://github.com/gentrace/gentrace-python/issues/367)) ([db8c361](https://github.com/gentrace/gentrace-python/commit/db8c3611d597d44611affba2e5ae01c3818be813))

## 1.4.0 (2025-08-11)

Full Changelog: [v1.3.1...v1.4.0](https://github.com/gentrace/gentrace-python/compare/v1.3.1...v1.4.0)

### Features

* **progress:** add progress reporting to evals ([#366](https://github.com/gentrace/gentrace-python/issues/366)) ([9b155dd](https://github.com/gentrace/gentrace-python/commit/9b155dd913c549b1d920b5ccae537389fdf1b874))


### Chores

* **ci:** add python version compatibility tests ([#364](https://github.com/gentrace/gentrace-python/issues/364)) ([afd3e2a](https://github.com/gentrace/gentrace-python/commit/afd3e2a9efed5e2c2aabab3713bd126595599067))
* **internal:** fix ruff target version ([e63f4e8](https://github.com/gentrace/gentrace-python/commit/e63f4e83f6e74bdc3e77f48b9afdb5394ab7cfd8))
* **internal:** update comment in script ([59722c4](https://github.com/gentrace/gentrace-python/commit/59722c4990e467136b116bca9a3d17ff1e51540b))
* update @stainless-api/prism-cli to v5.15.0 ([34c0978](https://github.com/gentrace/gentrace-python/commit/34c097861e79cc3901b0f3583d475e6dea4cda6c))

## 1.3.1 (2025-08-04)

Full Changelog: [v1.3.0...v1.3.1](https://github.com/gentrace/gentrace-python/compare/v1.3.0...v1.3.1)

### Bug Fixes

* **utils:** correct type hints for args and kwargs ([#362](https://github.com/gentrace/gentrace-python/issues/362)) ([bd7a525](https://github.com/gentrace/gentrace-python/commit/bd7a52586092f75c649adbd49f35cfdbb28251de))

## 1.3.0 (2025-07-31)

Full Changelog: [v1.2.0...v1.3.0](https://github.com/gentrace/gentrace-python/compare/v1.2.0...v1.3.0)

### Features

* **otlp:** add detailed export error handling ([2536a8f](https://github.com/gentrace/gentrace-python/commit/2536a8fae47269f83662e9b8c19b2bb9e6e7ef83))


### Bug Fixes

* **warnings:** remove redundant API key permission msg ([276ca6d](https://github.com/gentrace/gentrace-python/commit/276ca6d53e0e3038ea0fa6fd2c44de70f24ddff4))

## 1.2.0 (2025-07-31)

Full Changelog: [v1.1.0...v1.2.0](https://github.com/gentrace/gentrace-python/compare/v1.1.0...v1.2.0)

### Features

* **client:** support file upload requests ([7dd1eea](https://github.com/gentrace/gentrace-python/commit/7dd1eead01ea49fe486a1bf24ee05897801d549d))
* **otlp:** show partial success issues directly in the client SDK code ([#359](https://github.com/gentrace/gentrace-python/issues/359)) ([76c0ada](https://github.com/gentrace/gentrace-python/commit/76c0ada44160a53bd0f59fb3ae374072b3640c8a))


### Chores

* **examples:** add langgraph math agent example ([#360](https://github.com/gentrace/gentrace-python/issues/360)) ([b2f4d86](https://github.com/gentrace/gentrace-python/commit/b2f4d86f8fe3376a2f3d0e0c962e957f62f1b998))

## 1.1.0 (2025-07-24)

Full Changelog: [v1.0.1...v1.1.0](https://github.com/gentrace/gentrace-python/compare/v1.0.1...v1.1.0)

### Features

* **api:** api update ([f3de2b0](https://github.com/gentrace/gentrace-python/commit/f3de2b0bd0120e0fa365ff710bd854f08a33c972))
* **experiment:** Make pipeline_id optional ([#353](https://github.com/gentrace/gentrace-python/issues/353)) ([008d720](https://github.com/gentrace/gentrace-python/commit/008d720a68c08bb0faf63b23a2ff3915463962ef))


### Bug Fixes

* figure out the issue with test failures ([#354](https://github.com/gentrace/gentrace-python/issues/354)) ([b7c5c99](https://github.com/gentrace/gentrace-python/commit/b7c5c99f31eb16967b0588a4040b21932547134c))

## 1.0.1 (2025-07-23)

Full Changelog: [v1.0.0-alpha.13...v1.0.1](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.13...v1.0.1)

### Features

* add organizations resource access ([#343](https://github.com/gentrace/gentrace-python/issues/343)) ([a3440ca](https://github.com/gentrace/gentrace-python/commit/a3440cacfa89145680a9c8ee510e34c9d32f9e90))
* **api:** api update ([6d38ea8](https://github.com/gentrace/gentrace-python/commit/6d38ea8c4cf13fb78fdc8e3fb1994fdef9e2593b))
* **api:** correct the organization structure ([80dbc4f](https://github.com/gentrace/gentrace-python/commit/80dbc4f7203bffdc04db6dbb4d8806dc74ae259d))
* **api:** create organization methods ([a76d501](https://github.com/gentrace/gentrace-python/commit/a76d501e566b387e27ce44573999ac5696398765))
* clean up environment call outs ([1d10b59](https://github.com/gentrace/gentrace-python/commit/1d10b5962e502dd58e07b6f0b164a9148b85a3f9))
* **client:** add support for aiohttp ([d1c67c9](https://github.com/gentrace/gentrace-python/commit/d1c67c9e092374d7ec05696980b8d8a47eb53d8e))
* **client:** add support for aiohttp ([2a1a572](https://github.com/gentrace/gentrace-python/commit/2a1a5726fa89b9299df606abf7c6cfc79e4feb12))
* **examples:** add genai semantic conventions example ([#345](https://github.com/gentrace/gentrace-python/issues/345)) ([8061549](https://github.com/gentrace/gentrace-python/commit/8061549baccd638e9824f2403f9d06086a0c2e66))
* **experiment:** return experiment URL in result ([#344](https://github.com/gentrace/gentrace-python/issues/344)) ([2c7950b](https://github.com/gentrace/gentrace-python/commit/2c7950b3012ae36d5d19d5bbcaea3330bb1d82bc))
* **init:** warn on config changes in multiple init() ([#347](https://github.com/gentrace/gentrace-python/issues/347)) ([e5f66cb](https://github.com/gentrace/gentrace-python/commit/e5f66cb80896302acb9faa98a48831c698632630))
* **interaction:** support default pipeline usage ([#346](https://github.com/gentrace/gentrace-python/issues/346)) ([a81de7a](https://github.com/gentrace/gentrace-python/commit/a81de7a8730a1da91e6f02acfce5a1a96b526192))
* **warnings:** centralize and refactor warnings ([#341](https://github.com/gentrace/gentrace-python/issues/341)) ([eca923a](https://github.com/gentrace/gentrace-python/commit/eca923ab84f2693e8dd9845f345d309fc7951d32))


### Bug Fixes

* **ci:** correct conditional ([7aeac82](https://github.com/gentrace/gentrace-python/commit/7aeac821ff1de2eabec960ef6c4293b5bd43fba0))
* **ci:** release-doctor — report correct token name ([e5f4735](https://github.com/gentrace/gentrace-python/commit/e5f4735a859a0624ec303edfcab41b25363bf416))
* **client:** correctly parse binary response | stream ([36e3af4](https://github.com/gentrace/gentrace-python/commit/36e3af4906699c892a054d574cdf9ec9778cfc72))
* **client:** don't send Content-Type header on GET requests ([9a43359](https://github.com/gentrace/gentrace-python/commit/9a433594fca9ad6dc55d0961c0aff2616d47c08c))
* **eval_dataset:** simplify test case conversion logic ([#349](https://github.com/gentrace/gentrace-python/issues/349)) ([7b7a451](https://github.com/gentrace/gentrace-python/commit/7b7a451e59b7323e901cb76b710e7598089b891b))
* **parsing:** correctly handle nested discriminated unions ([e5b1210](https://github.com/gentrace/gentrace-python/commit/e5b1210ecb70f48b1a6fcb6c56c902eeb1da630d))
* **parsing:** ignore empty metadata ([93edce5](https://github.com/gentrace/gentrace-python/commit/93edce534896516c663e0b5e1bae1562eb6646f6))
* **parsing:** parse extra field types ([bb48320](https://github.com/gentrace/gentrace-python/commit/bb48320b8a174969e0a8e237f3724caeec54e90d))
* **pipeline:** improve async validation scheduling ([#348](https://github.com/gentrace/gentrace-python/issues/348)) ([a9abf88](https://github.com/gentrace/gentrace-python/commit/a9abf88a3eea71cefbbea00a413a61f58020c29a))
* **pipeline:** improve async validation scheduling ([#348](https://github.com/gentrace/gentrace-python/issues/348)) ([#352](https://github.com/gentrace/gentrace-python/issues/352)) ([26e6b2c](https://github.com/gentrace/gentrace-python/commit/26e6b2cecb246e0cee6006e13f9f4f3bd11c2929))
* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([bbd629e](https://github.com/gentrace/gentrace-python/commit/bbd629e3aa5d8cd17bcbb5e204be5f192bd1349d))


### Chores

* **ci:** change upload type ([9f4478a](https://github.com/gentrace/gentrace-python/commit/9f4478a61ef9bfa20e47d485b92c358d90c44b83))
* **ci:** enable for pull requests ([40f97e3](https://github.com/gentrace/gentrace-python/commit/40f97e3771d078713024e471d8f520380729a32b))
* **ci:** only run for pushes and fork pull requests ([4287211](https://github.com/gentrace/gentrace-python/commit/428721113ebd3dcbb9e98b9f7ddc94690c9c38f1))
* fix deps ([0107e7a](https://github.com/gentrace/gentrace-python/commit/0107e7ab08751d51dd08775539b65a65bddf3f8f))
* fix version ([4fa0928](https://github.com/gentrace/gentrace-python/commit/4fa0928bfee4b32a3bc55e5b0bb60f22a8e3ddf6))
* get tests to work with hotfix ([#351](https://github.com/gentrace/gentrace-python/issues/351)) ([8f2e49e](https://github.com/gentrace/gentrace-python/commit/8f2e49eeb803867d26629df45a928eb096a1ca32))
* **internal:** bump pinned h11 dep ([9d732a5](https://github.com/gentrace/gentrace-python/commit/9d732a5987d6b265bd3a33c77b3b1cae0c6078be))
* **internal:** update conftest.py ([1ed8233](https://github.com/gentrace/gentrace-python/commit/1ed8233418094097f0c7be9869b36c7265492bdc))
* **internal:** version bump ([3452596](https://github.com/gentrace/gentrace-python/commit/3452596693673801b642774cc2d6160768195839))
* **package:** mark python 3.13 as supported ([59c5862](https://github.com/gentrace/gentrace-python/commit/59c5862b54bf7a394b1974777b524c07aea7e5dd))
* **readme:** fix version rendering on pypi ([0bfd6e1](https://github.com/gentrace/gentrace-python/commit/0bfd6e1938a3d31a3dc9f3fa911cd883039ee300))
* **readme:** update badges ([0df37ad](https://github.com/gentrace/gentrace-python/commit/0df37ad9cd044f19a27fd35fdcf81a20b6f50330))
* **tests:** add tests for httpx client instantiation & proxies ([092a251](https://github.com/gentrace/gentrace-python/commit/092a251e699e18f328a994c67100b73750458d85))
* **tests:** run tests in parallel ([a892e5b](https://github.com/gentrace/gentrace-python/commit/a892e5b80bdc19f2058fad7bae4935c051325cd1))
* **tests:** skip some failing tests on the latest python versions ([bc643aa](https://github.com/gentrace/gentrace-python/commit/bc643aa42c733501dd174d748b4daff0d33d2e53))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([0ae37db](https://github.com/gentrace/gentrace-python/commit/0ae37db5b297ce830c9be70d9bb87d31b44d10d8))

## 1.0.0-alpha.13 (2025-07-15)

Full Changelog: [v1.0.0-alpha.12...v1.0.0-alpha.13](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.12...v1.0.0-alpha.13)

### Features

* **eval_dataset:** support plain array as data input ([#340](https://github.com/gentrace/gentrace-python/issues/340)) ([588dfef](https://github.com/gentrace/gentrace-python/commit/588dfef084a8855a61e25eb030203ba1f0fb065d))


### Bug Fixes

* Simplify background task scheduling method ([#337](https://github.com/gentrace/gentrace-python/issues/337)) ([c44a348](https://github.com/gentrace/gentrace-python/commit/c44a348099009f3fc5b3d170311ceec27334c039))
* update langchain_simple.py example ([#338](https://github.com/gentrace/gentrace-python/issues/338)) ([2b864d3](https://github.com/gentrace/gentrace-python/commit/2b864d3316d072492c55ce0ff49b8c3f3ce3c1e3))

## 1.0.0-alpha.12 (2025-07-08)

Full Changelog: [v1.0.0-alpha.11...v1.0.0-alpha.12](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.11...v1.0.0-alpha.12)

### Features

* Add max concurrency limit, create shared GentraceWarning abstraction ([#335](https://github.com/gentrace/gentrace-python/issues/335)) ([821e852](https://github.com/gentrace/gentrace-python/commit/821e8524f08a61168ca8411e580fb0cd9f7c9077))

## 1.0.0-alpha.11 (2025-07-07)

Full Changelog: [v1.0.0-alpha.10...v1.0.0-alpha.11](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.10...v1.0.0-alpha.11)

### Features

* Add simple dataset evaluation example with Gentrace ([#334](https://github.com/gentrace/gentrace-python/issues/334)) ([8573a96](https://github.com/gentrace/gentrace-python/commit/8573a963524da26f447ff11a928ef5264d296d0f))


### Chores

* remove vscode dir ([#332](https://github.com/gentrace/gentrace-python/issues/332)) ([3d11612](https://github.com/gentrace/gentrace-python/commit/3d11612492e152d454bc781044459da72e4d1a77))

## 1.0.0-alpha.10 (2025-07-07)

Full Changelog: [v1.0.0-alpha.9...v1.0.0-alpha.10](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.9...v1.0.0-alpha.10)

### Features

* Add Gentrace interaction tracking to manual config script ([7f23560](https://github.com/gentrace/gentrace-python/commit/7f23560f9e588cf0a9413bc92c9399a1892089e0))
* Add LangChain example with Gentrace instrumentation ([#330](https://github.com/gentrace/gentrace-python/issues/330)) ([c157138](https://github.com/gentrace/gentrace-python/commit/c1571380de3bb7f06f6945424c088d387848e3d1))


### Bug Fixes

* Automatically `init()` in the `interaction()` if it's not already initialized ([#328](https://github.com/gentrace/gentrace-python/issues/328)) ([b218e94](https://github.com/gentrace/gentrace-python/commit/b218e946e4f3bc589a7df8df26f697d1f1a0e9cb))

## 1.0.0-alpha.9 (2025-07-04)

Full Changelog: [v1.0.0-alpha.8...v1.0.0-alpha.9](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.8...v1.0.0-alpha.9)

### Chores

* Add otel_setup configuration in init() and check diff ([#324](https://github.com/gentrace/gentrace-python/issues/324)) ([241fdef](https://github.com/gentrace/gentrace-python/commit/241fdef2757b1b0800de5d68271f2faba2d69fc6))
* improve devx ([#329](https://github.com/gentrace/gentrace-python/issues/329)) ([7c76bf2](https://github.com/gentrace/gentrace-python/commit/7c76bf286f75cf796ecdd33f3572a0ce9991d1b2))

## 1.0.0-alpha.8 (2025-06-25)

Full Changelog: [v1.0.0-alpha.7...v1.0.0-alpha.8](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.7...v1.0.0-alpha.8)

### Chores

* Add Agent.instrument_all() call for tracing ([#325](https://github.com/gentrace/gentrace-python/issues/325)) ([91c3473](https://github.com/gentrace/gentrace-python/commit/91c347332ac02fa64da0307d8672064bfc000dcf))

## 1.0.0-alpha.7 (2025-06-25)

Full Changelog: [v1.0.0-alpha.6...v1.0.0-alpha.7](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.6...v1.0.0-alpha.7)

### Features

* Add OpenAI Agents instrumentation example ([#322](https://github.com/gentrace/gentrace-python/issues/322)) ([96f3f23](https://github.com/gentrace/gentrace-python/commit/96f3f23bcdc06603bc788557277490a6a8c07506))

## 1.0.0-alpha.6 (2025-06-20)

Full Changelog: [v1.0.0-alpha.5...v1.0.0-alpha.6](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.5...v1.0.0-alpha.6)

### Bug Fixes

* Deeply simplify the examples ([#319](https://github.com/gentrace/gentrace-python/issues/319)) ([eea245f](https://github.com/gentrace/gentrace-python/commit/eea245ff12e006c9aff0bb964088e9671de72487))

## 1.0.0-alpha.5 (2025-06-19)

Full Changelog: [v1.0.0-alpha.4...v1.0.0-alpha.5](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.4...v1.0.0-alpha.5)

### Features

* Add OTEL setup in `init()` ([#317](https://github.com/gentrace/gentrace-python/issues/317)) ([f6ed028](https://github.com/gentrace/gentrace-python/commit/f6ed028ec23bdd2ac83f054b454b40b1c50f256b))

## 1.0.0-alpha.4 (2025-06-06)

Full Changelog: [v1.0.0-alpha.3...v1.0.0-alpha.4](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.3...v1.0.0-alpha.4)

### Bug Fixes

* Fix incorrect ordering of type annotations ([#314](https://github.com/gentrace/gentrace-python/issues/314)) ([8594dd9](https://github.com/gentrace/gentrace-python/commit/8594dd9277b8f8191d27ef417a64ee1234c85c22))

## 1.0.0-alpha.3 (2025-06-06)

Full Changelog: [v1.0.0-alpha.1...v1.0.0-alpha.3](https://github.com/gentrace/gentrace-python/compare/v1.0.0-alpha.1...v1.0.0-alpha.3)

### Features

* Add Anthropic example and optional dependency ([#305](https://github.com/gentrace/gentrace-python/issues/305)) ([6252d12](https://github.com/gentrace/gentrace-python/commit/6252d1236a5edf6c4755856ace597e4f61eec661))
* add baggage support to eval methods ([#309](https://github.com/gentrace/gentrace-python/issues/309)) ([e8a5904](https://github.com/gentrace/gentrace-python/commit/e8a5904d9c1515f242e39cb35864256db380ad6f))
* Add Claude Assistant GitHub Action workflow ([#296](https://github.com/gentrace/gentrace-python/issues/296)) ([3ff4c9a](https://github.com/gentrace/gentrace-python/commit/3ff4c9acb53bdbfb37c86102e1d49aa8c4e84978))
* add PR title validation workflow ([#293](https://github.com/gentrace/gentrace-python/issues/293)) ([47c7730](https://github.com/gentrace/gentrace-python/commit/47c77301ea8470c5f0d23466396d478f77080092))
* add release type to PR title validation ([#308](https://github.com/gentrace/gentrace-python/issues/308)) ([758b70a](https://github.com/gentrace/gentrace-python/commit/758b70a1fee93587eab7abb1f58dfe6a7598efeb))
* **client:** add follow_redirects request option ([69d68d0](https://github.com/gentrace/gentrace-python/commit/69d68d0aa9fc06047186a4d22be30a49072c364c))
* Improve NUX for copying code snippets ([#304](https://github.com/gentrace/gentrace-python/issues/304)) ([610228a](https://github.com/gentrace/gentrace-python/commit/610228a257bcf934db5a05f06a4a01ef50db7d06))


### Bug Fixes

* add span hierarchy visualization to README ([#294](https://github.com/gentrace/gentrace-python/issues/294)) ([14447cd](https://github.com/gentrace/gentrace-python/commit/14447cd8e7f14743da2efb00c008173393bdd2f6))
* allow beta releases of the baggage span processor ([#307](https://github.com/gentrace/gentrace-python/issues/307)) ([ec1bb71](https://github.com/gentrace/gentrace-python/commit/ec1bb71e087cd693e9eb51e117e4b2cfed82b053))
* Fix the processing of asynchronous generator functions ([#313](https://github.com/gentrace/gentrace-python/issues/313)) ([bec5004](https://github.com/gentrace/gentrace-python/commit/bec500447e65108f9bfa08757c141b457a401dc4))


### Chores

* Add documentation note about `[@traced](https://github.com/traced)()` ([#291](https://github.com/gentrace/gentrace-python/issues/291)) ([b056034](https://github.com/gentrace/gentrace-python/commit/b0560340efb813f89469b81f93ffa212b422722e))
* Add GentraceSampler and GentraceSpanProcessor documentation to README ([#292](https://github.com/gentrace/gentrace-python/issues/292)) ([4113a1a](https://github.com/gentrace/gentrace-python/commit/4113a1a86b641a3228a3142b5f3c376724277fe1))
* Add PydanticAI example ([#310](https://github.com/gentrace/gentrace-python/issues/310)) ([89101f2](https://github.com/gentrace/gentrace-python/commit/89101f2e010427c3365818045d6fb3bdd4b3a533))
* **ci:** fix installation instructions ([68f1b5d](https://github.com/gentrace/gentrace-python/commit/68f1b5de16ac3033118ef1ac5ed02735fed5cb3a))
* **docs:** grammar improvements ([75f3b34](https://github.com/gentrace/gentrace-python/commit/75f3b3491769b9ad0534041e94cb0f457d79f2b5))
* **docs:** remove reference to rye shell ([bbd535e](https://github.com/gentrace/gentrace-python/commit/bbd535e7f8ce282534b448606e6d664e5649e12d))
* **internal:** codegen related update ([3194966](https://github.com/gentrace/gentrace-python/commit/3194966d363ad468af91cae1b063672d25770e66))

## 1.0.0-alpha.1 (2025-05-16)

Full Changelog: [v0.1.7...v1.0.0-alpha.1](https://github.com/gentrace/gentrace-python/compare/v0.1.7...v1.0.0-alpha.1)

### Features

* **api:** Change to API key from Bearer Token ([0002317](https://github.com/gentrace/gentrace-python/commit/00023175ec93452e4e188b3f0ea0b0c1e384aa0a))
* **api:** manual updates ([fd29846](https://github.com/gentrace/gentrace-python/commit/fd29846153cfb564ea64f7920de84214833ad5c5))


### Bug Fixes

* **api:** change the PyPI package name ([590bf1a](https://github.com/gentrace/gentrace-python/commit/590bf1a072693e868dc605cc030c3fccc1d7a7da))
* **package:** support direct resource imports ([d4cbf5e](https://github.com/gentrace/gentrace-python/commit/d4cbf5e345b436c3a9edadcae8215e1fc882cba2))


### Chores

* **ci:** upload sdks to package manager ([de63329](https://github.com/gentrace/gentrace-python/commit/de633299f30b4fc55888db8da9fd4346afa2a9ab))
* **internal:** avoid errors for isinstance checks on proxies ([02c9e3d](https://github.com/gentrace/gentrace-python/commit/02c9e3dceee7d4bde615c9528694447f3adf24eb))
* **internal:** version bump ([86c6815](https://github.com/gentrace/gentrace-python/commit/86c68153521fa5cb19c697bc1758325e5384a1a2))

## 0.1.7 (2025-05-07)

Full Changelog: [v0.0.1-alpha.0...v0.1.7](https://github.com/gentrace/gentrace-python/compare/v0.0.1-alpha.0...v0.1.7)

### Features

* Accept output steps ([#119](https://github.com/gentrace/gentrace-python/issues/119)) ([673b453](https://github.com/gentrace/gentrace-python/commit/673b45307be8d1f8e809b8b5eac99b8fd546d5e0))
* add asubmit (async submit) ([#39](https://github.com/gentrace/gentrace-python/issues/39)) ([dc3253f](https://github.com/gentrace/gentrace-python/commit/dc3253f2c74204df069f309f9aecdddc9701ddc9))
* Add bulk create SDK, remove OpenAI completion endpoint ([#192](https://github.com/gentrace/gentrace-python/issues/192)) ([f395b0f](https://github.com/gentrace/gentrace-python/commit/f395b0ff0c0444737234c93a6116ec3ec5aafe78))
* Add case filter to run_test() ([#188](https://github.com/gentrace/gentrace-python/issues/188)) ([86a2ee3](https://github.com/gentrace/gentrace-python/commit/86a2ee3155487c393ee4594856fe6c68d49b2c38))
* add chat completion templating ([#76](https://github.com/gentrace/gentrace-python/issues/76)) ([9ef50d2](https://github.com/gentrace/gentrace-python/commit/9ef50d24745fe5659aa3b17d119fc5ec8bd82c96))
* add ChatCompletion async streaming coverage ([#30](https://github.com/gentrace/gentrace-python/issues/30)) ([7128f53](https://github.com/gentrace/gentrace-python/commit/7128f5369652c39ed9b1d825f5eb57c58bcf10ca))
* Add datasets ([#237](https://github.com/gentrace/gentrace-python/issues/237)) ([2a79458](https://github.com/gentrace/gentrace-python/commit/2a794582f733e8885d258729f07144a764950cf4))
* add evaluation routes ([#91](https://github.com/gentrace/gentrace-python/issues/91)) ([f967745](https://github.com/gentrace/gentrace-python/commit/f967745a9dd3a4233c60b1cf32aab6a13f08bf16))
* Add evaluation routes, deprecate set ID a few calls ([#146](https://github.com/gentrace/gentrace-python/issues/146)) ([7d6fd9b](https://github.com/gentrace/gentrace-python/commit/7d6fd9b5445b1cb7a39ee085287ee680362e19ac))
* Add experiments alpha ([#259](https://github.com/gentrace/gentrace-python/issues/259)) ([3adb79f](https://github.com/gentrace/gentrace-python/commit/3adb79fedc9f5625ae2abe3cecdbb9561c69974e))
* add file uploading ([#168](https://github.com/gentrace/gentrace-python/issues/168)) ([38ed312](https://github.com/gentrace/gentrace-python/commit/38ed3128fdcf2d67305b7236b0a5c81d2a8f0f11))
* add heartbeat task, fix various overriding bugs ([#266](https://github.com/gentrace/gentrace-python/issues/266)) ([e7bfacc](https://github.com/gentrace/gentrace-python/commit/e7bfacc5fe17a986deeb52ffbd62b6b8ad99e1d6))
* add in gentrace.flush ([#44](https://github.com/gentrace/gentrace-python/issues/44)) ([f896cc2](https://github.com/gentrace/gentrace-python/commit/f896cc295cc59d3c525748bb2700bb5f70b0b967))
* add in log levels for library ([#70](https://github.com/gentrace/gentrace-python/issues/70)) ([8e6d8fa](https://github.com/gentrace/gentrace-python/commit/8e6d8fad14e93b3a62e5372b92d3165518e78103))
* add path to run ([#256](https://github.com/gentrace/gentrace-python/issues/256)) ([420a82f](https://github.com/gentrace/gentrace-python/commit/420a82f61efa9b513c72c74338748bb37599da21))
* Add result_name parameter to the test result submission ([#202](https://github.com/gentrace/gentrace-python/issues/202)) ([42d7dbe](https://github.com/gentrace/gentrace-python/commit/42d7dbe246285ab17fccafa56a9c93c904bb8587))
* Add run metadata ([#159](https://github.com/gentrace/gentrace-python/issues/159)) ([8a5f0c3](https://github.com/gentrace/gentrace-python/commit/8a5f0c3a03ad4a4c239f96546dc007efcfa5b155))
* Add string_parameter function in test_job_runner ([#264](https://github.com/gentrace/gentrace-python/issues/264)) ([49fffa4](https://github.com/gentrace/gentrace-python/commit/49fffa47cf283dd5e6e53779f821bec198c00f50))
* Add test case singular ([#186](https://github.com/gentrace/gentrace-python/issues/186)) ([03c358f](https://github.com/gentrace/gentrace-python/commit/03c358f31bea1219c0d55c6b7ed72e9dde4d76eb))
* Add test result endpoints ([#155](https://github.com/gentrace/gentrace-python/issues/155)) ([2d01cbd](https://github.com/gentrace/gentrace-python/commit/2d01cbd793aa7048aeaae1d396f4a22cb06a8c5a))
* Add test result metadata ([#163](https://github.com/gentrace/gentrace-python/issues/163)) ([4180462](https://github.com/gentrace/gentrace-python/commit/41804629790496b0ee01352a9d8748d02d312493))
* Add test result simple route, include step run flattening ([#148](https://github.com/gentrace/gentrace-python/issues/148)) ([daaa0c5](https://github.com/gentrace/gentrace-python/commit/daaa0c5528c632d60b6e8316362f57a9645ac59b))
* Add TestRun name ([#113](https://github.com/gentrace/gentrace-python/issues/113)) ([e99fe69](https://github.com/gentrace/gentrace-python/commit/e99fe69d9578d58e3d403b833c912aa345f0c2c3))
* add TestSet routes and testing ([#123](https://github.com/gentrace/gentrace-python/issues/123)) ([39b7b44](https://github.com/gentrace/gentrace-python/commit/39b7b44cdc7f88055482414e9565fb07178d095a))
* add the branch commit logic, init() function ([#99](https://github.com/gentrace/gentrace-python/issues/99)) ([2f6dd2c](https://github.com/gentrace/gentrace-python/commit/2f6dd2c80ffb68bc0e2685b4ec444d75268f9723))
* Add threading ([#161](https://github.com/gentrace/gentrace-python/issues/161)) ([1075e4e](https://github.com/gentrace/gentrace-python/commit/1075e4ed610713e71a50e3744d50c5917f46b278))
* Allow passing in `GENTRACE_BRANCH` and `GENTRACE_COMMIT` as env variables ([4f2327d](https://github.com/gentrace/gentrace-python/commit/4f2327da14a71c78c712f08faa65bc3a30d76cd8))
* api V2 supported (not used in core methods yet) ([#175](https://github.com/gentrace/gentrace-python/issues/175)) ([c0df3d0](https://github.com/gentrace/gentrace-python/commit/c0df3d068858a03f0bc97b8986b653fa3ada392a))
* get_evaluators SDK function w example ([#214](https://github.com/gentrace/gentrace-python/issues/214)) ([4fb03ac](https://github.com/gentrace/gentrace-python/commit/4fb03ace887ed4c8205a73075fc41a1f8319ccb4))
* get_test_runners and submit_test_runners with example ([#219](https://github.com/gentrace/gentrace-python/issues/219)) ([46db714](https://github.com/gentrace/gentrace-python/commit/46db71479815dc28ab83a082da287551899e1dec))
* Merge evaluate and observe ([#127](https://github.com/gentrace/gentrace-python/issues/127)) ([8529582](https://github.com/gentrace/gentrace-python/commit/85295823a807d8c02ca0f038316dadf301809454))
* Remove await from parse_obj call in runner ([#275](https://github.com/gentrace/gentrace-python/issues/275)) ([1baabf0](https://github.com/gentrace/gentrace-python/commit/1baabf0a57e389d8529f353d601bec32fc7950ba))
* run/step errors ([#244](https://github.com/gentrace/gentrace-python/issues/244)) ([20f0d42](https://github.com/gentrace/gentrace-python/commit/20f0d42706d574251c44457271314dbe67c35d98))
* setup ai configs in pipeline constructor ([#221](https://github.com/gentrace/gentrace-python/issues/221)) ([d981b41](https://github.com/gentrace/gentrace-python/commit/d981b4178cdf043e0f574ddeeb2ce1028a571981))
* Should allow no expected outputs ([#241](https://github.com/gentrace/gentrace-python/issues/241)) ([99b80a2](https://github.com/gentrace/gentrace-python/commit/99b80a2cddfae1f4b957798ffbe5ca0757729254))
* Simplify SDK for evaluation ([#105](https://github.com/gentrace/gentrace-python/issues/105)) ([ae605c1](https://github.com/gentrace/gentrace-python/commit/ae605c156489ca2913ec0bc3e2f35fbb5e57ba99))
* simplify the OpenAI interface syntax ([#50](https://github.com/gentrace/gentrace-python/issues/50)) ([0932029](https://github.com/gentrace/gentrace-python/commit/0932029f84600326326f846ca698916ce0f527f6))
* Support openai-python 1.x.x ([#167](https://github.com/gentrace/gentrace-python/issues/167)) ([f534741](https://github.com/gentrace/gentrace-python/commit/f534741f2e81b2639b7a120ffe1e5695ed861ca1))
* Update docstring punctuation in get_value function ([#271](https://github.com/gentrace/gentrace-python/issues/271)) ([8e05a26](https://github.com/gentrace/gentrace-python/commit/8e05a26ccf18ef619431c94204d600f41eb5e660))
* update gentrace-py version and streamline signal handling ([#279](https://github.com/gentrace/gentrace-python/issues/279)) ([7a5669f](https://github.com/gentrace/gentrace-python/commit/7a5669fa3dccc98572efbe6d7a4edb9385110f93))
* Update package version and improve signal handling ([#277](https://github.com/gentrace/gentrace-python/issues/277)) ([279c074](https://github.com/gentrace/gentrace-python/commit/279c074897185bb29e2b8bceaba272073e6ab656))
* update poetry.lock and pyproject.toml dependencies ([#273](https://github.com/gentrace/gentrace-python/issues/273)) ([a8c3559](https://github.com/gentrace/gentrace-python/commit/a8c3559bd4050fc0c7fd54f5fcff817c3ad05fbd))
* when ingesting test runs, support outputs (a JSON blob) and deprecate output / outputSteps ([#124](https://github.com/gentrace/gentrace-python/issues/124)) ([c63e23c](https://github.com/gentrace/gentrace-python/commit/c63e23cc1cd4bd87ef1f9bfbeb8525e5bfc9d832))


### Bug Fixes

* add another test fix ([#10](https://github.com/gentrace/gentrace-python/issues/10)) ([d65c520](https://github.com/gentrace/gentrace-python/commit/d65c520817ef405d1995f9ea52fb6b342719d28b))
* Add boolean metadata type to SDK ([#212](https://github.com/gentrace/gentrace-python/issues/212)) ([57bc876](https://github.com/gentrace/gentrace-python/commit/57bc87600b50b6eb2078dd27a95a8fec46bd08c2))
* add chat completion tests ([#74](https://github.com/gentrace/gentrace-python/issues/74)) ([b0ffcf8](https://github.com/gentrace/gentrace-python/commit/b0ffcf88130cc9392642062f1a115558354f5e36))
* Add collection method ([#134](https://github.com/gentrace/gentrace-python/issues/134)) ([4cbe774](https://github.com/gentrace/gentrace-python/commit/4cbe77438b819f2c0784af929a81e49c0ee0108a))
* Add context ([#150](https://github.com/gentrace/gentrace-python/issues/150)) ([c9fd8ff](https://github.com/gentrace/gentrace-python/commit/c9fd8ff910886c16c132072e52b26247eec4efd4))
* Add custom class input/output serialization ([#233](https://github.com/gentrace/gentrace-python/issues/233)) ([dcea498](https://github.com/gentrace/gentrace-python/commit/dcea4983a0635073af897e3e4aaf32f01c970216))
* Add dataset ID to create_test_case(s) ([#239](https://github.com/gentrace/gentrace-python/issues/239)) ([035a2b7](https://github.com/gentrace/gentrace-python/commit/035a2b73eae791608beba4f205dc3cfefdc7c43e))
* add evaluation tests ([#103](https://github.com/gentrace/gentrace-python/issues/103)) ([173dd00](https://github.com/gentrace/gentrace-python/commit/173dd002a158ec2a0f7e04da6bcf2218d518636e))
* add get_run function to Python SDK ([#210](https://github.com/gentrace/gentrace-python/issues/210)) ([42a3b65](https://github.com/gentrace/gentrace-python/commit/42a3b65b99e6b5ee24ba918981c5d42dc40ecb98))
* add heuristicFnLanguage to evaluator ([#223](https://github.com/gentrace/gentrace-python/issues/223)) ([1109895](https://github.com/gentrace/gentrace-python/commit/1109895efea01def7ca92d4a686a2b489b2b33cb))
* add in Pinecone PipelineHandler ([cc47d6e](https://github.com/gentrace/gentrace-python/commit/cc47d6e8aad7948af26329edf0ba02465153f4c7))
* add in simple SDK refactors ([#52](https://github.com/gentrace/gentrace-python/issues/52)) ([94a2ab9](https://github.com/gentrace/gentrace-python/commit/94a2ab98846956970230f84323fdc0d80fa77152))
* add in the OpenAI StepRuns ([0b47b60](https://github.com/gentrace/gentrace-python/commit/0b47b60d9e49503595e18335a68822f35d22f0ed))
* Add in upload_bytes ([#170](https://github.com/gentrace/gentrace-python/issues/170)) ([a2e8428](https://github.com/gentrace/gentrace-python/commit/a2e84283ba7234030d386ba950f303c9830a60a5))
* Add inputs and templates for chat completion rendering ([#142](https://github.com/gentrace/gentrace-python/issues/142)) ([dee4360](https://github.com/gentrace/gentrace-python/commit/dee43607485030742a50ce33b7c31e03d2290018))
* Add more permissions ([#248](https://github.com/gentrace/gentrace-python/issues/248)) ([fd176d6](https://github.com/gentrace/gentrace-python/commit/fd176d6dff9038afd3b8ff7a11da06207619e023))
* Add more specific models for metadata ([#208](https://github.com/gentrace/gentrace-python/issues/208)) ([c566008](https://github.com/gentrace/gentrace-python/commit/c566008b8a6967fed453a2feb690f6597768e6b2))
* add more tests around proper usage patterns ([#60](https://github.com/gentrace/gentrace-python/issues/60)) ([fe8970c](https://github.com/gentrace/gentrace-python/commit/fe8970cf4539bedddf74fa1f6956ef24f93c13e4))
* add Pinecone tests ([#61](https://github.com/gentrace/gentrace-python/issues/61)) ([5828612](https://github.com/gentrace/gentrace-python/commit/58286129fa46fae4bf08ff73413cc0141f7932f5))
* Add Python PR check ([#179](https://github.com/gentrace/gentrace-python/issues/179)) ([e5087c2](https://github.com/gentrace/gentrace-python/commit/e5087c20096952fb22978dadf212fc42afc29757))
* Add render key, rename "context" to "gentrace" to match Node ([#152](https://github.com/gentrace/gentrace-python/issues/152)) ([a864fd2](https://github.com/gentrace/gentrace-python/commit/a864fd2c730217b2fe939d761c0b8488dad5a1f6))
* Add result name for run_test() ([#204](https://github.com/gentrace/gentrace-python/issues/204)) ([4a59851](https://github.com/gentrace/gentrace-python/commit/4a5985145f33157b7640a2047940540cd56162a0))
* Add test counter ([#136](https://github.com/gentrace/gentrace-python/issues/136)) ([84172d7](https://github.com/gentrace/gentrace-python/commit/84172d73d7b5193ee9fa8d806d053cf6f8dece73))
* add test fix ([#7](https://github.com/gentrace/gentrace-python/issues/7)) ([42cc414](https://github.com/gentrace/gentrace-python/commit/42cc414cc0467bb83f8840031ab880523c4fb0a7))
* Add typings for get test cases ([#115](https://github.com/gentrace/gentrace-python/issues/115)) ([dbf8cd4](https://github.com/gentrace/gentrace-python/commit/dbf8cd4539979c78eab60166e6066c432bbeff91))
* add validity check for Pinecone ([#67](https://github.com/gentrace/gentrace-python/issues/67)) ([22fd42c](https://github.com/gentrace/gentrace-python/commit/22fd42c954e74291f005ef91913cbb3eabd411cf))
* add work on providing custom functionality ([9604ccd](https://github.com/gentrace/gentrace-python/commit/9604ccd60b60be7bcc8e1f5e3ac93f1ec9675dcc))
* adding in base generator assets ([d0d0984](https://github.com/gentrace/gentrace-python/commit/d0d0984c673ac4b8e7897893393e3002b1eff5ec))
* allow prompt, change to pipelineRunId ([#68](https://github.com/gentrace/gentrace-python/issues/68)) ([8d449cf](https://github.com/gentrace/gentrace-python/commit/8d449cf557965d7992cfbc8f5208bd4f8ec32705))
* cd into correct directory ([#14](https://github.com/gentrace/gentrace-python/issues/14)) ([07ba0d5](https://github.com/gentrace/gentrace-python/commit/07ba0d50575657241181f8fd51099edbfd1f7c8e))
* change directory structure to reflect docs ([#64](https://github.com/gentrace/gentrace-python/issues/64)) ([684b041](https://github.com/gentrace/gentrace-python/commit/684b04181b8f4e3cab6667ee0d4836bb0764f351))
* change name to gentrace-py ([#18](https://github.com/gentrace/gentrace-python/issues/18)) ([0bb41d0](https://github.com/gentrace/gentrace-python/commit/0bb41d00789cd2511febb744dbb121632096ee00))
* check hostname validity, throw exception if not correct ([#65](https://github.com/gentrace/gentrace-python/issues/65)) ([6429350](https://github.com/gentrace/gentrace-python/commit/6429350c32a11304749213de6951702ec771c111))
* create OpenAI embedding ([#32](https://github.com/gentrace/gentrace-python/issues/32)) ([13f0917](https://github.com/gentrace/gentrace-python/commit/13f0917eaba6dbb50d5fe65f35ec0446b2feb2b2))
* datetime invalidity in Python ([#72](https://github.com/gentrace/gentrace-python/issues/72)) ([e67d4b8](https://github.com/gentrace/gentrace-python/commit/e67d4b8fcf94db1a65014f60e4ac89c32e30384f))
* Deep copy inputs ([#198](https://github.com/gentrace/gentrace-python/issues/198)) ([d07fa62](https://github.com/gentrace/gentrace-python/commit/d07fa62d0757c686c01546b93b834af886093e50))
* define Makefile and poetry config/deps ([dc40e06](https://github.com/gentrace/gentrace-python/commit/dc40e0608da8cacb326ea375e9e9fde327d768a4))
* Do not use built-in type subscripting  ([#130](https://github.com/gentrace/gentrace-python/issues/130)) ([b825cf8](https://github.com/gentrace/gentrace-python/commit/b825cf832631c502bc17d939ffc1a9273f606da0))
* don't throw if pipeline ID isn't specified ([#63](https://github.com/gentrace/gentrace-python/issues/63)) ([6a06ed3](https://github.com/gentrace/gentrace-python/commit/6a06ed3d3ebcbb672c8103eeaa1273a9d01c971d))
* elapsed time is computed in the correct way ([#34](https://github.com/gentrace/gentrace-python/issues/34)) ([88bdf0c](https://github.com/gentrace/gentrace-python/commit/88bdf0c074fae1ab8829d144b440bd8e947cf8e5))
* Elapsed time is provided to the API sever as milliseconds ([#227](https://github.com/gentrace/gentrace-python/issues/227)) ([f4b088c](https://github.com/gentrace/gentrace-python/commit/f4b088cbeb1e929d5252e79eb3eccdc8e51811be))
* Ensure that run_test flushes at the end ([#139](https://github.com/gentrace/gentrace-python/issues/139)) ([255b813](https://github.com/gentrace/gentrace-python/commit/255b8133bc7e8e7b3f436fe0734431173868917e))
* Fix accidental Python 3.9 typing issue  ([#257](https://github.com/gentrace/gentrace-python/issues/257)) ([25f0022](https://github.com/gentrace/gentrace-python/commit/25f0022eb7eb3e7fe03c1bd38463ec02a4f5d08e))
* Fix ameasure submission ([#229](https://github.com/gentrace/gentrace-python/issues/229)) ([c520eb9](https://github.com/gentrace/gentrace-python/commit/c520eb90c6e4356a1ca308429e9478d90c5fa286))
* Fix ameasure() outputs ([#231](https://github.com/gentrace/gentrace-python/issues/231)) ([984bc5b](https://github.com/gentrace/gentrace-python/commit/984bc5bc221eaf74642c107a5e86be4b72c5a47f))
* Fix chat completion message failing ([#195](https://github.com/gentrace/gentrace-python/issues/195)) ([91c6396](https://github.com/gentrace/gentrace-python/commit/91c639650281c909aa19000c150f5edac0f2d2b7))
* Fix dependencies for Python Poetry environments ([#253](https://github.com/gentrace/gentrace-python/issues/253)) ([0c2a8e4](https://github.com/gentrace/gentrace-python/commit/0c2a8e49b3813f3c8eb90d335d495df6f09949b0))
* Fix dynamic schema serialization ([#235](https://github.com/gentrace/gentrace-python/issues/235)) ([f542112](https://github.com/gentrace/gentrace-python/commit/f5421127f4bd4ffde8b1de84d1759d83e982d69a))
* Fix Gentrace run name ([#165](https://github.com/gentrace/gentrace-python/issues/165)) ([3903289](https://github.com/gentrace/gentrace-python/commit/3903289d1931735083dc3719f25155748bb76242))
* Fix ISO checkpoint() issues for Python &lt;= 3.10.0 ([#177](https://github.com/gentrace/gentrace-python/issues/177)) ([b43e9db](https://github.com/gentrace/gentrace-python/commit/b43e9db1fc96b6046d4f43b943bc241fa950cf39))
* Fix issue with prior overriding value ([#178](https://github.com/gentrace/gentrace-python/issues/178)) ([0582776](https://github.com/gentrace/gentrace-python/commit/05827769831b330205f0ffc31f3ea2852beb7758))
* Fix issue with stale connection in pool ([#132](https://github.com/gentrace/gentrace-python/issues/132)) ([252a666](https://github.com/gentrace/gentrace-python/commit/252a66661845d5abe8904ef6ad9ae6a173eb235a))
* Fix Poetry lock file [#262](https://github.com/gentrace/gentrace-python/issues/262) ([140d791](https://github.com/gentrace/gentrace-python/commit/140d7910d24e19f783ce85498918d1f475889de5))
* Fix Python typing ([#157](https://github.com/gentrace/gentrace-python/issues/157)) ([afedadf](https://github.com/gentrace/gentrace-python/commit/afedadf09089acdb677fc6a1a29f914918654c93))
* Fix resolved host ([#183](https://github.com/gentrace/gentrace-python/issues/183)) ([d5c27aa](https://github.com/gentrace/gentrace-python/commit/d5c27aa52bbb508b094157e4e9385e86153f6005))
* Fix slug not accepted in Python invocation ([#144](https://github.com/gentrace/gentrace-python/issues/144)) ([660e7f7](https://github.com/gentrace/gentrace-python/commit/660e7f7b7ac5143f5d0c03592d12ecfc10b485b9))
* Fix typing issue with submit_test_result() ([#190](https://github.com/gentrace/gentrace-python/issues/190)) ([db282ea](https://github.com/gentrace/gentrace-python/commit/db282eab9441cdf4e362307dcbdaa87494f4d1a4))
* Handle tool_calls ([#206](https://github.com/gentrace/gentrace-python/issues/206)) ([777802b](https://github.com/gentrace/gentrace-python/commit/777802bb12274613899287c18c1a7bd2188a48ee))
* hopefully final test ([#16](https://github.com/gentrace/gentrace-python/issues/16)) ([bf8ec1e](https://github.com/gentrace/gentrace-python/commit/bf8ec1e28be359a40f8b42092c9def7d05aed010))
* include ruff, black, mypy formatters/linters ([8ffdfe4](https://github.com/gentrace/gentrace-python/commit/8ffdfe405a474d688034b7fc04df6ef99684d394))
* input for prompt just the entire prompt string ([#77](https://github.com/gentrace/gentrace-python/issues/77)) ([6c5fceb](https://github.com/gentrace/gentrace-python/commit/6c5fceb2166dfa53dff9184360f8aa706b39ad95))
* intercept chat completion and embedding ([50c9d1a](https://github.com/gentrace/gentrace-python/commit/50c9d1adc57fdf068c6350196d3857e490e15136))
* make stream work with returned pipeline_run_id ([#48](https://github.com/gentrace/gentrace-python/issues/48)) ([ffa60ad](https://github.com/gentrace/gentrace-python/commit/ffa60ada5023d0ee32e8ad5b4407c4f05979d218))
* make sure that lint works ([80af76a](https://github.com/gentrace/gentrace-python/commit/80af76a9ab634ce41f801997c306b013ae3a90d2))
* make sure that not applying a host is fine ([#79](https://github.com/gentrace/gentrace-python/issues/79)) ([0708570](https://github.com/gentrace/gentrace-python/commit/0708570500869b6db9763ec2db52c9939cbc15d1))
* Make sure that release please can work ([#249](https://github.com/gentrace/gentrace-python/issues/249)) ([ff56cad](https://github.com/gentrace/gentrace-python/commit/ff56cad9af1527538e7f8f5313c6ad864720dda0))
* many proper tests and bug fixes ([#56](https://github.com/gentrace/gentrace-python/issues/56)) ([97ab284](https://github.com/gentrace/gentrace-python/commit/97ab28496cd88b6921ae2f10163789bb31551edf))
* modify Pinecone usage to include dynamic assignment on module ([4056b0e](https://github.com/gentrace/gentrace-python/commit/4056b0e59681bb82ca3c91caae98d99fb625c2b4))
* modify prompt templating to be more Pythonic ([#37](https://github.com/gentrace/gentrace-python/issues/37)) ([0c96b84](https://github.com/gentrace/gentrace-python/commit/0c96b847e10cfa2ec1f4d5eac425d1d6bc78776a))
* modify README ([#22](https://github.com/gentrace/gentrace-python/issues/22)) ([6f399c4](https://github.com/gentrace/gentrace-python/commit/6f399c44b21f2f6f24356a1a4f60ee013a280d62))
* only import openai when used ([#225](https://github.com/gentrace/gentrace-python/issues/225)) ([1cd2075](https://github.com/gentrace/gentrace-python/commit/1cd2075b4dc7867599a05566405df81421c3b75a))
* Read `GENTRACE_API_KEY` from the environment  (109) ([755a907](https://github.com/gentrace/gentrace-python/commit/755a907db6568986e4cd0fdf19112a2a19950784))
* README, client-side makes no sense ([#20](https://github.com/gentrace/gentrace-python/issues/20)) ([2b6a784](https://github.com/gentrace/gentrace-python/commit/2b6a784b66f0b7fca2743b4fb10f244e6513f97e))
* remove print statement ([#172](https://github.com/gentrace/gentrace-python/issues/172)) ([4f82676](https://github.com/gentrace/gentrace-python/commit/4f8267697491b96d0334eb3df6d03f8f46f9b713))
* Remove pytest requirements ([#247](https://github.com/gentrace/gentrace-python/issues/247)) ([e243955](https://github.com/gentrace/gentrace-python/commit/e243955ec821fc1766deac27ca3bea6fa4f8911e))
* remove python-dotenv from mandatory requirements ([#82](https://github.com/gentrace/gentrace-python/issues/82)) ([b035bd7](https://github.com/gentrace/gentrace-python/commit/b035bd7300c871247ac3dd44242397abb7f0265b))
* simplify OpenAPI generator ([4fce65c](https://github.com/gentrace/gentrace-python/commit/4fce65cf39285fa88e4590c7ffe0848ff39b6687))
* Simplify test case creation multiple method ([#153](https://github.com/gentrace/gentrace-python/issues/153)) ([ffed81c](https://github.com/gentrace/gentrace-python/commit/ffed81cf1e1aab24b86f1066ba5af161537d76e7))
* Specify evaluation payloads ([#194](https://github.com/gentrace/gentrace-python/issues/194)) ([ef66bb5](https://github.com/gentrace/gentrace-python/commit/ef66bb504c7c039f13cfa7d17d47771e1126751b))
* store old create/acreate functions ([#58](https://github.com/gentrace/gentrace-python/issues/58)) ([b7414c6](https://github.com/gentrace/gentrace-python/commit/b7414c65071b061f560f5e2ec351bdc9237309b4))
* Support a more flexible urllib3 range ([#200](https://github.com/gentrace/gentrace-python/issues/200)) ([31aedf6](https://github.com/gentrace/gentrace-python/commit/31aedf6718d423c52d11911270197c394b5f5768))
* test fix behavior ([#9](https://github.com/gentrace/gentrace-python/issues/9)) ([2da4313](https://github.com/gentrace/gentrace-python/commit/2da4313d8baacca3cc428b87e535c2b839db55de))
* **test_job_runner:** Remove premature confirmation message ([#268](https://github.com/gentrace/gentrace-python/issues/268)) ([99f1a2b](https://github.com/gentrace/gentrace-python/commit/99f1a2b05702a14f5780539bafea0cccc6eea4b0))
* Uncomment API host configuration in test-job-runner ([#270](https://github.com/gentrace/gentrace-python/issues/270)) ([f886453](https://github.com/gentrace/gentrace-python/commit/f886453e535d38e8d9f9a512c89a052c475b6340))
* update archivedAt to use UnixSecondsNullable ([#216](https://github.com/gentrace/gentrace-python/issues/216)) ([27f206a](https://github.com/gentrace/gentrace-python/commit/27f206a68e801b1d8216b19aa2387c2192981a72))
* Update lock file ([#251](https://github.com/gentrace/gentrace-python/issues/251)) ([ad7bb12](https://github.com/gentrace/gentrace-python/commit/ad7bb12ba524df6b0fb4f7747b9c50188b9cbb00))
* update to pystache ([a44dbab](https://github.com/gentrace/gentrace-python/commit/a44dbabcbcb49cb680a7469fd1ce70b97cc3403d))
* updating OpenAI generated Python logic to "0.6.0" ([#94](https://github.com/gentrace/gentrace-python/issues/94)) ([2511ab5](https://github.com/gentrace/gentrace-python/commit/2511ab5b57b26ac46b9dfcfe9b882136ecddde8b))
* Use v1 tags from OpenAPI generator ([#181](https://github.com/gentrace/gentrace-python/issues/181)) ([34aba67](https://github.com/gentrace/gentrace-python/commit/34aba67e994757c3de9af8360846e3923aed4a45))
* workflow deploys to PyPI ([#12](https://github.com/gentrace/gentrace-python/issues/12)) ([89df6c1](https://github.com/gentrace/gentrace-python/commit/89df6c136bd7d51ce788053f189bff1f09dac444))
* Wrap parse() structured output ([#242](https://github.com/gentrace/gentrace-python/issues/242)) ([d91a13a](https://github.com/gentrace/gentrace-python/commit/d91a13a4960a29e6aa4374bef59db326b8740150))
* wrap streamed output correctly for the ChatCompletion endpoint ([#89](https://github.com/gentrace/gentrace-python/issues/89)) ([8cb0518](https://github.com/gentrace/gentrace-python/commit/8cb0518e7b07298bb3832954d1da4039f1c098bc))


### Chores

* Add API usage example ([#246](https://github.com/gentrace/gentrace-python/issues/246)) ([2137b46](https://github.com/gentrace/gentrace-python/commit/2137b4636c47de123594bc335b78e82a347eb17f))
* add code owners file ([800c403](https://github.com/gentrace/gentrace-python/commit/800c4030ce14bf3ac27f935f028330e3c6785235))
* add formatting as a Makefile target ([2c6eebd](https://github.com/gentrace/gentrace-python/commit/2c6eebdb103bb15ea51c32f41e2257fe4bf8fda1))
* add in Poetry basic skeletion ([5325408](https://github.com/gentrace/gentrace-python/commit/5325408464be69105b1918125d80264c5d58b67c))
* add in ruff cache to .gitignore ([b0f8f50](https://github.com/gentrace/gentrace-python/commit/b0f8f503ba5f06572cc951610d76780f360f19ba))
* add initial commit ([b2cbafd](https://github.com/gentrace/gentrace-python/commit/b2cbafdb6d04025e1bd64a3811321bc7c51ede83))
* add license ([f544e97](https://github.com/gentrace/gentrace-python/commit/f544e97212e70f7cbe105630ce1411b9f8596eb7))
* add license and repo urls ([78b1036](https://github.com/gentrace/gentrace-python/commit/78b1036562206829c6ae172ca71be5f82de9c88d))
* add pre-commit with linters and conventional commits([#21](https://github.com/gentrace/gentrace-python/issues/21)) ([9302bc4](https://github.com/gentrace/gentrace-python/commit/9302bc44811177ea673c10087bbfcd8b48163fe0))
* add pre-commit, pyyaml ([#24](https://github.com/gentrace/gentrace-python/issues/24)) ([144e852](https://github.com/gentrace/gentrace-python/commit/144e85278705af8c88b7d96382df4d3f232cccf3))
* add test commit ([8220f06](https://github.com/gentrace/gentrace-python/commit/8220f068621c824bfaf207e4fb3df16e68669866))
* adust Makefile for clarity ([4c93c05](https://github.com/gentrace/gentrace-python/commit/4c93c05519cf42658e613eb47f48c1bc5a6899fa))
* Cleaner examples for experiments ([#261](https://github.com/gentrace/gentrace-python/issues/261)) ([3fae03f](https://github.com/gentrace/gentrace-python/commit/3fae03f576cdffa8f5ebdfd7940ba392c6f83aa7))
* fix typing ([#27](https://github.com/gentrace/gentrace-python/issues/27)) ([e7c1e1f](https://github.com/gentrace/gentrace-python/commit/e7c1e1fafdf1fcc9cb845f35407d339a654eb396))
* fix up README ([#25](https://github.com/gentrace/gentrace-python/issues/25)) ([fc66533](https://github.com/gentrace/gentrace-python/commit/fc66533df52aeae5f8295839f9100a98e7cd918d))
* include poetry.lock ([72ca5dd](https://github.com/gentrace/gentrace-python/commit/72ca5dddc7b49b73b42a48a94541ec28f95d93df))
* **main:** release 0.1.0 ([#3](https://github.com/gentrace/gentrace-python/issues/3)) ([98081ff](https://github.com/gentrace/gentrace-python/commit/98081ff5d3d133db61ddf9e41dbb14cdaeb8edf7))
* **main:** release 0.1.1 ([#8](https://github.com/gentrace/gentrace-python/issues/8)) ([5128d27](https://github.com/gentrace/gentrace-python/commit/5128d279439e77ed3f75ae833c01f874ec862551))
* **main:** release 0.1.2 ([#11](https://github.com/gentrace/gentrace-python/issues/11)) ([0511de2](https://github.com/gentrace/gentrace-python/commit/0511de29fe1eaa3873b175e8c1dae7ec6e3453d1))
* **main:** release 0.1.3 ([#13](https://github.com/gentrace/gentrace-python/issues/13)) ([4a262a3](https://github.com/gentrace/gentrace-python/commit/4a262a314dc6b72c2b5f33affc652540eab21499))
* **main:** release 0.1.4 ([#17](https://github.com/gentrace/gentrace-python/issues/17)) ([01914ba](https://github.com/gentrace/gentrace-python/commit/01914bad37234b101150f004d26856b882f46a6b))
* **main:** release 0.1.5 ([#19](https://github.com/gentrace/gentrace-python/issues/19)) ([da6470d](https://github.com/gentrace/gentrace-python/commit/da6470d1b71d1579b097d772b0342910f76fa9b5))
* **main:** release 0.1.6 ([#23](https://github.com/gentrace/gentrace-python/issues/23)) ([d9553a9](https://github.com/gentrace/gentrace-python/commit/d9553a994e88223a0794cf26be8d786b6abe6adb))
* **main:** release 0.1.7 ([#29](https://github.com/gentrace/gentrace-python/issues/29)) ([92e1a9d](https://github.com/gentrace/gentrace-python/commit/92e1a9d35b5bb60da145093662b5296cc88c6b1b))
* **main:** release 0.10.0 ([#106](https://github.com/gentrace/gentrace-python/issues/106)) ([d7f8055](https://github.com/gentrace/gentrace-python/commit/d7f805530ce1132884de889a264c71b6d9b50556))
* **main:** release 0.11.0 ([#108](https://github.com/gentrace/gentrace-python/issues/108)) ([2f1ebb1](https://github.com/gentrace/gentrace-python/commit/2f1ebb1ab91052ed29c2de4b01cd17fea1ad3a36))
* **main:** release 0.11.1 ([#110](https://github.com/gentrace/gentrace-python/issues/110)) ([a1e9f0a](https://github.com/gentrace/gentrace-python/commit/a1e9f0a6c54f87a25077ccae701b3094387f77bf))
* **main:** release 0.12.0 ([#114](https://github.com/gentrace/gentrace-python/issues/114)) ([a22b88c](https://github.com/gentrace/gentrace-python/commit/a22b88cde929bb4643736941bbd43dfcad8922ba))
* **main:** release 0.12.1 ([#116](https://github.com/gentrace/gentrace-python/issues/116)) ([4a0d3fd](https://github.com/gentrace/gentrace-python/commit/4a0d3fde6a7454f6ce82825cb69a06bd73d609ef))
* **main:** release 0.13.0 ([#121](https://github.com/gentrace/gentrace-python/issues/121)) ([c529e72](https://github.com/gentrace/gentrace-python/commit/c529e72fc281ecc7663239000e8c2eb8e4273470))
* **main:** release 0.14.0 ([#125](https://github.com/gentrace/gentrace-python/issues/125)) ([f9ab9f5](https://github.com/gentrace/gentrace-python/commit/f9ab9f5f7c26eab623100e38545bc7e757007a80))
* **main:** release 0.15.0 ([#128](https://github.com/gentrace/gentrace-python/issues/128)) ([3a23032](https://github.com/gentrace/gentrace-python/commit/3a23032dbdd922aee1597036d3f4da1184244fea))
* **main:** release 0.15.1 ([#131](https://github.com/gentrace/gentrace-python/issues/131)) ([5375cde](https://github.com/gentrace/gentrace-python/commit/5375cde88882fae72d35c111e7bc2d5fa02e96d6))
* **main:** release 0.15.2 ([#133](https://github.com/gentrace/gentrace-python/issues/133)) ([b94afdf](https://github.com/gentrace/gentrace-python/commit/b94afdfe01fd0ee94730765fc46e1f01c1469885))
* **main:** release 0.15.3 ([#135](https://github.com/gentrace/gentrace-python/issues/135)) ([ff395df](https://github.com/gentrace/gentrace-python/commit/ff395dfb1c45b8a7b763af58e000a42175367e64))
* **main:** release 0.15.4 ([#140](https://github.com/gentrace/gentrace-python/issues/140)) ([9b2d803](https://github.com/gentrace/gentrace-python/commit/9b2d803e1f834da09ddfacbe48070df08fa645a5))
* **main:** release 0.15.5 ([#143](https://github.com/gentrace/gentrace-python/issues/143)) ([4d561a8](https://github.com/gentrace/gentrace-python/commit/4d561a8ad5f1c4b2d1524172f2d6dfdb6fc645d3))
* **main:** release 0.15.6 ([#145](https://github.com/gentrace/gentrace-python/issues/145)) ([338cc03](https://github.com/gentrace/gentrace-python/commit/338cc03d786048e0007837fcab2e955e28bec1b3))
* **main:** release 0.16.0 ([#147](https://github.com/gentrace/gentrace-python/issues/147)) ([b214d8d](https://github.com/gentrace/gentrace-python/commit/b214d8d030652f1d9b38c4090afd0c079bb9a3d7))
* **main:** release 0.17.0 ([#149](https://github.com/gentrace/gentrace-python/issues/149)) ([fa98694](https://github.com/gentrace/gentrace-python/commit/fa98694108b7712a8385ecfecb0e23c9cb4179fc))
* **main:** release 0.17.1 ([#151](https://github.com/gentrace/gentrace-python/issues/151)) ([1796909](https://github.com/gentrace/gentrace-python/commit/1796909150d0d49349fd4d202563976c852f2296))
* **main:** release 0.17.2 ([#154](https://github.com/gentrace/gentrace-python/issues/154)) ([11fafba](https://github.com/gentrace/gentrace-python/commit/11fafba8434deefa946f999a44dd7cfb5cec9e37))
* **main:** release 0.18.0 ([#156](https://github.com/gentrace/gentrace-python/issues/156)) ([e8222f0](https://github.com/gentrace/gentrace-python/commit/e8222f007df9e2021cc7a5a43650f056bf0bf061))
* **main:** release 0.18.1 ([#158](https://github.com/gentrace/gentrace-python/issues/158)) ([aced3f5](https://github.com/gentrace/gentrace-python/commit/aced3f577f6c6ac161ad4096f1564171bf0fd08f))
* **main:** release 0.19.0 ([#160](https://github.com/gentrace/gentrace-python/issues/160)) ([0c31819](https://github.com/gentrace/gentrace-python/commit/0c31819bb462635dd3d74b6501c7d2c9dead920c))
* **main:** release 0.2.0 ([#31](https://github.com/gentrace/gentrace-python/issues/31)) ([d8f296c](https://github.com/gentrace/gentrace-python/commit/d8f296c5322e9b2fb8f708234a2ea6744c7a234c))
* **main:** release 0.2.1 ([#35](https://github.com/gentrace/gentrace-python/issues/35)) ([c4da66f](https://github.com/gentrace/gentrace-python/commit/c4da66f443c2bc124f3ebdb4301f8d39443d696a))
* **main:** release 0.2.2 ([#38](https://github.com/gentrace/gentrace-python/issues/38)) ([d382b54](https://github.com/gentrace/gentrace-python/commit/d382b546892ed182d81f1f5f001998cc6f1588f8))
* **main:** release 0.20.0 ([#162](https://github.com/gentrace/gentrace-python/issues/162)) ([1dedc55](https://github.com/gentrace/gentrace-python/commit/1dedc5502fb52bf5520991527be177d17da49e43))
* **main:** release 0.21.0 ([#164](https://github.com/gentrace/gentrace-python/issues/164)) ([a416217](https://github.com/gentrace/gentrace-python/commit/a416217f0ae20862d97a5eacab75b65cdebfca5a))
* **main:** release 0.21.1 ([#166](https://github.com/gentrace/gentrace-python/issues/166)) ([f33f2ba](https://github.com/gentrace/gentrace-python/commit/f33f2bacc362a85de7a740e98a083c4817100f11))
* **main:** release 0.22.0 ([#169](https://github.com/gentrace/gentrace-python/issues/169)) ([1483bb8](https://github.com/gentrace/gentrace-python/commit/1483bb887e110420970dc50695d0b24a2b5352a5))
* **main:** release 0.22.1 ([#171](https://github.com/gentrace/gentrace-python/issues/171)) ([e4d93ca](https://github.com/gentrace/gentrace-python/commit/e4d93ca210b8ed658aa1d428399b71108b45caad))
* **main:** release 0.22.2 ([#173](https://github.com/gentrace/gentrace-python/issues/173)) ([124b439](https://github.com/gentrace/gentrace-python/commit/124b439f8bc8d26b4d73769932e4bdc810f1ffe7))
* **main:** release 0.23.0 ([#174](https://github.com/gentrace/gentrace-python/issues/174)) ([2a2a422](https://github.com/gentrace/gentrace-python/commit/2a2a422b23c6e873aed579e7dec81eff36885a6b))
* **main:** release 0.24.0 ([#176](https://github.com/gentrace/gentrace-python/issues/176)) ([e2b8c40](https://github.com/gentrace/gentrace-python/commit/e2b8c40b96f7cdf07f05acee93253c0001443e8c))
* **main:** release 0.24.1 ([#180](https://github.com/gentrace/gentrace-python/issues/180)) ([7dca95a](https://github.com/gentrace/gentrace-python/commit/7dca95adb8aa543fe2a4bd491a3bc6ccd3c61805))
* **main:** release 0.24.2 ([#182](https://github.com/gentrace/gentrace-python/issues/182)) ([c127dc5](https://github.com/gentrace/gentrace-python/commit/c127dc542339bfe9f82e77940d00ddcd8d5514a9))
* **main:** release 0.24.3 ([#184](https://github.com/gentrace/gentrace-python/issues/184)) ([23eba3a](https://github.com/gentrace/gentrace-python/commit/23eba3ab8845d100a3c7f18a3b3e4e3a060d0d01))
* **main:** release 0.25.0 ([#187](https://github.com/gentrace/gentrace-python/issues/187)) ([cde0b2b](https://github.com/gentrace/gentrace-python/commit/cde0b2b5f5431b39a3954a7f23ada41bce9f113d))
* **main:** release 0.26.0 ([#189](https://github.com/gentrace/gentrace-python/issues/189)) ([ff724d6](https://github.com/gentrace/gentrace-python/commit/ff724d6146eecf0a4f6f5f0b191c860e2a975c9e))
* **main:** release 0.26.1 ([#191](https://github.com/gentrace/gentrace-python/issues/191)) ([d5b6a99](https://github.com/gentrace/gentrace-python/commit/d5b6a99a2ba1742879a50d0893a3411245e00956))
* **main:** release 0.27.0 ([#193](https://github.com/gentrace/gentrace-python/issues/193)) ([e9fd1e1](https://github.com/gentrace/gentrace-python/commit/e9fd1e1a46d564a36d82948cef00cff9fb1f137e))
* **main:** release 0.27.1 ([#196](https://github.com/gentrace/gentrace-python/issues/196)) ([49e5cb8](https://github.com/gentrace/gentrace-python/commit/49e5cb8d4c8ed3d07d5d18d961c603c24b0385e5))
* **main:** release 0.27.2 ([#199](https://github.com/gentrace/gentrace-python/issues/199)) ([11f1f5f](https://github.com/gentrace/gentrace-python/commit/11f1f5f8da4c6e081230958f6b291961b716e53f))
* **main:** release 0.27.3 ([#201](https://github.com/gentrace/gentrace-python/issues/201)) ([a39480b](https://github.com/gentrace/gentrace-python/commit/a39480bad6b5acf18745b802a3c790608082833f))
* **main:** release 0.28.0 ([#203](https://github.com/gentrace/gentrace-python/issues/203)) ([f63be31](https://github.com/gentrace/gentrace-python/commit/f63be31d5e155f0f8be3543e9bdd19d63c9ec77f))
* **main:** release 0.28.1 ([#205](https://github.com/gentrace/gentrace-python/issues/205)) ([71650d9](https://github.com/gentrace/gentrace-python/commit/71650d996323571dd7b624ced22d32807b7d4583))
* **main:** release 0.28.2 ([#207](https://github.com/gentrace/gentrace-python/issues/207)) ([e3f5a99](https://github.com/gentrace/gentrace-python/commit/e3f5a990a2d2e4210a95c11346832a169dd29fe0))
* **main:** release 0.28.3 ([#209](https://github.com/gentrace/gentrace-python/issues/209)) ([87000ec](https://github.com/gentrace/gentrace-python/commit/87000ec73e202523c2c5785e3912f2adc1496046))
* **main:** release 0.28.4 ([#211](https://github.com/gentrace/gentrace-python/issues/211)) ([9900159](https://github.com/gentrace/gentrace-python/commit/99001598ca5e498a89951f039d48d23a9dda820f))
* **main:** release 0.28.5 ([#213](https://github.com/gentrace/gentrace-python/issues/213)) ([e31fc8f](https://github.com/gentrace/gentrace-python/commit/e31fc8f2ba88db4c985b919771491311279d53d5))
* **main:** release 0.29.0 ([#215](https://github.com/gentrace/gentrace-python/issues/215)) ([9eff1ab](https://github.com/gentrace/gentrace-python/commit/9eff1ab446bc4b5aebb76c7a8c31f1fa37155645))
* **main:** release 0.29.1 ([#217](https://github.com/gentrace/gentrace-python/issues/217)) ([266a35a](https://github.com/gentrace/gentrace-python/commit/266a35a55ab87d306f0fefffc9a27c9d18bced83))
* **main:** release 0.3.0 ([#40](https://github.com/gentrace/gentrace-python/issues/40)) ([efd0f9b](https://github.com/gentrace/gentrace-python/commit/efd0f9b25d70530f2e60b9e58ed49b76c3ce5999))
* **main:** release 0.30.0 ([#220](https://github.com/gentrace/gentrace-python/issues/220)) ([a871460](https://github.com/gentrace/gentrace-python/commit/a8714600de98f4013819125b252c39ddbde13607))
* **main:** release 0.31.0 ([#222](https://github.com/gentrace/gentrace-python/issues/222)) ([925c780](https://github.com/gentrace/gentrace-python/commit/925c7800fcd544ea4772b9a78eaca31834f0436c))
* **main:** release 0.31.1 ([#224](https://github.com/gentrace/gentrace-python/issues/224)) ([cb0384c](https://github.com/gentrace/gentrace-python/commit/cb0384c685951daf2fdc68a407688214e79c92eb))
* **main:** release 0.31.2 ([#226](https://github.com/gentrace/gentrace-python/issues/226)) ([91ef6ed](https://github.com/gentrace/gentrace-python/commit/91ef6ed24c09d6675c376de8ae5131eef8bd7d75))
* **main:** release 0.31.3 ([#228](https://github.com/gentrace/gentrace-python/issues/228)) ([cb09de0](https://github.com/gentrace/gentrace-python/commit/cb09de0f5f9b0282c285069ce58b4c14995b2035))
* **main:** release 0.31.4 ([#230](https://github.com/gentrace/gentrace-python/issues/230)) ([0417497](https://github.com/gentrace/gentrace-python/commit/0417497654261f15a7f886864237a2e226b64959))
* **main:** release 0.31.5 ([#232](https://github.com/gentrace/gentrace-python/issues/232)) ([0264bdf](https://github.com/gentrace/gentrace-python/commit/0264bdfcd87b0d1cda4b980b71143c49a110f1fd))
* **main:** release 0.31.6 ([#234](https://github.com/gentrace/gentrace-python/issues/234)) ([26d09bc](https://github.com/gentrace/gentrace-python/commit/26d09bce46fe59f0909925be4284d16452ded052))
* **main:** release 0.31.7 ([#236](https://github.com/gentrace/gentrace-python/issues/236)) ([bd2c977](https://github.com/gentrace/gentrace-python/commit/bd2c9773782e71c6937c8ed545a7f68ec98e5c9a))
* **main:** release 0.32.0 ([#238](https://github.com/gentrace/gentrace-python/issues/238)) ([991b517](https://github.com/gentrace/gentrace-python/commit/991b517f52a49de6c9bb303675421d9fda1073a9))
* **main:** release 0.32.1 ([#240](https://github.com/gentrace/gentrace-python/issues/240)) ([9e80170](https://github.com/gentrace/gentrace-python/commit/9e80170954084f0c738d7dcc03ce23d436eb0429))
* **main:** release 0.32.2 ([#243](https://github.com/gentrace/gentrace-python/issues/243)) ([7761515](https://github.com/gentrace/gentrace-python/commit/77615158b3ab9d932b43fb9afb2d7c7a832c016e))
* **main:** release 0.33.0 ([#250](https://github.com/gentrace/gentrace-python/issues/250)) ([f397eae](https://github.com/gentrace/gentrace-python/commit/f397eae5f3df06c5943c8c66e9b0c24c089ae632))
* **main:** release 0.33.1 ([#252](https://github.com/gentrace/gentrace-python/issues/252)) ([60ecedd](https://github.com/gentrace/gentrace-python/commit/60eceddc35cce296ac26802a8c154d5f1bb96229))
* **main:** release 0.34.0 ([#254](https://github.com/gentrace/gentrace-python/issues/254)) ([355c1de](https://github.com/gentrace/gentrace-python/commit/355c1deff5ad89c0ca4e00df06aa2e47a6517e63))
* **main:** release 0.34.1 ([#258](https://github.com/gentrace/gentrace-python/issues/258)) ([f7cc4ac](https://github.com/gentrace/gentrace-python/commit/f7cc4ac38c6289b7b5cd65b3e46da704df2a78c9))
* **main:** release 0.35.0 ([#260](https://github.com/gentrace/gentrace-python/issues/260)) ([a7c7bbb](https://github.com/gentrace/gentrace-python/commit/a7c7bbbce8c459bdc58e31b868ebd8ebb5fde1c4))
* **main:** release 0.35.1 ([#263](https://github.com/gentrace/gentrace-python/issues/263)) ([93cff6a](https://github.com/gentrace/gentrace-python/commit/93cff6a13043fc65e49ab324b294b627c07d6765))
* **main:** release 0.36.0 ([#265](https://github.com/gentrace/gentrace-python/issues/265)) ([1f90fe9](https://github.com/gentrace/gentrace-python/commit/1f90fe9c530613cccdf1f2b1c4ca58be224e80ad))
* **main:** release 0.37.0 ([#267](https://github.com/gentrace/gentrace-python/issues/267)) ([119c9c2](https://github.com/gentrace/gentrace-python/commit/119c9c2866f4deacc79a41aec235f88da03fdbc3))
* **main:** release 0.38.0 ([#272](https://github.com/gentrace/gentrace-python/issues/272)) ([33f8fb4](https://github.com/gentrace/gentrace-python/commit/33f8fb4b69b6126847d91463eddc5a696918a368))
* **main:** release 0.39.0 ([#274](https://github.com/gentrace/gentrace-python/issues/274)) ([930452f](https://github.com/gentrace/gentrace-python/commit/930452f45299a13e404a529baccd72a41a67ae2c))
* **main:** release 0.4.0 ([#46](https://github.com/gentrace/gentrace-python/issues/46)) ([711b8dd](https://github.com/gentrace/gentrace-python/commit/711b8dd538c3de4048f117d03f883a84bb8f85f4))
* **main:** release 0.4.1 ([#49](https://github.com/gentrace/gentrace-python/issues/49)) ([6b13508](https://github.com/gentrace/gentrace-python/commit/6b1350839be1cb745500f3b64fdc2a5cddbbd20b))
* **main:** release 0.40.0 ([#276](https://github.com/gentrace/gentrace-python/issues/276)) ([4145762](https://github.com/gentrace/gentrace-python/commit/4145762c6c185c063f4337c9448cf5f16eac530f))
* **main:** release 0.41.0 ([#278](https://github.com/gentrace/gentrace-python/issues/278)) ([471e7aa](https://github.com/gentrace/gentrace-python/commit/471e7aabfc62443c59cb3760d5f21a91dd8d0745))
* **main:** release 0.42.0 ([#280](https://github.com/gentrace/gentrace-python/issues/280)) ([cb7d2e5](https://github.com/gentrace/gentrace-python/commit/cb7d2e5d15e1cabb16c7dacb1d1118ed904ebec5))
* **main:** release 0.5.0 ([#51](https://github.com/gentrace/gentrace-python/issues/51)) ([0266475](https://github.com/gentrace/gentrace-python/commit/02664757ca245ddb10dc966962419c752c9ca031))
* **main:** release 0.5.1 ([#55](https://github.com/gentrace/gentrace-python/issues/55)) ([be05740](https://github.com/gentrace/gentrace-python/commit/be057401aa40df5872cc7931d4e39433170b233f))
* **main:** release 0.5.2 ([#57](https://github.com/gentrace/gentrace-python/issues/57)) ([19969da](https://github.com/gentrace/gentrace-python/commit/19969dab7e4f330babf0e7ec73e8fe99e668701c))
* **main:** release 0.5.3 ([#59](https://github.com/gentrace/gentrace-python/issues/59)) ([5ad0814](https://github.com/gentrace/gentrace-python/commit/5ad081497e4838319899ccbb478532f34e9ea6ce))
* **main:** release 0.5.4 ([#62](https://github.com/gentrace/gentrace-python/issues/62)) ([5d5b16f](https://github.com/gentrace/gentrace-python/commit/5d5b16f2fb27cecff4bb5ab23db53263652815be))
* **main:** release 0.5.5 ([#66](https://github.com/gentrace/gentrace-python/issues/66)) ([d21c11f](https://github.com/gentrace/gentrace-python/commit/d21c11f8c9b53ed13273866945d2d4a797dd6d6a))
* **main:** release 0.5.6 ([#69](https://github.com/gentrace/gentrace-python/issues/69)) ([2261bcd](https://github.com/gentrace/gentrace-python/commit/2261bcd335ca08615eebd0b5fc1b28552dacfc62))
* **main:** release 0.6.0 ([#71](https://github.com/gentrace/gentrace-python/issues/71)) ([34c3fb0](https://github.com/gentrace/gentrace-python/commit/34c3fb094386d2966752af3b2247f402c05f56b9))
* **main:** release 0.6.1 ([#73](https://github.com/gentrace/gentrace-python/issues/73)) ([c092380](https://github.com/gentrace/gentrace-python/commit/c09238023947115f38c06385f1bb8070d38336a3))
* **main:** release 0.7.0 ([#75](https://github.com/gentrace/gentrace-python/issues/75)) ([3bbb27f](https://github.com/gentrace/gentrace-python/commit/3bbb27fc0a93c5faa17c146d49270ac696de575b))
* **main:** release 0.7.1 ([#78](https://github.com/gentrace/gentrace-python/issues/78)) ([59c72d1](https://github.com/gentrace/gentrace-python/commit/59c72d1987c5c66b95b42720d55372e4798f2763))
* **main:** release 0.7.2 ([#80](https://github.com/gentrace/gentrace-python/issues/80)) ([e7172ca](https://github.com/gentrace/gentrace-python/commit/e7172ca6de7d49a707d18c35c194ddde1c3a070b))
* **main:** release 0.7.3 ([#83](https://github.com/gentrace/gentrace-python/issues/83)) ([7818f4e](https://github.com/gentrace/gentrace-python/commit/7818f4ed51d5820fc919c570ce1d626053869659))
* **main:** release 0.7.4 ([#90](https://github.com/gentrace/gentrace-python/issues/90)) ([d58ff91](https://github.com/gentrace/gentrace-python/commit/d58ff91cc7d58e88e80ae61b2e147fd5fa68105c))
* **main:** release 0.8.0 ([#92](https://github.com/gentrace/gentrace-python/issues/92)) ([68090c3](https://github.com/gentrace/gentrace-python/commit/68090c3293fbb9c0c70722b19483c4ae3653eb5d))
* **main:** release 0.8.1 ([#95](https://github.com/gentrace/gentrace-python/issues/95)) ([e1f803f](https://github.com/gentrace/gentrace-python/commit/e1f803f1c37bcb8bc22e1e481ce0cd629146ea86))
* **main:** release 0.9.0 ([#102](https://github.com/gentrace/gentrace-python/issues/102)) ([ca2440a](https://github.com/gentrace/gentrace-python/commit/ca2440ac602b0e0562d5a0a5c6ad53507a90318b))
* **main:** release 0.9.1 ([#104](https://github.com/gentrace/gentrace-python/issues/104)) ([8549cdb](https://github.com/gentrace/gentrace-python/commit/8549cdb3550fcc371439d0a27e2e7ae764685280))
* Periodic update to keep Pinecone index fresh ([#185](https://github.com/gentrace/gentrace-python/issues/185)) ([4a0cc19](https://github.com/gentrace/gentrace-python/commit/4a0cc191c3a2cd39b2df75f09b1980533178bce0))
* reference the deployed package ([#26](https://github.com/gentrace/gentrace-python/issues/26)) ([835b0ae](https://github.com/gentrace/gentrace-python/commit/835b0aebbe0f95ab4a17e124f2fb21c8fea8d04d))
* specify virtualenv within the project directory ([d8c9c2e](https://github.com/gentrace/gentrace-python/commit/d8c9c2efbbe9a63f77b8096499d755171045651a))
* sync repo ([09776d7](https://github.com/gentrace/gentrace-python/commit/09776d70341f9869dba0ced1e4c32c3b509dd544))
* test that reviewers were added correctly ([#4](https://github.com/gentrace/gentrace-python/issues/4)) ([3e3da24](https://github.com/gentrace/gentrace-python/commit/3e3da24132a64880c625f2ff84fe32eb2e7625e2))
* update README to point to the right docs ([#81](https://github.com/gentrace/gentrace-python/issues/81)) ([0f3ca95](https://github.com/gentrace/gentrace-python/commit/0f3ca9561cf5d1e70f7f372ff419bab1a364718f))
* update SDK settings ([c4608be](https://github.com/gentrace/gentrace-python/commit/c4608be33c138e7b66d7d7e58fa6c8944d72ff61))
* updating OpenAI generated Python logic to "0.4.0" ([#6](https://github.com/gentrace/gentrace-python/issues/6)) ([9b1771e](https://github.com/gentrace/gentrace-python/commit/9b1771ea28e8e7013b5329a89c1faf7512a2015b))
* updating OpenAI generated Python logic to "0.4.1" ([#36](https://github.com/gentrace/gentrace-python/issues/36)) ([d3c63ad](https://github.com/gentrace/gentrace-python/commit/d3c63ad53cdc2c2ecb659b9c59e8034ff6477ef5))
* updating OpenAI generated Python logic to "0.4.4" ([#43](https://github.com/gentrace/gentrace-python/issues/43)) ([5dcd0b2](https://github.com/gentrace/gentrace-python/commit/5dcd0b2f9fc12741e1e136e81a3316cf681c7f89))
* updating OpenAI generated Python logic to "0.4.6" ([#47](https://github.com/gentrace/gentrace-python/issues/47)) ([5833ca9](https://github.com/gentrace/gentrace-python/commit/5833ca99c8328de768a0da2d9fd2a79d41a24c7e))
* updating OpenAI generated Python logic to "0.4.8" ([#54](https://github.com/gentrace/gentrace-python/issues/54)) ([8803829](https://github.com/gentrace/gentrace-python/commit/8803829991c6a744b9043169d740fa998b9af20c))
* updating OpenAI generated Python logic to "0.6.2" ([#97](https://github.com/gentrace/gentrace-python/issues/97)) ([dade48c](https://github.com/gentrace/gentrace-python/commit/dade48cd2feef60c13b59c25a0ea75990aee10a6))
* updating OpenAI generated Python logic to "0.6.3" ([#98](https://github.com/gentrace/gentrace-python/issues/98)) ([89bb23d](https://github.com/gentrace/gentrace-python/commit/89bb23d6422565c3f8d4977d6a9e907eea7d767c))
* updating OpenAI generated Python logic to "0.6.4" ([#100](https://github.com/gentrace/gentrace-python/issues/100)) ([cd34c07](https://github.com/gentrace/gentrace-python/commit/cd34c07682f9d4ee04246aea5f44cb8982724d81))
* updating OpenAI generated Python logic to "0.7.1" ([#112](https://github.com/gentrace/gentrace-python/issues/112)) ([d04ac4d](https://github.com/gentrace/gentrace-python/commit/d04ac4dc58a1e53d3c25452f452fd0df63b6ab24))
* updating OpenAI generated Python logic to "0.8.0" ([#118](https://github.com/gentrace/gentrace-python/issues/118)) ([6896218](https://github.com/gentrace/gentrace-python/commit/6896218e486e95bc7e1ba346d613382790d57f67))
* updating OpenAI generated Python logic to "0.8.1" ([#120](https://github.com/gentrace/gentrace-python/issues/120)) ([54b16f6](https://github.com/gentrace/gentrace-python/commit/54b16f6e4cd0894eb266668172c0522f30ff036f))
* updating OpenAI generated Python logic to "0.9.0" ([#122](https://github.com/gentrace/gentrace-python/issues/122)) ([6fcfaea](https://github.com/gentrace/gentrace-python/commit/6fcfaea03f51173876522bde9d57b0f6d69b2a8e))
* use try/catch ([#33](https://github.com/gentrace/gentrace-python/issues/33)) ([681a3fc](https://github.com/gentrace/gentrace-python/commit/681a3fc8a1b9f8f81ea6d72e41442efafbb835d0))


### Build System

* Remove secondary source from pyproject.toml ([#269](https://github.com/gentrace/gentrace-python/issues/269)) ([3e6f859](https://github.com/gentrace/gentrace-python/commit/3e6f859143df601cbd15c113625f406c5e838469))
