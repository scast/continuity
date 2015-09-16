# -*- coding: utf-8 -*-
from fabric.api import task, run, cd, env, settings
from fabric.colors import cyan, green, red, yellow
from fabric.tasks import Task
from fabric.utils import abort

def check_setup(func):
    def wrapper(setup, *args, **kwargs):
        if setup is None:
            print yellow('No setup provided for this step, skipping...')
            return

        func(setup, *args, **kwargs)

    return wrapper

@task
def get_change_list(branch):
    with hide('running', 'stdout'):
        return run(
            'git diff-index --cached --name-only {branch}'.format(branch=branch)
        ).splitlines()

@task
@check_setup
def build(setup, action):
    with cd(env.project_path):
        # Fetch latest changes to the working branch.
        remote, branch = env.working_ref.split('/', 1)
        run('git fetch {remote}'.format(remote=remote))
        changed_files = get_change_list(branch)

        # Check if we have to build.
        if changed_files or action == 'force':
            build_env, build_task = setup
            with settings(**build_env):
                build_task(changed_files, action)

        return changed_files


class Continuity(Task):
    def __init__(self, *args, **kwargs):
        super(Continuity, self).__init__(*args, **kwargs)
        self._environments = {}

    def bootstrap(self, environment_name, working_ref, target_ref, deploy_setup,
                  build_setup=None, test_setup=None, merge_setup=None):
        self._environments[environment_name] = {
            'name': environment_name,
            'working_ref': working_ref,
            'target_ref': target_ref,
            'deploy_setup': deploy_setup,
            'build_setup': build_setup,
            'test_setup': test_setup,
            'merge_setup': merge_setup
        }

    def run(self, environment, action='check'):
        if environment not in self._environments:
            abort(red('Unknown environment: {}'.format(environment)))

        environment = self._environments[environment]
        print green('Starting Continuity\'s integration and deploy process')

        with settings(**environment):
            print '1. Building.'
            changed_files = build(env.build_setup, action)

            if not changed_files or action != 'force':
                return

        print green('Continuity process finished!')