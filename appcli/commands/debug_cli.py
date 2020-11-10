#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Common debug tasks.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# standard library
from appcli.variables_manager import VariablesManager

# vendor libraries
import click


# local libraries
from appcli.models.cli_context import CliContext
from appcli.models.configuration import Configuration
from pprint import pprint

# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------


class DebugCli:
    def __init__(self, configuration: Configuration):
        self.cli_configuration: Configuration = configuration

        self.app_name = self.cli_configuration.app_name

        # ------------------------------------------------------------------------------
        # CLI METHODS
        # ------------------------------------------------------------------------------

        @click.group(
            hidden=True, invoke_without_command=True, help="Common debugging tasks."
        )
        @click.pass_context
        def debug(ctx):
            if ctx.invoked_subcommand is not None:
                # subcommand provided
                return

            click.echo(ctx.get_help())

        @debug.command(
            help="Prints debug information about the current cli context, configuration, and settings.",
        )
        @click.pass_context
        def info(ctx):
            cli_context: CliContext = ctx.obj
            app_config_file = cli_context.get_app_configuration_file()
            variables_manager = VariablesManager(app_config_file)

            print()
            print("=== CLI CONTEXT ===")
            pprint(cli_context)

            print()
            print("=== CONFIGURATION ===")
            pprint(self.cli_configuration)

            print()
            print("=== ORCHESTRATOR CONFIGURATION ===")
            pprint(vars(self.cli_configuration.orchestrator))

            print()
            print("=== VARIABLES ===")
            pprint(variables_manager.get_all_variables())

        # Expose the commands
        self.commands = {"debug": debug}
