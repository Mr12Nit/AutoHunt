import os
import logSetup

logger = logSetup.log("FileHandler", "fileHandlerLog.txt")

class FileHandler:
    @staticmethod
    def read_file(path):
        """Reads lines from a file, returning a list of non-empty lines."""
        if FileHandler.check_if_file_exist(path):
            try:
                with open(path, 'r') as file:
                    lines = [line.strip() for line in file.readlines() if line.strip()]
                    return lines
            except FileNotFoundError:
                logger.error(f"File not found: {path}")
            except IOError as e:
                logger.error(f"IO error occurred while reading {path}: {e}")
        else:
            logger.error("File does not exist")
        return None  # Return None if the file doesn't exist or can't be read

    @staticmethod
    def make_dir(path):
        """Creates a directory if it does not exist."""
        try:
            os.makedirs(path, exist_ok=True)  # This will not raise an error if the directory exists
            logger.info(f"Directory created or already exists: {path}")
        except OSError as e:
            logger.error(f"Error creating directory {path}: {e}")

    @staticmethod
    def check_if_file_exist(path):
        """Checks if a file exists at the given path."""
        return os.path.isfile(path) if path else False
    
    @staticmethod
    def check_if_dir(dir_path):
        """Checks if a directory exists at the given path."""
        return os.path.isdir(dir_path)

    @staticmethod
    def write_to_file(file_name, data):
        """Writes data to a file. Appends if the file already exists."""
        try:
            with open(file_name, "a") as file:
                if isinstance(data, list):
                    file.write("\n".join(data) + '\n')  # Writing list data
                else:
                    file.write(data + '\n')  # Writing single data entry
            logger.info(f"Data written to file: {file_name}")
        except IOError as e:
            logger.error(f"Error writing to file {file_name}: {e}")
