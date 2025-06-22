#core.py
from command.program_launcher import execute_program_by_name

def handle_command(command_text):
    success = execute_program_by_name(command_text)
