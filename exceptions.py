import shutil #기본 라이브러리, 파일 수정 몇 복사, 이동에 사용
import textwrap #문자열 줄 바꿈 등 ... 참고 :https://gist.github.com/LeoHeo/2e54cf7d00d0497f183a8382a3ebaf74

# 오류 전담 파일
#Base Class for exceptions
class SeagullBotException(Exception):
    def __init__(self, message, *, expire_in=0):
        super().__init__(message) # super() 는 자식 클래스가 부모 클래스의 기능을 쓰고 싶을때 이용한다. 이건 뭘까...?
        self._message = message
        self.expire_in = expire_in

        @property
        def message(self):
            return self._message #접근지정자의 개념은 없지만, __는 private, _는 protected 의 개념으로 쓰인다.
                                 #@property 는 Get, @message.setter 는 Set 의 개념으로 쓰일 수 있다.
                                 #참고 : https://hamait.tistory.com/827

class HelpfulError(SeagullBotException): #자식 클래스
    def __init__(self, issue, solution, *, preface="An error has occured:", expire_in=0):
        self.issue = issue
        self.solution = solution
        self.preface = preface
        self.expire_in = expire_in
        self._message_format =  "\n{preface}\n{problem}\n\n{solution}"

    @property
    def message(self):
        return self._message_format.format(
            preface = self.preface,
            problem = self._pretty_wrap(self.issue,     "  problem:", width=None),
            solution = self._pretty_wrap(self.solution, "  solution:",width=None)
        )

    @staticmethod
    #나중에 자식 클래스가 HelpfulError 를 상속받아 속성값을 가져와도 HelpfulError 의 속성을 가져오게 만듬.
    def _pretty_wrap(text, pretext, *, width = -1):
        if width is None:
            return '\n'.join((pretext.strip(), text))
            #join() : 특정 구분자를 추가하여 문자열로 생성. 여기서는 줄바꿈이 구분자.
            #strip() : 양쪽 공백 지우기
        elif width == -1:
            pretext = pretext.rstrip() + '\n'
            width = shutil.get_terminal_size().columns

        lines = textwrap.wrap(text, width=width - 5)
        lines = (('    ' + line).rstrip().ljust(width - 1).rstrip() + '\n' for line in lines)

        return pretext + ''.join(lines).rstrip()

class FFmpegError(SeagullBotException):
    pass