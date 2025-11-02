# Contributing to PRsToText

Thank you for your interest in contributing to PRsToText! This is a simple, niche tool, but we welcome contributions that improve its functionality or usability.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/lmichaelwar/PRsToText/issues) section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your Python version and OS

### Submitting Changes

1. **Fork the repository**

2. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Keep changes focused and minimal
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**:
   ```bash
   python prs_to_text.py
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Add: brief description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** with:
   - Clear description of changes
   - Reference to any related issues
   - Examples of usage (if applicable)

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Keep functions focused on a single task
- Add docstrings for new functions

## Ideas for Contributions

- Add support for filtering PRs by label, author, or date range
- Implement pagination to fetch more than 100 PRs
- Add output format options (JSON, CSV, Markdown)
- Create additional example scripts
- Improve error handling and user feedback
- Add unit tests
- Enhance the GitHub Pages documentation

## Questions?

Feel free to open an issue with the "question" label if you need clarification on anything.

## Code of Conduct

Be respectful and constructive in all interactions. We're here to build something useful together!
