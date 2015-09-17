# -*- coding: utf-8 -*-
from contextlib import nested
from fabric.api import task, run, cd, env, settings, hide
from fabric.colors import cyan, green, red, yellow
from fabric.tasks import Task
from fabric.utils import abort

########## Basic tasks
@task
def get_change_list(branch):
    """Get a list of changes between `origin/branch` and `branch`"""
    with hide('running', 'stdout'):
        return run(
            'git diff-index --cached --name-only {branch}'.format(branch=branch)
        ).splitlines()

@task
def fetch_changes():
    """Fetch latest changes to the working branch."""
    remote, branch = env.working_ref.split('/', 1)
    run('git fetch {remote}'.format(remote=remote))


@task
def update_copy():
    """Update the local copy of the repository, getting a list of changes"""
    fetch_changes()
    changed_files = get_change_list(env.working_ref)
    run('git merge {working_ref}'.format(working_ref=env.working_ref))
    return changed_files


########## Continuity decorators

def build_step(build_task):
    @task
    def build(action):
        """Continuity's build step"""
        with cd(env.project_path):
            # Fetch changes from repository and update current branch
            changed_files = update_copy()

            # Check if we have to build.
            if changed_files or action == 'force':
                build_task(changed_files, action)

            return changed_files

    return build

def test_step(test_task):
    @task
    def test():
        """Continuity's test step: checks that the codebase is problem-free"""
        if test_task():
            print green('Changes are problem-free.')
        else:
            abort(red('Changes are not problem-free. Aborting...'))

    return test

def merge_step(push_task):
    @task
    def merge():
        """Continuity's merge and push step"""
        print 'Merging {working_ref} onto {target_ref}'.format(**env)
        with cd(env.project_path):
            remote, branch = target_ref.split('/', 1)
            _, work_branch = working_ref.split('/', 1)
            run('git checkout {branch}'.format(branch=branch))
            run('git merge {working_ref}'.format(working_ref=working_ref))
            run('git push {remote} {branch}'.format(remote=remote, branch=branch))
            run('git checkout {branch}'.format(branch=work_branch))

        push_task()

    return merge

deploy_step = task
