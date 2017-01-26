#!/usr/bin/env python
import os
import sys
import re
import threading

def read_env():
    """
    Function reads in and sets environment variables that are held in common.env
    Credit to https://gist.github.com/bennylope/2999704
    """
    try:
        with open('common.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

    from django.core.management import execute_from_command_line
    
    read_env()
    execute_from_command_line(sys.argv)

