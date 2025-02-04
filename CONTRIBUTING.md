# Contributing to Oracle MCP

First off, thank you for considering contributing to Oracle MCP! It's people like you that make Oracle MCP such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. **Check Existing Issues** - Check if the bug has already been reported.
2. **Collect Information** - Include:
   - Your OS and Python version
   - Steps to reproduce the issue
   - Expected behavior
   - Actual behavior
   - Any relevant logs or screenshots
3. **Create an Issue** - Use the bug report template.

### Suggesting Enhancements

1. **Check Existing Issues** - Check if the enhancement has been suggested.
2. **Provide Context** - Explain why this enhancement would be useful.
3. **Be Detailed** - Include:
   - Step-by-step description of the suggested enhancement
   - Specific examples of how it would be used
   - References to other similar features if applicable

### Pull Requests

1. **Fork the Repository**
2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
   - Follow the coding style
   - Add tests if applicable
   - Update documentation
4. **Run Tests**
   ```bash
   pytest
   ```
5. **Commit Your Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/)
6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/adityasugandhi/oracle_mcp.git
   cd oracle_mcp
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Create .env file:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Coding Style

- Follow PEP 8
- Use [Black](https://github.com/psf/black) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Add type hints
- Write docstrings for functions and classes

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update API documentation
- Include examples for new features

## Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code restructuring
- `test:` for adding tests
- `chore:` for maintenance

Example:
```
feat(api): add new endpoint for system status

- Add GET /api/v1/status endpoint
- Include system metrics in response
- Add tests for the new endpoint

Closes #123
```

## Questions?

Feel free to contact the maintainers or create an issue for questions.