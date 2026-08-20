# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/).
{% if cookiecutter.versioning_scheme -%}
This project uses {{ cookiecutter.versioning_scheme }} for versions.
{% if cookiecutter.versioning_scheme_details -%}
Policy details: {{ cookiecutter.versioning_scheme_details }}
{% endif -%}
{% endif %}

{% if cookiecutter.release_frequency -%}
Expected release cadence: {{ cookiecutter.release_frequency }}

{% endif -%}
{% if cookiecutter.distribution_channels.entries -%}
Release channels:

{% for channel in cookiecutter.distribution_channels.entries -%}
- {{ channel }}
{% endfor %}

{% endif -%}
## [Unreleased]

### Added

- Initial project scaffold.

### Changed

### Deprecated

### Removed

### Fixed

### Security

{% if cookiecutter.repository_url -%}
[Unreleased]: {{ cookiecutter.repository_url }}/compare/v{{ cookiecutter.version }}...HEAD
{% endif -%}
