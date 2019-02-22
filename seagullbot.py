import discord
import asyncio

recv_msg_log = []
send_msg_log = []


class Client(discord.Client):
#########   오버라이딩     ##############################################################################
    @asyncio.coroutine
    def send_message(self, destination, content=None, *, tts=False, embed=None):
        message = super(Client, self).send_message(destination, content=content, tts=tts, embed=embed)
        send_msg_log.append(message)
        return message

    @asyncio.coroutine
    def wait_for_message(self, timeout=None, *, author=None, channel=None, content=None, check=None):
        message = super(Client, self).wait_for_message(timeout=timeout, author=author, channel=channel, content=content, check=check)
        recv_msg_log.append(message)
        return message

    @asyncio.coroutine
    def edit_message(self, message, new_content=None, *, embed=None):
        edt_message = super(Client, self).edit_message(message=message, new_content=new_content, embed=embed)
        if message in recv_msg_log:
        #    recv_msg_log.remove(message)
            recv_msg_log.append(edt_message)
        elif message in send_msg_log:
        #    send_msg_log.remove(message)
            send_msg_log.append(edt_message)

        return edt_message

##########################################################################################################

    def log_send_message(self, message):
        send_msg_log.append(message)

    def log_recv_message(self, message):
        recv_msg_log.append(message)

    def clear_messages(self):
        del_list = send_msg_log

        if len(del_list) == 1:
            return super(Client, self).delete_message(del_list[0])
        else:
            return super(Client, self).delete_messages(del_list)
        send_msg_log.clear()

    def clear_all_messages(self):
        del_list = recv_msg_log + send_msg_log

        if len(del_list) == 1:
            return super(Client, self).delete_message(del_list[0])
        else:
            return super(Client, self).delete_messages(del_list)

        recv_msg_log.clear()
        send_msg_log.clear()
