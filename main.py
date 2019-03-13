import leagueoflegends as lol
import urf
import discord
from discord.voice_client import VoiceClient
import asyncio
import siege
import apexlegends as apex
import nacl
from constant import *
import configparser
import botutils
import os

client = discord.Client()

config = configparser.ConfigParser()
config.read('./config.ini')

DISCORD_TOKEN = config['DEFAULT']['DISCORD_TOKEN']


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(game=discord.Game(name=VERSION))


@client.event
async def on_server_join(server):
    # [190308][HKPARK] 서버 입장시 data/music/(서버ID) 식으로 폴더 생성한다.
    # [190313][HKPARK] 폴더 경로를 data/(서버ID)/music 식으로 변경.
    try:
        music_path = MUSIC_DIR_ID_FORMAT.format(server.id)
        if not (os.path.isdir(music_path)):
            os.makedirs(os.path.join(music_path))
            filepath = os.path.join(music_path, server.name + ".txt")
            fid = open(filepath, "w")
            if not os.path.isfile(filepath):
                fid.write(server.name)

            fid.close()
    except OSError as e:
        print('ERROR: ' + str(e))
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    argv = message.content.split(' ')
    argc = len(argv)

#########   봇 기본 명령어     ##########################################################################
    # !도움
    if argv[0] == COMMAND_HELP1 or argv[0] == COMMAND_HELP2:
        await botutils.botutil_help(client, message)

    # !정리
    elif argv[0] == COMMAND_CLEAR1 or argv[0] == COMMAND_CLEAR2:
        await botutils.botutil_clear(client, message)

    # !리액션
    elif argv[0] == COMMAND_REACTION1 or argv[0] == COMMAND_REACTION2:
        await botutils.botutil_reaction(argc, argv, client, message)

    # !투표
    elif argv[0] == COMMAND_VOTE:
        await botutils.botutil_vote(argc, argv, client, message)

    # !팀나누기
    elif argv[0] == COMMAND_TEAM:
        await botutils.botutil_team(argc, argv, client, message)

    # !팀나누기
    elif argv[0] == COMMAND_JEBI:
        await botutils.botutil_jebi(argc, argv, client, message)

################################ 관리자 명령어 ###########################################################

    # !봇조종
    elif argv[0] == COMMAND_BOTCTL:
        await botutils.botutil_botctl(argc, argv, client, message)

    # !봇말
    elif argv[0] == COMMAND_BOTSAY:
        await botutils.botutil_botsay(argc, argv, client, message)

    # !리액션업로드
    elif argv[0] == COMMAND_REACTION_UPLOAD:
        await botutils.botutil_reaction_upload(argc, argv, client, message)

    elif argv[0] == '!끼룩':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=m6qWcKLB7Ig')

##########################################################################################################

#########   롤 관련 명령어     ##########################################################################
    # !롤전적
    elif argv[0] == COMMAND_LOLSTAT:
        await client.send_message(message.channel, '아이디를 입력하세요.')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)

        if msg is None:
            await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
            return
        elif msg.content == '항상최선을다해서':
            embed = discord.Embed(title='함부로 그를 검색하지 마십시오. 경고합니다.',
                                  description='warning.or.kr',
                                  color=0x00ff00)
            await client.send_message(message.channel, embed=embed)            
        else:
            embed = discord.Embed(title='최근 전적',
                                  description='[OP.GG](http://www.op.gg/summoner/userName=' + msg.content.replace(" ", "") + ')',
                                  color=0x00ff00)
            embed.set_thumbnail(url="http://opgg-static.akamaized.net/images/profile_icons/profileIcon27.jpg")
            await client.send_message(message.channel, embed=embed)

    # !롤현재
    elif argv[0] == COMMAND_LOLNOW:
        if len(message.content.split(' ')) == 1:
            searching = await client.send_message(message.channel, '아이디를 입력하세요.')
            msg = await client.wait_for_message(timeout=15.0, author=message.author)
            player_id = msg.content
            await client.delete_message(msg)

            if msg is None:
                await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
                await client.delete_message(searching)
                return
            else:
                searching = await client.edit_message(searching, '검색중입니다...')
                await client.send_typing(message.channel)
        else:
            player_id = message.content.split(' ')[1]
            searching = await client.send_message(message.channel, '검색중입니다...')
            await client.send_typing(message.channel)

        temp = lol.search(player_id)
        if temp == 1:
            embed = discord.Embed(title='NOW PLAYING: **'+ lol.find_champion_name(player_id).upper() + '**',
                                  description='[OP.GG](http://www.op.gg/summoner/userName='+ player_id.replace(" ", "") + ') 에서 확인해보세요.',
                                  color=0x00ff00)
            embed.set_thumbnail(url=lol.find_champion_img(player_id))
            await client.delete_message(searching)
            await client.send_message(message.channel, embed=embed)
        elif temp == 0:
            embed = discord.Embed(title=player_id + ' is not playing right now. :zzz:',
                                  description='다른 사람을 검색하시려면 `!롤현재 (아이디)`',
                                  color=0xed2902)
            await client.delete_message(searching)
            await client.send_message(message.channel, embed=embed)

##########################################################################################################

#########   우르프 관련 명령어     ######################################################################
    # !우르프
    elif argv[0] == COMMAND_URF:
        await client.send_message(message.channel, '***:zap: URF TIER LIST :zap:** presented by* op.gg')
        (champions, winrate, kda) = urf.urf_rank()
        s = "```CHAMPION                                 WINRATE      KDA\n\n"
        index = 1

        while index < 11:
            if index == 10:
                s += str(index)+ '.' + str(champions[index-1]).ljust(38) + str(winrate[index-1]) + '       ' + str(kda[index-1]) + '\n'
            else:
                s += str(index) + '. ' + str(champions[index - 1]).ljust(38)+ str(winrate[index - 1]) + '       ' + str(kda[index - 1]) + '\n'

            index += 1
        s += "```"

        await client.send_message(message.channel, s)

##########################################################################################################

#########   레식 관련 명령어     ########################################################################
    # !레식전적
    elif argv[0] == COMMAND_R6STAT:
        await siege.siege_search_stats(argc, argv, client, message)

    # !레식오퍼
    elif argv[0] == COMMAND_R6OPER:
        await siege.siege_search_operator(argc, argv, client, message)

##########################################################################################################

###################에이펙스 관련 명령어 ##################################################################
    # !에이펙스
    elif argv[0] == COMMAND_APEX:
        if argc == 1:
            searching = await client.send_message(message.channel, '아이디를 입력하세요.')
            msg = await client.wait_for_message(timeout=15.0, author=message.author)
            player_id = msg.content
            await client.delete_message(msg)

            if msg is None:
                await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
                await client.delete_message(searching)
                return
            searching = await client.edit_message(searching, '검색중입니다...')
            await client.send_typing(message.channel)
        else:
            player_id = message.content.split(' ')[1]
            searching = await client.send_message(message.channel, '검색중입니다...')
            await client.send_typing(message.channel)

        result = apex.search(player_id)
        if result == -1:
            await client.edit_message(searching, '플레이어를 찾을 수 없습니다.')
        else:
            embed = discord.Embed(title='플레이어: **' + player_id + '**',
                                  description='```' + result + '```\n 더 많은 정보는 [여기서](https://apex.tracker.gg/profile/pc/'
                                              + player_id + ')',
                                  color=0x00ff00)
            await client.delete_message(searching)
            await client.send_message(message.channel, embed=embed)

##########################################################################################################


client.run(DISCORD_TOKEN)
