from invoke import Collection, task

from tasks.common import VENV_PREFIX


@task
def clean(ctx):
    """Remove all the tmp files in .gitignore"""
    ctx.run("git clean -Xdf")


@task
def dist(ctx):
    """Build distribution"""
    ctx.run(f"{VENV_PREFIX} python setup.py sdist bdist_wheel")


@task
def docker(ctx):
    """Build docker image"""
    ctx.run("pipenv lock --keep-outdated --requirements > requirements.txt")
    user_name = "lee_w"
    proj_name = "discord_reaction_to_role_bot"
    repo_name = f"{user_name}/{proj_name}"
    ctx.run(f"docker build -t {repo_name}:latest .")


build_ns = Collection("build")
build_ns.add_task(clean)
build_ns.add_task(dist)
build_ns.add_task(docker)
