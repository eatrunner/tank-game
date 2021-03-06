#!/usr/bin/env python

## @file manage.py
#  @brief Django run script

import os
import sys
sys.path.append(sys.path[0] + '/../game/')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
