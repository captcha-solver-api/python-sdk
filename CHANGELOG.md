# Changelog

All notable changes are documented here.

## [1.3.1] - 2026-11-26

### Documentation

- align example step descriptions
- refresh example comments
- update changelog for v1.3.0

### Maintenance

- set version to 1.3.1

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.3.0...v1.3.1)


## [1.3.0] - 2026-11-19

### Added

- add debug mode

### Fixed

- restore dedicated debug examples
- address debug mode review feedback
- align debug output with JavaScript SDK
- resolve strict type checks
- satisfy lint and security checks

### Documentation

- align example instructions
- expand example usage guides
- restore regular examples after review
- restore coordinates task description
- improve debug examples and usage steps
- update changelog for v1.2.0
- expand debug constructor guidance
- align README with SDK behavior
- support debug flag in all examples
- clarify API key placeholders
- expand example descriptions
- align step comments across examples
- add workflow guides to examples

### Maintenance

- set version to 1.3.0
- set version to 1.2.0
- cover package logger debug configuration

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.2.0...v1.3.0)


## [1.2.0] - 2026-11-18

### Added

- add Yandex SmartCaptcha Kaleidoscope support

### Fixed

- address Kaleidoscope review feedback

### Documentation

- describe Kaleidoscope constructor parameters
- expand Kaleidoscope example guidance
- complete Kaleidoscope README coverage
- update changelog for v1.1.0

### Maintenance

- set version to 1.2.0
- bump actions/setup-python from 5 to 7
- bump softprops/action-gh-release from 2 to 3
- bump actions/upload-artifact from 4 to 7
- bump actions/download-artifact from 4 to 8
- bump actions/checkout from 4 to 7

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.1.0...v1.2.0)


## [1.1.0] - 2026-11-03

### Added

- expose task_id on errors raised after task creation
- retry transient polling failures in solve()
- add Yandex SmartCaptcha image example

### Fixed

- send Yandex image captcha as SmartCaptchaTask
- validate version-specific GeeTest parameters
- tighten validation and document required task parameters
- format async proxyless examples
- validate required task parameters

### Documentation

- replace em dashes in contributor docs
- list https proxy type for Yandex SmartCaptcha
- expand async Image to Text example
- close the async client in every async example
- align task docs and examples after merging main
- add security policy
- split proxy examples into separate files
- explain py.typed marker
- clarify unavailable proxy task variants
- link package metadata to SDK readme
- update changelog for v1.0.4

### Maintenance

- set version to 1.1.0
- drop CodeQL job in favor of default setup
- raise minimum requests and httpx versions
- configure Dependabot for pip and GitHub Actions
- add dependency audit, bandit, and CodeQL checks
- pin test runner for Python 3.9
- run Python matrix on Ubuntu 22.04
- set version to 1.0.5

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.0.4...v1.1.0)


## [1.0.4] - 2026-10-09

### Documentation

- improve editor documentation and usage examples
- update changelog for v1.0.3

### Maintenance

- set version to 1.0.4
- grant discussions write permission for release discussion

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.0.3...v1.0.4)


## [1.0.3] - 2026-10-05

### Fixed

- support user agent for Turnstile Challenge

### Documentation

- add AI integration guide
- link Selenium Python examples
- add useful repository links
- add useful links section
- refresh README banner
- update banner install command
- add coverage badge to README
- use pepy.tech as downloads badge source
- add badges to README

### Maintenance

- set version to 1.0.3
- generate changelog on release
- generate changelog on release
- measure coverage and publish badge to gist
- open a discussion for each GitHub Release
- create GitHub Release on publish
- add mypy strict type checking
- run push trigger on main only to avoid duplicate runs
- describe every workflow job with a short comment
- add ruff lint and format checks

[Full diff](https://github.com/captcha-solver-api/python-sdk/compare/v1.0.2...v1.0.3)


New sections are generated from Conventional Commits when a version tag is published.

## [1.0.2] - 2026-09-18

### Fixed

- Removed the unsupported Yandex image puzzle mode.
- Kept reCAPTCHA v3 support proxyless-only.

## [1.0.1] - 2026-09-17

### Fixed

- Aligned the polling interval with API recommendations.

## [1.0.0] - 2026-09-17

### Added

- Published the initial Python SDK release.
