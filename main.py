import multiprocessing
import sys
import importlib
import os
from decimal import Decimal, InvalidOperation
from collections import OrderedDict
import logging
import logging.config
import pandas as pd
from dotenv import load_dotenv
from calculator.calculations import Calculations
from calculator.calculation import Calculation
from logger_config import configure_logging

# Load environment variables
def load_environment_variables():
    load_dotenv()
    settings = {key: value for key, value in os.environ.items()}
    logging.info("Environment variables loaded.")
    return settings


# Load plugins dynamically
def load_plugins():
    commands = OrderedDict()
    plugins_dir = os.path.join('calculator', 'plugins')
    
    if not os.path.exists(plugins_dir):
        logging.warning(f"Plugins directory not found: {plugins_dir}")
        return commands
    
    for filename in os.listdir(plugins_dir):
        if filename.endswith('_command.py'):
            try:
                module_name = filename[:-3]  
                module = importlib.import_module(f'calculator.plugins.{module_name}')
                command_class = getattr(module, module_name[:-8].capitalize() + 'Command')
                commands[module_name[:-8]] = command_class()
                logging.info(f"Loaded plugin: {module_name}")
            except (ImportError, AttributeError) as e:
                logging.error(f"Failed to load plugin {module_name}: {e}")

    return commands

# Decorator for logging execution
def log_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

@log_execution
def calculate_and_display_result(value1, value2, operation_key, operations_dict, enable_multiprocessing=False):
    logging.debug(f"Initiating computation: {value1} {operation_key} {value2}")
    
    try:
        # Convert input values to Decimal for precise computation
        num1_decimal, num2_decimal = map(Decimal, [value1, value2])
        
        # Retrieve the operation from the dictionary
        operation_handler = operations_dict.get(operation_key)
        
        if not operation_handler:
            logging.warning(f"Operation '{operation_key}' is not recognized.")
            print(f"Unknown operation type: {operation_key}")
            return
        
        # Handle multiprocessing if enabled
        if enable_multiprocessing:
            logging.debug("Multiprocessing enabled. Executing in a separate process.")
            
            result_holder = multiprocessing.Queue()
            process_instance = multiprocessing.Process(
                target=operation_handler.execute_multiprocessing,
                args=(num1_decimal, num2_decimal, result_holder)
            )
            process_instance.start()
            process_instance.join()

            if not result_holder.empty():
                final_result = result_holder.get()
                logging.info(f"Multiprocessing result for {operation_key}: {final_result}")
                print(f"The result of {value1} {operation_key} {value2} (multiprocessing) is {final_result}")
            else:
                logging.error("No result retrieved from multiprocessing queue.")
                print("Error: Multiprocessing computation failed.")
        
        # Handle normal execution
        else:
            final_result = operation_handler.execute(num1_decimal, num2_decimal)
            logging.info(f"Result for {operation_key}: {final_result}")
            print(f"The result of {value1} {operation_key} {value2} is {final_result}")
        
        # Record the calculation in history
        calc_record = Calculation(num1_decimal, num2_decimal, operation_handler)
        result_from_record = calc_record.operate()
        Calculations.add_calculation(calc_record)
        
        logging.debug("Calculation successfully saved to history.")
    
    except InvalidOperation:
        logging.error(f"Invalid numeric input received: {value1}, {value2}")
        print(f"Invalid input detected. '{value1}' or '{value2}' is not a valid number.")
    
    except Exception as error:
        logging.error(f"An unexpected error occurred: {error}")
        print(f"An error occurred during computation: {error}")



# Run the REPL interface
@log_execution
def run_repl(commands):
    """
    Run the REPL (Read-Eval-Print Loop) for interactive calculations.
    """
    print("Entering REPL mode. Type 'exit' to quit.")
    print("Add 'mp' at the end of a command to use multiprocessing.")
    
    while True:
        user_input = input("Enter command: ")
        if user_input == 'exit':
            print("Exiting REPL mode...")
            break
        elif user_input == 'menu':
            print("Available Commands:")
            for cmd_name in commands:
                print(f"- {cmd_name}")
            continue
        elif user_input == 'history':
            history_df = Calculations.get_all_calculations()
            if history_df.empty:
                print("No calculations in history.")
            else:
                print(history_df)
            continue
        elif user_input == 'clear_history':
            Calculations.clear_history()
            print("History cleared.")
            continue
        elif user_input.startswith('save_history'):
            _, filepath = user_input.split(maxsplit=1)
            Calculations.save_history(filepath)
            print(f"History saved to {filepath}.")
            continue
        elif user_input.startswith('load_history'):
            _, filepath = user_input.split(maxsplit=1)
            if os.path.exists(filepath):
                Calculations.load_history(filepath)
                print(f"History loaded from {filepath}.")
            else:
                print(f"File not found: {filepath}")
            continue
        elif user_input == 'latest':
            # Display the latest calculation
            latest_calculation = Calculations.get_latest()
            if latest_calculation:
                print(f"Latest calculation: {latest_calculation}")
            else:
                print("No calculations in history.")
            continue
        elif user_input.startswith('delete_history'):
            try:
                _, index_str = user_input.split(maxsplit=1)
                index = int(index_str)
                Calculations.delete_history(index)
            except (ValueError, IndexError):
                print("Usage: delete_history <index>")
            continue
        elif user_input.startswith('filter_with_operation'):
            try:
                _, operation_name = user_input.split(maxsplit=1)
                filtered_df = Calculations.filter_with_operation(operation_name)
                if filtered_df.empty:
                    print(f"No calculations found for operation: {operation_name}")
                else:
                    print(filtered_df)
            except ValueError:
                print("Usage: filter_with_operation <operation_name>")
            continue

        # Handling arithmetic commands
        parts = user_input.split()
        if len(parts) not in [3, 4]:  
            print("Usage: <command> <num1> <num2> [mp]")
            continue

        command_name, num1, num2 = parts[:3]
        use_multiprocessing = len(parts) == 4 and parts[3] == 'mp'

        if command_name not in commands:
            print(f"Unknown command: {command_name}")
            continue

        calculate_and_display_result(num1, num2, command_name, commands, use_multiprocessing)



# Main function
@log_execution
def main():
    """
    Main function to handle command-line arguments and initiate the calculation.
    """
    commands = load_plugins()  

    if len(sys.argv) == 4:  
        _, num1, num2, operation_type = sys.argv
        calculate_and_display_result(num1, num2, operation_type, commands)
        
    elif len(sys.argv) == 5:  
        _, num1, num2, operation_type, mp_flag = sys.argv
        use_multiprocessing = mp_flag == "mp"
        calculate_and_display_result(num1, num2, operation_type, commands, use_multiprocessing)
    
    elif len(sys.argv) == 2 and sys.argv[1] == 'repl':  
        run_repl(commands)
        
    else:
        print("Usage: python main.py <number1> <number2> <operation> [mp] or python main.py repl")

# Entry point
if __name__ == '__main__':
    settings = load_environment_variables()
    log_level = settings.get("LOG_LEVEL", "INFO").upper()
    configure_logging(log_level=log_level)
    logging.info(f"Environment: {settings.get('ENVIRONMENT')}")
    logging.info("Application started.")
    main()