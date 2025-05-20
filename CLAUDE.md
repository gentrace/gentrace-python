# Claude Guidelines for gentrace-python

## Project Overview
gentrace-python is a Python SDK for the Gentrace API, which provides tools for evaluating and monitoring AI applications.

## Code Style Guidelines
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Maintain consistent indentation (4 spaces)
- Use meaningful variable and function names
- Add docstrings for public APIs
- Follow the existing error handling patterns

## Testing Requirements
- Write unit tests for new functionality using pytest
- Ensure all tests pass before submitting PRs
- Maintain or improve test coverage

## PR Guidelines
- Keep PRs focused on a single feature or bug fix
- Include clear descriptions of changes
- Reference related issues
- Update documentation as needed

## Commit Message Format
- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

## Dependencies
- Minimize adding new dependencies
- Prefer well-maintained, widely-used packages
- Consider compatibility with different Python versions

## Security Considerations
- Never expose API keys or sensitive information
- Follow secure coding practices
- Validate user inputs

## Documentation
- Update README.md for significant changes
- Document new features and APIs
- Keep code comments up-to-date

## Performance
- Consider performance implications of changes
- Avoid unnecessary computations or memory usage

