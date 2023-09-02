<!-- Top Section -->
<p align="center">
  <a href="https://oribarilan.github.io/oplog"><img src="https://oribarilan.github.io/oplog/imgs/logo_full.png" alt="oplog logo"></a>
</p>

<p align="center">
  <b>Modern logging library for Python applications.</b>
</p>

<!-- Badges using https://shields.io/badges/ -->
<p align="center">
  <!-- Python versions -->
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue" alt="python versions">
  </a>
  <!-- Downloads -->
  <a href="https://pypi.org/project/op-log/">
    <img src="https://img.shields.io/pypi/dm/op-log?link=https%3A%2F%2Fpypi.org%2Fproject%2Fop-log%2F" alt="downloads">
  </a>
  <!-- Ruff credit -->
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <!-- Build -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/package_build.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/package_build.yml" alt="build">
  </a>
  <!-- Lint -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/lint.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/lint.yml?label=lint" alt="lint">
  </a>
  <!-- Coverage -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/coverage.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/coverage.yml?label=coverage%3E95%25" alt="coverage">
  </a>
  <!-- Security -->
  <a href="https://github.com/oribarilan/oplog/actions/workflows/security_check.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/oribarilan/oplog/security_check.yml?label=security" alt="security">
  </a>
</p>

<hr>

Full documentation: [oribarilan.github.io/oplog](https://oribarilan.github.io/oplog/).

Source code: [github.com/oribarilan/oplog](http://www.github.com/oribarilan/oplog/).

---

## What is oplog?

!!! warning

    oplog is currently in beta. At this point, we expect the API to be stable and core functionality to be working as expected. However, there are still some features that you may find missing. If you have any feedback, please open an issue.


oplog is a modern logging library for Python applications.
oplog offers a different paradigm for logging, which is based on the concept of logging operations.
Instead of creating a "log-book", which is a long scroll of text messages, oplog is about logging operations with rich data.

## Key features

1. **Object Oriented**: Intuitive API, easy to use and extend.
2. **Modern & Scalable**: Unlike log messages, oplog is scaleable. Ingesting oplogs to a columnar database allows you to query, analyze and monitor your app in a modern and performant way.
3. **Standardized**: No more mess and inconsistency across your logs. oplog creates a standard for how logs should be written across your code base. Clean code, clean logs.
4. **Production Ready**: Easily create dashboards and monitors on top of logged data.
5. **Lightweight**: oplog is a layer on top of the standard Python logging library. It is easy to integrate and use.
6. **Minimal**: While oplog is rich with metadata, you only log what you need. Creating smaller and more efficient logs.