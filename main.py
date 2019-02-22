import leagueoflegends as lol
import urf
import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(game=discord.Game(name="ver 0.10"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'test!')
    
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

client.run('NTQyNjgyMTkyMjEyMzkzOTg0.DzxmWA.QhMZJ-8KNgo9Nxjt0eLPgkHNQYg')