import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import discord
import asyncio
import prettytable
from selenium import webdriver
import datetime
from constant import *
import os


async def botutil_help(client, message):
    msg = '\n'
    for i in range(0, len(HELP_LIST)):
        msg += '**' + HELP_LIST[i][0] + '**\n' + HELP_LIST[i][1] + '\n사용법: `' + HELP_LIST[i][2] + '`\n\n'
    embed = discord.Embed(description= msg,
                          color=0x00ff00)
    await client.send_message(message.channel, '***ULTIMATE GUIDES for SEAGULLBOT***')
    await client.send_message(message.channel, embed=embed)


async def botutil_clear(client, message):
    msg_list = []
    async for x in client.logs_from(message.channel, limit=100):
        flag = 0
        for command in COMMAND_LIST:
            if x.content.startswith(command):
                flag = 1
                break

        if x.author.display_name == client.user.name or flag == 1:
            msg_list.append(x)
            if len(msg_list) >= 100:
                break

    for i in range(0, len(msg_list)):
        await client.delete_message(msg_list[i])


#ffmpeg 가 필요하며, ffmpeg 의 bin 폴더를 환경변수 설정해야 합니다.
async def botutil_reaction(argc, argv, client, message):
    # 먼저 이 함수가 호출되면 디렉토리를 스캔해서 리스트를 만든다
    reaction_list = []
    file_list = os.listdir(REACTION_DIR)
    file_list.sort()
    for reaction in file_list:
        if ".mp3" in reaction:
            reaction_list.append(reaction.replace(".mp3", ""))

    # Step 1. 파라미터 갯수 체크
    if argc == 1:
        embed = discord.Embed(title='!리액션 (커맨드)로 리액션을 재생할 수 있습니다.',
                              description='*커맨드 목록*\n```' + str(reaction_list) + '```',
                              color=0xfdee00)
        await client.send_message(message.channel, embed=embed)
        return

    # Step 2. 유효한 커맨드인지 체크
    command = argv[1]
    if command not in reaction_list:
        embed = discord.Embed(title='존재하지 않는 커맨드입니다.',
                              description='*커맨드 목록*\n```' + str(reaction_list) + '```',
                              color=0xfdee00)
        await client.send_message(message.channel, embed=embed)
        return

    # Step 3. 사용자가 음성채팅에 접속해 있는지 체크
    author = message.author
    channel = author.voice_channel
    if channel is None:
        await client.send_message(message.channel, '음성 채팅에 접속해야 이용할 수 있습니다.')
        return

    voice = await client.join_voice_channel(channel)
    try:
        player = voice.create_ffmpeg_player(REACTION_DIR + command + '.mp3', options=" -af 'volume=0.25'")
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        player.stop()
    except Exception as ex:
        print("예외발생: " + str(ex))
    finally:
        await voice.disconnect()


async def botutil_vote(argc, argv, client, message):
    if argc == 1:
        time = 30
    else:
        time = int(argv[1])

    msg = await client.send_message(message.channel, '투표하세요! 시간제한: *' + str(time) + '초*')
    reactions = ['👍', '👎']
    for emoji in reactions: await client.add_reaction(msg, emoji)
    await asyncio.sleep(time)

    cache_msg = discord.utils.get(client.messages, id=msg.id)
    for reactor in cache_msg.reactions:
        reactors = await client.get_reaction_users(reactor)

        # from here you can do whatever you need with the member objects
        for member in reactors:
            if member.name != '갈매기봇':
                await client.send_message(message.channel, member.name)