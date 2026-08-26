# Primers for additional rs-files-templates files

These GitHub-facing files are reusable across language templates and are good
candidates for `rs-files-templates`. Keep language package code, language test
implementations, documentation-builder configuration, container recipes, and
language environment setup in the repository generator.

For every model below:

- use `FileTemplateModel` or `rsm_template_base` with `extra="forbid"`;
- render through the package `StrictUndefined` environment;
- use concise NumPy-style module and function docstrings;
- test model validation, exact output paths, YAML parsing where applicable,
  conditional sections, and a trailing newline;
- export the model from `rs_files_templates.models` and document it in the API
  inventory.

## Pull request template

- **Output:** `.github/pull_request_template.md`
- **Suggested model:** `PullRequestTemplateModel`
- **RSM fields:** `documentation_types`, `include_metadata`, `test_types`
- **Content:** summary prompts, Conventional Commit title reminder, focused
  review checklist, conditional metadata/docs/tests checks, CI status, secrets
  and sensitive-data check, and commands run or skipped.
- **Source to migrate:** `_cc_shared/.github/pull_request_template.md`
- **Important behavior:** omit checklist items for artifacts the project does
  not generate. The consumer decides whether the file itself is selected by
  `community_files`.

## Bug report issue form

- **Output:** `.github/ISSUE_TEMPLATE/bug_report.yml`
- **Suggested model:** `BugReportIssueFormModel`
- **RSM fields:** none required for the initial static form.
- **Content:** existing-issue confirmation, summary, expected behavior, minimal
  reproduction, environment, additional context, and a public-data warning.
- **Source to migrate:** `_cc_shared/.github/ISSUE_TEMPLATE/bug_report.yml`
- **Validation:** parse as YAML and require unique body `id` values and all
  required GitHub issue-form top-level keys.

## Feature request issue form

- **Output:** `.github/ISSUE_TEMPLATE/feature_request.yml`
- **Suggested model:** `FeatureRequestIssueFormModel`
- **RSM fields:** none required for the initial static form.
- **Content:** existing-request confirmation, problem or need, proposed
  solution, alternatives, expected impact, and a public-data warning.
- **Source to migrate:** `_cc_shared/.github/ISSUE_TEMPLATE/feature_request.yml`
- **Validation:** apply the same structural checks as the bug report form.

## Issue template configuration

- **Output:** `.github/ISSUE_TEMPLATE/config.yml`
- **Suggested model:** `IssueTemplateConfigModel`
- **RSM fields:** `support_routes`, `urls`
- **Content:** disable blank issues, add the documentation URL when present,
  and add distinct public support routes as contact links.
- **Source to migrate:** `_cc_shared/.github/ISSUE_TEMPLATE/config.yml`
- **Important behavior:** remove duplicate documentation routes and omit
  `contact_links` entirely when no valid URLs are available.

## Dependabot configuration

- **Output:** `.github/dependabot.yml`
- **Suggested model:** `DependabotModel`
- **RSM fields:** `programming_languages`, `project_manager`
- **Content:** always update pinned GitHub Actions; add only package ecosystems
  that can be derived confidently from the selected manager or languages.
- **Source to migrate:** `_cc_shared/.github/dependabot.yml`
- **Important behavior:** keep weekly grouped updates, deduplicate ecosystems,
  and do not guess an ecosystem for unsupported managers. A small package-local
  mapping is preferable to exposing generator-private fields.

## Metadata validation workflow

- **Output:** `.github/workflows/metadata.yml`
- **Suggested model:** `MetadataWorkflowModel`
- **RSM fields:** `include_metadata`
- **Content:** read-only permissions, push and pull-request triggers,
  concurrency cancellation, a job timeout, checkout, and the immutable
  `LUMC-DCC/rs-metadata` action reference.
- **Source to migrate:** `_cc_shared/.github/workflows/metadata.yml`
- **Important behavior:** the consumer omits this file when metadata is not
  selected. Keep action references in one tested constants module so automated
  dependency updates can refresh them.

## Changelog validation command

- **Output:** `tools/check_changelog.py`
- **Suggested model:** `ChangelogCheckModel`
- **RSM fields:** none required.
- **Content:** validate Keep a Changelog headings, release dates, Unreleased
  ordering, and reference labels without deciding whether a change deserves an
  entry.
- **Source to migrate:** `_cc_shared/tools/check_changelog.py`
- **Important behavior:** keep the validator importable for unit tests and the
  `main()` function usable by CI. Test valid, missing, malformed, and yanked
  release headings.

## Changelog validation workflow

- **Output:** `.github/workflows/changelog.yml`
- **Suggested model:** `ChangelogWorkflowModel`
- **RSM fields:** `community_files`
- **Content:** read-only permissions, push and pull-request triggers,
  concurrency cancellation, a job timeout, Python setup, and execution of the
  generated changelog checker.
- **Source to migrate:** `_cc_shared/.github/workflows/changelog.yml`
- **Important behavior:** the consumer emits both the checker and workflow only
  when `CHANGELOG.md` is selected.

## Security workflow

- **Output:** `.github/workflows/security.yml`
- **Suggested model:** `SecurityWorkflowModel`
- **RSM fields:** `programming_languages`, `security_measures`
- **Content:** dependency review on pull requests and scheduled CodeQL analysis
  for languages supported by CodeQL, with minimal permissions, concurrency,
  timeouts, and immutable action references.
- **Source to migrate:**
  `python/{{cookiecutter.project_slug}}/.github/workflows/security.yml`
- **Important behavior:** emit only when vulnerability scanning is selected;
  map controlled language names to CodeQL identifiers; omit unsupported
  languages rather than guessing; omit the CodeQL job when no selected language
  is supported while retaining dependency review.

## Suggested migration order

1. Pull request and issue templates.
2. Metadata and changelog workflow bundle.
3. Dependabot configuration.
4. Security workflow after the language-to-CodeQL mapping is agreed.

After each upstream release, replace the matching sync-map entries or local
templates here with package rendering and keep one generation-level integration
test per migrated file family.
