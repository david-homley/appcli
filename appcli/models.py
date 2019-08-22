#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

from types import LambdaType, FunctionType
from typing import NamedTuple, List
from pathlib import Path

class ConfigSetting(NamedTuple):
    path: str
    message: str
    validate: LambdaType = lambda _, x: True

class ConfigSettingsGroup(NamedTuple):
    title: str
    settings: List[ConfigSetting]

class ConfigCli(NamedTuple):
    settings_groups: List[ConfigSettingsGroup]

class Configuration(NamedTuple):
    app_name: str
    docker_image: str
    seed_dir: Path
    #apply_configuration_settings_callback: FunctionType
    #config_cli: ConfigCli
    #pre_configuration_callback: FunctionType = lambda *a, **k: None

class CliContext(NamedTuple):
    configuration_dir: Path
    generated_configuration_dir: Path
    data_dir: Path
    subcommand_args: tuple
