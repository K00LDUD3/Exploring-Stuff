import os

class IntegerTracker:
    def __init__(self, file_name):
        self.file_name = file_name
        self.initialize_file()

    def initialize_file(self):
        """Initialize the file with a starting value of 0 if it doesn't exist."""
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as file:
                file.write("0")

    def read_value(self):
        """Read the current integer value from the file."""
        with open(self.file_name, 'r') as file:
            value = int(file.read().strip())
        return value

    def update_value(self, new_value):
        """Update the integer value in the file."""
        with open(self.file_name, 'w') as file:
            file.write(str(new_value))

    def increment_value(self):
        """Increment the integer value by 1 and update the file."""
        current_value = self.read_value()
        new_value = current_value + 1
        self.update_value(new_value)
        return new_value

    def reset_value(self):
        """Reset the integer value to 0 and update the file."""
        self.update_value(0)
        return 0