#!/usr/bin/env python3

import os, json

def get_all_monitors(monitor_root):
    # set initial monitor files
    print(monitor_root)
    monitor_files = []
    all_monitors = []

    # search all .monitor files in monitor_root recursively
    for roots, dirs, files in os.walk(monitor_root):
        for file in files:
            if file.lower().endswith('.monitor'):
                monitor_files.append(os.path.join(roots, file))
    print('\n'.join(monitor_files))


    # read monitor files and add to a list
    for monitor_file in monitor_files:
        # read the file
        with open(monitor_file) as monitor_file_stream:
            # read the file content to monitors variable
            # if not a list then failed
            monitors = ''
            try:
                monitors = json.loads(monitor_file_stream.read())
            except:
                raise Exception('Failed to parse .monitor file for (not valid json format): {}'.format(monitor_file))

            # monitor file is not a list
            if type(monitors) is not list:
                raise Exception('Failed to parse .monitor file for (not a list): {}'.format(monitor_file))
                
            # extedn to all_monitors variable
            else:
                all_monitors.extend(monitors)

    return all_monitors
