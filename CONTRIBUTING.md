# Contributing

I welcome all contributions to the `topologyx` project! By contributing, you help improve the tools and resources available to the community.

## Community Guidelines

1. Be respectful and considerate in your interactions.
2. Provide constructive feedback.
3. Be open to feedback on your contributions.

## How to Contribute

### Reporting Bugs

If you find a bug in the project, please create an issue on GitHub with detailed information about the bug, how to reproduce it, and any relevant screenshots or logs.

### Suggesting Enhancements

If you have an idea for an enhancement or new feature, please create an issue on GitHub with a detailed description of the enhancement, the motivation behind it, and any potential implementation ideas.

### Pull Requests

1. **Fork the Repository**: Create a personal fork of the project on GitHub.
2. **Clone Your Fork**: Clone your fork to your local machine.
3. **Create a Branch:** Create a new branch for your feature or bug fix.
4. **Make Changes:** Make your changes to the codebase.
5. **Commit Changes:** Commit your changes with a clear and descriptive commit message.
6. **Push Changes:** Push your changes to your fork.
7. **Create Pull Request:** Create a pull request from your forked repository to the main repository, describing your changes in detail.

## IDE Recommendations

I recommend working with VSCode, an IDE that does not need to be presented. Internally, I use a set of code extensions enabling a minimum of code standardization, making the life of many developers more enjoyable. Those extensions are given in `.vscode/extensions.json`, and can be downloaded directly via the VSCode extension store. This goes hand and hand with properly configured VSCode workspace settings, available in `.vscode/settings.json`.

## Code Quality

### Return Statements:

A comment that will come back often in PR reviews is the spacing in your code. The overall strategy is to split your code by functional blocks, aka adding empty lines to differentiate loops, if-statements or clusters of similar actions. There are also a few more guidelines:

1. Return statements should be isolated from any code blocks
2. Do not use spacing between a function name and the first line of code

An application of those guidelines is illustrated below:

```python
# do
def function():
  return object

# don't
def function():

  return object

# do
def function():
  object = get_object()

  return object

# don't
def function():
  object = get_object()
  return object
```

### Assert Statements:

The guidelines are the same for `assert` statements than they are for `return` statements.

### Helpers:

I use Python 3.13 so make sure to install a clean venv environment depending on a 3.13.\* version. I rely on [uv](https://docs.astral.sh/uv/) for environment and package management.

I use some packages to help with code quality, those are:

- [ruff](https://docs.astral.sh/ruff/) configured in `pyproject.toml` for linting and formatting
- [ty](https://docs.astral.sh/ty/) configured in `pyproject.toml` for type checking

### Pre-commit Hooks:

This project uses pre-commit hooks to ensure code quality before each commit. After cloning the repository, run:

```bash
make setup
```

This will install all dependencies and set up the pre-commit hooks, including:

- Trailing whitespace removal
- End of file fixer
- YAML/TOML syntax checking
- Ruff formatting and linting
- Commitizen for conventional commit messages

### Naming Conventions:

"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

That is exactly why it is important everyone follow guidelines regarding naming conventions, especially when moving quickly as a team. Here are a set of rules that will most likely guide you through any problem you would face:

1. Do not use abbreviations
2. Use at least 2 words for function names
3. Boolean variables should be inferred from their name (e.g. start with `is_` or `has_`)
4. Use `snake_case` for folder names, function names
5. Use `PascalCase` for class names
6. Use `SCREAMING_SNAKE_CASE` for constants
7. Use `_` prefix for private functions

### Typing:

Typing is key to maintainability. It will increase the readability of the code, but will also passively document your code. Finally, type checking will help to find some obvious bugs.

I rely on dynamic typing via [Pydantic](https://pydantic-docs.helpmanual.io/) and use static typing via VSCode for now. To enable static typing, ensure that you are using the VSCode extension [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

Static typing is handled via the help of [ty](https://docs.astral.sh/ty/) from Astral.

## Git Conventions

### Branches:

I have a simple convention for branch naming: `{initials}/{descriptive-kebab-case}`. Keep them all lowercase. For John Doe working on a feature A, that would be `jd/feature-a`.

### Commits:

The Conventional Commits specification is a light convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages. Learn more [here](https://www.conventionalcommits.org/en/v1.0.0/).

Pre-commit hooks enforce conventional commits via [commitizen](https://commitizen-tools.github.io/commitizen/).
