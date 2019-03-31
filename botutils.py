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
    # [190308][HKPARK] Default와 자신의 서버 ID의 폴더를 스캔한다. 이때 서버 ID의 폴더가 존재하지 않는다면 생성
    fid = None
    music_path_dir = MUSIC_DIR_ID_FORMAT.format(message.server.id)
    try:
        if not (os.path.isdir(music_path_dir)):
            os.makedirs(os.path.join(music_path_dir))
            filepath = os.path.join(music_path_dir, message.server.name + ".txt")
            fid = open(filepath, "w")
            if not os.path.isfile(filepath):
                fid.write(message.server.name)

    except OSError as e:
        print('ERROR: ' + str(e))
    finally:
        if fid is not None:
            fid.close()

    reaction_list = []
    file_list = os.listdir(REACTION_DEFAULT_DIR)
    file_list.sort()
    for reaction in file_list:
        if ".mp3" in reaction:
            reaction_list.append(reaction.replace(".mp3", ""))

    file_list = os.listdir(music_path_dir)
    file_list.sort()
    for reaction in file_list:
        if ".mp3" in reaction:
            reaction_list.append(reaction.replace(".mp3", ""))

    # 중복제거
    reaction_list = list(set(reaction_list))
    reaction_list.sort()

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
        # [190308][HKPARK] 경로 검사를 먼저 해봐야함; 이게 Default에 있는 음악파일인지 서버 폴더에 있는 파일인지
        # 만약 둘 다 파일명이 존재하면 서버 폴더 우선
        voice = await client.join_voice_channel(channel)
        music_path = "{}/{}.mp3".format(music_path_dir, command) if os.path.exists("{}/{}.mp3".format(music_path_dir, command)) \
                                                            else "{}/{}.mp3".format(REACTION_DEFAULT_DIR, command)
        player = voice.create_ffmpeg_player(music_path, options=" -af 'volume=0.3'")
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

    if argc <= 2:
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
    for i in range(0, jebi_count):
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

    await client.send_message(message.channel, '타겟 설정 완료, 서버 ID: {}, 채널 ID: {}'.format(argv[1], argv[2]))


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
    try:
        target_channel = client.get_server(botctl_dic[message.author.id][0]).get_channel(botctl_dic[message.author.id][1])
        if target_channel is None:
            await client.send_message(message.channel, '타겟이 잘못되었습니다. 재설정 해주세요.')
            return

        await client.send_message(target_channel, message.content[message.content.find(' ')+1:])
    except Exception as ex:
        print(ex)
        return '타겟이 잘못되었습니다. 재설정 해주세요.'

async def botutil_reaction_upload(argc, argv, client, message):
    music_path = MUSIC_DIR_ID_FORMAT.format(message.server.id)
    uploadplz = await client.send_message(message.channel, '리액션 mp3를 업로드 하세요.')
    msg = await client.wait_for_message(timeout=60.0, author=message.author)
    await client.delete_message(uploadplz)

    if msg is None or len(msg.attachments) == 0:
        await client.send_message(message.channel, '업로드된 파일이 없습니다.')
        if msg is not None:
            await client.delete_message(msg)
        return

    url = msg.attachments[0]['url']
    if url is None or url[-4:] != '.mp3':
        await client.send_message(message.channel, 'mp3 파일을 업로드 해주세요!')
        await client.delete_message(msg)
        return

    file_name = msg.content
    if file_name is None or len(file_name) == 0:
        file_name = msg.attachments[0]['filename'].replace('.mp3', '')

    # 업로드 전 해당 파일명이 있는지 검사
    if os.path.exists(music_path+'/'+file_name+'.mp3'):
        await client.send_message(message.channel, '이미 존재하는 파일명입니다.')
        await client.delete_message(msg)
        return

    uploading = await client.send_message(message.channel, '업로드 중..')
    await download_mp3_file(url, music_path, file_name)
    await client.delete_message(msg)
    await client.edit_message(uploading, '업로드가 완료되었습니다.')

async def download_mp3_file(url, path, file_name):

    if not os.path.exists(path):
        os.makedirs(path)
    headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
    }
    r = requests.get(url, headers=headers, stream=True)
    with open(path+'/'+str(file_name)+'.mp3', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
