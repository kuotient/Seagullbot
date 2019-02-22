import leagueoflegends as lol
import urf
import discord
import seagullbot
import asyncio
import siege

#client = discord.Client()
client = seagullbot.Client()

command_list = [
    ['!도움', '명령어 리스트를 보여줍니다', '사용법: !도움'],
    ['!롤전적', '롤 전적을 보여줍니다', '사용법: !롤전적'],
    ['!롤현재', '현재 플레이중인 롤 정보를 보여줍니다', '사용법: !롤현재'],
    ['!우르프', '우르프 전적를 보여줍니다', '사용법: !우르프'],
    ['!레식전적', '레인보우식스 시즈 전적를 보여줍니다', '사용법: !우르프'],
]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(game=discord.Game(name="ver 0.11"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for check in command_list:
        if check[0] in message.content:
            client.log_recv_message(message)
            break

#########   봇 기본 명령어     ##########################################################################
    if message.content.startswith('!도움') or message.content.startswith('!help'):
        msg = ''
        for i in range(0, len(command_list)):
            msg += '**' + command_list[i][0] + '**\n\t' + command_list[i][1] + '\n\t_' + command_list[i][2] + '_\n\n'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!test'):
        await client.send_message(message.channel, 'test!')

    elif message.content.startswith('!정리') or message.content.startswith('!clear'):
        mgs = []
        async for x in client.logs_from(message.channel, limit=1000):
            mgs.append(x)
        await client.delete_messages(mgs)
        #await client.clear_messages()

    elif message.content.startswith('!모두정리') or message.content.startswith('!clearall'):
        await client.clear_all_messages()

##########################################################################################################

#########   롤 관련 명령어     ##########################################################################
    elif message.content.startswith('!롤전적'):
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
                                  description='[OP.GG](http://www.op.gg/summoner/userName='+ msg.content.replace(" ", "") +')',
                                  color=0x00ff00)
            embed.set_thumbnail(url="http://opgg-static.akamaized.net/images/profile_icons/profileIcon27.jpg")
            await client.send_message(message.channel, embed=embed)
    
    elif message.content.startswith('!롤현재'):
        await client.send_message(message.channel, '아이디를 입력하세요.')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)

        if msg is None:
            await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
            return
        else:
            temp = lol.search(msg.content)
            if temp == 1:
                embed = discord.Embed(title='NOW PLAYING: **'+ lol.find_champion_name(msg.content).upper() + '**',
                                      description='[OP.GG](http://www.op.gg/summoner/userName='+ msg.content.replace(" ", "") + ') 에서 확인해보세요.',
                                      color=0x00ff00)
                embed.set_thumbnail(url=lol.find_champion_img(msg.content))
                await client.send_message(message.channel, embed=embed)
            elif temp == 0:
                embed = discord.Embed(title= msg.content + ' is not playing right now. :zzz:',
                                      description='다른 사람을 검색하시려면 !롤현재',
                                      color=0xed2902)
                await client.send_message(message.channel, embed=embed)

##########################################################################################################

#########   우르프 관련 명령어     ######################################################################
    elif message.content.startswith('!우르프'):
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
    elif message.content.startswith('!레식전적'):
        if len(message.content.split(' ')) == 1:
            searching = await client.send_message(message.channel, '아이디를 입력하세요.')
            msg = await client.wait_for_message(timeout=15.0, author=message.author)
            player_id = msg.content
            await client.delete_message(msg)

            if player_id is None:
                await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
                await client.delete_message(searching)
                return
            searching = await client.edit_message(searching, '검색중입니다..')
        else:
            player_id = message.content.split(' ')[1]
            searching = await client.send_message(message.channel, '검색중입니다..')

        result = siege.search(player_id)
        await client.edit_message(searching, result)

##########################################################################################################

#client.run('NTQyNjgyMTkyMjEyMzkzOTg0.DzxmWA.QhMZJ-8KNgo9Nxjt0eLPgkHNQYg')
client.run('NTQ4MzIxNDQyODE5ODY2NjU1.D1DrCg.4oZpqUgQ4PEHhPgZD29tPVWsdwU')