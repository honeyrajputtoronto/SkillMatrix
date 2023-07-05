import os
import random
import sys
import dotenv
import threading
import socket
from django.core.management import execute_from_command_line



def main():
    """Run administrative tasks."""
    dotenv.load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academy_hustlers.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute Django command-line utility
    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
