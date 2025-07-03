# Contributing to WhisperLite

Thank you for your interest in contributing to WhisperLite! We welcome contributions from everyone. This guide outlines the process for contributing to the project, from reporting bugs to submitting new features.

## How to Contribute

### 1. Reporting Bugs

If you encounter a bug, please [open an issue](https://github.com/aporb/whisperlite/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBug%5D+) on our GitHub repository. When reporting a bug, please include:

-   A clear and descriptive title.
-   A detailed description of the problem, including steps to reproduce it.
-   Information about your operating system and WhisperLite version.
-   Any relevant logs or screenshots.

### 2. Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one, please [open an issue](https://github.com/aporb/whisperlite/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature%5D+) to discuss it. This allows us to provide feedback and ensure that your contribution aligns with the project's goals.

### 3. Submitting a Pull Request

To contribute code or documentation, please follow these steps:

1.  **Fork the repository**: Create your own fork of the WhisperLite repository.
2.  **Create a new branch**: `git checkout -b feature/my-new-feature`
3.  **Make your changes**: Implement your feature or bug fix.
4.  **Commit your changes**: Follow the [commit message format](#commit-message-format) described below.
5.  **Push to your branch**: `git push origin feature/my-new-feature`
6.  **Open a pull request**: Submit a pull request to the `main` branch of the WhisperLite repository. You can use the [Pull Request Template](https://github.com/aporb/whisperlite/compare) for guidance.

## Style Guide

### Python

-   Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
-   Use `black` for code formatting.
-   Use `isort` for import sorting.

### Rust

-   Follow the official [Rust style guide](https://doc.rust-lang.org/1.0.0/style/).
-   Use `rustfmt` for code formatting.

### Markdown

-   Use [GitHub Flavored Markdown](https://github.github.com/gfm/).
-   Use `prettier` for formatting.

## Commit Message Format

We use the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This helps us to automate the release process and generate changelogs.

Each commit message should have the following format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

-   **type**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
-   **scope**: The part of the codebase that the commit affects (e.g., `python`, `rust`, `ui`).
-   **subject**: A concise description of the change.

**Example:**

```
feat(python): add support for custom models

This commit allows users to specify a custom whisper.cpp model file.

Closes #123
```

## Triage Issues

If you are a maintainer, you can help triage issues by:

-   **Labeling issues**: Apply relevant labels (e.g., `bug`, `enhancement`, `good first issue`).
-   **Reproducing bugs**: Confirm that reported bugs are reproducible.
-   **Asking for more information**: If an issue is unclear, ask for more details.

## Propose a Feature

To propose a new feature, please [open an issue](https://github.com/aporb/whisperlite/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature%5D+) with the following information:

-   A clear and descriptive title.
-   A detailed description of the proposed feature and its benefits.
-   Any relevant mockups or design documents.

## Debugging the Hybrid Application

Debugging a hybrid Rust-Python-Tauri application can be challenging. For a detailed guide on debugging, please refer to the [Debugging Guide](DEBUGGING_GUIDE.md).

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.