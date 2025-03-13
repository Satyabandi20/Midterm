# Midterm Project

# Advanced Python Utility Application

## Project Overview

This project is aimed at developing a versatile Python-based utility application. It is designed with modern software development practices in mind, focusing on modular architecture, maintainable code, comprehensive logging, dynamic configuration using environment variables, efficient data handling with Pandas, and a command-line interface (REPL) for interactive user interaction.

## Features

1. **Interactive REPL Interface**  
   The application features a Read-Eval-Print Loop (REPL) interface, allowing users to execute commands and see results immediately.

2. **Modular Plugin System**  
   The application supports dynamically loading utility modules (plugins), making it easy to extend functionality without changing the core codebase.

3. **Data and History Management**  
   Uses Pandas to manage data processing history, including executed commands and output results. Supports exporting history to multiple formats such as CSV, Excel, and more.

4. **Logging**  
   Utilizes Python's built-in logging module to capture and manage detailed logs at various levels (DEBUG, INFO, WARNING, ERROR). The logging configuration is customizable through environment variables.

5. **Design Patterns Implemented**  
   - **Facade Pattern**: Provides a simplified interface for complex subsystems, making the calculator easier to use and maintain.
   - **Command Pattern**: Encapsulates calculation requests as objects, supporting undo/redo operations.
   - **Factory Method**: Creates calculation operation instances, allowing easy extension for new operation types.
   - **Singleton Pattern**: Ensures that only one instance of certain classes (e.g., logging manager) exists.
   - **Strategy Pattern**: Allows different calculation strategies to be defined independently and dynamically switched during runtime.

6. **Testing and Code Quality**:
   - Achieves 100% test coverage with Pytest.
   - Adheres to PEP 8 standards, with code quality verified by Pylint.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual environment (`venv`)
- Git

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd <repository-folder>
2. **Create and Activate a Virtual Environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Set Up Environment Variables**:
    Create a .env file in the root folder and add the following:
    makefile
   ```bash
   ENVIRONMENT=Production
   LOG_LEVEL=INFO
   LOG_FILE=logs/application.log

### Running the Application
- **Command-Line Interface (REPL)**
   ```bash
   python main.py repl
- a) Use commands like `add 5 3`, `subtract 8 4`, or `multiply 2 3` to perform calculations.
- b) Type `menu` to see all available commands.
- c) Use `history` to view the calculation history.
- d) try `clear_history` to clear the history.
- e) Commands like `save_history <filename>` and `load_history <filename>` allow managing history.
- f) `delete_history <index>` helps you to delete a particular operation in history.

## Testing the Application
- Run the following command to test the application with coverage:
    ```bash
    pytest --cov=app --cov-report=term-missing

### Design Patterns
1. **Command Pattern**
Each arithmetic operation is encapsulated as a separate class implementing a shared interface (Command), promoting flexibility and separation of concerns.
2. **Facade Pattern**
Provides a simplified interface for complex Pandas operations related to history management, such as filtering, loading, and saving history.
3. **Factory Method Pattern**
Dynamically loads commands from the plugins directory without modifying the core code, promoting an open/closed design principle.
4. **Singleton Pattern**
Ensures a single instance of certain classes like PandasFacade for managing calculation history.
5. **Strategy Pattern**
Allows different calculation strategies to be defined independently and dynamically switched during runtime.

## Environment Variables

The application uses environment variables to dynamically configure its settings. These can be set in a `.env` file for flexibility across different deployment environments.

- **LOG_LEVEL**: Specifies the logging level (e.g., INFO, WARNING, ERROR).
- **LOG_FILE**: Specifies the file path for log output.
- **ENVIRONMENT**: Specifies the environment.

## Logging Configuration

The log level (`LOG_LEVEL`) and log file location (`LOG_FILE`) can be set in a `.env` file, demonstrating flexibility in setting logging behavior based on deployment or testing environments.

### Example Usage in Code
     import os
     import logging
    
     def configure_logging(log_level=None):
        log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()
        log_file = os.getenv("LOG_FILE", "logs/application.log")
        # Logging configuration setup code here

## Logging

The application uses the `logging` module to capture different levels of log messages:

- **INFO**: Logs regular application operations (e.g., calculation results).
- **DEBUG**: Logs deeper insights for debugging.
- **WARNING**: Logs unexpected but recoverable situations.
- **ERROR**: Logs errors and exceptions for debugging purposes.

### Example Usage

    ```python
    try:
        result = operation_function.execute(num1, num2)
        logging.info(f"Calculated result: {result}")
    except DivisionByZero as e:
        logging.error("Attempted to divide by zero.")
        print("Error: Division by zero.")

## Error Handling

- **Look Before You Leap (LBYL)**: Used when loading configuration settings from environment variables to check for their existence before using them.
- **Easier to Ask for Forgiveness than Permission (EAFP)**: Uses `try-except` blocks to handle exceptions, such as invalid operations or division by zero.

### Error Handling Example

    ```python
    try:
        result = command.execute(num1, num2)
    except DivisionByZero as e:
        logging.error("Division by zero error.")
        print("Cannot divide by zero.")

## Testing

- **Pytest**: Achieves almost 100% coverage.
  - Includes unit tests for all arithmetic operations, calculation history management, and error handling.

## Code Quality

- Verified by **Pylint** for adherence to PEP 8 standards.

## Development Practices

- **Version Control**: Commits are logically grouped, following best practices for Git workflows.


## Video Demonstration


---

This README covers the essential details required to understand, set up, and run the Advanced Python Calculator project. For more information, refer to the source code and documentation in the repository.

---