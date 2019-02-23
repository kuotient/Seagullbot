import leagueoflegends as lol
import urf
import discord
from discord.voice_client import VoiceClient
import asyncio
import siege
import apexlegends as apex
import nacl

client = discord.Client()
###################### 버전 ################################
VERSION = 'ver 0.37'
############################################################

#########   명령어 상수 정의     ##########################################################################
COMMAND_REACTION = '!리액션'
COMMAND_HELP1 = '!도움'
COMMAND_HELP2 = '!help'
COMMAND_LOLSTAT = '!롤전적'
COMMAND_LOLNOW = '!롤현재'
COMMAND_URF = '!우르프'
COMMAND_R6STAT = '!레식전적'
COMMAND_APEX = '!에이펙스'
COMMAND_CLEAR1 = '!정리'
COMMAND_CLEAR2 = '!clear'


COMMAND_LIST = [
    COMMAND_HELP1,
    COMMAND_HELP2,
    COMMAND_LOLSTAT,
    COMMAND_LOLNOW,
    COMMAND_URF,
    COMMAND_R6STAT,
    COMMAND_APEX,
    COMMAND_CLEAR1,
    COMMAND_CLEAR2
]

HELP_LIST = [
    [COMMAND_HELP1 + ', ' + COMMAND_HELP2, '명령어 리스트를 보여줍니다.', COMMAND_HELP1 + '`or `' + COMMAND_HELP2],
    [COMMAND_LOLSTAT, '롤 전적을 보여줍니다.', COMMAND_LOLSTAT],
    [COMMAND_LOLNOW, '현재 플레이중인 롤 정보를 보여줍니다.', COMMAND_LOLNOW],
    [COMMAND_URF, '현재 우르프 티어를 보여줍니다.', COMMAND_URF],
    [COMMAND_R6STAT, '레인보우식스 시즈 전적을 보여줍니다.', COMMAND_R6STAT + ' (아이디)'],
    [COMMAND_APEX, '에이펙스 레전드 전적을 보여줍니다.', COMMAND_APEX + ' (아이디)'],
]

##########################################################################################################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(game=discord.Game(name=VERSION))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#########   봇 기본 명령어     ##########################################################################
    # !도움
    if message.content.startswith(COMMAND_HELP1) or message.content.startswith(COMMAND_HELP2):
        msg = '\n'
        for i in range(0, len(HELP_LIST)):
            msg += '**' + HELP_LIST[i][0] + '**\n' + HELP_LIST[i][1] + '\n사용법: `' + HELP_LIST[i][2] + '`\n\n'
        embed = discord.Embed(title='***ULTIMATE GUIDES for SEAGULLBOT                    ***',
                              description= msg,
                              color=0x00ff00)
        await client.send_message(message.channel, embed=embed)

    # !정리
    elif message.content.startswith(COMMAND_CLEAR1) or message.content.startswith(COMMAND_CLEAR2):
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

##########################################################################################################

#########   롤 관련 명령어     ##########################################################################
    # !롤전적
    elif message.content.startswith(COMMAND_LOLSTAT):
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
    elif message.content.startswith(COMMAND_LOLNOW):
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
    elif message.content.startswith(COMMAND_URF):
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
    elif message.content.startswith(COMMAND_R6STAT):
        if len(message.content.split(' ')) == 1:
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

        result = siege.search(player_id)
        await client.edit_message(searching, result)

##########################################################################################################

###################에이펙스 관련 명령어 ##################################################################
    # !에이펙스
    elif message.content.startswith(COMMAND_APEX):
        if len(message.content.split(' ')) == 1:
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

##################리액션 관련 명령어######################################################################
    elif message.content.startswith(COMMAND_REACTION):
        if len(message.content.split(' ')) == 1:
            embed = discord.Embed(title='!리액션 (커맨드)로 리액션을 재생할 수 있습니다.',
                                  description='*커맨드 목록*\n```temp\nCOMMAND LIST BLAH BLAH```',
                                  color=0xfdee00)
            await client.send_message(message.channel, embed=embed)

        else:
            command = message.content.split(' ')[1]
            author = message.author
            channel = author.voice_channel
            if channel != None:
                voice = await client.join_voice_channel(channel)
                player = voice.create_ffmpeg_player('data/music/Vu.mp3')
                player.start()
                while not player.is_done():
                    await asyncio.sleep(1)
                # disconnect after the player has finished
                player.stop()
                await voice.disconnect()
            else:
                await client.send_message(message.channel, '음성 채팅에 접속해있어야 합니다.')

##########################################################################################################

client.run('NTQyNjgyMTkyMjEyMzkzOTg0.DzxmWA.QhMZJ-8KNgo9Nxjt0eLPgkHNQYg')
#client.run('NTQ4MzIxNDQyODE5ODY2NjU1.D1DrCg.4oZpqUgQ4PEHhPgZD29tPVWsdwU')