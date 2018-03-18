import sys
import time
import urllib
import urllib.request
from urllib.request import Request, urlopen
import os
import platform
import io
import telepot
import telepot.aio
import asyncio
import random
import json
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

HJ_Ver = "1.0.2.1"
print("[Info] Starting HJ Util version ", HJ_Ver, "...")
#Config
print("[Info] Loading config...")
try:
    if sys.argv[1] == 'test':
        configraw = {
            "//TOKEN": "Insert your telegram bot token here.",
            "TOKEN": "",
            "//pastebin_dev_key": "Insert your pastebin dev token here.",
            "pastebin_dev_key": "",
            "//pastebin_user_key": "Get your user key here: https://pastebin.com/api/api_user_key.html",
            "pastebin_user_key": "",
            "//OWNERID": "Your user id as integer.",
            "OWNERID": 135405898,
            "//Debug": "If true,raw debug info will be logged into -debug.log file",
            "Debug": True
        }
    else:
        raise SyntaxError("Invaild command santax: {0}".format(sys.argv[1]))
except IndexError:
    try:
        with open('./config.json','r') as fs:
            configraw = json.load(fs)
    except FileNotFoundError:
        print("[Error] Can't load config.json: File not found.\n[Info] Generating empty config...")
        with open('./config.json', 'w') as fs:
            fs.write(
    '''{
        "//TOKEN":"Insert your telegram bot token here.",
        "TOKEN":"", 

        "//pastebin_dev_key":"Insert your pastebin dev token here.",
        "pastebin_dev_key" : "", 

        "//pastebin_user_key":"Get your user key here: https://pastebin.com/api/api_user_key.html",
        "pastebin_user_key" : "", 

        "//OWNERID":"Your user id as integer.",
        "OWNERID": 0, 
        
        "//Debug":"If true,raw debug info will be logged into -debug.log file",
        "Debug" : false 
        
    }
    '''
        )
        print("\n[Info] Fill your config and try again.")
        exit()
    except json.decoder.JSONDecodeError as e1:
        print("[Error] Can't load config.json: JSON decode error:", e1.args, "\n\n[Info] Check your config format and try again.")
        exit()
class config:
    TOKEN = configraw['TOKEN']
    pastebin_dev_key = configraw["pastebin_dev_key"]
    pastebin_user_key = configraw["pastebin_user_key"]
    Debug = configraw["Debug"]
    OWNERID = configraw["OWNERID"]

#Language
try:
    with open("./langs/list.py", "r") as fs:
        langlist = eval(fs.read())
except FileNotFoundError:
    print("Can't load langs/list.py: File not found.")
    exit()
except Exception as e1:
    print("Can't load langs/list.py:", e1.args)
    exit()
lang = {}
for i in langlist:
    lang[i] = {}
    with open(langlist[i]["file"], "r") as fs:
        lang[i]["display"] = eval(fs.read())
        lang[i]["display_name"] = langlist[i]["display_name"]

confirmsg = None
function_list_data = None
chat_config = {}
delete_msg_sender = {}

async def on_chat_message(msg):
    try:
        tmp = msg['edit_date']
    except KeyError:
        edited = False
    else:
        edited = True
    content_type, chat_type, chat_id = telepot.glance(msg)
    await logger.logmsg(msg)
    try:
        chat_config[str(chat_id)]
    except KeyError:
        chatconfig.default_lang(chat_id)
    if chat_type == 'private':
        if content_type == 'text' and edited == False:
            cmd = msg['text'].split()
            if cmd[0] == '/start':
                await startc(chat_id, msg)
            if cmd[0] == '/getme':
                await user.getme(chat_id, msg)
            if cmd[0] == '/getfile':
                await getfile(chat_id, msg, cmd)
            if cmd[0] == '/exportblog':
                await exportblog(chat_id, msg)
            if cmd[0] == '/ping':
                await ping(chat_id, msg)
            if cmd[0] == '/echo':
                await echo(chat_id, msg)
            if cmd[0] == '/ns':
                await ns(chat_id, msg, cmd)
            if cmd[0] == '/gtts':
                await gtts(chat_id, msg)
            if cmd[0] == '/help':
                await helpp(chat_id, msg)
            if cmd[0] == '/setlang':
                await chatconfig.set_lang_command(chat_id, msg, cmd)
            if cmd[0] == '/delmsg':
                await delmsg.delmsg(chat_id, msg, chat_type)
            if cmd[0] == '/a2z':
                await a2zc(chat_id, msg)
    elif chat_type == 'group' or chat_type == 'supergroup':
        #command_detect
        global function_list_data
        try:
            groupfundict = function_list_data[str(chat_id)]
        except KeyError:
            await function.function_default(chat_id, msg, chat_type)
            groupfundict = function_list_data[str(chat_id)]
        try:
            chat_config[str(chat_id)]
        except KeyError:
            chatconfig.default_lang(chat_id)
        if content_type == 'text' and edited == False:
            cmd = msg['text'].split()
            cmd[0] = cmd[0].lower()
            sortedcmd = []
            for i in cmd:
                if i not in sortedcmd:
                    sortedcmd.append(i)
            if cmd[0] == '/start' or cmd[0] == '/start@'+bot_me.username.lower():
                await startc(chat_id, msg)
            if cmd[0] == '/cgp' or cmd[0] == '/cgp@'+bot_me.username.lower():
                if groupfundict['grouppic']:
                    await grouppic.cgp(chat_id, msg, chat_type)
            if cmd[0] == '/rgp' or cmd[0] == '/rgp@'+bot_me.username.lower():
                if groupfundict['grouppic']:
                    await grouppic.rgp(chat_id, msg, chat_type)
            if cmd[0] == '/echo' or cmd[0] == '/echo@'+bot_me.username.lower():
                if groupfundict['echo']:
                    await echo(chat_id, msg)
            if cmd[0] == '/ns' or cmd[0] == '/ns@'+bot_me.username.lower():
                if groupfundict['numbersystem']:
                    await ns(chat_id, msg, cmd)
            if cmd[0] == '/ping' or cmd[0] == '/ping@'+bot_me.username.lower():
                if groupfundict['ping']:
                    await ping(chat_id, msg)
                    return
            if cmd[0] == '/title' or cmd[0] == '/title@'+bot_me.username.lower():
                if groupfundict['title']:
                    await title.title(chat_id, msg, chat_type)
            if cmd[0] == '/lsadmins' or cmd[0] == '/lsadmins@'+bot_me.username.lower():
                if groupfundict['lsadmins']:
                    await lsadmins(chat_id, msg, cmd)
            if cmd[0] == '/groupinfo' or cmd[0] == '/groupinfo@'+bot_me.username.lower():
                if groupfundict['groupinfo']:
                    await groupinfo(chat_id, msg, chat_type)
            if cmd[0] == '/leavegroup' or cmd[0] == '/leavegroup@'+bot_me.username.lower():
                await leavegroup(chat_id, msg, chat_type)
            if cmd[0] == '/a2z' or cmd[0] == '/a2z@'+bot_me.username.lower():
                if groupfundict['a2z']:
                    await a2zc(chat_id, msg)
            if cmd[0] == '/getuser' or cmd[0] == '/getuser@'+bot_me.username.lower():
                if groupfundict['user']:
                    await user.getuser(chat_id, msg, cmd)
            if cmd[0] == '/getme' or cmd[0] == '/getme@'+bot_me.username.lower():
                if groupfundict['user']:
                    await user.getme(chat_id, msg)
            if cmd[0] == '/exportchatlink' or cmd[0] == '/exportchatlink@'+bot_me.username.lower():
                if groupfundict['export_link']:
                    await ecl.exportchatlink(chat_id, msg, chat_type)
            if cmd[0] == '/delmsg' or cmd[0] == '/delmsg@'+bot_me.username.lower():
                if groupfundict['delete_message']:
                    await delmsg.delmsg(chat_id, msg, chat_type)
            if cmd[0] == '/pin' or cmd[0] == '/pin@'+bot_me.username.lower():
                if groupfundict['pin']:
                    await pin.pin(chat_id, msg, chat_type)
            if cmd[0] == '/replace' or cmd[0] == '/replace@'+bot_me.username.lower():
                if groupfundict['replace_str']:
                    await replace(chat_id, msg, cmd)
            if cmd[0] == '/getfile' or cmd[0] == '/getfile@'+bot_me.username.lower():
                if groupfundict['files']:
                    await getfile(chat_id, msg, cmd)
            if cmd[0] == '/fileinfo' or cmd[0] == '/fileinfo@'+bot_me.username.lower():
                if groupfundict['files']:
                    await fileinfo(chat_id, msg)
            if cmd[0] == '/tag' or cmd[0] == '/tag@'+bot_me.username.lower():
                if groupfundict['tag']:
                    try:
                        a = sortedcmd[2]
                    except IndexError:
                        try:
                            if cmd[1] == 'list' and cmd[2] == 'list':
                                sortedcmd.append('list')
                        except IndexError:
                            pass
                    await tag.tag(chat_id, msg, sortedcmd, chat_type)
            if cmd[0] == '/function' or cmd[0] == '/function@'+bot_me.username.lower():
                await function.function(chat_id, msg, cmd, chat_type)
                return
            if cmd[0] == '/confirm' or cmd[0] == '/confirm@'+bot_me.username.lower():
                await tag.confirm(chat_id, msg)
            if cmd[0] == '/gtts' or cmd[0] == '/gtts@'+bot_me.username.lower():
                if groupfundict['google_tts']:
                    await gtts(chat_id, msg)
            if cmd[0] == '/help' or cmd[0] == '/help@'+bot_me.username.lower():
                await help(chat_id, msg, chat_type)
            if cmd[0] == '/setlang' or cmd[0] == '/setlang@'+bot_me.username.lower():
                await chatconfig.set_lang(chat_id, msg, cmd, chat_type)
            if msg['text'].lower().find('#pin') != -1:
                if groupfundict['pin']:
                    await pin.pinh(chat_id, msg, chat_type)
            if msg['text'].lower().find('ping') != -1:
                try:
                    if msg['text'][msg['text'].lower().find('ping')+4] != '@':
                        if groupfundict['ping']:
                            await ping(chat_id, msg)
                            return
                except IndexError:
                    if groupfundict['ping']:
                        await ping(chat_id, msg)
                        return
            for txt in sortedcmd:
                if txt == '@tagall':
                    #tag(chat_id,msg,["/tag","all"],chat_type)
                    pass
                elif txt == '@tagadmin' or txt == '@admin':
                    if groupfundict['tag']:
                        await tag.tag(chat_id, msg, ["/tag", "admin"], chat_type)
                elif txt[0:4] == '@tag':
                    if txt == '@tag':
                        return
                    else:
                        if groupfundict['tag']:
                            await tag.tag(chat_id, msg, [
                                "/tag", "tag", txt[4:]], chat_type)
            if groupfundict['replace_str']:
                repsep = msg['text'].split('/', 2)
                if repsep[0] == "s":
                    try:
                        tobereplaced = repsep[1]
                        toreplace = repsep[2]
                    except IndexError:
                        pass
                    else:
                        await replace(chat_id, msg, [
                                '/replace', tobereplaced, toreplace])
        else:
            try:
                cmd = msg['caption'].split()
                cmd[0] = cmd[0].lower()
                sortedcmd = []
                for i in cmd:
                    if i not in sortedcmd:
                        sortedcmd.append(i)
            except KeyError:
                pass
            else:
                for txt in sortedcmd:
                    if txt == '@tagall':
                        #tag(chat_id,msg,["/tag","all"],chat_type)
                        pass
                    elif txt[0:4] == '@tag':
                        if txt == '@tag':
                            return
                        else:
                            if groupfundict['tag']:
                                await tag.tag(chat_id, msg, [
                                    "/tag", "tag", txt[4:]], chat_type)
                if msg['caption'].lower().find('#pin') != -1:
                    if groupfundict['pin']:
                        await pin.pinh(chat_id, msg, chat_type)
            if groupfundict['replace_str']:
                try:
                    repsep = msg['caption'].split('/', 2)
                except:
                    time.sleep(0)
                else:
                    if repsep[0] == "s":
                        try:
                            tobereplaced = repsep[1]
                            toreplace = repsep[2]
                        except IndexError:
                            pass
                        else:
                            await replace(chat_id, msg, [
                                    '/replace', tobereplaced, toreplace])
    return

async def on_callback_query(msg):
    logger.log("[Debug] Raw query data:"+str(msg))
    orginal_message = msg['message']['reply_to_message']
    message_with_inline_keyboard = msg['message']
    content_type, chat_type, chat_id = telepot.glance(orginal_message)
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    logger.clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info]["+str(query_id) +
         "] Callback query form "+str(from_id)+" to "+str(orginal_message['message_id'])+" :" + data)
    if data == 'confirm_delete':
        await delmsg.confirm_delete(chat_id, orginal_message, query_id,
                       message_with_inline_keyboard, from_id)
    elif data == 'cancel_delete':
        await delmsg.cancel_delete(chat_id, orginal_message, query_id,
                      message_with_inline_keyboard, from_id)

    return

async def startc(chat_id, msg):
    dre = await bot.sendMessage(chat_id, 'JUST an utilities bot\n/help',
                          reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    return

class grouppicc:
    async def cgp(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['cgp']
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            dre = await bot.sendMessage(chat_id,
                                langport['all_member_are_admin'],
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        try:
            reply_to = msg['reply_to_message']
        except KeyError:
            if msg['from']['id'] == config.OWNERID:
                logger.clog('[Info] Owner Matched for \n[Info] ' +
                    str(await bot.getChatMember(chat_id, msg['from']['id'])))
                await self.__cgp('url', msg, langport, chat_id)
                return
            else:
                logger.clog('[Info] Searching admins in '+msg['chat']
                    ['title']+'('+str(chat_id) + ')')
                for admin in await bot.getChatAdministrators(chat_id):
                    if msg['from']['id'] == admin['user']['id']:
                        logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                        await self.__cgp('url', msg, langport,chat_id)
                        return
                logger.clog('[Info] No admins matched with ' + msg['from']
                    ['username']+'('+str(msg['from']['id']) + ')')
                await bot.sendMessage(
                    chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
                return
        else:
            if msg['from']['id'] == config.OWNERID:
                logger.clog('[Info] Owner Matched for \n[Info] ' +
                            str(await bot.getChatMember(chat_id, msg['from']['id'])))
                await self.__cgp('photo', msg, langport,chat_id)
                return
            else:
                logger.clog('[Info] Searching admins in '+msg['chat']
                    ['title']+'('+str(chat_id) + ')')
                for admin in await bot.getChatAdministrators(chat_id):
                    if msg['from']['id'] == admin['user']['id']:
                        logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                        await self.__cgp('photo', msg, langport,chat_id)
                        return
                logger.clog('[Info] No admins matched with ' + msg['from']
                    ['username']+'('+str(msg['from']['id']) + ')')
                await bot.sendMessage(
                    chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
                return
        return
    async def __cgp(self, type, msg, langport, chat_id):
        if type == 'url':
            url = msg['text'].split(' ', 1)
            try:
                logger.log("[Debug] Attemping to download "+url[1])
                urllib.request.urlretrieve(url[1], "image.jpg")
            except Exception as e1:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
        elif type == 'photo':
            try:
                photo_array = msg['reply_to_message']['photo']
                logger.log("[Debug] File_id to set:"+str(photo_array))
            except KeyError:
                dre = await bot.sendMessage(
                    chat_id, langport['reply_not_pic'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                await bot.sendChatAction(chat_id, 'upload_photo')
                photo_array.reverse()
                file = await bot.getFile(photo_array[0]['file_id'])['file_path']
                urllib.request.urlretrieve(
                    "https://api.telegram.org/file/bot"+config.TOKEN+"/"+file, "image.jpg")
        with open(os.getcwd()+"/image.jpg", 'rb') as fo:
            try:
                await bot.setChatPhoto(chat_id, fo)
            except telepot.exception.TelegramError as e1:
                await bot.sendChatAction(chat_id, 'typing')
                dre = await bot.sendMessage(chat_id,
                                    langport['error'].format(
                                        '<code>'+str(e1.args)+'</code>'),
                                    parse_mode='HTML',
                                    reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                logger.clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title'] +
                            '('+str(chat_id)+') : '+str(e1.args))
            else:
                logger.clog('[Info] Sucessfully changed the Group photo in ' +
                    msg['chat']['title']+'('+str(chat_id)+')')
        os.remove('image.jpg')
        return
    async def rgp(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['rgp']
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            dre = await bot.sendMessage(chat_id,
                                langport['all_member_are_admin'],
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        if msg['from']['id'] == config.OWNERID:
            logger.clog('[Info] Owner Matched for \n[Info] ' +
                str(await bot.getChatMember(chat_id, msg['from']['id'])))
            await self.__rgp(msg, langport, chat_id)
            return
        else:
            logger.clog('[Info] Searching admins in '+msg['chat']
                ['title']+'('+str(chat_id) + ')')
            for admin in await bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                    await self.__rgp(msg, langport, chat_id)
                    return
            logger.clog('[Info] No admins matched with ' + msg['from']
                ['username']+'('+str(msg['from']['id']) + ')')
            await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])

        return
    async def __rgp(self, msg, langport, chat_id):
        try:
            await bot.deleteChatPhoto(chat_id)
        except telepot.exception.TelegramError as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                parse_mode='HTML',
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] Unable to remove the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '
                        + str(e1.args))
        else:
            logger.clog('[Info] Sucessfully removed the Group photo in ' +
                msg['chat']['title']+'('+str(chat_id)+')')
        return
grouppic = grouppicc()

async def echo(chat_id, msg):
    echotxt = msg['text'].split(' ', 1)
    try:
        dre = await bot.sendMessage(
            chat_id, echotxt[1], parse_mode='Markdown', reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    except:
        dre = await bot.sendMessage(chat_id, '/echo <String>',
                              reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def ns(chat_id, msg, txt):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['ns']
    try:
        logger.clog("[Info] Number to transfer :"+txt[2])
    except:
        dre = await bot.sendMessage(
            chat_id, langport['help'], parse_mode='Markdown', reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
        return
    if txt[1] == "todec":
        try:
            result = int(txt[2], 0)
        except Exception as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when transfering to dec in'+msg['chat']['title']+'('+str(chat_id)+') : '
                 + str(e1.args))
        else:
            logger.clog("[Info] ---> "+str(result))
            try:
                dre = await bot.sendMessage(
                    chat_id, "`"+str(result)+"`", parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            except telepot.exception.TelegramError as e1:
                dre = await bot.sendMessage(chat_id,
                                      pastebin(
                                          str(result), 'dec-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'", "")),
                                      parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tobin":
        try:
            result = bin(int(txt[2], 0))
        except Exception as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '
                 + str(e1.args))
        else:
            logger.clog("[Info] ---> "+str(result))
            try:
                dre = await bot.sendMessage(
                    chat_id, "`"+str(result)[2:]+"`", parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            except telepot.exception.TelegramError as e1:
                dre = await bot.sendMessage(chat_id,
                                      pastebin(
                                          str(result)[2:], 'bin-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'", "")),
                                      parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tooct":
        try:
            result = oct(int(txt[2], 0))
        except Exception as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '
                 + str(e1.args))
        else:
            logger.clog("[Info] ---> "+str(result))
            try:
                dre = await bot.sendMessage(
                    chat_id, "`"+str(result)[2:]+"`", parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            except telepot.exception.TelegramError as e1:
                dre = await bot.sendMessage(chat_id,
                                      pastebin(
                                          str(result)[2:], 'oct-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'", "")),
                                      parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tohex":
        try:
            result = hex(int(txt[2], 0))
        except Exception as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '
                 + str(e1.args))
        else:
            logger.clog("[Info] ---> "+str(result))
            try:
                dre = await bot.sendMessage(
                    chat_id, "`"+str(result)[2:]+"`", parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            except telepot.exception.TelegramError as e1:
                dre = await bot.sendMessage(chat_id,
                                      pastebin(
                                          str(result)[2:], 'hex-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'", "")),
                                      parse_mode='Markdown', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        dre = await bot.sendMessage(
            chat_id, langport['help'], parse_mode='Markdown', reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def ping(chat_id, msg):
    if msg['text'].startswith('/'):
        dre = await bot.sendMessage(
            chat_id, 'Pong', reply_to_message_id=msg['message_id'])
    else:
        dre = await bot.sendMessage(chat_id, msg['text'].replace('i', 'o').replace(
            'I', 'O'), reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    return

class titlec:
    async def title(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['title']
        cmd = msg['text'].split(' ', 1)
        try:
            title = cmd[1]
        except:
            if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                dre = await bot.sendMessage(
                    chat_id, langport['all_member_are_admin'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            return
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            dre = await bot.sendMessage(
                chat_id, langport['all_member_are_admin'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            if msg['from']['id'] == config.OWNERID:
                logger.clog('[Info] Owner Matched for \n[Info] ' +
                    str(await bot.getChatMember(chat_id, msg['from']['id'])))
                await self.__title(msg, chat_id, title, langport)
                return
            logger.clog('[Info] Searching admins in '+msg['chat']
                ['title']+'('+str(chat_id) + ')')
            for admin in await bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                    await self.__title(msg, chat_id, title, langport)
                    return
            logger.clog('[Info] No admins matched with ' + msg['from']
                ['username']+'('+str(msg['from']['id']) + ')')
            await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            return
        return
    async def __title(self, msg, chat_id, title, langport):
        try:
            await bot.setChatTitle(chat_id, title)
        except Exception as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                parse_mode='HTML',
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] Unable to change the Group title in '+msg['chat']['title']+'('+str(chat_id)+') : '
                + str(e1.args))
        else:
            logger.clog('[Info] Sucessfully changed the Group title in ' +
                msg['chat']['title']+'('+str(chat_id)+')')
        return
title = titlec()

async def lsadmins(chat_id, msg, cmd):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['lsadmins']
    await bot.sendChatAction(chat_id, "typing")
    try:
        group = cmd[1]
    except IndexError:
        group = chat_id
    else:
        try:
            await bot.getChatAdministrators(group)
        except telepot.exception.TelegramError as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when getting group'+group + ' : '
                 + str(e1.args))
            group = chat_id
    target_group = await bot.getChat(group)
    group_type = target_group['type']
    logger.log("[Debug] Group type: "+group_type)
    adminmsg = target_group['title']
    logger.log("[Debug] Raw admins data:"+str(await bot.getChatAdministrators(group)))
    for admin in await bot.getChatAdministrators(group):
        if admin['status'] == "creator":
            firstname = admin['user']['first_name']
            try:
                lastname = admin['user']['last_name']
            except KeyError:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + \
                    admin['user']['username'] + '">' + \
                    firstname + ' ' + lastname+'</a>'
            except KeyError:
                nickname = firstname + ' ' + lastname
            adminmsg += "\n" + \
                langport['creator'].format(nickname)+"\n"
            if group_type == 'group' and target_group['all_members_are_administrators'] == True:
                adminmsg += '\n'+langport['everyone_is_admin']
    for admin in await bot.getChatAdministrators(group):
        adminmsg += '\n'
        if admin['status'] == "administrator":
            firstname = admin['user']['first_name']
            try:
                lastname = admin['user']['last_name']
            except KeyError:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + \
                    admin['user']['username'] + '">' + \
                    firstname + ' ' + lastname+'</a>'
            except KeyError:
                nickname = firstname + ' ' + lastname
            if group_type == 'supergroup':
                if admin['can_change_info'] == True:
                    adminmsg += "ℹ️"
                else:
                    adminmsg += "🌚"
                if admin['can_delete_messages'] == True:
                    adminmsg += "🗑️"
                else:
                    adminmsg += "🌚"
                if admin['can_restrict_members'] == True:
                    adminmsg += "🚫"
                else:
                    adminmsg += "🌚"
                if admin['can_pin_messages'] == True:
                    adminmsg += "📌"
                else:
                    adminmsg += "🌚"
                if admin['can_promote_members'] == True:
                    adminmsg += "👮‍♀️"
                else:
                    adminmsg += "🌚"
                if admin['can_invite_users'] == True:
                    adminmsg += "➕ "
                else:
                    adminmsg += "🌚 "
            else:
                adminmsg += langport['admin_badge']+" - "
            adminmsg += nickname
    dre = await bot.sendMessage(chat_id, adminmsg, parse_mode='HTML',
                          disable_web_page_preview=True, reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    print('[Info]Admin list for ', target_group['title'],
          ' ( ', str(target_group['id']), ' ): ')
    logger.clog("[Info]")
    logger.clog(adminmsg)
    return

async def groupinfo(chat_id, msg, chat_type):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['groupinfo']
    dre = await bot.sendMessage(chat_id,
                          langport['grouptype'].format(chat_type)+"\n" +
                          langport['groupname'].format(msg['chat']['title'])+"\n" +
                          langport['groupcount'].format(str(await bot.getChatMembersCount(chat_id))) + "\n" +
                          langport['groupid'].format(
                              "<code>"+str(chat_id) + "</code>"),
                          parse_mode='HTML',
                          reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def leavegroup(chat_id, msg, chat_type):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['leavegroup']
    if msg['from']['id'] == config.OWNERID:
        logger.clog('[Info] Owner Matched for \n[Info] ' +
             str(await bot.getChatMember(chat_id, msg['from']['id'])))
        dre = await bot.sendMessage(
            chat_id, langport['farewell'], reply_to_message_id=msg['message_id'])
        await bot.leaveChat(chat_id)
        logger.log("[Debug] Raw sent data:"+str(dre))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = await bot.sendMessage(
            chat_id, langport['farewell'], reply_to_message_id=msg['message_id'])
        await bot.leaveChat(chat_id)
        logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        logger.clog('[Info] Searching admins in '+msg['chat']
             ['title']+'('+str(chat_id) + ')')
        for admin in await bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                dre = await bot.sendMessage(
                    chat_id, langport['farewell'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                await bot.leaveChat(chat_id)
                return
        logger.clog('[Info] No admins matched with ' + msg['from']
             ['username']+'('+str(msg['from']['id']) + ')')
        dre = await bot.sendMessage(
            chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
        return
    return

async def a2zc(chat_id, msg):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['a2z']
    try:
        reply_to = msg['reply_to_message']
    except:
        alpt = msg['text'].split(' ', 1)
        try:
            tcm = alpt[1]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            temp = tcm.split(' ', 1)
            if temp[0] == 'etan':
                string = a2z_etan(temp[1])
            else:
                string = a2z(tcm)
            dre = await bot.sendMessage(
                chat_id, string, reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[A2Z] --->'+string)
    else:
        cmd = msg['text'].split(' ', 1)
        try:
            tcm = reply_to['text']
        except KeyError:
            try:
                tcm = reply_to['caption']
            except KeyError:
                dre = await bot.sendMessage(
                    chat_id, langport['not_text'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                temp = cmd[1]
            except IndexError:
                string = a2z(tcm)
            else:
                if temp == 'etan':
                    string = a2z_etan(tcm)
                else:
                    string = a2z(tcm)
            dre = await bot.sendMessage(
                chat_id, string, reply_to_message_id=reply_to['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[A2Z] --->'+string)
    return

class userc:
    async def getuser(self, chat_id, msg, txt):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['getuser']
        try:
            reply_to = msg['reply_to_message']
        except KeyError:
            try:
                uuser_id = int(txt[1])
            except IndexError:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], parse_mode='HTML', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                await self.__getuser(chat_id, uuser_id, msg, langport)
        else:
            try:
                cmd = txt[1]
            except IndexError:
                uuser_id = reply_to['from']['id']
            else:
                if cmd == 'forward':
                    try:
                        uuser_id = reply_to['forward_from']['id']
                    except KeyError:
                        uuser_id = reply_to['from']['id']
                else:
                    uuser_id = reply_to['from']['id']
            await self.__getuser(chat_id, uuser_id, msg, langport)
        return

    async def getme(self, chat_id, msg):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['getuser']
        await self.__getuser(chat_id, msg['from']['id'], msg, langport)
        return

    async def __getuser(self, chat_id, uuser_id, msg, langport):
        try:
            user = await bot.getChatMember(chat_id, uuser_id)
        except telepot.exception.TelegramError as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                parse_mode='HTML',
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] ERROR when getting user'+str(uuser_id) + 'in'+msg['chat']['title']+'('+str(chat_id)+') : '
                + str(e1.args))
        else:
            firstname = user['user']['first_name']
            try:
                lastname = user['user']['last_name']
            except KeyError:
                lastname = ''
            try:
                uusername = '@' + user['user']['username']
                nickname = '<a href="https://t.me/' + \
                    user['user']['username'] + '">' + \
                    firstname + ' ' + lastname+'</a>'
            except KeyError:
                uusername = 'Undefined'
                nickname = firstname + ' ' + lastname
            userid = str(user['user']['id'])
            dre = await bot.sendMessage(chat_id,
                                langport['nick'].format(nickname) + '\n' +
                                langport['username'].format(uusername) + '\n' +
                                langport['userid'].format('<code>' + userid + '</code>') + '\n' +
                                langport['status'].format(user['status']), parse_mode='HTML', reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        return
user = userc()

class pinc:
    async def pin(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['pin']
        try:
            reply_to = msg['reply_to_message']
        except:
            dre = await bot.sendMessage(
                chat_id, langport['reply_help'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            if chat_type == 'group':
                dre = await bot.sendMessage(
                    chat_id, langport['group'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                if msg['from']['id'] == config.OWNERID:
                    logger.clog('[Info] Owner Matched for \n[Info] ' +
                        str(await bot.getChatMember(chat_id, msg['from']['id'])))
                    await self.__pin(chat_id, reply_to, langport, msg)
                    return
                logger.clog('[Info] Searching admins in '+msg['chat']
                    ['title']+'('+str(chat_id) + ')')
                for admin in await bot.getChatAdministrators(chat_id):
                    if msg['from']['id'] == admin['user']['id']:
                        logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                        await self.__pin(chat_id, reply_to, langport, msg)
                        return
                logger.clog('[Info] No admins matched with ' + msg['from']
                    ['username']+'('+str(msg['from']['id']) + ')')
                dre = await bot.sendMessage(
                    chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
        return
    async def pinh(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['pin']        
        if msg['from']['id'] == config.OWNERID:
            logger.clog('[Info] Owner Matched for \n[Info] ' +
                str(await bot.getChatMember(chat_id, msg['from']['id'])))
            await self.__pin(chat_id, msg, langport, msg)
            return
        logger.clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id) + ')')
        for admin in await bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                await self.__pin(chat_id, msg, langport, msg)
                return
        logger.clog('[Info] No admins matched with ' + msg['from']
            ['username']+'('+str(msg['from']['id']) + '),ignoring...')
        return
    async def __pin(self, chat_id, reply_to, langport, msg):
        chat = await bot.getChat(chat_id)
        try:
            dre = await bot.sendMessage(
                chat_id, "#Pin #Backup", reply_to_message_id=chat['pinned_message']['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        except KeyError:
            pass
        try:
            await bot.pinChatMessage(
                chat_id, reply_to['message_id'], disable_notification=True)
        except telepot.exception.TelegramError as e1:
            await bot.sendChatAction(chat_id, 'typing')
            try:
                msg_idf = telepot.message_identifier(dre)
                await bot.deleteMessage(msg_idf)
            except NameError:
                pass
            dre = await bot.sendMessage(chat_id,
                                langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                parse_mode='HTML',
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] Unable to pin the message '+str(reply_to['message_id'])+' in '+msg['chat']
                ['title']+'('+str(chat_id)+') : '+str(e1.args))
        else:
            logger.clog('[Info] Sucessfully pinned the message '+str(reply_to['message_id']
                                                            )+' in '+msg['chat']['title']+'('+str(chat_id)+')')
        return
pin = pinc()

async def replace(chat_id, msg, cmd):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['replace']
    try:
        reply_to = msg['reply_to_message']
    except KeyError:
        dre = await bot.sendMessage(
            chat_id, langport['help_not_reply'], reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            rstring = reply_to['text']
        except KeyError:
            try:
                rstring = reply_to['caption']
            except KeyError:
                dre = await bot.sendMessage(
                    chat_id, langport['not_text'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
        try:
            test = cmd[1]
            test = cmd[2]
        except KeyError:
            dre = await bot.sendMessage(chat_id, langport['help'],
                                  parse_mode='Markdown', reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                if cmd[2] == "''":
                    rstring = rstring.replace(cmd[1], '')
                else:
                    rstring = rstring.replace(cmd[1], cmd[2])
            except IndexError:
                tp, val, tb = sys.exc_info()
                await bot.sendChatAction(chat_id, 'typing')
                dre = await bot.sendMessage(chat_id,
                                      langport['error'].format(str(val).split(
                                          ',')[0].replace('(', '').replace("'", "`")),
                                      parse_mode='Markdown',
                                      reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                logger.clog('[ERROR] ERROR when replacing '+cmd[1]+' to ' + cmd[2]+msg['chat']['title']+'('+str(chat_id)+') : '
                     + str(val).split(',')[0].replace('(', '').replace("'", ""))
            else:
                fuser = msg['from']
                fnick = fuser['first_name']
                try:
                    fnick = fnick + ' ' + fuser['last_name']
                except KeyError:
                    fnick = fnick
                tuser = msg['reply_to_message']['from']
                tnick = tuser['first_name']
                try:
                    tnick = tnick + ' ' + tuser['last_name']
                except KeyError:
                    tnick = tnick
                if fuser['id'] == tuser['id']:
                    smsg = langport['result_self'].format(
                        '<a href="tg://user?id='+str(tuser['id'])+'">'+tnick+'</a>', '<i>'+rstring + '</i>')
                else:
                    smsg = langport['result'].format('<a href="tg://user?id='+str(fuser['id'])+'">'+fnick+'</a>',
                                                     '<a href="tg://user?id='+str(tuser['id'])+'">'+tnick+'</a>', '<i>'+rstring + '</i>')
                dre = await bot.sendMessage(
                    chat_id, smsg, parse_mode="HTML", reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def getfile(chat_id, msg, cmd):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['getfile']
    await bot.sendChatAction(chat_id, "upload_document")
    try:
        file_id = cmd[1]
    except IndexError:
        dre = await bot.sendMessage(
            chat_id, langport['help'], reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            file = await bot.getFile(file_id)
            logger.log("[Debug] Raw get data:"+str(file))
        except telepot.exception.TelegramError as e1:
            dre = await bot.sendMessage(chat_id,
                                  langport['error'].format(
                                      "<code>"+str(e1.args)+"</code>"),
                                  parse_mode='HTML',
                                  reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] Unable to fetch the file '+file_id+'  : ' +
                 str(e1.args))
        else:
            type = file['file_path'].split("/")
            try:
                if type[0] == 'photos':
                    dre = await bot.sendPhoto(
                        chat_id, file_id, reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                elif type[0] == 'voice':
                    dre = await bot.sendVoice(
                        chat_id, file_id, reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                elif type[0] == 'videos':
                    dre = await bot.sendVideo(
                        chat_id, file_id, reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                else:
                    dre = await bot.sendDocument(
                        chat_id, file_id, reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
            except telepot.exception.TelegramError as e1:
                dre = await bot.sendMessage(chat_id,
                                      langport['senderror'].format(
                                          '<code>'+str(e1.args)+"</code>"),
                                      parse_mode='HTML',
                                      reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                logger.clog('[ERROR] Unable to send the file '+file_id+'  : ' +
                     str(e1.args))
    return

async def fileinfo(chat_id, msg):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['fileinfo']
    try:
        reply_to = msg['reply_to_message']
    except KeyError:
        dre = await bot.sendMessage(
            chat_id, langport['help'], reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        tcontent_type, tchat_type, tchat_id = telepot.glance(reply_to)
        if tcontent_type == 'text':
            dre = await bot.sendMessage(
                chat_id, lang['istext'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        elif tcontent_type == 'photo':
            photo_array = reply_to['photo']
            photo_array.reverse()
            fileid = photo_array[0]['file_id']
        elif tcontent_type == 'audio':
            fileid = reply_to['audio']['file_id']
        elif tcontent_type == 'document':
            fileid = reply_to['document']['file_id']
        elif tcontent_type == 'video':
            fileid = reply_to['video']['file_id']
        elif tcontent_type == 'voice':
            fileid = reply_to['voice']['file_id']
        elif tcontent_type == 'sticker':
            fileid = reply_to['sticker']['file_id']
        dre = await bot.sendMessage(chat_id,
                              langport['filetype'].format(tcontent_type)+"\n" +
                              langport['fileid'].format(
                                  '<code>'+fileid+"</code>"),
                              parse_mode="HTML", reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def exportblog(chat_id, msg):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['exportblog']
    cmd = msg['text'].split(" ", 1)
    try:
        debugs = cmd[1]
    except:
        if msg['from']['id'] == config.OWNERID:
            f = open(logger.logpath+".log", "rb")
            dre = await bot.sendDocument(
                chat_id, f, reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            f.close()
        else:
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
    else:
        if msg['from']['id'] == config.OWNERID:
            if config.Debug == True and debugs == "-debug":
                f = open(logger.logpath+"-debug.log", "rb")
                dre = await bot.sendDocument(
                    chat_id, f, reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                f.close()
            else:
                if config.Debug == False and debugs == "-debug":
                    dre = await bot.sendMessage(
                        chat_id, langport['debug_off'], reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                elif config.Debug == True and debugs != "-debug":
                    dre = await bot.sendMessage(
                        chat_id, langport['debug'], reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                f = open(logger.logpath+".log", "rb")
                dre = await bot.sendDocument(
                    chat_id, f, reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                f.close()
        else:
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
    return

class tagc:
    def readtag(self):
        logger.clog("[Info] Reading tag data...")
        if os.path.isfile("./tagdata.json") == False:
            with open("./tagdata.json", "w") as fs:
                fs.write("{}")
        try:
            with open("./tagdata.json", "r") as fs:
                data = json.load(fs) 
        except json.decoder.JSONDecodeError as e1:
            logger.clog("[Error] Can't load tagdata.json: JSON decode error:"+ str(e1.args)+ "\n[Info] Trying to read using python format.")
            try:
                with open("./tagdata.json", "r") as fs:
                    data = eval(fs.read())
            except Exception as e1:
                logger.clog("[Error] Can't load tagdata.json: "+ str(e1.args)+ "\n\n[Info] Try fix the data or reset the data.")
                exit()
            else:
                logger.clog("[Info] Converting to json format...")
                with open("./tagdata.json.bak", "w") as fs:
                    fs.write(str(data))
                with open("./tagdata.json", "w") as fs:
                    json.dump(data, fs, indent=2)
                logger.clog("[Info] Reloading...")
                with open("./tagdata.json", "r") as fs:
                    data = json.load(fs) 
                
        return(data)

    def writetag(self, data):
        logger.clog("[Info] Writing tag data...")
        with open("./tagdata.json", "w") as fs:
            json.dump(data,fs,indent=2)
        return

    async def addtag(self, chat_id, msg, cmd):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['add']
        try:
            reply_to = msg['reply_to_message']
        except KeyError:
            data = self.readtag()
            try:
                temptaglist = data[str(chat_id)][cmd[2]]
            except KeyError:
                temptaglist = []
            except IndexError:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            try:
                grouptagdict = data[str(chat_id)]
            except KeyError:
                grouptagdict = {}
            try:
                tagname = cmd[2]
            except IndexError:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                try:
                    testcmduser = cmd[3]
                except IndexError:
                    dre = await bot.sendMessage(
                        chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                else:
                    successmsg = langport['b_success'].format(
                        "<b>" + tagname + "</b>")+"\n"
                    successcount = 0
                    errmsg = langport['b_error'].format(
                        "<b>" + tagname + "</b>")+"\n"
                    errcount = 0
                    if len(cmd) >= 54:
                        dre = await bot.sendMessage(chat_id, langport['too_many'], parse_mode="HTML",
                                            disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        cmd = cmd[0:53]
                    await bot.sendChatAction(chat_id, "typing")
                    for a in cmd[3:]:
                        try:
                            adduser = await bot.getChatMember(chat_id, int(a))
                        except telepot.exception.TelegramError as e1:
                            logger.clog("[ERROR] Errored when getting user " + a + " :" +
                                str(e1.args))
                            errmsg = errmsg + "<b>" + a + "</b> : <code>" + \
                                str(e1.args)+"</code>\n"
                            errcount += 1
                            continue
                        else:
                            if int(a) in temptaglist:
                                logger.clog("[ERROR] Errored when adding user " + a +
                                    " to "+tagname+" :The user is already in the list")
                                errmsg = errmsg + "<b>" + a + "</b> : <code>" + \
                                    langport['already_exist']+"</code>\n"
                                errcount += 1
                                continue
                            else:
                                temptaglist.append(int(a))
                            firstname = adduser['user']['first_name']
                            try:
                                lastname = adduser['user']['last_name']
                            except KeyError:
                                lastname = ''
                            try:
                                nickname = '<a href="https://t.me/' + \
                                    adduser['user']['username'] + '">' + \
                                    firstname + ' ' + lastname+'</a>'
                            except KeyError:
                                nickname = firstname + ' ' + lastname
                            successmsg = successmsg + nickname + "\n"
                            successcount += 1
                            logger.clog("[Info] " + firstname + ' ' +
                                lastname + " was added to "+tagname)
                    grouptagdict[tagname] = temptaglist
                    if len(grouptagdict[tagname]) == 0:
                        del grouptagdict[tagname]
                    data[str(chat_id)] = grouptagdict
                    self.writetag(data)
                    successmsg = successmsg + "\n"
                    errmsg = errmsg + "\n"
                    if successcount == 0:
                        successmsg = ""
                    if errcount == 0:
                        errmsg = ""
                    dre = await bot.sendMessage(chat_id, successmsg+errmsg, parse_mode="HTML",
                                        disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            data = self.readtag()
            try:
                temptaglist = data[str(chat_id)][cmd[2]]
            except KeyError:
                temptaglist = []
            try:
                grouptagdict = data[str(chat_id)]
            except KeyError:
                grouptagdict = {}
            smsg = ""
            userid = reply_to['from']['id']
            try:
                adduser = await bot.getChatMember(chat_id, userid)
            except telepot.exception.TelegramError as e1:
                logger.clog("[ERROR] Errored when getting user " + str(userid) +
                    " :"+str(e1.args))
                smsg = langport['r_error'].format("<b>" + str(userid) + "</b>", "<b>" + cmd[2] + "</b>", "<code>"+str(
                    e1.args)+"</code>")+"\n"
                dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                    disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                if userid in temptaglist:
                    logger.clog("[ERROR] Errored when adding user " + str(userid) +
                        " to "+cmd[2]+" :The user is already in the list")
                    smsg = langport['r_error'].format(
                        "<b>" + str(userid) + "</b>", "<b>" + cmd[2] + "</b>", "<code>"+langport['already_exist']+"</code>")+"\n"
                    dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                        disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                else:
                    temptaglist.append(userid)
                firstname = adduser['user']['first_name']
                try:
                    lastname = adduser['user']['last_name']
                except KeyError:
                    lastname = ''
                try:
                    nickname = '<a href="https://t.me/' + \
                        adduser['user']['username'] + '">' + \
                        firstname + ' ' + lastname+'</a>'
                except KeyError:
                    nickname = firstname + ' ' + lastname
                smsg = smsg + \
                    langport['r_success'].format(nickname, "<b>" + cmd[2] + "</b>")
                logger.clog("[Info] " + firstname + ' ' +
                    lastname + " was added to "+cmd[2])
            grouptagdict[cmd[2]] = temptaglist
            if len(grouptagdict[cmd[2]]) == 0:
                del grouptagdict[cmd[2]]
            data[str(chat_id)] = grouptagdict
            self.writetag(data)
            dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def rmtag(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['remove']
        try:
            reply_to = msg['reply_to_message']
        except:
            data = self.readtag()
            try:
                temptaglist = data[str(chat_id)][cmd[2]]
            except KeyError:
                temptaglist = []
            except IndexError:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            try:
                grouptagdict = data[str(chat_id)]
            except KeyError:
                grouptagdict = {}
            try:
                tagname = cmd[2]
            except IndexError:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                if tagname == "*":
                    global confirmsg
                    if grouptagdict == {}:
                        dre = await bot.sendMessage(chat_id, langport['no_list'], parse_mode="HTML",
                                            disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        return
                    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                        dre = await bot.sendMessage(chat_id, langport['remove_all']['warn'], parse_mode="HTML",
                                            disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        confirmsg = dre
                        return
                    else:
                        if msg['from']['id'] == config.OWNERID:
                            logger.clog('[Info] Owner Matched for \n[Info] ' +
                                str(await bot.getChatMember(chat_id, msg['from']['id'])))
                            dre = await bot.sendMessage(chat_id, langport['remove_all']['warn'], parse_mode="HTML",
                                                disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                            confirmsg = dre
                            logger.log("[Debug] Raw sent data:"+str(dre))
                            return
                        logger.clog('[Info] Searching admins in '+msg['chat']
                            ['title']+'('+str(chat_id) + ')')
                        for admin in await bot.getChatAdministrators(chat_id):
                            if msg['from']['id'] == admin['user']['id']:
                                logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                                dre = await bot.sendMessage(chat_id, langport['remove_all']['warn'], parse_mode="HTML",
                                                    disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                                confirmsg = dre
                                logger.log("[Debug] Raw sent data:"+str(dre))
                                return
                        logger.clog('[Info] No admins matched with ' + msg['from']
                            ['username']+'('+str(msg['from']['id']) + ')')
                        dre = await bot.sendMessage(
                            chat_id, langport['remove_all']['no_perm'], reply_to_message_id=msg['message_id'])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        return
                try:
                    testcmduser = cmd[3]
                except IndexError:
                    dre = await bot.sendMessage(
                        chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                else:
                    if testcmduser == "*":
                        if temptaglist == []:
                            logger.clog("[ERROR] List "+cmd[2] + "not found.")
                            dre = await bot.sendMessage(chat_id, langport['list_not_exist'].format(
                                "<b>"+cmd[2]+"</b>"), parse_mode="HTML", disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                            logger.log("[Debug] Raw sent data:"+str(dre))
                            return
                        del grouptagdict[cmd[2]]
                        logger.clog("[Info] Cleared the list "+cmd[2])
                        data[str(chat_id)] = grouptagdict
                        self.writetag(data)
                        dre = await bot.sendMessage(chat_id, langport['list_removed'].format(
                            "<b>"+cmd[2]+"</b>"), parse_mode="HTML", disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        return
                    successmsg = langport['b_success'].format(
                        "<b>" + cmd[2] + "</b>")+"\n"
                    successcount = 0
                    errmsg = langport['b_error'].format(
                        "<b>" + cmd[2] + "</b>")+":\n"
                    errcount = 0
                    if len(cmd) >= 54:
                        dre = await bot.sendMessage(chat_id, langport['too_many'], parse_mode="HTML",
                                            disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        cmd = cmd[0:53]
                    await bot.sendChatAction(chat_id, "typing")
                    for a in cmd[3:]:
                        try:
                            rmuser = await bot.getChatMember(chat_id, int(a))
                        except telepot.exception.TelegramError as e1:
                            if int(a) in temptaglist:
                                temptaglist.remove(int(a))
                                successmsg = successmsg + langport['User_Not_Found'].format(a) + "\n"
                                successcount += 1
                            else:
                                logger.clog("[ERROR] Errored when getting user " + a + " :" +
                                    str(e1.args))
                                errmsg = errmsg + "<b>" + a + "</b> : <code>" + \
                                    str(e1.args)+"</code>\n"
                                errcount += 1
                        else:
                            if int(a) in temptaglist:
                                temptaglist.remove(int(a))
                            else:
                                logger.clog("[ERROR] Errored when removing user " + a +
                                    " from "+cmd[2]+" :The user is not in the list")
                                errmsg = errmsg + "<b>" + a + "</b> : <code>" + \
                                    langport['not_in_list']+"</code>\n"
                                errcount += 1
                                continue
                            firstname = rmuser['user']['first_name']
                            try:
                                lastname = rmuser['user']['last_name']
                            except KeyError:
                                lastname = ''
                            try:
                                nickname = '<a href="https://t.me/' + \
                                    rmuser['user']['username'] + '">' + \
                                    firstname + ' ' + lastname+'</a>'
                            except KeyError:
                                nickname = firstname + ' ' + lastname
                            successmsg = successmsg + nickname + "\n"
                            successcount += 1
                            logger.clog("[Info] " + firstname + ' ' +
                                lastname + " was removed from "+cmd[2])
                    grouptagdict[cmd[2]] = temptaglist
                    if len(grouptagdict[cmd[2]]) == 0:
                        del grouptagdict[cmd[2]]
                    data[str(chat_id)] = grouptagdict
                    self.writetag(data)
                    successmsg = successmsg + "\n"
                    errmsg = errmsg + "\n"
                    if successcount == 0:
                        successmsg = ""
                    if errcount == 0:
                        errmsg = ""
                    dre = await bot.sendMessage(chat_id, successmsg+errmsg, parse_mode="HTML",
                                        disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            data = self.readtag()
            try:
                temptaglist = data[str(chat_id)][cmd[2]]
            except KeyError:
                temptaglist = []
            try:
                grouptagdict = data[str(chat_id)]
            except KeyError:
                grouptagdict = {}
            smsg = ""
            userid = reply_to['from']['id']
            try:
                adduser = await bot.getChatMember(chat_id, userid)
            except telepot.exception.TelegramError as e1:
                logger.clog("[ERROR] Errored when getting user " + str(userid) +
                    " :"+str(e1.args))
                smsg = langport['r_error'].format("<b>" + userid + "</b>", "<b>" + cmd[2] + "</b>", "<code>"+str(
                    e1.args)+"</code>")+"\n"
                dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                    disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                if userid in temptaglist:
                    temptaglist.remove(userid)
                else:
                    logger.clog("[ERROR] Errored when remving user " + str(userid) +
                        " from "+cmd[2]+" :The user is not in the list")
                    smsg = langport['r_error'].format(
                        "<b>" + str(userid) + "</b>", "<b>" + cmd[2] + "</b>", "<code>"+langport['not_in_list']+"</code>")+"\n"
                    dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                        disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                firstname = adduser['user']['first_name']
                try:
                    lastname = adduser['user']['last_name']
                except KeyError:
                    lastname = ''
                try:
                    nickname = '<a href="https://t.me/' + \
                        adduser['user']['username'] + '">' + \
                        firstname + ' ' + lastname+'</a>'
                except KeyError:
                    nickname = firstname + ' ' + lastname
                smsg = smsg + \
                    langport['r_success'].format(nickname, "<b>" + cmd[2] + "</b>")
                logger.clog("[Info] " + firstname + ' ' +
                    lastname + " was removed from "+cmd[2])
            grouptagdict[cmd[2]] = temptaglist
            if len(grouptagdict[cmd[2]]) == 0:
                del grouptagdict[cmd[2]]
            data[str(chat_id)] = grouptagdict
            self.writetag(data)
            dre = await bot.sendMessage(chat_id, smsg, parse_mode="HTML",
                                disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def confirm(self, chat_id, msg):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['confirm']
        username = bot_me.username.replace(' ', '')
        try:
            reply_to = msg['reply_to_message']
        except KeyError:
            dre = await bot.sendMessage(chat_id, langport['donotknow_confirmabout'],
                                disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            global confirmsg
            rreplyto = confirmsg['reply_to_message']
            if confirmsg == None:
                dre = await bot.sendMessage(chat_id, langport['donotknow_confirmabout'],
                                    disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            if reply_to["message_id"] == confirmsg["message_id"]:
                if msg['from']['id'] != rreplyto['from']['id']:
                    dre = await bot.sendMessage(chat_id, langport['donotknow_confirmabout'],
                                        disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                ccmd = rreplyto['text'].split()
                if ccmd[0] == '/tag' or ccmd[0] == '/tag@'+username:
                    if ccmd[1] == 'remove' and ccmd[2] == "*":
                        data = self.readtag()
                        del data[str(chat_id)]
                        self.writetag(data)
                        dre = await bot.sendMessage(chat_id, langport['remove_all_success'], disable_web_page_preview=True,
                                            reply_to_message_id=rreplyto["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        confirmsg = None
            else:
                dre = await bot.sendMessage(chat_id, langport['donotknow_confirmabout'],
                                    disable_web_page_preview=True, reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return

        return

    async def lstag(self, chat_id, msg, cmd):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['lstag']
        data = self.readtag()
        smsg = ""
        try:
            grouptagdict = data[str(chat_id)]
        except KeyError:
            dre = await bot.sendMessage(
                chat_id, langport['no_list'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        try:
            listname = cmd[2]
        except IndexError:
            for ttag in grouptagdict:
                temptaglist = grouptagdict[ttag]
                smsg+= \
                    langport['all'].format(
                        "<b>"+ttag+"</b>", "<b>" + str(len(temptaglist)) + "</b>")+"\n"
        else:
            try:
                temptaglist = grouptagdict[listname]
            except KeyError:
                dre = await bot.sendMessage(chat_id, langport['list_not_exist'].format(
                    "<b>"+listname+"</b>"), parse_mode="HTML", reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                smsg+= langport['list_prefix'].format(
                    "<b>"+listname+"</b>", "<b>" + str(len(temptaglist)) + "</b>")+"\n"
                count = 0
                for userid in temptaglist:
                    try:
                        adduser = await bot.getChatMember(chat_id, int(userid))
                    except telepot.exception.TelegramError:
                        smsg += langport['User_Not_Found'].format(userid)
                    else:
                        firstname = adduser['user']['first_name']
                        try:
                            lastname = adduser['user']['last_name']
                        except KeyError:
                            lastname = ''
                        try:
                            nickname = '<a href="https://t.me/' + \
                                adduser['user']['username'] + '">' + \
                                firstname + ' ' + lastname+'</a>'
                        except KeyError:
                            nickname = firstname + ' ' + lastname
                        smsg+= nickname + " "
                    count = count + 1
                    if count >= 2:
                        smsg += "\n"
                        count = 0
        dre = await bot.sendMessage(chat_id, smsg, disable_web_page_preview=True,
                            parse_mode="HTML", reply_to_message_id=msg["message_id"])
        logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def tags(self, chat_id, msg, cmd):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['tag']
        data = self.readtag()
        smsg = ""
        emsg = ""
        try:
            listname = cmd[2]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                temptaglist = data[str(chat_id)][listname]
            except KeyError:
                dre = await bot.sendMessage(chat_id, langport['list_not_exist'].format(
                    "<b>"+listname+"</b>"), parse_mode="HTML", reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                if temptaglist == []:
                    dre = await bot.sendMessage(chat_id, langport['list_not_exist'].format(
                        "<b>"+listname+"</b>"), parse_mode="HTML", reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                dre = await bot.sendMessage(chat_id, langport['tag_prefix'].format("<b>"+listname+"</b>", "<b>"+str(
                    len(temptaglist))+"</b>"), parse_mode="HTML", reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
                totalcount = 0
                errcount = 0
                for userid in temptaglist:
                    try:
                        await bot.getChatMember(chat_id, int(userid))
                    except telepot.exception.TelegramError as e1:
                        emsg += langport['user_fetch_fail'].format(str(userid), '<code>'+str(e1.args)+'</code>') + '\n'
                        errcount += 1
                    else:
                        smsg = smsg + "[.](tg://user?id="+str(userid)+")"
                        totalcount += 1
                    if totalcount >= 5:
                        dre = await bot.sendMessage(chat_id, smsg, parse_mode="Markdown")
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        smsg = ""
                        totalcount = 0
                if totalcount != 0:
                    dre = await bot.sendMessage(chat_id, smsg, parse_mode="Markdown")
                    logger.log("[Debug] Raw sent data:"+str(dre))
                if errcount != 0:
                    dre = await bot.sendMessage(chat_id, emsg, parse_mode="HTML")
                    logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def tag_admin(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['tagadmin']
        if chat_type == "group" and msg['chat']['all_members_are_administrators'] == True:
            dre = await bot.sendMessage(
                chat_id, langport['all_member_are_admin'], parse_mode="HTML", reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        admin_list = await bot.getChatAdministrators(chat_id)
        dre = await bot.sendMessage(chat_id, langport['tag_prefix'].format(
            "<b>"+str(len(admin_list))+"</b>"), parse_mode="HTML", reply_to_message_id=msg["message_id"])
        logger.log("[Debug] Raw sent data:"+str(dre))
        smsg = ""
        totalcount = 0
        for admin in admin_list:
            smsg = smsg + "[.](tg://user?id="+str(admin['user']['id'])+")"
            totalcount = totalcount+1
            if totalcount >= 5:
                dre = await bot.sendMessage(chat_id, smsg, parse_mode="Markdown")
                logger.log("[Debug] Raw sent data:"+str(dre))
                smsg = ""
                totalcount = 0
        if totalcount != 0:
            dre = await bot.sendMessage(chat_id, smsg, parse_mode="Markdown")
            logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def tag(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['tag']['general']
        try:
            subcmd = cmd[1]
        except:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            if subcmd == "add":
                await self.addtag(chat_id, msg, cmd)
            elif subcmd == "remove":
                await self.rmtag(chat_id, msg, cmd, chat_type)
            elif subcmd == "list":
                await self.lstag(chat_id, msg, cmd)
            elif subcmd == "tag":
                await self.tags(chat_id, msg, cmd)
            elif subcmd == "all":
                dre = await bot.sendMessage(
                    chat_id, langport['PWRAPI'], parse_mode='Markdown', reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
            elif subcmd == "admin":
                await self.tag_admin(chat_id, msg, chat_type)
            else:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))

        return
tag = tagc()

class exportChatLink:
    async def exportchatlink(self, chat_id, msg, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['exportchatlink']
        if msg['from']['id'] == config.OWNERID:
            logger.clog('[Info] Owner Matched for \n[Info] ' +
                str(await bot.getChatMember(chat_id, msg['from']['id'])))
            await self.__export(chat_id, msg, langport)
            return
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            logger.clog('[Info] Detected a group with all members are admin enabled.')
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            logger.clog('[Info] Searching admins in '+msg['chat']
                ['title']+'('+str(chat_id) + ')')
            for admin in await bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    logger.clog(
                        '[Info] Admin Matched for \n[Info] ' + str(admin))
                    await self.__export(chat_id, msg, langport)
                    return
            logger.clog('[Info] No admins matched with ' + msg['from']
                ['username']+'('+str(msg['from']['id']) + ')')
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        return
    async def __export(self, chat_id, msg, langport):
        try:
            link = await bot.exportChatInviteLink(chat_id)
        except telepot.exception.TelegramError as e1:
            await bot.sendChatAction(chat_id, 'typing')
            dre = await bot.sendMessage(chat_id,
                                langport['error'].format('<code>'+str(e1.args)+'</code>'),
                                parse_mode='HTML',
                                reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            logger.clog('[ERROR] Unable to export chat link in '+msg['chat']
                ['title']+'('+str(chat_id)+') : '+str(e1.args))
        else:
            await bot.sendMessage(
                chat_id, link, reply_to_message_id=msg['message_id'])
            logger.clog('[Info] Exported chat link: {0}'.format(link))
        return
ecl = exportChatLink()

class delmsgc:
    async def delmsg(self, chat_id, msg, chat_type):
        global delete_msg_sender
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['delmsg']
        try:
            reply_to_message = msg['reply_to_message']
        except KeyError:
            dre = await bot.sendMessage(
                chat_id, langport['no_reply'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                tmp = delete_msg_sender[chat_id]
            except KeyError:
                delete_msg_sender[chat_id] = {}
            if chat_type == "private":
                markup = self.__inlinekeyboardbutton(chat_id)
                dre = await bot.sendMessage(chat_id, langport['confirm'], reply_markup=markup,
                                    parse_mode="HTML", reply_to_message_id=reply_to_message["message_id"])
                delete_msg_sender[chat_id][dre['message_id']] = msg
                logger.log("[Debug] Raw sent data:"+str(dre))
            elif chat_type == 'group' or chat_type == 'supergroup':
                if msg['from']['id'] == config.OWNERID:
                    logger.clog('[Info] Owner Matched for \n[Info] ' +
                        str(await bot.getChatMember(chat_id, msg['from']['id'])))
                    await self.__del(reply_to_message, msg, chat_id, langport, chat_type)
                    return
                if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                    logger.clog(
                        '[Info] Detected a group with all members are admin enabled.')
                    dre = await bot.sendMessage(
                        chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                else:
                    logger.clog('[Info] Searching admins in '+msg['chat']
                        ['title']+'('+str(chat_id) + ')')
                    for admin in await bot.getChatAdministrators(chat_id):
                        if msg['from']['id'] == admin['user']['id']:
                            logger.clog(
                                '[Info] Admin Matched for \n[Info] ' + str(admin))
                            await self.__del(reply_to_message, msg, chat_id, langport, chat_type)
                            return
                    logger.clog('[Info] No admins matched with ' + msg['from']
                        ['username']+'('+str(msg['from']['id']) + ')')
                    dre = await bot.sendMessage(
                        chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
        return

    async def __del(self, reply_to_message, msg, chat_id, langport, chat_type):
        if reply_to_message['from']['id'] == msg['from']['id']:
            dre = await bot.sendMessage(
                chat_id, langport['deleting_self_msg'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        elif reply_to_message['from']['id'] == bot_me.id:
            markup = self.__inlinekeyboardbutton(chat_id)
            dre = await bot.sendMessage(chat_id, langport['confirm'], reply_markup=markup,
                                parse_mode="HTML", reply_to_message_id=reply_to_message["message_id"])
            delete_msg_sender[chat_id][dre['message_id']] = msg
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                dre = await bot.sendMessage(
                    chat_id, langport['all_member_are_admin'], reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
                return
            for admin in await bot.getChatAdministrators(chat_id):
                if bot_me.id == admin['user']['id']:
                    if chat_type == 'supergroup':
                        if admin['can_delete_messages']:
                            markup = self.__inlinekeyboardbutton(
                                chat_id)
                            dre = await bot.sendMessage(
                                chat_id, langport['confirm'], reply_markup=markup, parse_mode="HTML", reply_to_message_id=reply_to_message["message_id"])
                            delete_msg_sender[chat_id][dre['message_id']] = msg
                            logger.log("[Debug] Raw sent data:"+str(dre))
                            return
                        else:
                            dre = await bot.sendMessage(
                                chat_id, langport['bot_no_perm'], reply_to_message_id=msg['message_id'])
                            logger.log("[Debug] Raw sent data:"+str(dre))
                            return
                    elif chat_type == 'group':
                        markup = self.__inlinekeyboardbutton(chat_id)
                        dre = await bot.sendMessage(
                            chat_id, langport['confirm'], reply_markup=markup, parse_mode="HTML", reply_to_message_id=reply_to_message["message_id"])
                        delete_msg_sender[chat_id][dre['message_id']] = msg
                        logger.log("[Debug] Raw sent data:"+str(dre))
                        return
            dre = await bot.sendMessage(
                chat_id, langport['bot_no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def confirm_delete(self, chat_id, orginal_message, query_id, message_with_inline_keyboard, from_id):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['delmsg']
        try:
            tmp = delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
        except KeyError:
            await bot.answerCallbackQuery(query_id, langport["message_expired"])
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.editMessageText(msg_idf, langport["message_expired"])
            return
        if from_id != tmp['from']['id']:
            await bot.answerCallbackQuery(query_id, langport["not_proposer"])
            return
        try:
            msg_idf = telepot.message_identifier(orginal_message)
            await bot.deleteMessage(msg_idf)
        except telepot.exception.TelegramError as e1:
            await bot.answerCallbackQuery(query_id, langport['error'].format(
                str(e1.args)))
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.editMessageText(msg_idf, langport['error'].format(
                "<code>"+str(e1.args)+"</code>"), parse_mode="HTML")
        else:
            await bot.answerCallbackQuery(query_id, langport["success"])
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.deleteMessage(msg_idf)
            try:
                msg_idf = telepot.message_identifier(tmp)
                await bot.deleteMessage(msg_idf)
            except telepot.exception.TelegramError:
                pass
            del delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
        return

    async def cancel_delete(self, chat_id, orginal_message, query_id, message_with_inline_keyboard, from_id):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['delmsg']
        try:
            tmp = delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
        except KeyError:
            await bot.answerCallbackQuery(query_id, langport["message_expired"])
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            await bot.editMessageText(msg_idf, langport["message_expired"])
            return
        if from_id != tmp['from']['id']:
            await bot.answerCallbackQuery(query_id, langport["not_proposer"])
            return
        await bot.answerCallbackQuery(query_id, langport["canceled"])
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        await bot.editMessageText(msg_idf, langport["canceled"])
        del delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
        return

    def __inlinekeyboardbutton(self, chat_id):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['delmsg']
        roll = random.randint(1, 5)
        if roll == 1:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['yes'],
                                    callback_data='confirm_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
            ])
        elif roll == 2:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='confirm_delete')],
                [InlineKeyboardButton(
                    text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
            ])
        elif roll == 3:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
            ])
        elif roll == 4:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
            ])
        elif roll == 5:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['no_'+str(random.randint(1, 4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(
                    text=langport['yes'], callback_data='confirm_delete')],
            ])
        return markup
delmsg = delmsgc()

async def gtts(chat_id, msg):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['gtts']
    cmd = msg['text'].split(' ', 2)
    try:
        clang = cmd[1]
    except IndexError:
        dre = await bot.sendMessage(
            chat_id, langport['help'], reply_to_message_id=msg["message_id"])
        logger.log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        try:
            txt = cmd[2]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            smsg = '[Link](https://translate.google.com.tw/translate_tts?ie=UTF-8&q=' + \
                txt+'&tl='+clang+'&client=tw-ob)'
            dre = await bot.sendMessage(
                chat_id, smsg, parse_mode="Markdown", reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
    return

class chatconfigc:
    def read_chatconfig(self):
        global chat_config
        logger.clog('[Info] Reading chat config data...')
        if os.path.isfile("./chatconfig.json") == False:
            with open("./chatconfig.json", "w") as fs:
                json.dump({'config_ver': HJ_Ver}, fs, indent=2)
        try:
            with open("./chatconfig.json", "r") as fs:
                chat_config = json.load(fs)
        except json.decoder.JSONDecodeError as e1:
            logger.clog("[Error] Can't load chatconfig.json: JSON decode error:"+ str(e1.args)+ "\n[Info] Trying to read using python format.")
            try:
                with open("./chatconfig.json", "r") as fs:
                    chat_config = eval(fs.read())
            except Exception as e1:
                logger.clog("[Error] Can't load chatconfig.json: " + str(e1.args) +
                            "\n\n[Info] Try fix the data or reset the data.")
                exit()
            else:
                logger.clog("[Info] Converting to json format...")
                with open("./chatconfig.json.bak", "w") as fs:
                    fs.write(str(chat_config))
                with open("./chatconfig.json", "w") as fs:
                    json.dump(chat_config, fs, indent=2)
                logger.clog("[Info] Reloading...")
                with open("./chatconfig.json", "r") as fs:
                    chat_config = json.load(fs)
        logger.clog('... Done.')
        if chat_config['config_ver'] != HJ_Ver:
            logger.clog('[Info] Updating chat config data...')
            old_chat_config = str(chat_config)
            chat_config['config_ver'] = HJ_Ver
            for i in chat_config:
                if i == 'config_ver':
                    continue
                #New configs here
                
            for i in chat_config:
                if i == 'config_ver':
                    continue
                for j in eval(old_chat_config)[i]:
                    chat_config[i][j] = eval(old_chat_config)[i][j]
            self.write_chatconfig(chat_config)
        return

    def write_chatconfig(self, data):
        logger.clog("[Info] Writing chat config data...")
        with open("./chatconfig.json", "w") as fs:
            json.dump(data, fs, indent=2)
        return

    def default_lang(self, chat_id):
        chat_config[str(chat_id)] = {"lang": "en_US"}
        self.write_chatconfig(chat_config)
        return

    async def set_lang(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['config']
        if msg['from']['id'] == config.OWNERID:
            logger.clog('[Info] Owner Matched for \n[Info] ' +
                str(await bot.getChatMember(chat_id, msg['from']['id'])))
            await self.set_lang_command(chat_id, msg, cmd)
            return
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            logger.clog('[Info] Detected a group with all members are admin enabled.')
            dre = await bot.sendMessage(
                chat_id, langport['lang_noperm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            logger.clog('[Info] Searching admins in '+msg['chat']
                ['title']+'('+str(chat_id) + ')')
            for admin in await bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                    await self.set_lang_command(chat_id, msg, cmd)
                    return
            logger.clog('[Info] No admins matched with ' + msg['from']
                ['username']+'('+str(msg['from']['id']) + ')')
            dre = await bot.sendMessage(
                chat_id, langport['lang_noperm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        return

    async def set_lang_command(self, chat_id, msg, cmd):
        global chat_config
        try:
            slang = cmd[1]
        except IndexError:
            smsg = ""
            for i in lang:
                smsg = smsg + "- <code>" + i + "</code> <i>" + \
                    lang[i]["display_name"]+"</i>\n"
            dre = await bot.sendMessage(chat_id, "/setlang &lt;language&gt;\n\n" +
                                smsg, parse_mode="HTML", reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            try:
                tmp = chat_config[str(chat_id)]
            except KeyError:
                try:
                    tmp = lang[slang]
                except KeyError:
                    smsg = ""
                    for i in lang:
                        smsg = smsg + "- <code>" + i + "</code> <i>" + \
                            lang[i]["display_name"]+"</i>\n"
                    dre = await bot.sendMessage(chat_id, "Language {0} not exist.\n\n".format(
                        "<b>"+slang+"</b>")+smsg, parse_mode="HTML", reply_to_message_id=msg["message_id"])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                    return
                else:
                    chat_config[str(chat_id)] = {"lang": slang}
                    self.write_chatconfig(chat_config)
                    dre = await bot.sendMessage(chat_id,
                                        lang[chat_config[str(chat_id)]["lang"]]["display"]["config"]["langsuccess"].format(lang[chat_config[str(chat_id)]["lang"]]["display_name"]), reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                if slang != chat_config[str(chat_id)]["lang"]:
                    try:
                        tmp = lang[slang]
                    except KeyError:
                        smsg = ""
                        for i in lang:
                            smsg = smsg + "- <code>" + i + "</code> <i>" + \
                                lang[i]["display_name"]+"</i>\n"
                        dre = await bot.sendMessage(chat_id, "Language {0} not exist.\n\n".format(
                            "<b>"+slang+"</b>")+smsg, parse_mode="HTML", reply_to_message_id=msg["message_id"])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                    else:
                        chat_config[str(chat_id)]["lang"] = slang
                        self.write_chatconfig(chat_config)
                        dre = await bot.sendMessage(chat_id,
                                            lang[chat_config[str(chat_id)]["lang"]]["display"]["config"]["langsuccess"].format(lang[chat_config[str(chat_id)]["lang"]]["display_name"]), reply_to_message_id=msg['message_id'])
                        logger.log("[Debug] Raw sent data:"+str(dre))
                else:
                    dre = await bot.sendMessage(chat_id, lang[chat_config[str(chat_id)]["lang"]]["display"]["config"]["langexist"].format(
                        lang[chat_config[str(chat_id)]["lang"]]["display_name"]), reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
        return
chatconfig = chatconfigc()

class functionc:
    def read_function_list(self):
        global function_list_data
        logger.clog('[Info] Reading function list data...')
        if os.path.isfile("./fctlsdata.json") == False:
            with open("./fctlsdata.json", "w") as fs:
                json.dump({'config_ver': HJ_Ver }, fs, indent=2)
        try:
            with open("./fctlsdata.json", "r") as fs:
                function_list_data = json.load(fs)
        except json.decoder.JSONDecodeError as e1:
            logger.clog("[Error] Can't load fctlsdata.json: JSON decode error:"+ str(e1.args)+ "\n[Info] Trying to read using python format.")
            try:
                with open("./fctlsdata.json", "r") as fs:
                    function_list_data = eval(fs.read())
            except Exception as e1:
                logger.clog("[Error] Can't load fctlsdata.json: " + str(e1.args) +
                            "\n\n[Info] Try fix the data or reset the data.")
                exit()
            else:
                logger.clog("[Info] Converting to json format...")
                with open("./fctlsdata.json.bak", "w") as fs:
                    fs.write(str(function_list_data))
                with open("./fctlsdata.json", "w") as fs:
                    json.dump(function_list_data, fs, indent=2)
                logger.clog("[Info] Reloading...")
                with open("./fctlsdata.json", "r") as fs:
                    function_list_data = json.load(fs)
        logger.clog('... Done.')
        if function_list_data['config_ver'] != HJ_Ver:
            logger.clog('[Info] Updating function list data...')
            old_function_list_data = str(function_list_data)
            function_list_data['config_ver'] = HJ_Ver
            for i in function_list_data:
                if i == 'config_ver':
                    continue
                self.function_set_default(i)
            for i in function_list_data:
                if i == 'config_ver':
                    continue
                for j in eval(old_function_list_data)[i]:
                    function_list_data[i][j] = eval(old_function_list_data)[i][j]
            self.write_function_list(function_list_data)
        return

    def write_function_list(self, data):
        logger.clog("[Info] Writing function list data...")
        with open("./fctlsdata.json", "w") as fs:
            json.dump(data, fs, indent=2)
        return

    async def function(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]
                        ]["display"]['function']['general']
        if msg['from']['id'] == config.OWNERID:
            logger.clog('[Info] Owner Matched for \n[Info] ' +
                str(await bot.getChatMember(chat_id, msg['from']['id'])))
            await self.__cmd(chat_id, msg, cmd, langport, chat_type)
            return
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            logger.clog('[Info] Detected a group with all members are admin enabled.')
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            logger.clog('[Info] Searching admins in '+msg['chat']
                ['title']+'('+str(chat_id) + ')')
            for admin in await bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    logger.clog('[Info] Admin Matched for \n[Info] ' + str(admin))
                    await self.__cmd(chat_id, msg, cmd, langport, chat_type)
                    return
            logger.clog('[Info] No admins matched with ' + msg['from']
                ['username']+'('+str(msg['from']['id']) + ')')
            dre = await bot.sendMessage(
                chat_id, langport['no_perm'], reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        return

    async def __cmd(self, chat_id, msg, cmd, langport, chat_type):
        try:
            subcmd = cmd[1]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        else:
            if subcmd == "enable":
                await self.function_enable(chat_id, msg, cmd, chat_type)
            elif subcmd == "disable":
                await self.function_disable(chat_id, msg, cmd, chat_type)
            elif subcmd == "chkadminf":
                await self.function_admincheck(chat_id, msg, chat_type, True)
            elif subcmd == "stats":
                await self.function_stats(chat_id, msg)
            elif subcmd == "reset":
                await self.function_default(chat_id, msg, chat_type)
                dre = await bot.sendMessage(
                    chat_id, langport['reset_complete'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = await bot.sendMessage(
                    chat_id, langport['help'], reply_to_message_id=msg["message_id"])
                logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def function_enable(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]
                        ]["display"]['function']['enable']
        global function_list_data
        try:
            testarg = cmd[2]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        try:
            groupfundict = function_list_data[str(chat_id)]
        except KeyError:
            await self.function_default(chat_id, msg, chat_type)
            dre = await bot.sendMessage(
                chat_id, langport['deploy'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        smsg = ""
        for funct in cmd[2:]:
            try:
                currentv = groupfundict[funct]
            except KeyError:
                smsg += langport['funct_not_exist'].format(
                    '<b>'+funct+'</b>') + '\n'
                continue
            if currentv == True:
                smsg += langport['failed'].format('<b>'+funct+'</b>',
                                                '<code>'+langport['already_true']+'</code>') + '\n'
                continue
            if funct == 'grouppic' or funct == 'title' or funct == 'pin' or funct == 'export_link':
                if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                    logger.clog('[Info] Detected a group with all members are admin enabled.')
                    smsg += langport['failed'].format(
                        '<b>'+funct+'</b>', '<code>'+langport['all_member_are_admin']+'</code>') + '\n'
                    continue
                logger.clog('[Info] Searching admins in '+msg['chat']
                    ['title']+'('+str(chat_id) + ')')
                hasperm = False
                for admin in await bot.getChatAdministrators(chat_id):
                    if bot_me.id == admin['user']['id']:
                        hasperm = True
                        if chat_type == 'supergroup':
                            logger.clog(
                                '[Info] I am an admin in this chat,checking further permissions...')
                            if funct == 'grouppic':
                                if admin['can_change_info']:
                                    groupfundict['grouppic'] = True
                                    smsg += langport['success'].format(
                                        '<b>'+funct+'</b>')+"\n"
                                    continue
                                else:
                                    smsg += langport['failed'].format(
                                        '<b>'+funct+'</b>', '<code>'+langport['no_perm']+'</code>')+'\n'
                                    continue
                            if funct == 'title':
                                if admin['can_change_info']:
                                    groupfundict['title'] = True
                                    smsg += langport['success'].format(
                                        '<b>'+funct+'</b>')+'\n'
                                    continue
                                else:
                                    smsg += langport['failed'].format(
                                        '<b>'+funct+'</b>', '<code>'+langport['no_perm']+'</code>')+'\n'
                                    continue
                            if funct == 'pin':
                                if admin['can_pin_messages']:
                                    groupfundict['pin'] = True
                                    smsg += langport['success'].format(
                                        '<b>'+funct+'</b>')+'\n'
                                    continue
                                else:
                                    smsg += langport['failed'].format(
                                        '<b>'+funct+'</b>', '<code>'+langport['no_perm']+'</code>') + '\n'
                                    continue
                            if funct == 'export_link':
                                if admin['can_invite_users']:
                                    groupfundict['export_link'] = True
                                    smsg += langport['success'].format(
                                        '<b>'+funct+'</b>')+'\n'
                                    continue
                                else:
                                    smsg += langport['failed'].format(
                                        '<b>'+funct+'</b>', '<code>'+langport['no_perm']+'</code>') + '\n'
                                    continue
                        elif chat_type == 'group':
                            logger.clog(
                                '[Info] I am an admin in this chat,enabling admin functions without pin...')
                            if funct == 'grouppic':
                                groupfundict['grouppic'] = True
                                smsg += langport['success'].format(
                                    '<b>'+funct+'</b>')+'\n'
                                continue
                            if funct == 'title':
                                groupfundict['title'] = True
                                smsg += langport['success'].format(
                                    '<b>'+funct+'</b>')+'\n'
                                continue
                            if funct == 'pin':
                                smsg += langport['failed'].format(
                                    '<b>'+funct+'</b>', '<code>'+langport['group_cant_pin']+'</code>')+'\n'
                                continue
                            if funct == 'export_link':
                                smsg += langport['failed'].format(
                                    '<b>'+funct+'</b>', '<code>'+langport['group_cant_export']+'</code>')+'\n'
                                continue
                    continue
                if hasperm:
                    continue
                logger.clog('[Info] I am not an admin in this chat.')
                smsg += langport['failed'].format('<b>'+funct+'</b>',
                                                '<code>'+langport['no_perm']+'</code>')+'\n'
                continue
            else:
                groupfundict[funct] = True
                smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                continue
        dre = await bot.sendMessage(chat_id,
                            smsg,
                            parse_mode='HTML', reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
        function_list_data[str(chat_id)] = groupfundict
        self.write_function_list(function_list_data)
        return

    async def function_disable(self, chat_id, msg, cmd, chat_type):
        langport = lang[chat_config[str(chat_id)]["lang"]
                        ]["display"]['function']['disable']
        global function_list_data
        try:
            testarg = cmd[2]
        except IndexError:
            dre = await bot.sendMessage(
                chat_id, langport['help'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        try:
            groupfundict = function_list_data[str(chat_id)]
        except KeyError:
            await self.function_default(chat_id, msg, chat_type)
            dre = await bot.sendMessage(
                chat_id, langport['deploy'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        if testarg == 'all':
            for funct in groupfundict:
                groupfundict[funct] = False
            function_list_data[str(chat_id)] = groupfundict
            self.write_function_list(function_list_data)
            dre = await bot.sendMessage(
                chat_id, langport['success_all'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
            return
        smsg = ''
        for funct in cmd[2:]:
            try:
                currentv = groupfundict[funct]
            except KeyError:
                smsg += langport['funct_not_exist'].format('<b>'+funct+'</b>')+'\n'
                continue
            if currentv == False:
                smsg += langport['failed'].format('<b>'+funct+'</b>',
                                                '<code>'+langport['already_false']+'</code>')+'\n'
                continue
            groupfundict[funct] = False
            smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
        dre = await bot.sendMessage(chat_id,
                            smsg,
                            parse_mode='HTML', reply_to_message_id=msg['message_id'])
        logger.log("[Debug] Raw sent data:"+str(dre))
        function_list_data[str(chat_id)] = groupfundict
        self.write_function_list(function_list_data)
        return

    async def function_admincheck(self, chat_id, msg, chat_type, sendchat):
        langport = lang[chat_config[str(chat_id)]["lang"]
                        ]["display"]['function']['admin_check']
        global function_list_data
        try:
            groupfundict = function_list_data[str(chat_id)]
        except KeyError:
            groupfundict = {}
        smsg = ''
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            logger.clog('[Info] Detected a group with all members are admin enabled,disabling admin functions...')
            if sendchat:
                dre = await bot.sendMessage(chat_id,
                                    langport['all_member_are_admin'],
                                    parse_mode='HTML', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            groupfundict['grouppic'] = False
            smsg = smsg + \
                langport['success_disable'].format('<b>grouppic</b>')+'\n'
            groupfundict['pin'] = False
            smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
            groupfundict['title'] = False
            smsg = smsg + langport['success_disable'].format('<b>title</b>')+'\n'
            groupfundict['export_link'] = False
            smsg = smsg + \
                langport['success_disable'].format('<b>export_link</b>')+'\n'
            function_list_data[str(chat_id)] = groupfundict
            self.write_function_list(function_list_data)
            if sendchat:
                dre = await bot.sendMessage(chat_id,
                                    smsg,
                                    parse_mode='HTML', reply_to_message_id=msg['message_id'])
                logger.log("[Debug] Raw sent data:"+str(dre))
            return
        if sendchat:
            dre = await bot.sendMessage(
                chat_id, langport['msg_checking_admin'], reply_to_message_id=msg["message_id"])
            logger.log("[Debug] Raw sent data:"+str(dre))
        logger.clog('[Info] Searching admins in '+msg['chat']
            ['title']+'('+str(chat_id) + ')')

        for admin in await bot.getChatAdministrators(chat_id):
            if bot_me.id == admin['user']['id']:
                if chat_type == 'supergroup':
                    logger.clog(
                        '[Info] I am an admin in this chat,checking further permissions...')
                    if admin['can_change_info']:
                        groupfundict['grouppic'] = True
                        smsg = smsg + \
                            langport['success_enable'].format(
                                '<b>grouppic</b>')+'\n'
                        groupfundict['title'] = True
                        smsg = smsg + \
                            langport['success_enable'].format('<b>title</b>')+'\n'
                    else:
                        groupfundict['grouppic'] = False
                        smsg = smsg + \
                            langport['success_disable'].format(
                                '<b>grouppic</b>')+'\n'
                        groupfundict['title'] = False
                        smsg = smsg + \
                            langport['success_disable'].format('<b>title</b>')+'\n'
                    if admin['can_pin_messages'] == True:
                        groupfundict['pin'] = True
                        smsg = smsg + \
                            langport['success_enable'].format('<b>pin</b>')+'\n'
                    else:
                        groupfundict['pin'] = False
                        smsg = smsg + \
                            langport['success_disable'].format('<b>pin</b>')+'\n'
                    if admin['can_invite_users'] == True:
                        groupfundict['export_link'] = True
                        smsg = smsg + \
                            langport['success_enable'].format(
                                '<b>export_link</b>')+'\n'
                    else:
                        groupfundict['export_link'] = False
                        smsg = smsg + \
                            langport['success_disable'].format(
                                '<b>export_link</b>')+'\n'
                elif chat_type == 'group':
                    logger.clog(
                        '[Info] I am an admin in this chat,enabling admin functions without pin...')
                    groupfundict['grouppic'] = True
                    smsg = smsg + \
                        langport['success_enable'].format('<b>grouppic</b>')+'\n'
                    groupfundict['pin'] = False
                    smsg = smsg + \
                        langport['success_disable'].format('<b>pin</b>')+'\n'
                    groupfundict['title'] = True
                    smsg = smsg + \
                        langport['success_enable'].format('<b>title</b>')+'\n'
                    groupfundict['export_link'] = False
                    smsg = smsg + \
                        langport['success_disable'].format(
                            '<b>export_link</b>')+'\n'
                function_list_data[str(chat_id)] = groupfundict
                self.write_function_list(function_list_data)
                if sendchat:
                    dre = await bot.sendMessage(chat_id,
                                        smsg,
                                        parse_mode='HTML', reply_to_message_id=msg['message_id'])
                    logger.log("[Debug] Raw sent data:"+str(dre))
                return
        logger.clog('[Info] I am not an admin in this chat.')
        groupfundict['grouppic'] = False
        smsg = smsg + langport['success_disable'].format('<b>grouppic</b>')+'\n'
        groupfundict['pin'] = False
        smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
        groupfundict['title'] = False
        smsg = smsg + langport['success_disable'].format('<b>title</b>')+'\n'
        groupfundict['export_link'] = False
        smsg = smsg + langport['success_disable'].format('<b>export_link</b>')+'\n'
        function_list_data[str(chat_id)] = groupfundict
        self.write_function_list(function_list_data)
        if sendchat:
            dre = await bot.sendMessage(chat_id,
                                smsg,
                                parse_mode='HTML', reply_to_message_id=msg['message_id'])
            logger.log("[Debug] Raw sent data:"+str(dre))
        return

    async def function_default(self, chat_id, msg, chat_type):
        global function_list_data
        self.function_set_default(chat_id)
        self.write_function_list(function_list_data)
        await self.function_admincheck(chat_id, msg, chat_type, False)
        return

    def function_set_default(self, chat_id):
        global function_list_data
        try:
            groupfundict = function_list_data[str(chat_id)]
        except:
            groupfundict = {}
        groupfundict['a2z'] = True
        groupfundict['grouppic'] = False
        groupfundict['ping'] = True
        groupfundict['echo'] = True
        groupfundict['groupinfo'] = True
        groupfundict['pin'] = False
        groupfundict['title'] = False
        groupfundict['user'] = True
        groupfundict['numbersystem'] = True
        groupfundict['files'] = True
        groupfundict['lsadmins'] = True
        groupfundict['tag'] = True
        groupfundict['google_tts'] = True
        groupfundict['replace_str'] = True
        groupfundict['delete_message'] = True
        groupfundict['export_link'] = False
        function_list_data[str(chat_id)] = groupfundict
        return

    async def function_stats(self, chat_id, msg):
        global function_list_data
        try:
            groupfundict = function_list_data[str(chat_id)]
        except:
            groupfundict = {}
        smsg = ''
        for funct in groupfundict:
            smsg = smsg + \
                '<b>{0}</b> : <code>{1}</code>\n'.format(
                    funct, str(groupfundict[funct]))
        dre = await bot.sendMessage(chat_id, smsg, parse_mode='HTML',
                            reply_to_message_id=msg["message_id"])
        logger.log("[Debug] Raw sent data:"+str(dre))
        return
function = functionc()

async def help(chat_id, msg, chat_type):
    langport = lang[chat_config[str(chat_id)]["lang"]]["display"]['help']
    global function_list_data
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        await function.function_default(chat_id, msg, chat_type)
    smsg = ''
    if groupfundict['a2z']:
        smsg = smsg + '/a2z\n'
    if groupfundict['grouppic']:
        smsg = smsg + '/cgp\n/rgp\n'
    if groupfundict['ping']:
        smsg = smsg + '/ping\n'
    if groupfundict['echo']:
        smsg = smsg + '/echo\n'
    if groupfundict['groupinfo']:
        smsg = smsg + '/groupinfo\n'
    if groupfundict['pin']:
        smsg = smsg + '/pin\n'
    if groupfundict['title']:
        smsg = smsg + '/title\n'
    if groupfundict['user']:
        smsg = smsg + '/getme\n/getuser\n'
    if groupfundict['numbersystem']:
        smsg = smsg + '/ns\n'
    if groupfundict['files']:
        smsg = smsg + '/getfile\n/fileinfo\n'
    if groupfundict['lsadmins']:
        smsg = smsg + '/lsadmins\n'
    if groupfundict['tag']:
        smsg = smsg + '/tag\n'
    if groupfundict['google_tts']:
        smsg = smsg + '/gtts\n'
    if groupfundict['replace_str']:
        smsg = smsg + '/replace\n'
    if groupfundict['export_link']:
        smsg = smsg + '/exportchatlink\n'
    if groupfundict['delete_message']:
        smsg = smsg + '/delmsg\n'
    if smsg == '':
        smsg = langport['nofunction']+'\n/setlang'
    else:
        smsg = smsg + '/function\n/setlang'
    dre = await bot.sendMessage(chat_id, smsg, reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    return

async def helpp(chat_id, msg):
    dre = await bot.sendMessage(chat_id,
                          '/ping\n/echo\n/getme\n/ns\n/getfile\n/gtts\n/exportblog\n/setlang\n/delmsg',
                          reply_to_message_id=msg['message_id'])
    logger.log("[Debug] Raw sent data:"+str(dre))
    return

def pastebin(data, title):
    if config.pastebin_dev_key != "none" and config.pastebin_user_key != "none":
        pastebin_vars = {'api_dev_key': config.pastebin_dev_key,
                         'api_option': 'paste', 'api_paste_code': data,
                         'api_paste_private': '1',
                         'api_user_key': config.pastebin_user_key,
                         'api_paste_name': title}
        response = urllib.request.urlopen('http://pastebin.com/api/api_post.php',
                                          bytes(urllib.parse.urlencode(pastebin_vars), 'utf-8'))
        url = response.read()
        logger.clog("[Pastebin]Uploaded to pastebin URL:"+str(url, 'utf-8'))
        return(str(url, 'utf-8'))
    else:
        return("invalid pastebin key")

def a2z(textLine):
    zh = textLine.lower()
    zh = zh.replace("ａ", "a")
    zh = zh.replace("ｂ", "b")
    zh = zh.replace("ｃ", "c")
    zh = zh.replace("ｄ", "d")
    zh = zh.replace("ｅ", "e")
    zh = zh.replace("ｆ", "f")
    zh = zh.replace("ｇ", "g")
    zh = zh.replace("ｈ", "h")
    zh = zh.replace("ｉ", "i")
    zh = zh.replace("ｊ", "j")
    zh = zh.replace("ｋ", "k")
    zh = zh.replace("ｌ", "l")
    zh = zh.replace("ｍ", "m")
    zh = zh.replace("ｎ", "n")
    zh = zh.replace("ｏ", "o")
    zh = zh.replace("ｐ", "p")
    zh = zh.replace("ｑ", "q")
    zh = zh.replace("ｒ", "r")
    zh = zh.replace("ｓ", "s")
    zh = zh.replace("ｔ", "t")
    zh = zh.replace("ｕ", "u")
    zh = zh.replace("ｖ", "v")
    zh = zh.replace("ｗ", "w")
    zh = zh.replace("ｘ", "x")
    zh = zh.replace("ｙ", "y")
    zh = zh.replace("ｚ", "z")
    zh = zh.replace("１", "1")
    zh = zh.replace("２", "2")
    zh = zh.replace("３", "3")
    zh = zh.replace("４", "4")
    zh = zh.replace("５", "5")
    zh = zh.replace("６", "6")
    zh = zh.replace("７", "7")
    zh = zh.replace("８", "8")
    zh = zh.replace("９", "9")
    zh = zh.replace("０", "0")
    zh = zh.replace("－", "-")
    zh = zh.replace("；", ";")
    zh = zh.replace("，", ",")
    zh = zh.replace("．", ".")
    zh = zh.replace("／", "/")
    zh = zh.replace('1', 'ㄅ')
    zh = zh.replace('2', 'ㄉ')
    zh = zh.replace('3', 'ˇ')
    zh = zh.replace('4', 'ˋ')
    zh = zh.replace('5', 'ㄓ')
    zh = zh.replace('6', 'ˊ')
    zh = zh.replace('7', '˙')
    zh = zh.replace('8', 'ㄚ')
    zh = zh.replace('9', 'ㄞ')
    zh = zh.replace('0', 'ㄢ')
    zh = zh.replace('-', 'ㄦ')
    zh = zh.replace('q', 'ㄆ')
    zh = zh.replace('w', 'ㄊ')
    zh = zh.replace('e', 'ㄍ')
    zh = zh.replace('r', 'ㄐ')
    zh = zh.replace('t', 'ㄔ')
    zh = zh.replace('y', 'ㄗ')
    zh = zh.replace('u', 'ㄧ')
    zh = zh.replace('i', 'ㄛ')
    zh = zh.replace('o', 'ㄟ')
    zh = zh.replace('p', 'ㄣ')
    zh = zh.replace('a', 'ㄇ')
    zh = zh.replace('s', 'ㄋ')
    zh = zh.replace('d', 'ㄎ')
    zh = zh.replace('f', 'ㄑ')
    zh = zh.replace('g', 'ㄕ')
    zh = zh.replace('h', 'ㄘ')
    zh = zh.replace('j', 'ㄨ')
    zh = zh.replace('k', 'ㄜ')
    zh = zh.replace('l', 'ㄠ')
    zh = zh.replace(';', 'ㄤ')
    zh = zh.replace('z', 'ㄈ')
    zh = zh.replace('x', 'ㄌ')
    zh = zh.replace('c', 'ㄏ')
    zh = zh.replace('v', 'ㄒ')
    zh = zh.replace('b', 'ㄖ')
    zh = zh.replace('n', 'ㄙ')
    zh = zh.replace('m', 'ㄩ')
    zh = zh.replace(',', 'ㄝ')
    zh = zh.replace('.', 'ㄡ')
    zh = zh.replace('/', 'ㄥ')
    return zh

def a2z_etan(textLine):
    zh = textLine.lower()
    zh = zh.replace("ａ", "a")
    zh = zh.replace("ｂ", "b")
    zh = zh.replace("ｃ", "c")
    zh = zh.replace("ｄ", "d")
    zh = zh.replace("ｅ", "e")
    zh = zh.replace("ｆ", "f")
    zh = zh.replace("ｇ", "g")
    zh = zh.replace("ｈ", "h")
    zh = zh.replace("ｉ", "i")
    zh = zh.replace("ｊ", "j")
    zh = zh.replace("ｋ", "k")
    zh = zh.replace("ｌ", "l")
    zh = zh.replace("ｍ", "m")
    zh = zh.replace("ｎ", "n")
    zh = zh.replace("ｏ", "o")
    zh = zh.replace("ｐ", "p")
    zh = zh.replace("ｑ", "q")
    zh = zh.replace("ｒ", "r")
    zh = zh.replace("ｓ", "s")
    zh = zh.replace("ｔ", "t")
    zh = zh.replace("ｕ", "u")
    zh = zh.replace("ｖ", "v")
    zh = zh.replace("ｗ", "w")
    zh = zh.replace("ｘ", "x")
    zh = zh.replace("ｙ", "y")
    zh = zh.replace("ｚ", "z")
    zh = zh.replace("１", "1")
    zh = zh.replace("２", "2")
    zh = zh.replace("３", "3")
    zh = zh.replace("４", "4")
    zh = zh.replace("５", "5")
    zh = zh.replace("６", "6")
    zh = zh.replace("７", "7")
    zh = zh.replace("８", "8")
    zh = zh.replace("９", "9")
    zh = zh.replace("０", "0")
    zh = zh.replace("－", "-")
    zh = zh.replace("；", ";")
    zh = zh.replace("，", ",")
    zh = zh.replace("．", ".")
    zh = zh.replace("＼", "/")
    zh = zh.replace("＝", "=")
    zh = zh.replace("’", "'")
    zh = zh.replace('1', '˙')
    zh = zh.replace('2', 'ˊ')
    zh = zh.replace('3', 'ˇ')
    zh = zh.replace('4', 'ˋ')
    zh = zh.replace('7', 'ㄑ')
    zh = zh.replace('8', 'ㄢ')
    zh = zh.replace('9', 'ㄣ')
    zh = zh.replace('0', 'ㄤ')
    zh = zh.replace('-', 'ㄥ')
    zh = zh.replace('=', 'ㄦ')
    zh = zh.replace('q', 'ㄟ')
    zh = zh.replace('w', 'ㄝ')
    zh = zh.replace('e', 'ㄧ')
    zh = zh.replace('r', 'ㄜ')
    zh = zh.replace('t', 'ㄊ')
    zh = zh.replace('y', 'ㄡ')
    zh = zh.replace('u', 'ㄩ')
    zh = zh.replace('i', 'ㄞ')
    zh = zh.replace('o', 'ㄛ')
    zh = zh.replace('p', 'ㄆ')
    zh = zh.replace('a', 'ㄚ')
    zh = zh.replace('s', 'ㄙ')
    zh = zh.replace('d', 'ㄉ')
    zh = zh.replace('f', 'ㄈ')
    zh = zh.replace('g', 'ㄐ')
    zh = zh.replace('h', 'ㄏ')
    zh = zh.replace('j', 'ㄖ')
    zh = zh.replace('k', 'ㄎ')
    zh = zh.replace('l', 'ㄌ')
    zh = zh.replace(';', 'ㄗ')
    zh = zh.replace("'", 'ㄘ')
    zh = zh.replace('z', 'ㄠ')
    zh = zh.replace('x', 'ㄨ')
    zh = zh.replace('c', 'ㄒ')
    zh = zh.replace('v', 'ㄍ')
    zh = zh.replace('b', 'ㄅ')
    zh = zh.replace('n', 'ㄋ')
    zh = zh.replace('m', 'ㄇ')
    zh = zh.replace(',', 'ㄓ')
    zh = zh.replace('.', 'ㄔ')
    zh = zh.replace('/', 'ㄕ')
    return zh

class Log:
    logpath = "./logs/"+time.strftime("%Y-%m-%d-%H-%M-%S").replace("'","")
    def __init__(self):
        if os.path.isdir("./logs") == False:
            os.mkdir("./logs")
        self.log("[Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
        self.log("[Debug][Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
        self.log("[Debug] Bot's TOKEN is "+config.TOKEN)
    async def logmsg(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.log("[Debug] Raw message:"+str(msg))
        dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info]"
        flog = ""
        try:
            dlog += "[EDITED"+str(msg['edit_date'])+"]"
        except KeyError:
            pass
        try:
            fuser= await bot.getChatMember(chat_id, msg['from']['id'])
        except KeyError:
            fnick = "Channel Admin"
            fuserid = None
        else:
            fnick = fuser['user']['first_name']
            try:
                fnick += ' ' + fuser['user']['last_name']
            except KeyError:
                pass
            try:
                fnick +="@"+ fuser['user']['username']
            except KeyError:
                pass
            fuserid = str(fuser['user']['id'])
        if chat_type == 'private':
            dlog += "[Private]"
        dlog += "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except KeyError:
            pass
        else:
            if chat_type != 'channel':
                if reply_to == bot_me.id:
                    dlog += " ( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
                else:
                    tuser = msg['reply_to_message']['from']['first_name']
                    try:
                        tuser += ' ' + msg['reply_to_message']['from']['last_name']
                    except KeyError:
                        pass
                    try:
                        tuser += '@' + msg['reply_to_message']['from']['username']
                    except KeyError:
                        pass
                    dlog += " ( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
            else:
                dlog += \
                    " ( Reply to " + \
                    str(msg['reply_to_message']['message_id'])+" )"
        if chat_type == 'private':
            if content_type == 'text':
                dlog += ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
            else:
                dlog += ' ' + fnick + \
                    " ( "+fuserid+" ) sent a " + content_type
        elif chat_type == 'group' or chat_type == 'supergroup':
            if content_type == 'text':
                dlog += ' ' + fnick + \
                    " ( "+fuserid+" ) in "+msg['chat']['title'] + \
                    ' ( '+str(chat_id) + ' ): ' + msg['text']
            elif content_type == 'new_chat_member':
                if msg['new_chat_member']['id'] == bot_me.id:
                    dlog += ' I have been added to ' + \
                        msg['chat']['title'] + \
                        ' ( '+str(chat_id) + ' ) by ' + fnick + " ( "+fuserid+" )"
                else:
                    tuser = msg['new_chat_member']['first_name']
                    try:
                        tuser += ' ' + msg['new_chat_member']['last_name']
                    except KeyError:
                        pass
                    try:
                        tuser += '@' + msg['new_chat_member']['username']
                    except KeyError:
                        pass
                    dlog += ' ' + tuser + ' joined the ' + chat_type + \
                        ' '+msg['chat']['title']+' ( '+str(chat_id) + ' ) '
            elif content_type == 'left_chat_member':
                if msg['left_chat_member']['id'] == bot_me.id:
                    dlog += ' I have been kicked from ' + \
                        msg['chat']['title'] + \
                        ' ( '+str(chat_id) + ' ) by ' + fnick + " ( "+fuserid+" )"
                else:
                    tuser = msg['left_chat_member']['first_name']
                    try:
                        tuser += ' ' + msg['left_chat_member']['last_name']
                    except KeyError:
                        pass
                    try:
                        tuser += '@' + msg['left_chat_member']['username']
                    except KeyError:
                        pass
                    dlog += ' ' + tuser + ' left the ' + chat_type + \
                        ' '+msg['chat']['title']+' ( '+str(chat_id) + ' ) '
            elif content_type == 'pinned_message':
                tuser = msg['pinned_message']['from']['first_name']
                try:
                    tuser += ' ' + \
                        msg['pinned_message']['from']['last_name']
                except KeyError:
                    pass
                try:
                    tuser += '@' + msg['pinned_message']['from']['username']
                except KeyError:
                    pass
                tmpcontent_type, tmpchat_type = telepot.glance(
                    msg['pinned_message'])
                if tmpcontent_type == 'text':
                    dlog += ' ' + tuser + "'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to " +\
                        msg['chat']['title']+' ( '+str(chat_id) + ' ) by ' + fnick + \
                        " ( "+fuserid+" ):\n"+msg['pinned_message']['text']
                else:
                    dlog += ' ' + tuser + "'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to " +\
                        msg['chat']['title'] + \
                        ' ( '+str(chat_id) + ' ) by ' + fnick + " ( "+fuserid+" )"
                    self.__log_media(tmpchat_type, msg['pinned_message'])
            elif content_type == 'new_chat_photo':
                dlog += " The photo of this "+chat_type + ' ' + \
                    msg['chat']['title']+' ( '+str(chat_id) + \
                    ' ) was changed by '+fnick + " ( "+fuserid+" )"
                flog = "[New Chat Photo]"
                photo_array = msg['new_chat_photo']
                photo_array.reverse()
                try:
                    flog = flog + "Caption = " + \
                        msg['caption'] + " ,FileID:" + photo_array[0]['file_id']
                except KeyError:
                    flog = flog + "FileID:" + photo_array[0]['file_id']
            elif content_type == 'group_chat_created':
                if msg['new_chat_member']['id'] == bot_me.id:
                    dlog += ' ' + fnick + " ( "+fuserid+" ) created a " + chat_type + ' ' + \
                        msg['chat']['title'] + \
                        ' ( '+str(chat_id) + ' ) and I was added into the group.'
            elif content_type == 'migrate_to_chat_id':
                newgp = await bot.getChat(msg['migrate_to_chat_id'])
                dlog += ' ' + chat_type + ' ' + msg['chat']['title']+' ( '+str(
                    chat_id) + ' ) was migrated to ' + newgp['type'] + ' ' + newgp['title'] + ' ('+str(newgp['id'])+')  by ' + fnick + " ( "+fuserid+" )"
            elif content_type == 'migrate_from_chat_id':
                oldgp = await bot.getChat(msg['migrate_from_chat_id'])
                dlog += ' ' + chat_type + ' ' + msg['chat']['title']+' ( '+str(
                    chat_id) + ' ) was migrated from ' + oldgp['type'] + ' ' + oldgp['title'] + ' ('+str(oldgp['id'])+')  by ' + fnick + " ( "+fuserid+" )"
            elif content_type == 'delete_chat_photo':
                dlog += " The photo of this "+chat_type + ' ' + \
                    msg['chat']['title']+' ( '+str(chat_id) + \
                    ' ) was deleted by '+fnick + " ( "+fuserid+" )"
            elif content_type == 'new_chat_title':
                dlog += " The title of this "+chat_type + " was changed to " + \
                    msg['new_chat_title']+" by "+fnick + " ( "+fuserid+" )"
            else:
                dlog += ' ' + fnick + \
                    " ( "+fuserid+" ) in "+msg['chat']['title'] + \
                    ' ( '+str(chat_id) + ' ) sent a ' + content_type
        elif chat_type == 'channel':
            if content_type == 'text':
                dlog += ' ' + fnick
                if fuserid:
                    dlog += " ( "+fuserid+" )"
                dlog += ' ' + " in channel " + \
                    msg['chat']['title']+' ( '+str(chat_id) + ' ): ' + msg['text']
            elif content_type == 'new_chat_photo':
                dlog += " The photo of this "+chat_type+"" + ' ' + \
                    msg['chat']['title'] + \
                    ' ( '+str(chat_id) + ' ) was changed by '+fnick
                if fuserid:
                    dlog += " ( "+fuserid+" )"
                flog = "[New Chat Photo]"
                photo_array = msg['new_chat_photo']
                photo_array.reverse()
                try:
                    flog = flog + "Caption = " + \
                        msg['caption'] + " ,FileID:" + photo_array[0]['file_id']
                except KeyError:
                    flog = flog + "FileID:" + photo_array[0]['file_id']
            elif content_type == 'pinned_message':
                tmpcontent_type, tmpchat_type, tmpchat_id = telepot.glance(msg['pinned_message'])
                if tmpcontent_type == 'text':
                    dlog += ' ' + "A message["+str(msg['pinned_message']['message_id'])+"] was pinned to " +\
                        msg['chat']['title']+' ( '+str(chat_id) + ' ) by :\n'+msg['pinned_message']['text']
                else:
                    dlog += ' ' "A message["+str(msg['pinned_message']['message_id'])+"] was pinned to " +\
                        msg['chat']['title'] + \
                        ' ( '+str(chat_id) + ' ) '
                    self.__log_media(tmpchat_type, msg['pinned_message'])
            elif content_type == 'delete_chat_photo':
                dlog += " The photo of this "+chat_type + ' ' + \
                    msg['chat']['title'] + \
                    ' ( '+str(chat_id) + ' ) was deleted by '+fnick
                if fuserid:
                    dlog += " ( "+fuserid+" )"
            elif content_type == 'new_chat_title':
                dlog += " The title of this "+chat_type + " was changed to " +\
                    msg['new_chat_title'] + " by "
                if fuserid:
                    dlog += " ( "+fuserid+" )"
            else:
                dlog += ' ' + fnick
                if fuserid:
                    dlog += " ( "+fuserid+" )"
                dlog += " in channel" + \
                    msg['chat']['title'] + \
                    ' ( '+str(chat_id) + ' ) sent a ' + content_type
        self.clog(dlog)
        self.__log_media(content_type, msg)
        if flog != "":
            self.clog(flog)
        return
    def __log_media(self, content_type, msg):
        flog = ""
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array = msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + photo_array[0]['file_id']
            except:
                flog = flog + "FileID:" + photo_array[0]['file_id']
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + msg['audio']['file_id']
            except:
                flog = flog + "FileID:" + msg['audio']['file_id']
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + msg['document']['file_id']
            except:
                flog = flog + "FileID:" + msg['document']['file_id']
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + msg['video']['file_id']
            except:
                flog = flog + "FileID:" + msg['video']['file_id']
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + msg['voice']['file_id']
            except:
                flog = flog + "FileID:" + msg['voice']['file_id']
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " + \
                    msg['caption'] + " ,FileID:" + msg['sticker']['file_id']
            except:
                flog = flog + "FileID:" + msg['sticker']['file_id']
        if flog != "":
            self.clog(flog)
        return
    def clog(self, text):
        print(text)
        self.log(text)
    def log(self, text):
        if text[0:7] == "[Debug]":
            if config.Debug == True:
                with io.open(self.logpath+"-debug.log","a",encoding='utf8') as logger:
                    logger.write("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"]"+text+"\n")
            return
        with io.open(self.logpath+".log","a",encoding='utf8') as logger:
            logger.write(text+"\n")
        return
logger = Log()
try:
    if sys.argv[1] == 'test':
        print('There is no santax error,exiting...')
        exit()
    else:
        raise SyntaxError("Invaild command santax: {0}".format(sys.argv[1]))
except IndexError:
    pass

botwoasync = telepot.Bot(config.TOKEN)
bot = telepot.aio.Bot(config.TOKEN)

class botprofile:
    def __init__(self):
        self.__bot_me = botwoasync.getMe()
        self.id = self.__bot_me['id']
        self.first_name = self.__bot_me['first_name']
        self.username = self.__bot_me['username']
bot_me = botprofile()

function.read_function_list()

chatconfig.read_chatconfig()

answerer = telepot.helper.Answerer(bot)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_forever())
logger.clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Bot has started")
logger.clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Listening ...")
if os.path.isfile('./statusmessage.py'):
    with open('./statusmessage.py') as fs:
        statMessage = eval(fs.read())
    msg_idf = telepot.message_identifier(statMessage)
    botwoasync.editMessageText(msg_idf,'✅ @'+bot_me.username+' is currently online.')
try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Interrupt signal received,stopping.")
    if os.path.isfile('./statusmessage.py'):
        with open('./statusmessage.py') as fs:
            statMessage = eval(fs.read())
        msg_idf = telepot.message_identifier(statMessage)
        botwoasync.editMessageText(
            msg_idf, '🔴 @'+bot_me.username+' is currently offline.')
