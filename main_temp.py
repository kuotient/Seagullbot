import os
import sys
import logging

import discord

from .config import Config,ConfigDefaults
from .constants import VERSION as BOTVERSION
from .constants import DISCORD_MSG_CHAR_LIMIT


log = logging.getLogger(__name__)
#logging 라이브러리의 log 출력. 참고 : https://hamait.tistory.com/880

class SeagullBot(discord.Client):
    def __init__(self, config_file=None):

        if config_file is None:
            config_file = ConfigDefaults.options_file

        self.config = Config(config_file)

        log.info('Starting SeagullBot ver.{}'.format(BOTVERSION))

    def _setup_logger(self):
        pass

    async def command_help(self, message, channel, command=None):
        """
        사용법:
            {command_prefix}help [커맨드] 혹은 {command_prefix}도움 [커맨드]

        도움 메세지를 출력합니다.
        커맨드가 명시되면, 그 커맨드의 가이드를 출력합니다.
        커맨드가 명시되지 않았을 경우, 모든 커맨드 목록을 출력합니다.
        """

        self.commands = []
        self.is_all = False


    async def get_command_list