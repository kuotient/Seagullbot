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
import random


async def botutil_help(client, message):
    msg = '※ ()은 선택, <>은 필수입니다.\n'
    for i in range(0, len(HELP_LIST)):
        msg += '**' + HELP_LIST[i][0] + '**\n' + HELP_LIST[i][1] + '\n사용법: `' + HELP_LIST[i][2] + '`\n\n'
    embed = discord.Embed(description=msg,
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

        if x.author.id == client.user.id or flag == 1:
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

    # Step 4. 이미 재생중인지 체크
    if client.is_voice_connected(channel.server):
        await client.send_message(message.channel, '현재 재생이 끝난 후 사용해 주세요.')
        return

    voice = None
    try:
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(REACTION_DIR + command + '.mp3', options=" -af 'volume=0.25'")
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        player.stop()
    except discord.ClientException as ex:
        await client.send_message(message.channel, '현재 재생이 끝난 후 사용해 주세요.')
    except Exception as ex:
        print(ex)
    finally:
        if voice is not None:
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


async def botutil_team(argc, argv, client, message):
    team_count = 0
    if argc == 1:
        team_count = 2
    else:
        team_count = int(argv[1])

    if team_count < 2:
        await client.send_message(message.channel, '팀 수는 2 이상 가능합니다.')
        return

    party_string = ''
    team_no = []

    for i in range(0, team_count):
        team_no.append([])

    if argc == 2:
        party = await client.send_message(message.channel, '참여원을 콤마(,)로 구분지어서 적어주세요.(제한시간 1분)')
        msg = await client.wait_for_message(timeout=60.0, author=message.author)
        await client.delete_message(party)
        if msg is None:
            await client.send_message(message.channel, '입력받은 시간 초과입니다.')
            return
        party_string = msg.content
        await client.delete_message(msg)
    else:
        party_string = argv[3]

    party_list = party_string.split(',')
    team_member_count = int(len(party_list) / team_count)

    for i in range(0, team_count):
        for j in range(0, team_member_count):
            random_member = random.choice(party_list)
            team_no[i].append(random_member)
            party_list.remove(random_member)

    if len(party_list) is not 0:
        index = 0
        while len(party_list) is not 0:
            team_no[index % team_count].append(party_list[0])
            party_list.remove(party_list[0])
            index += 1

    await client.send_message(message.channel, '팀 나누기 결과 : \n')
    result_msg = ''
    for i in range(0, team_count):
        result_msg += '팀 ' + str(i + 1) + ': ' + str(team_no[i]).replace(' ', '') + '\n'

    await client.send_message(message.channel, result_msg)


async def botutil_jebi(argc, argv, client, message):
    jebi_count = 0
    if argc == 1:
        jebi_count = 1
    else:
        jebi_count = int(argv[1])

    party_string = ''
    if argc <= 2:
        team_no = []

        party = await client.send_message(message.channel, '참여원을 콤마(,)로 구분지어서 적어주세요.(제한시간 1분)')
        msg = await client.wait_for_message(timeout=60.0, author=message.author)
        await client.delete_message(party)
        if msg is None:
            await client.send_message(message.channel, '입력받은 시간 초과입니다.')
            return
        party_string = msg.content
        await client.delete_message(msg)
    else:
        party_string = argv[3]

    party_list = party_string.split(',')

    if len(party_list) <= jebi_count:
        await client.send_message(message.channel, '뽑을 사람수와 참여하는 사람수를 확인해주세요.')
        return

    jebi_list = []
    for i in range(0, int(argv[1])):
        jebi_target = random.choice(party_list)
        jebi_list.append(jebi_target)
        party_list.remove(jebi_target)
    await client.send_message(message.channel, '뽑힌사람은.. ')
    await asyncio.sleep(1)
    await client.send_message(message.channel, str(jebi_list).replace(" ", "") + '!')


async def botutil_botctl(argc, argv, client, message):
    if argc != 3:
        await client.send_message(message.channel, '타겟 설정이 잘못되었습니다. 다시 해주세요.')
        return

    botctl_dic = {}
    if os.path.exists('./botctl.json'):
        with open('botctl.json') as json_file:
            botctl_dic = json.load(json_file)

    botctl_dic[message.author.id] = [argv[1], argv[2]]

    with open('botctl.json', 'w') as new_file:
        json.dump(botctl_dic, new_file, ensure_ascii=False, indent='\t')


async def botutil_botsay(argc, argv, client, message):
    botctl_dic = {}
    if not os.path.exists('./botctl.json'):
        await client.send_message(message.channel, '먼저 타겟을 설정해야 합니다.')
        return

    with open('botctl.json') as json_file:
        botctl_dic = json.load(json_file)

    if message.author.id not in botctl_dic:
        # !봇조종 <서버ID> <채널ID>
        await client.send_message(message.channel, '먼저 타겟을 설정해야 합니다.')
        return

    target_channel = client.get_server(botctl_dic[message.author.id][0]).get_channel(botctl_dic[message.author.id][1])
    if target_channel is None:
        await client.send_message(message.channel, '타겟이 잘못되었습니다. 재설정 해주세요.')
        return

    await client.send_message(target_channel, message.content[message.content.find(' ')+1:])

