
<!-- TEXT_SECTION:header:START -->
<h1 align="center">
Gentrace Python SDK
</h1>
<p align="center">
  <a href="https://github.com/gentrace/gentrace-node/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Gentrace is released under the MIT license." />
  </a>
  <a href="https://github.com/gentrace/gentrace-node/actions/workflows/release-please.yaml">
    <img src="https://github.com/gentrace/gentrace-node/actions/workflows/release-please.yaml/badge.svg" alt="Release Github action status" />
  </a>
</p>
<!-- TEXT_SECTION:header:END -->


The Gentrace Python library provides convenient access to the Gentrace API from Python applications. Most of the code in this library is generated from our [OpenAPI specification](https://github.com/gentrace/gentrace-openapi).

**Important note: this library is meant for server-side usage only.**

## Installation

```bash
$ pip install gentrace-py
```

Install package dependencies and activate the Poetry shell:

```bash
cd package
poetry install
poetry shell
```

If you want to run examples, install the examples directory Packages and activate the Poetry shellhe. You'll also need to configure a .env file with the necessary services to run the application

```bash
cd examples

# Dependency installation
poetry install
poetry shell

cp .env.example .env
# Make modifications to .env

python examples/pinecone/fetch.py
```

## Getting started

Visit our [guides](https://docs.gentrace.ai/docs/overview) to learn how to get started.

### API reference 

Visit our [API reference](https://docs.gentrace.ai/reference/post_pipeline-run) to construct API requests interactively.

