# general helper file for website content that is dynamically
# generated but relatively unchanging, so "semi-static"

import os
import markdown

cached_resources = {}

cached_changelog = {'content' : None, 'mtime' : None}

def get(resource_name):
    should_load = False
    source_path = os.path.join(os.path.dirname(__file__), 'content', resource_name)
    if not os.path.exists(source_path):
        return None
    current_mtime = os.path.getmtime(source_path)

    if resource_name not in cached_resources:
        should_load = True
    else:
        cached_mtime = cached_resources[resource_name]['mtime']
        if cached_mtime is None or cached_mtime < current_mtime:
            should_load = True

    if should_load:
        with open(source_path, 'r') as infile:
            content = markdown.markdown(infile.read(), extensions=['extra'], output='html5')
        cached_resources[resource_name] = {
            'content' : content,
            'mtime' :current_mtime
            }

    return cached_resources[resource_name]['content']
