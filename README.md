# PickForMe Tool

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#Usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction

**PickForMe** is a command-line tool designed to help users make decisions when faced with multiple options. Whether you're deciding on a place to visit, a sport to play, or a restaurant to dine at, PickForMe assists in managing and selecting from your list of choices.

The tool organizes options into a three-layer hierarchy:
1. **Groups**: Representing different contexts or teams.
2. **Categories**: Representing types of activities within a group.
3. **Activities**: Representing specific options or entries within a category.

## Features

- **Three-layer hierarchy**: Organize your options into groups, categories, and activities.
- **Soft Deletion**: Mark records as deleted without permanently removing them.
- **Database-backed**: Uses SQL databases for data storage and master password management.
- **User-friendly CLI**: Simple command-line interface for managing and selecting options.
- **Secure**: Master password protection for critical operations like deleting data.

## Installation

### Prerequisites

- Python 3.7 or higher
- SQLAlchemy
- prettytable
- colorama

### Steps

1. Install PickForMe from PyPI:
    ```bash
    pip install pickforme
    ```

## Usage

1. Run the application:
    ```bash
    pickforme
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---