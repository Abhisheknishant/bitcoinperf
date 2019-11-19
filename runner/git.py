import os
import shutil
import shlex
import subprocess
import typing as t
from pathlib import Path

from . import sh, config
from .logging import get_logger

logger = get_logger()


GitCheckout = t.NamedTuple('GitCheckout', [
    # e.g. "HEAD"
    ('ref', str),
    # e.g. "e59c59c7befdbb0a600b557f05f009c03f98c2c8"
    ('sha', str),
    # Used to verify cache correctness later on.
    ('commit_msg', str),
])

BITCOIN_URL_TEMPLATE = 'https://github.com/{}/bitcoin.git'


def checkout_in_dir(
        cfg: config.Config, target: config.Target, git_path: Path) \
        -> GitCheckout:
    """Given a path to a repository, cd to it and checkout a specific ref."""
    git_cache_path = cfg.bitcoinperf_home_path() / 'bitcoin.cached.git'

    copy_from_path = None
    if cfg.cache_git and git_cache_path.exists():
        copy_from_path = git_cache_path

    if not git_path.exists():
        if copy_from_path:
            logger.info(
                "Copying bitcoin repo from local path %s", copy_from_path)
            shutil.copytree(copy_from_path, git_path)
        else:
            url = BITCOIN_URL_TEMPLATE.format('bitcoin')
            logger.info("Cloning bitcoin repo from url %s", url)
            sh.run("git clone {} {}".format(url, git_path))

    if cfg.cache_git and not git_cache_path.exists():
        shutil.copytree(git_path, git_cache_path)

    os.chdir(git_path)
    sh.run('echo \'[remote "upstream-pull"]\'                                  >> .git/config')
    sh.run('echo \'        fetch = +refs/pull/*:refs/remotes/upstream-pull/*\' >> .git/config')
    sh.run('echo \'        url = https://github.com/bitcoin/bitcoin\'          >> .git/config')
    new_remote = target.gitremote
    if new_remote:
        sh.run("git remote add {} https://github.com/{}/bitcoin.git"
               .format(new_remote, new_remote),
               check_returncode=False)
    sh.run('git fetch --all')

    sh.run("git checkout origin/master".format(new_remote))
    # Delete the branch if it exists - might be old
    if target.gitref != 'origin/master':
        sh.run("git branch -D {}".format(target.gitref),
               check_returncode=False)
    sh.run("git fetch --all")
    sh.run("git checkout {}".format(target.gitref))
    sh.run("git pull {} {}".format(target.gitremote, target.gitref))

    gitsha = get_sha('HEAD')

    sh.run("git config user.email 'bench@bitcoinperf.com'")
    sh.run("git config user.name 'Bitcoinperf'")
    if target.gitref not in ('master', 'origin/master') and target.rebase:
        sh.run('git merge origin/master')
        logger.info("Merged %s (%s) with master (%s)",
                    target.gitref, gitsha, get_sha('origin/master'))

    co = GitCheckout(
        ref=target.gitref, sha=gitsha, commit_msg=get_commit_msg('HEAD'))
    logger.info("Checked out {}".format(co))

    return co


def get_sha(ref: str) -> str:
    return subprocess.check_output(
        shlex.split('git rev-parse {}'.format(ref))).strip().decode()


def get_commit_msg(ref: str) -> str:
    return subprocess.check_output(
        shlex.split('git log -1 --pretty=%B {}'.format(ref))).strip().decode()
