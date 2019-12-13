#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Handles git repositories for configuration directories for appcli
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# # standard library
import git
from pathlib import Path
from typing import List

# vendor libraries
import click

# local libraries
from appcli.functions import error_and_exit
from appcli.logger import logger
from appcli.models.cli_context import CliContext


# ------------------------------------------------------------------------------
# PRIVATE CLASSES
# ------------------------------------------------------------------------------


class GitRepository:
    """Class which encapsulates different git repo actions for configuration repositories
    """

    def __init__(self, repo_path: str, ignores: List[str] = None):
        self.repo_path = repo_path
        self.ignores = ignores
        self.actor: git.Actor = git.Actor(f"cli_managed", "")

    def init(self):
        """Initialise the git repository, create .gitignore if required, and commit the initial files
        """
        logger.debug("Initialising repository at [%s]", self.repo_path)

        # Confirm that a repo doesn't already exist at this directory
        if self.repo_exists():
            error_and_exit(
                f"Cannot initialise repo at [{self.repo_path}], already exists."
            )

        # git init, and write to the .gitignore file
        repo = git.Repo.init(self.repo_path)
        logger.debug("Repo initialised at [%s]", repo.working_dir)
        if self.ignores:
            ignore_file = open(self.repo_path.joinpath(".gitignore"), "w+")
            for ignore in self.ignores:
                ignore_file.write(f"{ignore}\n")
            ignore_file.close()
            logger.debug("Wrote out .gitignore with ignores: [%s]", self.ignores)
            repo.index.add(".gitignore")

        # do the initial commit on the repo
        repo.index.add("*")
        repo.index.commit("Initialising repository", author=self.actor)
        logger.debug("Initialised repository at [%s].", repo.working_dir)

    def commit_changes(self):
        """Commit the existing changes to the git repository
        """
        # Get the repository (or exit if it doesn't exist)
        try:
            repo = git.Repo(self.repo_path)
        except:
            error_and_exit(f"No git repo found at [{self.repo_path}]")

        # If the repo isn't dirty, don't commit
        if not repo.is_dirty(untracked_files=True):
            logger.info(
                "No changes found in repository [%s], no commit was made.",
                repo.working_dir,
            )
            return

        # Add all files (and optionally the .gitignore if it exists)
        if Path(repo.working_dir).joinpath(".gitignore").exists():
            repo.index.add(".gitignore")
        repo.index.add("*")

        # Get a list of the modified files (added/modified/deleted)
        changed_files = [diff.a_path for diff in repo.index.diff("HEAD")]
        commit_message = (
            input(
                f"Changes to [{changed_files}]. Optional message describing changes: "
            ).strip()
            or "Committing changes."
        )

        commit_message += f"\nChanged files: {changed_files}"
        repo.index.commit(commit_message, author=self.actor)

    def is_dirty(self, untracked_files: bool = False):
        """Tests if the repository is dirty or not. True if dirty, False if not.
        
        Args:
            untracked_files (bool, optional): Whether the check includes untracked files. Defaults to False.
        
        Returns:
            [bool]: True if repository is considered dirty, False otherwise.
        """
        try:
            repo = git.Repo(self.repo_path)
        except:
            error_and_exit(f"No git repo found at [{self.repo_path}]")

        return repo.is_dirty(untracked_files=untracked_files)

    def repo_exists(self):
        """Tests if the underlying repository has been initialised.
        
        Returns:
            [bool]: return True if the repository has been initialised, otherwise False.
        """
        try:
            git.Repo(self.repo_path)
            return True
        except:
            return False


# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------


class ConfigurationGitRepository(GitRepository):
    def __init__(self, cli_context: CliContext):
        super().__init__(cli_context.configuration_dir, [".generated*"])


class GeneratedConfigurationGitRepository(GitRepository):
    def __init__(self, cli_context: CliContext):
        super().__init__(cli_context.generated_configuration_dir)

