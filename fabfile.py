from contextlib import contextmanager
from fabric.api import env, run, task, local

from continuity import continuity

env.project_name = 'continuity'
env.user = 'continuity'
env.repository = 'git@git.talpor.com:continuity.git'
env.project_path = '/Users/scb/Projects/talPor/continuity'

def build_settings():
    return {
        'some_setting': True
    }

def build_task():
    print 'FROM THE BUILD TASK!'

continuity.bootstrap('dev',
                     working_ref='origin/development',
                     target_ref='origin/master',
                     build_setup=(build_settings(), build),
                     deploy_setup=None
)
