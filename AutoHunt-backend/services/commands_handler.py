import subprocess
from typing import Tuple
from services.log_setup import setup_logger
import shutil  # Built into Python and requires no external dependencies - cross-platform

logger = setup_logger("CommandsHandler", "log.txt")

class CommandsHandler:
    """
    A Class to handle command execution in a clean and reusable manner.

    Methods:
        execute_command(command): Executes a shell command and returns output.
        check_command_success(return_code): Checks if a command was successful.
        is_tool_installed(tool_name): Checks if a tool is installed on the system.
    """

    @staticmethod
    def execute_command(command: list) -> Tuple[int, str, str]:
        """
        Executes a shell command and returns the output.

        Args:
            command (list): The shell command to execute as a list of arguments.

        Returns:
            Tuple[int, str, str]: A tuple containing the return code, standard output, and standard error.
        """
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}, Return code: {e.returncode}")
            return e.returncode, e.output, e.stderr
        except FileNotFoundError:
            logger.error("Command not found. Ensure the tool is installed and available in the system PATH.")
            return -1, "", "Command not found."

    @staticmethod
    def check_command_success(return_code: int) -> bool:
        """
        Checks if the command was successful based on the return code.

        Args:
            return_code (int): The return code from the command execution.

        Returns:
            bool: True if the command was successful, False otherwise.
        """
        if return_code == 0:
            return True
        else:
            logger.warning(f"Command failed with return code: {return_code}")
            return False

    @staticmethod
    def is_tool_installed(tool_name: str) -> bool:
        """
        Checks if a tool is installed on the system.

        Args:
            tool_name (str): The name of the tool to check.

        Returns:
            bool: True if the tool is installed, False otherwise.
        """
        if shutil.which(tool_name):
            logger.info(f"Tool '{tool_name}' is installed.")
            return True
        else:
            logger.warning(f"Tool '{tool_name}' is not installed.")
            return False
