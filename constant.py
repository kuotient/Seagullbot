
###################### 버전 ################################
VERSION = 'ver 0.6'
############################################################

#########   명령어 상수 정의     ##########################################################################
COMMAND_REACTION1 = '!리액션'
COMMAND_REACTION2 = '!react'
COMMAND_HELP1 = '!도움'
COMMAND_HELP2 = '!help'
COMMAND_LOLSTAT = '!롤전적'
COMMAND_LOLNOW = '!롤현재'
COMMAND_URF = '!우르프'
COMMAND_R6STAT = '!레식전적'
COMMAND_R6OPER = '!레식오퍼'
COMMAND_APEX = '!에이펙스'
COMMAND_CLEAR1 = '!정리'
COMMAND_CLEAR2 = '!clear'
COMMAND_VOTE = '!투표'
COMMAND_TEAM = '!팀나누기'


COMMAND_LIST = [
    COMMAND_REACTION1,
    COMMAND_REACTION2,
    COMMAND_HELP1,
    COMMAND_HELP2,
    COMMAND_LOLSTAT,
    COMMAND_LOLNOW,
    COMMAND_URF,
    COMMAND_R6STAT,
    COMMAND_R6OPER,
    COMMAND_APEX,
    COMMAND_CLEAR1,
    COMMAND_CLEAR2,
    COMMAND_VOTE,
    COMMAND_TEAM
]

HELP_LIST = [
    [COMMAND_HELP1 + ', ' + COMMAND_HELP2, '명령어 리스트를 보여줍니다.', COMMAND_HELP1 + '` or `' + COMMAND_HELP2],
    [COMMAND_LOLSTAT, '롤 전적을 보여줍니다.', COMMAND_LOLSTAT],
    [COMMAND_LOLNOW, '현재 플레이중인 롤 정보를 보여줍니다.', COMMAND_LOLNOW],
    [COMMAND_URF, '현재 우르프 티어를 보여줍니다.', COMMAND_URF],
    [COMMAND_R6STAT, '레인보우식스 시즈 전적을 보여줍니다.', COMMAND_R6STAT + ' (아이디)'],
    [COMMAND_R6OPER, '레인보우식스 시즈 오퍼레이터 순위를 플레이타임 순으로 보여줍니다.', COMMAND_R6OPER + ' (아이디)'],
    [COMMAND_APEX, '에이펙스 레전드 전적을 보여줍니다.', COMMAND_APEX + ' (아이디)'],
    [COMMAND_REACTION1, '보이스챗 리액션을 할 수 있습니다. 자세한 정보는 `!리액션`에서.', COMMAND_REACTION1 + ' (리스트) or ' + \
                                                                                    COMMAND_REACTION2 + ' (리스트)'],
    [COMMAND_TEAM, '팀을 나눌 수 있습니다.', COMMAND_TEAM + ' <팀 수>']
]

# VOICE_COMMAND_LIST = [
#     'airhorn', 'airhorn2', 'sad', 'sad2', 'johncena', 'wow', 'wasted', 'haha', 'cheers','nope', 'evil', 'ps1'
# ]

REACTION_DIR = './data/music/'

##########################################################################################################