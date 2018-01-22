#-*-coding:UTF-8-*-
import sys
import time
import urllib
import urllib.request
from urllib.request import Request, urlopen
import os
import platform
import io
import telepot
import random
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

HJ_Ver = "1.0.2"
try:
    fs = open("./config.json", "r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading config.json:"+\
        str(val).split(',')[0].replace('(', '').replace("'", ""))
    programPause = input("Press any key to stop...\n")
    exit()

#load config
config = eval(fs.read())
fs.close()
TOKEN = config["TOKEN"]
pastebin_dev_key = config["pastebin_dev_key"]
pastebin_user_key = config["pastebin_user_key"]
Debug = config["Debug"]
OWNERID = config["OWNERID"]

try:
    fs = open("./langs/list.py", "r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading list.py:"+\
        str(val).split(',')[0].replace('(', '').replace("'", ""))
    programPause = input("Press any key to stop...\n")
    exit()
langlist = eval(fs.read())
fs.close()
lang = {}
for i in langlist:
    lang[i] = {}
    #if i != "en_US":
    #    fs = open(langlist["en_US"]["file"],"r")
        #lang[i]["display"] = eval(fs.read())
        #fs.close()
    fs = open(langlist[i]["file"], "r")
    lang[i]["display"] = eval(fs.read())
    lang[i]["display_name"] = langlist[i]["display_name"]
    fs.close()

confirmsg = None
function_list_data = None
chat_config = {}
delete_msg_sender = {}

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'


def on_chat_message(msg):
    edited = False
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me = bot.getMe()
    username= bot_me['username'].replace(' ', '')
    log("[Debug] Raw message:"+str(msg))
    dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info]"
    dlogwc = color.GREEN +"["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"]"+color.BLUE + "[Info]" +color.RESET
    flog = ""
    try:
        dlog=dlog+"[EDITED"+str(msg['edit_date'])+"]"
        dlogwc=dlogwc+color.YELLOW+"[EDITED"+str(msg['edit_date'])+"]"+color.RESET
        edited = True
    except:
        time.sleep(0)
    try:
        fuser= bot.getChatMember(chat_id,msg['from']['id'])
    except:
        fnick = "Channel Admin"
        fuserid = None
    else:
        fnick = fuser['user']['first_name']
        try:
            fnick = fnick + ' ' + fuser['user']['last_name']
        except:
            fnick = fnick
        try:
            fnick= fnick +"@"+ fuser['user']['username']
        except:
            fnick= fnick
        fuserid = str(fuser['user']['id'])
    try:
        temp=chat_config[chat_id]
    except:
        chat_config[chat_id]={"lang":"en_US"}
        write_chatconfig(chat_config)
    if chat_type == 'private':
        dlog = dlog + "[Private]["+str(msg['message_id'])+"]"
        dlogwc = dlogwc + color.BLUE +"[Private]"+color.RESET+"["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + " ( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
                dlogwc = dlogwc + color.PURPLE + " ( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"+color.RESET
            else:
                tuser= msg['reply_to_message']['from']['first_name']
                try:
                    tuser= tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser= tuser 
                dlog = dlog + " ( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
                dlogwc = dlogwc + color.PURPLE + " ( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"+color.RESET
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
            dlogwc = dlogwc+color.CYAN+ ' ' + fnick + color.RESET+" ( "+fuserid+" )  : " + msg['text']
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) sent a "+ content_type
            dlogwc = dlogwc+color.CYAN+  ' ' + fnick + color.RESET+" ( "+fuserid+" ) sent a "+ content_type
        clog(dlog,dlogwc)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
        if flog != "":
            clog(flog)
        #command_detect
        try:
            chat_config[chat_id]
        except:
            default_lang(chat_id)
        if content_type == 'text' and edited == False:
            cmd = msg['text'].split()
            if cmd[0] == '/start':
                startc(chat_id, msg)
            if cmd[0] == '/getme':
                getme(chat_id, msg)
            if cmd[0] == '/getfile':
                getfile(chat_id,msg, cmd)
            if cmd[0] == '/exportblog':
                exportblog(chat_id, msg)
            if cmd[0] == '/ping':
                ping(chat_id, msg)
            if cmd[0] == '/echo':
                echo(chat_id, msg)
            if cmd[0] == '/ns':
                ns(chat_id,msg, cmd)
            if cmd[0] == '/gtts':
                gtts(chat_id, msg)
            if cmd[0] == '/help':
                helpp(chat_id, msg)
            if cmd[0] == '/setlang':
                set_lang_command(chat_id, msg,cmd)
            if cmd[0] == '/delmsg':
                delmsg(chat_id,msg, chat_type)
            if cmd[0] == '/a2z':
                a2zc(chat_id, msg)
    elif chat_type == 'group' or chat_type == 'supergroup':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        dlogwc = dlogwc + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + " ( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
                dlogwc = dlogwc + color.PURPLE + " ( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"+color.RESET
            else:
                tuser= msg['reply_to_message']['from']['first_name']
                try:
                    tuser= tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser= tuser 
                dlog = dlog + " ( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
                dlogwc = dlogwc + color.PURPLE + " ( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"+color.RESET
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
            dlogwc = dlogwc+color.CYAN+ ' ' + fnick + color.RESET+" ( "+fuserid+" ) in "+color.YELLOW +msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ): ' + msg['text']
        elif content_type == 'new_chat_member':
            if msg['new_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been added to ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
                dlogwc = dlogwc+color.GREEN +' I have been added to '+ color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) '+color.GREEN +'by '+color.CYAN+ fnick + color.RESET+" ( "+fuserid+" )"
            else:
                tuser= msg['new_chat_member']['first_name']
                try:
                    tuser= tuser + ' ' + msg['new_chat_member']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['new_chat_member']['username']
                except:
                    tuser= tuser 
                dlog = dlog+' '+ tuser +' joined the ' + chat_type+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
                dlogwc = dlogwc+color.CYAN+' '+ tuser +color.GREEN+' joined the ' + chat_type+ ' '+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) '
        elif content_type == 'left_chat_member':
            if msg['left_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been kicked from ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
                dlogwc = dlogwc+color.RED+ ' I have been kicked from ' +color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) '+color.RED+'by '+color.CYAN+ fnick + color.RESET+" ( "+fuserid+" )"
            else:
                tuser= msg['left_chat_member']['first_name']
                try:
                    tuser= tuser + ' ' + msg['left_chat_member']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['left_chat_member']['username']
                except:
                    tuser= tuser 
                dlog = dlog+' '+ tuser +' left the ' + chat_type + ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
                dlogwc = dlogwc+color.CYAN+' '+ tuser +color.RED+' left the ' + chat_type +color.YELLOW+ ' '+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) '
        elif content_type == 'pinned_message':
            tuser= msg['pinned_message']['from']['first_name']
            try:
                tuser= tuser + ' ' + msg['pinned_message']['from']['last_name']
            except:
                tuser= tuser
            try:
                tuser= tuser + '@' + msg['pinned_message']['from']['username']
            except:
                tuser= tuser 
            tmpcontent_type, tmpchat_type, tmpchat_id = telepot.glance(msg['pinned_message'])
            if tmpcontent_type == 'text':
                dlog = dlog + ' ' + tuser + "'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to "+\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" ):\n"+msg['pinned_message']['text']
                dlogwc = dlogwc +color.CYAN+ ' ' + tuser +color.RESET+"'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to "+color.YELLOW+\
                    msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) by '+color.CYAN+ fnick +color.RESET+ " ( "+fuserid+" ):\n"+msg['pinned_message']['text']
            else:
                dlog = dlog + ' ' + tuser + "'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to "+\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
                dlogwc = dlogwc +color.CYAN+ ' ' + tuser + color.RESET+"'s message["+str(msg['pinned_message']['message_id'])+"] was pinned to "+color.YELLOW+\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+color.CYAN+ fnick +color.RESET+ " ( "+fuserid+" )"
                if tmpcontent_type == 'photo':
                    flog = "[Pinned Photo]"
                    photo_array=msg['pinned_message']['photo']
                    photo_array.reverse()
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
                    except:
                        flog = flog +"FileID:"+ photo_array[0]['file_id']
                elif tmpcontent_type == 'audio':
                    flog = "[Pinned Audio]"
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['pinned_message']['audio']['file_id']
                    except:
                        flog = flog +"FileID:"+ msg['pinned_message']['audio']['file_id']
                elif tmpcontent_type == 'document':
                    flog = "[Pinned Document]"
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['pinned_message']['document']['file_id']
                    except:
                        flog = flog +"FileID:"+ msg['pinned_message']['document']['file_id']
                elif tmpcontent_type == 'video':
                    flog = "[Pinned Video]"
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['pinned_message']['video']['file_id']
                    except:
                        flog = flog +"FileID:"+ msg['pinned_message']['video']['file_id']
                elif tmpcontent_type == 'voice':
                    flog = "[Pinned Voice]"
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['pinned_message']['voice']['file_id']
                    except:
                        flog = flog +"FileID:"+ msg['pinned_message']['voice']['file_id']
                elif tmpcontent_type == 'sticker':
                    flog = "[Pinned Sticker]"
                    try:
                        flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['pinned_message']['sticker']['file_id']
                    except:
                        flog = flog +"FileID:"+ msg['pinned_message']['sticker']['file_id']
        elif content_type == 'new_chat_photo':
            dlog = dlog + " The photo of this "+chat_type+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) was changed by '+fnick + " ( "+fuserid+" )"
            dlogwc = dlogwc + " The photo of this "+chat_type+""+color.YELLOW+ ' '+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was changed by '+color.CYAN+fnick + color.RESET+" ( "+fuserid+" )"
            flog = "[New Chat Photo]"
            photo_array=msg['new_chat_photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'group_chat_created':
            if msg['new_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' ' + fnick +" ( "+fuserid+" ) created a "+ chat_type + ' '+ msg['chat']['title']+' ( '+str(chat_id)+ ' ) and I was added into the group.'
                dlogwc = dlogwc+color.CYAN +' ' + fnick +color.RESET+ " ( "+fuserid+" )"+color.GREEN+" created a "+ chat_type + ' ' +color.YELLOW+ msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' )'+color.GREEN+' and I was added into the group.'
        elif content_type == 'migrate_to_chat_id':
            newgp = bot.getChat(msg['migrate_to_chat_id'])
            dlog = dlog+ ' ' + chat_type + ' ' + msg['chat']['title']+' ( '+str(chat_id)+ ' ) was migrated to '+ newgp['type'] + ' ' + newgp['title'] +' ('+str(newgp['id'])+')  by '+ fnick + " ( "+fuserid+" )"
            dlogwc = dlogwc+ ' ' + chat_type + ' '+color.YELLOW + msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was migrated to '+ newgp['type'] + ' ' +color.YELLOW+ newgp['title'] +color.RESET+' ('+str(newgp['id'])+')  by '+color.CYAN+ fnick +color.RESET+ " ( "+fuserid+" )"
        elif content_type == 'migrate_from_chat_id':
            oldgp = bot.getChat(msg['migrate_from_chat_id'])
            dlog = dlog+ ' ' + chat_type + ' ' + msg['chat']['title']+' ( '+str(chat_id)+ ' ) was migrated from '+ oldgp['type'] + ' ' + oldgp['title'] +' ('+str(oldgp['id'])+')  by '+ fnick + " ( "+fuserid+" )"
            dlogwc = dlogwc+ ' ' + chat_type + ' ' +color.YELLOW+ msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was migrated from '+ oldgp['type'] + ' '+color.YELLOW + oldgp['title'] +color.RESET+' ('+str(oldgp['id'])+')  by '+color.CYAN+ fnick +color.RESET+ " ( "+fuserid+" )"
        elif content_type == 'delete_chat_photo':
            dlog = dlog + " The photo of this "+chat_type+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) was deleted by '+fnick +" ( "+fuserid+" )"
            dlogwc = dlogwc + " The photo of this "+chat_type+color.YELLOW+ ' '+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was deleted by '+color.CYAN+fnick +color.RESET+ " ( "+fuserid+" )"
        elif content_type == 'new_chat_title':
            dlog = dlog + " The title of this "+chat_type+ " was changed to "+msg['new_chat_title']+" by "+fnick + " ( "+fuserid+" )"
            dlogwc = dlogwc + " The title of this "+chat_type+ " was changed to "+color.YELLOW+msg['new_chat_title']+color.RESET+" by "+color.CYAN+fnick +color.RESET+ " ( "+fuserid+" )"
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
            dlogwc = dlogwc+ ' ' + color.CYAN+fnick + color.RESET+" ( "+fuserid+" ) in "+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog,dlogwc)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
        if flog != "":
            clog(flog)
        #command_detect
        global function_list_data
        try:
            groupfundict = function_list_data[str(chat_id)]
        except:
            function_default(chat_id,msg,chat_type)
            groupfundict = function_list_data[str(chat_id)]
        try:
            chat_config[chat_id]
        except:
            default_lang(chat_id)
        if content_type == 'text' and edited == False:
            cmd = msg['text'].split()
            cmd[0]=cmd[0].lower()
            sortedcmd = []
            for i in cmd:
                if i not in sortedcmd:
                    sortedcmd.append(i)
            if cmd[0] == '/start' or cmd[0] == '/start@'+username.lower():
                startc(chat_id,msg)
            if cmd[0] == '/cgp' or cmd[0] == '/cgp@'+username.lower():
                if groupfundict['grouppic']:
                    cgp(chat_id,msg,chat_type)
            if cmd[0] == '/rgp' or cmd[0] == '/rgp@'+username.lower():
                if groupfundict['grouppic']:
                    rgp(chat_id,msg,chat_type)
            if cmd[0] == '/echo' or cmd[0] == '/echo@'+username.lower():
                if groupfundict['echo']:
                    echo(chat_id,msg)
            if cmd[0] == '/ns' or cmd[0] == '/ns@'+username.lower():
                if groupfundict['numbersystem']:
                    ns(chat_id,msg,cmd)
            if cmd[0] == '/ping' or cmd[0] == '/ping@'+username.lower():
                if groupfundict['ping']:
                    ping(chat_id,msg)
                    return
            if cmd[0] == '/title' or cmd[0] == '/title@'+username.lower():
                if groupfundict['title']:
                    title(chat_id,msg,chat_type)
            if cmd[0] == '/lsadmins' or cmd[0] == '/lsadmins@'+username.lower():
                if groupfundict['lsadmins']:
                    lsadmins(chat_id,msg,cmd)
            if cmd[0] == '/groupinfo' or cmd[0] == '/groupinfo@'+username.lower():
                if groupfundict['groupinfo']:
                    groupinfo(chat_id,msg,chat_type)
            if cmd[0] == '/leavegroup' or cmd[0] == '/leavegroup@'+username.lower():
                leavegroup(chat_id,msg,chat_type)
            if cmd[0] == '/a2z' or cmd[0] == '/a2z@'+username.lower():
                if groupfundict['a2z']:
                    a2zc(chat_id,msg)
            if cmd[0] == '/getuser' or cmd[0] == '/getuser@'+username.lower():
                if groupfundict['user']:
                    getuser(chat_id,msg,cmd)
            if cmd[0] == '/getme' or cmd[0] == '/getme@'+username.lower():
                if groupfundict['user']:
                    getme(chat_id,msg)
            if cmd[0] == '/exportchatlink' or cmd[0] == '/exportchatlink@'+username.lower():
                if groupfundict['export_link']:
                    exportchatlink(chat_id,msg,chat_type)
            if cmd[0] == '/delmsg' or cmd[0] == '/delmsg@'+username.lower():
                if groupfundict['delete_message']:
                    delmsg(chat_id,msg,chat_type)
            if cmd[0] == '/pin' or cmd[0] == '/pin@'+username.lower():
                if groupfundict['pin']:
                    pin(chat_id,msg,chat_type)
            if cmd[0] == '/replace' or cmd[0] == '/replace@'+username.lower():
                if groupfundict['replace_str']:
                    replace(chat_id,msg,cmd)
            if cmd[0] == '/getfile' or cmd[0] == '/getfile@'+username.lower():
                if groupfundict['files']:
                    getfile(chat_id,msg,cmd)
            if cmd[0] == '/fileinfo' or cmd[0] == '/fileinfo@'+username.lower():
                if groupfundict['files']:
                    fileinfo(chat_id,msg)
            if cmd[0] == '/tag' or cmd[0] == '/tag@'+username.lower():
                if groupfundict['tag']:
                    try:
                        a = sortedcmd[2]
                    except:
                        try:
                            if cmd[1] == 'list' and cmd[2] == 'list':
                                sortedcmd.append('list')
                        except:
                            time.sleep(0)
                    tag(chat_id,msg,sortedcmd,chat_type)
            if cmd[0] == '/function' or cmd[0] == '/function@'+username.lower():
                function(chat_id,msg,cmd,chat_type)
                return
            if cmd[0] == '/confirm' or cmd[0] == '/confirm@'+username.lower():
                confirm(chat_id,msg)
            if cmd[0] == '/gtts' or cmd[0] == '/gtts@'+username.lower():
                if groupfundict['google_tts']:
                    gtts(chat_id,msg)
            if cmd[0] == '/help' or cmd[0] == '/help@'+username.lower():
                help(chat_id,msg)
            if cmd[0] == '/setlang' or cmd[0] == '/setlang@'+username.lower():
                set_lang(chat_id,msg,cmd,chat_type)
            if msg['text'].lower().find('ping') != -1:
                if groupfundict['ping']:
                    ping(chat_id,msg)
                    return
            for txt in sortedcmd:
                if txt == '@tagall':
                    #tag(chat_id,msg,["/tag","all"],chat_type)
                    time.sleep(0)
                elif txt == '@tagadmin' or txt == '@admin':
                    if groupfundict['tag']:
                        tag(chat_id,msg,["/tag","admin"],chat_type)
                elif txt[0:4] == '@tag':
                    if txt == '@tag':
                        return
                    else:
                        if groupfundict['tag']:
                            tag(chat_id,msg,["/tag","tag",txt[4:]],chat_type)
            if groupfundict['replace_str']:
                repsep = msg['text'].split('/',2)
                if repsep[0] == "s":
                    try:
                        tobereplaced = repsep[1]
                        toreplace = repsep[2]
                    except:
                        clog('[Info] Imcompleted replace method.Ignoring.')
                    else:
                        replace(chat_id,msg,['/replace',tobereplaced,toreplace])
        else:
            try:
                cmd = msg['caption'].split()
                cmd[0]=cmd[0].lower()
                sortedcmd = []
                for i in cmd:
                    if i not in sortedcmd:
                        sortedcmd.append(i)
            except:
                time.sleep(0)
            else:
                for txt in sortedcmd:
                    if txt == '@tagall':
                        #tag(chat_id,msg,["/tag","all"],chat_type)
                        time.sleep(0)
                    elif txt[0:4] == '@tag':
                        if txt == '@tag':
                            return
                        else:
                            if groupfundict['tag']:
                                tag(chat_id,msg,["/tag","tag",txt[4:]],chat_type)
            if groupfundict['replace_str']:
                try:
                    repsep = msg['caption'].split('/',2)
                except:
                    time.sleep(0)
                else:
                    if repsep[0] == "s":
                        try:
                            tobereplaced = repsep[1]
                            toreplace = repsep[2]
                        except:
                            clog('[Info] Imcompleted replace method.Ignoring.')
                        else:
                            replace(chat_id,msg,['/replace',tobereplaced,toreplace])
    elif chat_type == 'channel':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        dlogwc = dlogwc + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']
        except:
            dlog = dlog
        else: 
            dlog = dlog + " ( Reply to "+str(msg['reply_to_message']['message_id'])+" )"
            dlogwc = dlogwc+color.PURPLE + " ( Reply to "+str(msg['reply_to_message']['message_id'])+" )"+color.RESET
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick 
            dlogwc = dlogwc+color.CYAN+ ' ' + fnick +color.RESET
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
                dlogwc = dlogwc + " ( "+fuserid+" )"
            dlog = dlog + ' ' + " in channel "+msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
            dlogwc = dlogwc + ' ' + " in channel "+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ): ' + msg['text']
        elif content_type == 'new_chat_photo':
            dlog = dlog + " The photo of this "+chat_type+""+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) was changed by '+fnick 
            dlogwc = dlogwc + " The photo of this "+chat_type+""+ ' '+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was changed by '+color.CYAN+fnick +color.RESET

            if fuserid:
                dlog = dlog+ " ( "+fuserid+" )"
            flog = "[New Chat Photo]"
            photo_array=msg['new_chat_photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'delete_chat_photo':
            dlog = dlog + " The photo of this "+chat_type+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) was deleted by '+fnick
            dlogwc = dlogwc + " The photo of this "+chat_type+ ' '+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) was deleted by '+color.BLUE+fnick+color.RESET
            if fuserid:
                dlog = dlog+ " ( "+fuserid+" )"
        elif content_type == 'new_chat_title':
            dlog = dlog + " The title of this "+chat_type+ " was changed to "+color.yellow+msg['new_chat_title']+color.RESET+" by "+color.CYAN+fnick+color.RESET
            if fuserid:
                dlog = dlog+ " ( "+fuserid+" )"
        else:
            dlog = dlog + ' ' + fnick 
            dlogwc = dlogwc + ' ' +color.CYAN+ fnick+color.RESET
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
            dlog = dlog +" in channel"+msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
            dlogwc = dlogwc +" in channel"+color.YELLOW+msg['chat']['title']+color.RESET+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
        if flog != "":
            clog(flog)

def on_callback_query(msg):
    log("[Debug] Raw query data:"+str(msg))
    orginal_message = msg['message']['reply_to_message']
    message_with_inline_keyboard = msg['message']
    content_type, chat_type, chat_id = telepot.glance(orginal_message)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info]["+str(query_id)+"] Callback query form "+str(from_id)+" to "+str(orginal_message['message_id'])+" :"+ data)
    if data == 'confirm_delete':
        confirm_delete(chat_id,orginal_message,query_id,message_with_inline_keyboard,from_id)
    elif data == 'cancel_delete':
        cancel_delete(chat_id,orginal_message,query_id,message_with_inline_keyboard,from_id)

def startc(chat_id,msg):
    dre = bot.sendMessage(chat_id,'JUST an utilities bot\n/help',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def cgp(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['cgp']
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,\
            langport['all_member_are_admin'],\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        reply_to = msg['reply_to_message']
    except:
        if msg['from']['id'] == OWNERID:
            clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
            url = msg['text'].split(' ',1)
            try:
                log("[Debug] Attemping to download "+url[1])
                urllib.request.urlretrieve (url[1],"image.jpg")
            except:
                dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                fo=open(os.getcwd()+"/image.jpg", 'rb')
                try:
                    bot.sendChatAction(chat_id,'upload_photo')
                    log("[Debug]Uploading...")
                    bot.setChatPhoto(chat_id,fo)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                        +str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
                fo.close()
                os.remove('image.jpg')
            return
        else:
            clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
            for admin in bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                    url = msg['text'].split(' ',1)
                    log("[Debug] Attemping to download "+url[1])
                    try:
                        urllib.request.urlretrieve (url[1],"image.jpg")
                    except:
                        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                    else:
                        fo=open(os.getcwd()+"/image.jpg", 'rb')
                        try:
                            bot.sendChatAction(chat_id,'upload_photo')
                            log("[Debug]Uploading...")
                            bot.setChatPhoto(chat_id,fo)
                        except:
                            tp, val, tb = sys.exc_info()
                            sval=str(val)
                            bot.sendChatAction(chat_id,'typing')
                            dre = bot.sendMessage(chat_id,\
                                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                                parse_mode = 'Markdown',\
                                reply_to_message_id=msg['message_id'])
                            log("[Debug] Raw sent data:"+str(dre))
                            clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                                +str(val).split(',')[0].replace('(','').replace("'",""))
                        else:
                            clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
                        fo.close()
                        os.remove('image.jpg')
                    return
            clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
            bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
            return
        
    else:
        if msg['from']['id'] == OWNERID:
            clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
            try:
                photo_array=msg['reply_to_message']['photo']
                log("[Debug] File_id to set:"+str(photo_array))
            except:
                dre = bot.sendMessage(chat_id,langport['reply_not_pic'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                bot.sendChatAction(chat_id,'upload_photo')
                photo_array.reverse()
                file = bot.getFile(photo_array[0]['file_id'])['file_path']
                urllib.request.urlretrieve ("https://api.telegram.org/file/bot"+TOKEN+"/"+file, "image.jpg")
                fo=open(os.getcwd()+"/image.jpg", 'rb')
                try:
                    bot.setChatPhoto(chat_id,fo)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
                fo.close()
                os.remove('image.jpg')
            return
        else:
            clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
            for admin in bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                    try:
                        photo_array=msg['reply_to_message']['photo']
                        log("[Debug] File_id to set:"+str(photo_array))
                    except:
                        dre = bot.sendMessage(chat_id,langport['reply_not_pic'],reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                    else:
                        bot.sendChatAction(chat_id,'upload_photo')
                        photo_array.reverse()
                        file = bot.getFile(photo_array[0]['file_id'])['file_path']
                        urllib.request.urlretrieve ("https://api.telegram.org/file/bot"+TOKEN+"/"+file, "image.jpg")
                        fo=open(os.getcwd()+"/image.jpg", 'rb')
                        try:
                            bot.setChatPhoto(chat_id,fo)
                        except:
                            tp, val, tb = sys.exc_info()
                            sval=str(val)
                            bot.sendChatAction(chat_id,'typing')
                            dre = bot.sendMessage(chat_id,\
                                langport['error'].format(+str(val).split(',')[0].replace('(','').replace("'","`")),\
                                parse_mode = 'Markdown',\
                                reply_to_message_id=msg['message_id'])
                            log("[Debug] Raw sent data:"+str(dre))
                            clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                        else:
                            clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
                        fo.close()
                        os.remove('image.jpg')
                    return
            clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
            bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
            return
    return

def rgp(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['rgp']
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,\
            langport['all_member_are_admin'],\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    if msg['from']['id'] == OWNERID:
        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
        try:
            bot.deleteChatPhoto(chat_id)
        except:
            tp, val, tb = sys.exc_info()
            sval=str(val)
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] Unable to remove the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            clog('[Info] Sucessfully removed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
        return
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                try:
                    bot.deleteChatPhoto(chat_id)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to remove the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                        +str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully removed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
    
    return

def echo(chat_id,msg):
    echotxt = msg['text'].split(' ',1)
    try:
        dre = bot.sendMessage(chat_id,echotxt[1],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    except:
        dre = bot.sendMessage(chat_id,'/echo <String>',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return

def ns(chat_id,msg,txt):     
    langport=lang[chat_config[chat_id]["lang"]]["display"]['ns']
    try:
        log("[Info] Number to transfer :"+txt[2])
    except:
        dre = bot.sendMessage(chat_id,langport['help'],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    if txt[1] == "todec":
        try:
            result = int(txt[2],0)
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] ERROR when transfering to dec in'+msg['chat']['title']+'('+str(chat_id)+') : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            clog("[Info] ---> "+str(result))
            try:
                dre = bot.sendMessage(chat_id,"`"+str(result)+"`",parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            except:
                dre = bot.sendMessage(chat_id,\
                    pastebin(str(result),'dec-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'","")),\
                    parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tobin":
        try:
            result = bin(int(txt[2],0))
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            clog("[Info] ---> "+str(result))
            try:
                dre = bot.sendMessage(chat_id,"`"+str(result)[2:]+"`",parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            except:
                dre = bot.sendMessage(chat_id,\
                    pastebin(str(result)[2:],'bin-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'","")),\
                    parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tooct":
        try:
            result = oct(int(txt[2],0))
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','')).replace("'","`"),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            clog("[Info] ---> "+str(result))
            try:
                dre = bot.sendMessage(chat_id,"`"+str(result)[2:]+"`",parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            except:
                dre = bot.sendMessage(chat_id,\
                    pastebin(str(result)[2:],'oct-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'","")),\
                    parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    elif txt[1] == "tohex":
        try:
            result = hex(int(txt[2],0))
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] ERROR when transfering to bin in'+msg['chat']['title']+'('+str(chat_id)+') : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            clog("[Info] ---> "+str(result))
            try:
                dre = bot.sendMessage(chat_id,"`"+str(result)[2:]+"`",parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            except:
                dre = bot.sendMessage(chat_id,\
                    pastebin(str(result)[2:],'hex-'+time.strftime("%Y/%d/%m-%H:%M:%S").replace("'","")),\
                    parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    else:
        dre = bot.sendMessage(chat_id,langport['help'],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return
  
def ping(chat_id,msg):
    if msg['text'].startswith('/'):
        dre = bot.sendMessage(chat_id,'Pong',reply_to_message_id=msg['message_id'])
    else:
        dre = bot.sendMessage(chat_id,msg['text'].replace('i', 'o').replace('I', 'O'), reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def title(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['title']
    cmd=msg['text'].split(' ',1)
    try:
        title=cmd[1]
    except:
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            dre = bot.sendMessage(chat_id,langport['all_member_are_admin'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,langport['all_member_are_admin'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        if msg['from']['id'] == OWNERID:
            clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
            try:
                bot.setChatTitle(chat_id,title)
            except:
                tp, val, tb = sys.exc_info()
                sval=str(val)
                bot.sendChatAction(chat_id,'typing')
                dre = bot.sendMessage(chat_id,\
                    langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                    parse_mode = 'Markdown',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] Unable to change the Group title in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                    +str(val).split(',')[0].replace('(','').replace("'",""))
            else:
                clog('[Info] Sucessfully changed the Group title in '+msg['chat']['title']+'('+str(chat_id)+')')
            return
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                try:
                    bot.setChatTitle(chat_id,title)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to change the Group title in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                        +str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully changed the Group title in '+msg['chat']['title']+'('+str(chat_id)+')')
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        return
    return

def lsadmins(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['lsadmins']
    bot.sendChatAction(chat_id,"typing")
    try:
        group=cmd[1]
    except:
        group=chat_id
    else:
        try:
            bot.getChatAdministrators(group)
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] ERROR when getting group'+group+ ' : '\
                +str(val).split(',')[0].replace('(','').replace("'",""))
            group=chat_id
    target_group = bot.getChat(group)
    group_type = target_group['type']
    log("[Debug] Group type: "+group_type)
    adminmsg = target_group['title'] 
    log("[Debug] Raw admins data:"+str(bot.getChatAdministrators(group)))
    for admin in bot.getChatAdministrators(group):
        if admin['status'] == "creator":
            firstname = admin['user']['first_name']
            try:
                lastname = admin['user']['last_name']
            except:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + admin['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
            except:
                nickname = firstname + ' ' + lastname
            adminmsg=adminmsg + "\n"+langport['creator'].format(nickname)+"\n"
            if group_type == 'group' and target_group['all_members_are_administrators'] == True:
                adminmsg = adminmsg + '\n'+langport['everyone_is_admin']
    for admin in bot.getChatAdministrators(group):
        adminmsg = adminmsg + '\n'
        if admin['status'] == "administrator":
            firstname = admin['user']['first_name']
            try:
                lastname = admin['user']['last_name']
            except:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + admin['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
            except:
                nickname = firstname + ' ' + lastname
            if group_type == 'supergroup':
                if admin['can_change_info'] == True:
                    adminmsg = adminmsg + "ℹ️"
                else:
                    adminmsg = adminmsg + "🌚"
                if admin['can_delete_messages'] == True:
                    adminmsg = adminmsg + "🗑️"
                else:
                    adminmsg = adminmsg + "🌚"
                if admin['can_restrict_members'] == True:
                    adminmsg = adminmsg + "🚫"
                else:
                    adminmsg = adminmsg + "🌚"
                if admin['can_pin_messages'] == True:
                    adminmsg = adminmsg + "📌"
                else:
                    adminmsg = adminmsg + "🌚"
                if admin['can_promote_members'] == True:
                    adminmsg = adminmsg + "👮‍♀️"
                else:
                    adminmsg = adminmsg + "🌚"
                if admin['can_invite_users'] == True:
                    adminmsg = adminmsg + "➕ "
                else:
                    adminmsg = adminmsg + "🌚 "
            else:
                adminmsg = adminmsg + langport['admin_badge']+" - "
            adminmsg = adminmsg +nickname
    dre = bot.sendMessage(chat_id,adminmsg,parse_mode = 'HTML',disable_web_page_preview=True,reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    print('[Info]Admin list for ',target_group['title'],' ( ',str(target_group['id']), ' ): ')
    log("[Info]")
    clog(adminmsg)
    return

def groupinfo(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['groupinfo']
    dre = bot.sendMessage(chat_id,\
        langport['grouptype'].format(chat_type)+"\n"+\
        langport['groupname'].format(msg['chat']['title'])+"\n"+\
        langport['groupcount'].format(str(bot.getChatMembersCount(chat_id))) +"\n"+\
        langport['groupid'].format("<code>"+str(chat_id) + "</code>"),\
        parse_mode = 'HTML',\
        reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def leavegroup(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['leavegroup']
    if msg['from']['id'] == OWNERID:
        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
        dre = bot.sendMessage(chat_id,langport['farewell'],reply_to_message_id=msg['message_id'])
        bot.leaveChat(chat_id)
        log("[Debug] Raw sent data:"+str(dre))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,langport['farewell'],reply_to_message_id=msg['message_id'])
        bot.leaveChat(chat_id)
        log("[Debug] Raw sent data:"+str(dre))
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                dre = bot.sendMessage(chat_id,langport['farewell'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                bot.leaveChat(chat_id)
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    return

def a2zc(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['a2z']
    try:
        reply_to = msg['reply_to_message']
    except:
        alpt = msg['text'].split(' ',1)
        try:
            tcm=alpt[1]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            temp=tcm.split(' ',1)
            if temp[0] == 'etan':
                string=a2z_etan(temp[1])
            else:
                string=a2z(tcm)
            dre = bot.sendMessage(chat_id,string,reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    else:
        cmd = msg['text'].split(' ',1)
        try:
            tcm = reply_to['text']
        except:
            dre = bot.sendMessage(chat_id,langport['not_text'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                temp = cmd[1]
            except:
                string=a2z(tcm)
            else:
                if temp == 'etan':
                    string=a2z_etan(tcm)
                else:
                    string=a2z(tcm)
            dre = bot.sendMessage(chat_id,string,reply_to_message_id=reply_to['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    return

def getuser(chat_id,msg,txt):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['getuser']
    try:
        reply_to = msg['reply_to_message']
    except:
        try:
            uuser_id = int(txt[1])
        except:
            dre = bot.sendMessage(chat_id,langport['help'],parse_mode = 'HTML',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                user = bot.getChatMember(chat_id,uuser_id)
            except:
                tp, val, tb = sys.exc_info()
                bot.sendChatAction(chat_id,'typing')
                dre = bot.sendMessage(chat_id,\
                    langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                    parse_mode = 'Markdown',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] ERROR when getting user'+str(uuser_id)+ 'in'+msg['chat']['title']+'('+str(chat_id)+') : '\
                    +str(val).split(',')[0].replace('(','').replace("'",""))
            else:
                firstname = user['user']['first_name']
                try:
                    lastname = user['user']['last_name']
                except:
                    lastname = ''
                try:
                    uusername = '@' + user['user']['username']
                    nickname = '<a href="https://t.me/' + user['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
                except:
                    uusername = 'Undefined'
                    nickname = firstname + ' ' + lastname
                userid = str(user['user']['id'])
                dre = bot.sendMessage(chat_id, \
                    langport['nick'].format(nickname) + '\n'+\
                    langport['username'].format(uusername)  + '\n' +\
                    langport['userid'].format('<code>' + userid +'</code>')+ '\n' +\
                    langport['status'].format(user['status']),parse_mode = 'HTML',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            cmd = txt[1]
        except:
            uuserid = reply_to['from']['id']
        else:
            if cmd == 'forward':
                try:
                    uuserid = reply_to['forward_from']['id']
                except:
                    uuserid = reply_to['from']['id']
            else:
                uuserid = reply_to['from']['id']
        user = bot.getChatMember(chat_id,uuserid)
        firstname = user['user']['first_name']
        try:
            lastname = user['user']['last_name']
        except:
            lastname = ''
        try:
            uusername = '@' + user['user']['username']
            nickname = '<a href="https://t.me/' + user['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
        except:
            uusername = 'Undefined'
            nickname = firstname + ' ' + lastname
        userid = str(user['user']['id'])
        dre = bot.sendMessage(chat_id, \
            langport['nick'].format(nickname) + '\n'+\
            langport['username'].format(uusername)  + '\n' +\
            langport['userid'].format('<code>' + userid +'</code>')+ '\n' +\
            langport['status'].format(user['status']),parse_mode = 'HTML',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return

def getme(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['getuser']
    user= bot.getChatMember(chat_id,msg['from']['id'])
    firstname = user['user']['first_name']
    try:
        lastname = user['user']['last_name']
    except:
        lastname = ''
    try:
        uusername = '@' + user['user']['username']
        nickname = '<a href="https://t.me/' + user['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
    except:
        uusername = 'Undefined'
        nickname = firstname + ' ' + lastname
    userid = str(user['user']['id'])
    dre = bot.sendMessage(chat_id, \
        langport['nick'].format(nickname) + '\n'+\
        langport['username'].format(uusername)  + '\n' +\
        langport['userid'].format('<code>' + userid +'</code>')+ '\n' +\
        langport['status'].format(user['status']),parse_mode = 'HTML',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def pin(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['pin']
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,langport['reply_help'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        if chat_type == 'group':
            dre = bot.sendMessage(chat_id,langport['group'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if msg['from']['id'] == OWNERID:
                clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
                try:
                    bot.pinChatMessage(chat_id,reply_to['message_id'],disable_notification=True)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to pin the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully pinned the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+')')
                return
            clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
            for admin in bot.getChatAdministrators(chat_id):
                if msg['from']['id'] == admin['user']['id']:
                    clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                    try:
                        bot.pinChatMessage(chat_id,reply_to['message_id'],disable_notification=True)
                    except:
                        tp, val, tb = sys.exc_info()
                        sval=str(val)
                        bot.sendChatAction(chat_id,'typing')
                        dre = bot.sendMessage(chat_id,\
                            langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                            parse_mode = 'Markdown',\
                            reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        clog('[ERROR] Unable to pin the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                    else:
                        clog('[Info] Sucessfully pinned the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+')')
                    return
            clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
            dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            return
    return

def replace(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['replace']
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,langport['help_not_reply'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            rstring=reply_to['text']
        except:
            try:
                rstring=reply_to['caption']
            except:
                dre = bot.sendMessage(chat_id,langport['not_text'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
        try:
            test=cmd[1]
            test=cmd[2]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],\
                parse_mode='Markdown',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                if cmd[2] == "''" :
                    rstring = rstring.replace(cmd[1],'')
                else:
                    rstring = rstring.replace(cmd[1],cmd[2])
            except:
                tp, val, tb = sys.exc_info()
                bot.sendChatAction(chat_id,'typing')
                dre = bot.sendMessage(chat_id,\
                    langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                    parse_mode = 'Markdown',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] ERROR when replacing '+cmd[1]+' to ' + cmd[2]+msg['chat']['title']+'('+str(chat_id)+') : '\
                    +str(val).split(',')[0].replace('(','').replace("'",""))
            else:
                fuser = msg['from']
                fnick = fuser['first_name']
                try:
                    fnick = fnick + ' ' + fuser['last_name']
                except:
                    fnick = fnick
                tuser = msg['reply_to_message']['from']
                tnick = tuser['first_name']
                try:
                    tnick = tnick + ' ' + tuser['last_name']
                except:
                    tnick = tnick
                if fuser['id'] == tuser['id']:
                    smsg= langport['result_self'].format('<a href="tg://user?id='+str(tuser['id'])+'">'+tnick+'</a>','<i>'+rstring +'</i>')
                else:
                    smsg= langport['result'].format('<a href="tg://user?id='+str(fuser['id'])+'">'+fnick+'</a>','<a href="tg://user?id='+str(tuser['id'])+'">'+tnick+'</a>','<i>'+rstring +'</i>')
                dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    return

def getfile(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['getfile']
    bot.sendChatAction(chat_id,"upload_document")
    try:
        file_id = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            file = bot.getFile(file_id)
            log("[Debug] Raw get data:"+str(file))
        except:
            tp, val, tb = sys.exc_info()
            dre = bot.sendMessage(chat_id,\
                langport['error'].format("<code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>"),\
                parse_mode = 'HTML',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] Unable to fetch the file '+file_id+'  : '+str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            type = file['file_path'].split("/")
            try:
                if type[0] == 'photos':
                    dre = bot.sendPhoto(chat_id,file_id,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                elif type[0] == 'voice':
                    dre = bot.sendVoice(chat_id,file_id,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                elif type[0] == 'videos':
                    dre = bot.sendVideo(chat_id,file_id,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                else:
                    dre = bot.sendDocument(chat_id,file_id,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
            except:
                tp, val, tb = sys.exc_info()
                dre = bot.sendMessage(chat_id,\
                    langport['senderror'].format('<code>'+str(val).split(',')[0].replace('(','').replace("'","")+"</code>"),\
                    parse_mode = 'HTML',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] Unable to send the file '+file_id+'  : '+str(val).split(',')[0].replace('(','').replace("'",""))
    return

def fileinfo(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['fileinfo']
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        tcontent_type, tchat_type, tchat_id = telepot.glance(reply_to)
        if tcontent_type == 'text':
            dre = bot.sendMessage(chat_id,lang['istext'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            return
        elif tcontent_type == 'photo':
            photo_array=reply_to['photo']
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
        dre = bot.sendMessage(chat_id,\
            langport['filetype'].format(tcontent_type)+"\n"+\
            langport['fileid'].format('<code>'+fileid+"</code>"),\
            parse_mode="HTML",reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return

def exportblog(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['exportblog']
    cmd = msg['text'].split(" ",1)
    try:
        debugs = cmd[1]
    except:
        if msg['from']['id'] == OWNERID:
            f = open(logpath+".log","rb")
            dre = bot.sendDocument(chat_id,f,reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            f.close()
        else:
            dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
    else:
        if msg['from']['id'] == OWNERID:
            if Debug == True and debugs == "-debug":
                f = open(logpath+"-debug.log","rb")
                dre = bot.sendDocument(chat_id,f,reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                f.close()
            else:
                if Debug == False and debugs == "-debug":
                    dre = bot.sendMessage(chat_id,langport['debug_off'],reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                elif Debug == True and debugs != "-debug":
                    dre = bot.sendMessage(chat_id,langport['debug'],reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                f = open(logpath+".log","rb")
                dre = bot.sendDocument(chat_id,f,reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                f.close()
        else:
            dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
    return

def readtag():
    clog("[Info] Reading tag data...",color.BLUE+"[Info]"+color.RESET+" Reading tag data...")
    if os.path.isfile("./tagdata.json") == False:
        fs = open("./tagdata.json","w")
        fs.write("{}")
        fs.close
    fs = open("./tagdata.json","r")
    data = eval(fs.read())
    fs.close
    return(data)

def writetag(data):
    clog("[Info] Writing tag data...",color.BLUE+"[Info]"+color.RESET+" Writing tag data...")
    fs = open("./tagdata.json","w")
    fs.write(str(data))
    fs.close
    return

def addtag(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['add']
    try:
        reply_to = msg['reply_to_message']
    except:
        data=readtag()
        try:
            temptaglist = data[str(chat_id)][cmd[2]]
        except:
            temptaglist = []
        try:
            grouptagdict = data[str(chat_id)]
        except:
            grouptagdict = {}
        try:
            tagname = cmd[2]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                testcmduser = cmd[3]
            except:
                dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                successmsg = langport['b_success'].format("<b>" + cmd[2] + "</b>")+"\n"
                successcount = 0
                errmsg = langport['b_error'].format("<b>" + cmd[2] + "</b>")+"\n"
                errcount = 0
                if len(cmd) >= 54:
                    dre = bot.sendMessage(chat_id,langport['too_many'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    cmd = cmd[0:53]
                bot.sendChatAction(chat_id,"typing")
                for a in cmd[3:]:
                    try:
                        user = bot.getChatMember(chat_id,int(a))
                    except:
                        tp, val, tb = sys.exc_info()
                        clog("[ERROR] Errored when getting user "+ a + " :"+str(val).split(',')[0].replace('(','').replace("'",""))
                        errmsg = errmsg +"<b>"+ a + "</b> : <code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>\n"
                        errcount = errcount + 1
                        continue
                    else:
                        try:
                            temptaglist.index(int(a))
                        except:
                            temptaglist.append(int(a))
                        else:
                            clog("[ERROR] Errored when adding user " + a + " to "+cmd[2]+" :The user is already in the list")
                            errmsg = errmsg +"<b>"+ a + "</b> : <code>"+langport['already_exist']+"</code>\n"
                            errcount = errcount + 1
                            continue
                        adduser = bot.getChatMember(chat_id,int(a))
                        firstname = adduser['user']['first_name']
                        try:
                            lastname = adduser['user']['last_name']
                        except:
                            lastname = ''
                        try:
                            nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
                        except:
                            nickname = firstname + ' ' + lastname
                        successmsg = successmsg + nickname + "\n"
                        successcount = successcount + 1
                        clog("[Info] " + firstname + ' ' + lastname + " was added to "+cmd[2])
                grouptagdict[cmd[2]]=temptaglist
                if len(grouptagdict[cmd[2]]) == 0:
                    del grouptagdict[cmd[2]]
                data[str(chat_id)]=grouptagdict
                writetag(data)
                successmsg = successmsg + "\n"
                errmsg = errmsg + "\n"        
                if successcount == 0:
                    successmsg = ""
                if errcount == 0:
                    errmsg = ""
                dre = bot.sendMessage(chat_id,successmsg+errmsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
    else:
        data=readtag()
        try:
            temptaglist = data[str(chat_id)][cmd[2]]
        except:
            temptaglist = []
        try:
            grouptagdict = data[str(chat_id)]
        except:
            grouptagdict = {}
        smsg=""
        userid=reply_to['from']['id']
        try:
            user = bot.getChatMember(chat_id,userid)
        except:
            tp, val, tb = sys.exc_info()
            clog("[ERROR] Errored when getting user " + str(userid) + " :"+str(val).split(',')[0].replace('(','').replace("'",""))
            smsg = langport['r_error'].format("<b>" + str(userid) + "</b>","<b>" + cmd[2] +"</b>","<code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>")+"\n"
            dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            try:
                temptaglist.index(userid)
            except:
                temptaglist.append(userid)
            else:
                clog("[ERROR] Errored when adding user " + str(userid) + " to "+cmd[2]+" :The user is already in the list")
                smsg = langport['r_error'].format("<b>" + str(userid) + "</b>","<b>" + cmd[2] +"</b>","<code>"+langport['already_exist']+"</code>")+"\n"
                dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            adduser = bot.getChatMember(chat_id,userid)
            firstname = adduser['user']['first_name']
            try:
                lastname = adduser['user']['last_name']
            except:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
            except:
                nickname = firstname + ' ' + lastname
            smsg = smsg +langport['r_success'].format(nickname,"<b>" + cmd[2] + "</b>")
            clog("[Info] " + firstname + ' ' + lastname + " was added to "+cmd[2])
        grouptagdict[cmd[2]]=temptaglist
        if len(grouptagdict[cmd[2]]) == 0:
            del grouptagdict[cmd[2]]
        data[str(chat_id)]=grouptagdict
        writetag(data)
        dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    return

def rmtag(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['remove']
    try:
        reply_to = msg['reply_to_message']
    except:
        data=readtag()
        try:
            temptaglist = data[str(chat_id)][cmd[2]]
        except:
            temptaglist = []
        try:
            grouptagdict = data[str(chat_id)]
        except:
            grouptagdict = {}
        try:
            tagname = cmd[2]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if tagname == "*":
                global confirmsg
                if grouptagdict == {}:
                    dre = bot.sendMessage(chat_id,langport['no_list'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
                if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                    dre = bot.sendMessage(chat_id,langport['remove_all']['warn'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    confirmsg = dre
                    return
                else:
                    if msg['from']['id'] == OWNERID:
                        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
                        dre = bot.sendMessage(chat_id,langport['remove_all']['warn'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                        confirmsg = dre
                        log("[Debug] Raw sent data:"+str(dre))
                        return
                    clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
                    for admin in bot.getChatAdministrators(chat_id):
                        if msg['from']['id'] == admin['user']['id']:
                            clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                            dre = bot.sendMessage(chat_id,langport['remove_all']['warn'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                            confirmsg = dre
                            log("[Debug] Raw sent data:"+str(dre))
                            return
                    clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
                    dre = bot.sendMessage(chat_id,langport['remove_all']['no_perm'],reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
            try:
                testcmduser = cmd[3]
            except:
                dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                if cmd[3] == "*":
                    if temptaglist == []:
                        clog("[ERROR] List "+cmd[2]+ "not found.")
                        dre = bot.sendMessage(chat_id,langport['list_not_exist'].format("<b>"+cmd[2]+"</b>"),parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                        log("[Debug] Raw sent data:"+str(dre))
                        return
                    del grouptagdict[cmd[2]]
                    clog("[Info] Cleared the list "+cmd[2])
                    data[str(chat_id)]=grouptagdict
                    writetag(data)
                    dre = bot.sendMessage(chat_id,langport['list_removed'].format("<b>"+cmd[2]+"</b>"),parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
                successmsg = langport['b_success'].format("<b>" + cmd[2] + "</b>")+"\n"
                successcount = 0
                errmsg = langport['b_error'].format("<b>" + cmd[2] + "</b>")+":\n"
                errcount = 0
                if len(cmd) >= 54:
                    dre = bot.sendMessage(chat_id,langport['too_many'],parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    cmd = cmd[0:53]
                bot.sendChatAction(chat_id,"typing")
                for a in cmd[3:]:
                    try:
                        user = bot.getChatMember(chat_id,int(a))
                    except:
                        tp, val, tb = sys.exc_info()
                        clog("[ERROR] Errored when getting user " + a + " :"+str(val).split(',')[0].replace('(','').replace("'",""))
                        errmsg = errmsg +"<b>"+ a + "</b> : <code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>\n"
                        errcount = errcount + 1
                    else:
                        try:
                            temptaglist.index(int(a))
                        except:
                            clog("[ERROR] Errored when removing user " + a + " from "+cmd[2]+" :The user is not in the list")
                            errmsg = errmsg +"<b>"+ a + "</b> : <code>"+langport['not_in_list']+"</code>\n"
                            errcount = errcount + 1
                            continue
                        else:
                            temptaglist.remove(int(a))
                        rmuser = bot.getChatMember(chat_id,int(a))
                        firstname = rmuser['user']['first_name']
                        try:
                            lastname = rmuser['user']['last_name']
                        except:
                            lastname = ''
                        try:
                            nickname = '<a href="https://t.me/' + rmuser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
                        except:
                            nickname = firstname + ' ' + lastname
                        successmsg = successmsg + nickname + "\n"
                        successcount = successcount + 1
                        clog("[Info] " + firstname + ' ' + lastname + " was removed from "+cmd[2])
                grouptagdict[cmd[2]]=temptaglist
                if len(grouptagdict[cmd[2]]) == 0:
                    del grouptagdict[cmd[2]]
                data[str(chat_id)]=grouptagdict
                writetag(data)
                successmsg = successmsg + "\n"
                errmsg = errmsg + "\n"        
                if successcount == 0:
                    successmsg = ""
                if errcount == 0:
                    errmsg = ""
                dre = bot.sendMessage(chat_id,successmsg+errmsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
    else:
        data=readtag()
        try:
            temptaglist = data[str(chat_id)][cmd[2]]
        except:
            temptaglist = []
        try:
            grouptagdict = data[str(chat_id)]
        except:
            grouptagdict = {}
        smsg=""
        userid=reply_to['from']['id']
        try:
            user = bot.getChatMember(chat_id,userid)
        except:
            tp, val, tb = sys.exc_info()
            clog("[ERROR] Errored when getting user " + str(userid) + " :"+str(val).split(',')[0].replace('(','').replace("'",""))
            smsg = langport['r_error'].format("<b>" + userid + "</b>","<b>" + cmd[2] +"</b>","<code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>")+"\n"
            dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            try:
                temptaglist.index(userid)
            except:
                clog("[ERROR] Errored when remving user " + str(userid) + " from "+cmd[2]+" :The user is not in the list")
                smsg = langport['r_error'].format("<b>" + str(userid) + "</b>","<b>" + cmd[2] +"</b>","<code>"+langport['not_in_list']+"</code>")+"\n"
                dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                temptaglist.remove(userid)
            adduser = bot.getChatMember(chat_id,userid)
            firstname = adduser['user']['first_name']
            try:
                lastname = adduser['user']['last_name']
            except:
                lastname = ''
            try:
                nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
            except:
                nickname = firstname + ' ' + lastname
            smsg = smsg + langport['r_success'].format(nickname,"<b>" + cmd[2] + "</b>")
            clog("[Info] " + firstname + ' ' + lastname + " was removed from "+cmd[2])
        grouptagdict[cmd[2]]=temptaglist
        if len(grouptagdict[cmd[2]]) == 0:
            del grouptagdict[cmd[2]]
        data[str(chat_id)]=grouptagdict
        writetag(data)
        dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    return

def confirm(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['confirm']
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,langport['donotknow_confirmabout'],disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        global confirmsg
        if confirmsg == None:
            dre = bot.sendMessage(chat_id,langport['donotknow_confirmabout'],disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        if reply_to["message_id"] == confirmsg["message_id"]:
            if msg['from']['id'] != confirmsg['reply_to_message']['from']['id']:
                dre = bot.sendMessage(chat_id,langport['donotknow_confirmabout'],disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            ccmd = confirmsg['reply_to_message']['text'].split()
            if ccmd[0] == '/tag' or ccmd[0] == '/tag@'+username:
                if ccmd[1] == 'remove' and ccmd[2] == "*":
                    data=readtag()
                    del data[str(chat_id)]
                    writetag(data)
                    dre = bot.sendMessage(chat_id,langport['remove_all_success'],disable_web_page_preview=True,reply_to_message_id=confirmsg['reply_to_message']["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    confirmsg = None
        else:
            dre = bot.sendMessage(chat_id,langport['donotknow_confirmabout'],disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return

    return

def lstag(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['lstag']
    data=readtag()
    smsg = ""
    try:
        grouptagdict = data[str(chat_id)]
    except:
        dre = bot.sendMessage(chat_id,langport['no_list'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        listname = cmd[2]
    except:
        for ttag in data[str(chat_id)]:
            temptaglist = data[str(chat_id)][ttag]
            smsg = smsg +langport['all'].format("<b>"+ttag+"</b>","<b>" + str(len(temptaglist)) +"</b>")+"\n"
    else:
        try:
            temptaglist = data[str(chat_id)][listname]
        except:
            dre = bot.sendMessage(chat_id,langport['list_not_exist'].format("<b>"+listname+"</b>"),parse_mode="HTML",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            smsg = smsg +langport['list_prefix'].format("<b>"+listname+"</b>","<b>" + str(len(temptaglist)) +"</b>")+"\n"
            count = 0
            for userid in temptaglist:
                adduser = bot.getChatMember(chat_id,int(userid))
                firstname = adduser['user']['first_name']
                try:
                    lastname = adduser['user']['last_name']
                except:
                    lastname = ''
                try:
                    nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
                except:
                    nickname = firstname + ' ' + lastname
                smsg = smsg + nickname + " "
                count = count +1
                if count >= 2:
                    smsg = smsg + "\n"
                    count = 0
    dre = bot.sendMessage(chat_id,smsg,disable_web_page_preview=True,parse_mode="HTML",reply_to_message_id=msg["message_id"])
    log("[Debug] Raw sent data:"+str(dre))
    return

def tags(chat_id,msg,cmd):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['tag']
    data=readtag()
    smsg = ""
    try:
        listname = cmd[2]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            temptaglist = data[str(chat_id)][listname]
        except:
            dre = bot.sendMessage(chat_id,langport['list_not_exist'].format("<b>"+listname+"</b>"),parse_mode="HTML",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if temptaglist == []:
                dre = bot.sendMessage(chat_id,langport['list_not_exist'].format("<b>"+listname+"</b>"),parse_mode="HTML",reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            dre = bot.sendMessage(chat_id,langport['tag_prefix'].format("<b>"+listname+"</b>","<b>"+str(len(temptaglist))+"</b>"),parse_mode="HTML",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            totalcount=0
            linecount=0
            for userid in temptaglist:
                smsg = smsg + "[.](tg://user?id="+str(userid)+")"
                totalcount=totalcount+1
                linecount=linecount+1
                #if linecount >= 50:
                #    smsg = smsg + "\n"
                #    linecount = 0
                if totalcount >= 5:
                    dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
                    log("[Debug] Raw sent data:"+str(dre))
                    smsg=""
                    totalcount=0
            if totalcount != 0:
                dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
                log("[Debug] Raw sent data:"+str(dre))
    return

def tag_admin(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['tagadmin']
    if chat_type == "group" and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,langport['all_member_are_admin'],parse_mode="HTML",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    admin_list = bot.getChatAdministrators(chat_id)
    dre = bot.sendMessage(chat_id,langport['tag_prefix'].format("<b>"+str(len(admin_list))+"</b>"),parse_mode="HTML",reply_to_message_id=msg["message_id"])
    log("[Debug] Raw sent data:"+str(dre))
    smsg = ""
    totalcount=0
    for admin in admin_list:
        smsg = smsg + "[.](tg://user?id="+str(admin['user']['id'])+")"
        totalcount=totalcount+1
        if totalcount >= 5:
            dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
            log("[Debug] Raw sent data:"+str(dre))
            smsg=""
            totalcount=0
    if totalcount != 0:
        dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
        log("[Debug] Raw sent data:"+str(dre))
    return
#def tagall(chat_id,msg):
#    dre = bot.sendMessage(chat_id,"正在提及群組內的所有人",parse_mode="HTML",reply_to_message_id=msg["message_id"])
#    log("[Debug] Raw sent data:"+str(dre))
#    try:
#        full_response = pwrtg_getchat(chat_id)
#    except:
#        tp, val, tb = sys.exc_info()
#        clog("[ERROR] Errored when getting chat "+str(chat_id)+":"+str(val))
#        dre = bot.sendMessage(chat_id,\
#                    '向[pwrtelegram](https://t.me/pwrtelegram)取得該群組成員時時發生錯誤\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
#                    parse_mode = 'Markdown',\
#                    reply_to_message_id=msg['message_id'])
#        log("[Debug] Raw sent data:"+str(dre))
#    else:
#        totalcount=0
#        linecount=0
#        smsg=""
#        for user in full_response['participants']:
#            if user['user']['type'] != 'bot':
#                smsg = smsg + "[.](tg://user?id="+str(user['user']['id'])+")"
#                totalcount=totalcount+1
#                linecount=linecount+1
#            if linecount >= 50:
#                smsg = smsg + "\n"
#                linecount = 0
#            if totalcount >= 100:
#                dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
#                log("[Debug] Raw sent data:"+str(dre))
#                smsg=""
#                totalcount=0
#        if totalcount != 0:
#            dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown")
#            log("[Debug] Raw sent data:"+str(dre))
        
def tag(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['tag']['general']
    try:
        testsubcmd = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        if cmd[1] == "add":
            addtag(chat_id,msg,cmd)
        elif cmd[1] == "remove":
            rmtag(chat_id,msg,cmd,chat_type)
        elif cmd[1] == "list":
            lstag(chat_id,msg,cmd)
        elif cmd[1] == "tag":
            tags(chat_id,msg,cmd)
        elif cmd[1] == "all":
            #tagall(chat_id,msg)
            dre = bot.sendMessage(chat_id,langport['PWRAPI'],parse_mode='Markdown',reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        elif cmd[1] == "admin":
            tag_admin(chat_id,msg,chat_type)
        else:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))

    return

def exportchatlink(chat_id,msg,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['exportchatlink']
    if msg['from']['id'] == OWNERID:
        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
        try:
            link = bot.exportChatInviteLink(chat_id)
        except:
            tp, val, tb = sys.exc_info()
            sval=str(val)
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] Unable to export chat link '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
        else:
            bot.sendMessage(chat_id,link,reply_to_message_id=msg['message_id'])
            clog('[Info] Exported chat link: {0}'.format(link))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        clog('[Info] Detected a group with all members are admin enabled.')
        dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                try:
                    link = bot.exportChatInviteLink(chat_id)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","`")),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to export chat link '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    bot.sendMessage(chat_id,link,reply_to_message_id=msg['message_id'])
                    clog('[Info] Exported chat link: {0}'.format(link))
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    return

def delmsg(chat_id,msg,chat_type):
    global delete_msg_sender
    langport=lang[chat_config[chat_id]["lang"]]["display"]['delmsg']
    bot_me = bot.getMe()
    try:
        reply_to_message=msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,langport['no_reply'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            tmp=delete_msg_sender[chat_id]
        except:
            delete_msg_sender[chat_id]={}
        if chat_type == "private":
            markup = inlinekeyboardbutton_delete(chat_id)
            dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
            delete_msg_sender[chat_id][dre['message_id']]=msg
            log("[Debug] Raw sent data:"+str(dre))
        elif chat_type == 'group' or chat_type == 'supergroup':
            if msg['from']['id'] == OWNERID:
                clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
                if reply_to_message['from']['id'] == msg['from']['id']:
                    dre = bot.sendMessage(chat_id,langport['deleting_self_msg'],reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                elif reply_to_message['from']['id'] == bot_me['id']:
                    markup = inlinekeyboardbutton_delete(chat_id)
                    dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                    delete_msg_sender[chat_id][dre['message_id']]=msg
                    log("[Debug] Raw sent data:"+str(dre))
                else:
                    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                        dre = bot.sendMessage(chat_id,langport['all_member_are_admin'],reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        return
                    for admin in bot.getChatAdministrators(chat_id):
                        if bot_me['id'] == admin['user']['id']:
                            if chat_type == 'supergroup':
                                if admin['can_delete_messages']:
                                    markup = inlinekeyboardbutton_delete(chat_id)
                                    dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                                    delete_msg_sender[chat_id][dre['message_id']]=msg
                                    log("[Debug] Raw sent data:"+str(dre))
                                    return
                                else:
                                    dre = bot.sendMessage(chat_id,langport['bot_no_perm'],reply_to_message_id=msg['message_id'])
                                    log("[Debug] Raw sent data:"+str(dre))
                                    return
                            elif chat_type == 'group':
                                markup = inlinekeyboardbutton_delete(chat_id)
                                dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                                delete_msg_sender[chat_id][dre['message_id']]=msg
                                log("[Debug] Raw sent data:"+str(dre))
                                return
                    dre = bot.sendMessage(chat_id,langport['bot_no_perm'],reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                return
            if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                clog('[Info] Detected a group with all members are admin enabled.')
                dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
                for admin in bot.getChatAdministrators(chat_id):
                    if msg['from']['id'] == admin['user']['id']:
                        clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                        if reply_to_message['from']['id'] == msg['from']['id']:
                            dre = bot.sendMessage(chat_id,langport['deleting_self_msg'],reply_to_message_id=msg['message_id'])
                            log("[Debug] Raw sent data:"+str(dre))
                        elif reply_to_message['from']['id'] == bot_me['id']:
                            markup = inlinekeyboardbutton_delete(chat_id)
                            dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                            delete_msg_sender[chat_id][dre['message_id']]=msg
                            log("[Debug] Raw sent data:"+str(dre))
                        else:
                            if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                                dre = bot.sendMessage(chat_id,langport['all_member_are_admin'],reply_to_message_id=msg['message_id'])
                                log("[Debug] Raw sent data:"+str(dre))
                                return
                            for admin in bot.getChatAdministrators(chat_id):
                                if bot_me['id'] == admin['user']['id']:
                                    if chat_type == 'supergroup':
                                        if admin['can_delete_messages']:
                                            markup = inlinekeyboardbutton_delete(chat_id)
                                            dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                                            delete_msg_sender[chat_id][dre['message_id']]=msg
                                            log("[Debug] Raw sent data:"+str(dre))
                                            return
                                        else:
                                            dre = bot.sendMessage(chat_id,langport['bot_no_perm'],reply_to_message_id=msg['message_id'])
                                            log("[Debug] Raw sent data:"+str(dre))
                                            return
                                    elif chat_type == 'group':
                                        markup = inlinekeyboardbutton_delete(chat_id)
                                        dre = bot.sendMessage(chat_id,langport['confirm'], reply_markup=markup,parse_mode="HTML",reply_to_message_id=reply_to_message["message_id"])
                                        delete_msg_sender[chat_id][dre['message_id']]=msg
                                        log("[Debug] Raw sent data:"+str(dre))
                                        return
                            dre = bot.sendMessage(chat_id,langport['bot_no_perm'],reply_to_message_id=msg['message_id'])
                            log("[Debug] Raw sent data:"+str(dre))
                        return
                clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
                dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
    return

def confirm_delete(chat_id,orginal_message,query_id,message_with_inline_keyboard,from_id):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['delmsg']
    try:
        tmp = delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
    except:
        bot.answerCallbackQuery(query_id, langport["message_expired"])
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        bot.editMessageText(msg_idf,langport["message_expired"])
        return
    if from_id != tmp['from']['id']:
        bot.answerCallbackQuery(query_id,langport["not_proposer"])
        return
    try:
        msg_idf = telepot.message_identifier(orginal_message)
        bot.deleteMessage(msg_idf)
    except:
        tp, val, tb = sys.exc_info()
        bot.answerCallbackQuery(query_id,langport['error'].format(str(val).split(',')[0].replace('(','').replace("'","")))
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        bot.editMessageText(msg_idf,langport['error'].format("<code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>"),parse_mode="HTML")
    else:
        bot.answerCallbackQuery(query_id,langport["success"])
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        bot.deleteMessage(msg_idf)
        try:
            msg_idf = telepot.message_identifier(tmp)
            bot.deleteMessage(msg_idf)
        except:
            time.sleep(0)
        del delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
        #bot.editMessageText(msg_idf, langport["success"])
    return

def cancel_delete(chat_id,orginal_message,query_id,message_with_inline_keyboard,from_id):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['delmsg']
    try:
        tmp = delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
    except:
        bot.answerCallbackQuery(query_id, langport["message_expired"])
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        bot.editMessageText(msg_idf,langport["message_expired"])
        return
    if from_id != tmp['from']['id']:
        bot.answerCallbackQuery(query_id,langport["not_proposer"])
        return
    bot.answerCallbackQuery(query_id, langport["canceled"])
    msg_idf = telepot.message_identifier(message_with_inline_keyboard)
    bot.editMessageText(msg_idf,langport["canceled"])
    del delete_msg_sender[chat_id][message_with_inline_keyboard['message_id']]
    return

def inlinekeyboardbutton_delete(chat_id):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['delmsg']
    roll = random.randint(1,5)
    if roll == 1:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
            ])
    elif roll == 2:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='confirm_delete')],
                [InlineKeyboardButton(text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
            ])
    elif roll == 3:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
            ])
    elif roll == 4:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['yes'], callback_data='confirm_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
            ])
    elif roll == 5:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['no_'+str(random.randint(1,4))], callback_data='cancel_delete')],
                [InlineKeyboardButton(text=langport['yes'], callback_data='confirm_delete')],
            ])
    return markup
def gtts(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['gtts']
    cmd = msg['text'].split(' ',2)
    try:
        clang = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        try:
            txt = cmd[2]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            smsg = '[Link](https://translate.google.com.tw/translate_tts?ie=UTF-8&q='+txt+'&tl='+clang+'&client=tw-ob)'
            dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
    return

def read_chatconfig():
    global chat_config
    clog('[Info] Reading chat config data...',color.BLUE+'[Info]'+color.RESET+' Reading chat config data...')
    if os.path.isfile("./chatconfig.json") == False:
        fs = open("./chatconfig.json","w")
        fs.write("{'config_ver':'"+HJ_Ver+"'}")
        fs.close
    fs = open("./chatconfig.json","r")
    chat_config = eval(fs.read())
    fs.close
    clog('... Done.','...'+color.GREEN+'Done.')
    if chat_config['config_ver'] != HJ_Ver:
        clog('[Info] Updating chat config data...',color.BLUE+'[Info]'+color.RESET+' Updating chat config data...')
        old_chat_config = str(chat_config)
        chat_config['config_ver'] = HJ_Ver
        for i in chat_config:
            if i == 'config_ver':
                continue
            #New configs here
            time.sleep(0)
        for i in chat_config:
            if i == 'config_ver':
                continue
            for j in eval(old_chat_config)[i]:
                chat_config[i][j]=eval(old_chat_config)[i][j]
        write_chatconfig(chat_config)
    return

def write_chatconfig(data):
    clog("[Info] Writing chat config data...",color.BLUE+"[Info]"+color.RESET+" Writing chat config data...")
    fs = open("./chatconfig.json","w")
    fs.write(str(data))
    fs.close
    return

def default_lang(chat_id):
    chat_config[chat_id]={"lang":"en_US"}
    write_chatconfig(chat_config)
    return

def set_lang(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['config']
    if msg['from']['id'] == OWNERID:
        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
        set_lang_command(chat_id,msg,cmd)
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        clog('[Info] Detected a group with all members are admin enabled.')
        dre = bot.sendMessage(chat_id,langport['lang_noperm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                set_lang_command(chat_id,msg,cmd)
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        dre = bot.sendMessage(chat_id,langport['lang_noperm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    return

def set_lang_command(chat_id,msg,cmd):
    global chat_config
    bot_me = bot.getMe()
    try:
        slang=cmd[1]
    except:
        smsg=""
        for i in lang:
            smsg = smsg + "- <code>" + i + "</code> <i>"+lang[i]["display_name"]+"</i>\n"
        dre = bot.sendMessage(chat_id,"/setlang &lt;language&gt;\n\n"+smsg,parse_mode="HTML",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        try:
            tmp = chat_config[chat_id]
        except:
            try:
                tmp = lang[slang]
            except:
                smsg=""
                for i in lang:
                    smsg = smsg + "- <code>" + i + "</code> <i>"+lang[i]["display_name"]+"</i>\n"
                dre = bot.sendMessage(chat_id,"Language {0} not exist.\n\n".format("<b>"+slang+"</b>")+smsg,parse_mode="HTML",reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                chat_config[chat_id]={"lang":slang}
                write_chatconfig(chat_config)
                dre = bot.sendMessage(chat_id,\
                    lang[chat_config[chat_id]["lang"]]["display"]["config"]["langsuccess"].format(lang[chat_config[chat_id]["lang"]]["display_name"]),reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
        else:
            if slang != chat_config[chat_id]["lang"]:
                try:
                    tmp = lang[slang]
                except:
                    smsg=""
                    for i in lang:
                        smsg = smsg + "- <code>" + i + "</code> <i>"+lang[i]["display_name"]+"</i>\n"
                    dre = bot.sendMessage(chat_id,"Language {0} not exist.\n\n".format("<b>"+slang+"</b>")+smsg,parse_mode="HTML",reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                else:
                    chat_config[chat_id]["lang"] = slang
                    write_chatconfig(chat_config)
                    dre = bot.sendMessage(chat_id,\
                        lang[chat_config[chat_id]["lang"]]["display"]["config"]["langsuccess"].format(lang[chat_config[chat_id]["lang"]]["display_name"]),reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendMessage(chat_id,lang[chat_config[chat_id]["lang"]]["display"]["config"]["langexist"].format(lang[chat_config[chat_id]["lang"]]["display_name"]),reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    return

def read_function_list():
    global function_list_data
    clog('[Info] Reading function list data...',color.BLUE+'[Info]'+color.RESET+' Reading function list data...')
    if os.path.isfile("./fctlsdata.json") == False:
        fs = open("./fctlsdata.json","w")
        fs.write("{'config_ver':'"+HJ_Ver+"'}")
        fs.close
    fs = open("./fctlsdata.json","r")
    function_list_data = eval(fs.read())
    fs.close
    clog('... Done.','...'+color.GREEN+'Done.')
    if function_list_data['config_ver'] != HJ_Ver:
        clog('[Info] Updating function list data...',color.BLUE+'[Info]'+color.RESET+' Updating function list data...')
        old_function_list_data = str(function_list_data)
        function_list_data['config_ver'] = HJ_Ver
        for i in function_list_data:
            if i == 'config_ver':
                continue
            function_set_default(i)
        for i in function_list_data:
            if i == 'config_ver':
                continue
            for j in eval(old_function_list_data)[i]:
                function_list_data[i][j]=eval(old_function_list_data)[i][j]
        write_function_list(function_list_data)
    return

def write_function_list(data):
    clog("[Info] Writing function list data...",color.BLUE+"[Info]"+color.RESET+" Writing function list data...")
    fs = open("./fctlsdata.json","w")
    fs.write(str(data))
    fs.close
    return

def function(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['function']['general']
    if msg['from']['id'] == OWNERID:
        clog('[Info] Owner Matched for \n[Info] '+ str(bot.getChatMember(chat_id,msg['from']['id'])))
        try:
            testsubcmd = cmd[1]
        except:
            dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if cmd[1] == "enable":
                function_enable(chat_id,msg,cmd,chat_type)
            elif cmd[1] == "disable":
                function_disable(chat_id,msg,cmd,chat_type)
            elif cmd[1] == "chkadminf":
                function_admincheck(chat_id,msg,chat_type,True)
            elif cmd[1] == "stats":
                function_stats(chat_id,msg)
            elif cmd[1] == "reset":
                function_default(chat_id,msg,chat_type)
                dre = bot.sendMessage(chat_id,langport['reset_complete'],reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        clog('[Info] Detected a group with all members are admin enabled.')
        dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                try:
                    testsubcmd = cmd[1]
                except:
                    dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                else:
                    if cmd[1] == "enable":
                        function_enable(chat_id,msg,cmd,chat_type)
                    elif cmd[1] == "disable":
                        function_disable(chat_id,msg,cmd,chat_type)
                    elif cmd[1] == "chkadminf":
                        function_admincheck(chat_id,msg,chat_type,True)
                    elif cmd[1] == "stats":
                        function_stats(chat_id,msg)
                    elif cmd[1] == "reset":
                        function_default(chat_id,msg,chat_type)
                        dre = bot.sendMessage(chat_id,langport['reset_complete'],reply_to_message_id=msg["message_id"])
                        log("[Debug] Raw sent data:"+str(dre))
                    else:
                        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
                        log("[Debug] Raw sent data:"+str(dre))
                return
        clog('[Info] No admins matched with ' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        dre = bot.sendMessage(chat_id,langport['no_perm'],reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    return

def function_enable(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['function']['enable']
    global function_list_data
    bot_me = bot.getMe()
    try:
        testarg=cmd[2]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        function_default(chat_id,msg,chat_type)
        dre = bot.sendMessage(chat_id,langport['deploy'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    smsg = ""
    for funct in cmd[2:]:
        try:
            currentv = groupfundict[funct]
        except:
            smsg += langport['funct_not_exist'].format('<b>'+funct+'</b>') + '\n'
            # dre = bot.sendMessage(chat_id,langport['funct_not_exist'].format('<b>'+funct+'</b>'),parse_mode='HTML',reply_to_message_id=msg["message_id"])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
        if currentv == True:
            smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['already_true']+'</code>') + '\n'
            # dre = bot.sendMessage(chat_id,\
                    # langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['already_true']+'</code>'),\
                    # parse_mode='HTML',reply_to_message_id=msg['message_id'])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
        if funct == 'grouppic' or funct == 'title' or funct == 'pin' or funct == 'export_link':
            if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                clog('[Info] Detected a group with all members are admin enabled.')
                smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['all_member_are_admin']+'</code>') +'\n'
                # dre = bot.sendMessage(chat_id,\
                #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['all_member_are_admin']+'</code>'),\
                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                # log("[Debug] Raw sent data:"+str(dre))
                # function_list_data[str(chat_id)] = groupfundict
                # write_function_list(function_list_data)
                continue
            clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
            hasperm = False
            for admin in bot.getChatAdministrators(chat_id):
                if bot_me['id'] == admin['user']['id']:
                    hasperm = True
                    if chat_type == 'supergroup':
                        clog('[Info] I am an admin in this chat,checking further permissions...')
                        if funct == 'grouppic':
                            if admin['can_change_info']:
                                groupfundict['grouppic'] = True
                                smsg += langport['success'].format('<b>'+funct+'</b>')+"\n"
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['success'].format('<b>'+funct+'</b>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                            else:
                                smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>')+'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                        if funct == 'title':
                            if admin['can_change_info']:
                                groupfundict['title'] = True
                                smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['success'].format('<b>'+funct+'</b>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                            else:
                                smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>')+'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                        if funct == 'pin':
                            if admin['can_pin_messages']:
                                groupfundict['pin'] = True
                                smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['success'].format('<b>'+funct+'</b>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                            else:
                                smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>') +'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                        if funct == 'export_link':
                            if admin['can_invite_users']:
                                groupfundict['export_link'] = True
                                smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['success'].format('<b>'+funct+'</b>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                            else:
                                smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>') + '\n'
                                # dre = bot.sendMessage(chat_id,\
                                #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>'),\
                                #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                                # log("[Debug] Raw sent data:"+str(dre))
                                continue
                    elif chat_type == 'group':
                        clog('[Info] I am an admin in this chat,enabling admin functions without pin...')
                        if funct == 'grouppic':
                            groupfundict['grouppic'] = True
                            smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                            # dre = bot.sendMessage(chat_id,\
                            #     langport['success'].format('<b>'+funct+'</b>'),\
                            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                            # log("[Debug] Raw sent data:"+str(dre))
                            continue
                        if funct == 'title':
                            groupfundict['title'] = True
                            smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
                            # dre = bot.sendMessage(chat_id,\
                            #     langport['success'].format('<b>'+funct+'</b>'),\
                            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                            # log("[Debug] Raw sent data:"+str(dre))
                            continue
                        if funct == 'pin':
                            smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['group_cant_pin']+'</code>')+'\n'
                            # dre = bot.sendMessage(chat_id,\
                            #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['group_cant_pin']+'</code>'),\
                            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                            # log("[Debug] Raw sent data:"+str(dre))
                            continue
                        if funct == 'export_link':
                            smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['group_cant_export']+'</code>')+'\n'
                            # dre = bot.sendMessage(chat_id,\
                            #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['group_cant_export']+'</code>'),\
                            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
                            # log("[Debug] Raw sent data:"+str(dre))
                            continue
                # function_list_data[str(chat_id)] = groupfundict
                # write_function_list(function_list_data)
                continue
            if hasperm:
                continue
            clog('[Info] I am not an admin in this chat.')
            smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>')+'\n'
            # dre = bot.sendMessage(chat_id,\
            #     langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['no_perm']+'</code>'),\
            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
        else:
            groupfundict[funct]=True
            smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
            # dre = bot.sendMessage(chat_id,\
            #     langport['success'].format('<b>'+funct+'</b>'),\
            #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
    dre = bot.sendMessage(chat_id,\
                smsg,\
                parse_mode='HTML',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    function_list_data[str(chat_id)] = groupfundict
    write_function_list(function_list_data)
    return

def function_disable(chat_id,msg,cmd,chat_type):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['function']['disable']
    global function_list_data
    bot_me=bot.getMe()
    try:
        testarg=cmd[2]
    except:
        dre = bot.sendMessage(chat_id,langport['help'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        function_default(chat_id,msg,chat_type)
        dre = bot.sendMessage(chat_id,langport['deploy'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    if testarg == 'all':
        for funct in groupfundict:
            groupfundict[funct] = False
        function_list_data[str(chat_id)] = groupfundict
        write_function_list(function_list_data)
        dre = bot.sendMessage(chat_id,langport['success_all'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    smsg = ''
    for funct in cmd[2:]:
        try:
            currentv = groupfundict[funct]
        except:
            smsg += langport['funct_not_exist'].format('<b>'+funct+'</b>')+'\n'
            # dre = bot.sendMessage(chat_id,langport['funct_not_exist'].format('<b>'+funct+'</b>'),parse_mode='HTML',reply_to_message_id=msg["message_id"])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
        if currentv == False:
            smsg += langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['already_false']+'</code>')+'\n'
            # dre = bot.sendMessage(chat_id,\
            #         langport['failed'].format('<b>'+funct+'</b>','<code>'+langport['already_false']+'</code>'),\
            #         parse_mode='HTML',reply_to_message_id=msg['message_id'])
            # log("[Debug] Raw sent data:"+str(dre))
            continue
        groupfundict[funct]=False
        smsg += langport['success'].format('<b>'+funct+'</b>')+'\n'
        # dre = bot.sendMessage(chat_id,\
        #     langport['success'].format('<b>'+funct+'</b>'),\
        #     parse_mode='HTML',reply_to_message_id=msg['message_id'])
        # log("[Debug] Raw sent data:"+str(dre))
    dre = bot.sendMessage(chat_id,\
        smsg,\
        parse_mode='HTML',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    function_list_data[str(chat_id)] = groupfundict
    write_function_list(function_list_data)
    return

def function_admincheck(chat_id,msg,chat_type,sendchat):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['function']['admin_check']
    global function_list_data
    bot_me=bot.getMe()
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        groupfundict = {}
    smsg = ''
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        clog('[Info] Detected a group with all members are admin enabled,disabling admin functions...')
        if sendchat:
            dre = bot.sendMessage(chat_id,\
                langport['all_member_are_admin'],\
                parse_mode='HTML',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        groupfundict['grouppic'] = False
        smsg = smsg + langport['success_disable'].format('<b>grouppic</b>')+'\n'
        groupfundict['pin'] = False
        smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
        groupfundict['title'] = False
        smsg = smsg + langport['success_disable'].format('<b>title</b>')+'\n'
        groupfundict['export_link'] = False
        smsg = smsg + langport['success_disable'].format('<b>export_link</b>')+'\n'
        function_list_data[str(chat_id)] = groupfundict
        write_function_list(function_list_data)
        if sendchat:
            dre = bot.sendMessage(chat_id,\
                smsg,\
                parse_mode='HTML',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        return
    if sendchat:
        dre = bot.sendMessage(chat_id,langport['msg_checking_admin'],reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
    
    for admin in bot.getChatAdministrators(chat_id):
        if bot_me['id'] == admin['user']['id']:
            if chat_type == 'supergroup':
                clog('[Info] I am an admin in this chat,checking further permissions...')
                if admin['can_change_info']:
                    groupfundict['grouppic'] = True
                    smsg = smsg + langport['success_enable'].format('<b>grouppic</b>')+'\n'
                    groupfundict['title'] = True
                    smsg = smsg + langport['success_enable'].format('<b>title</b>')+'\n'
                else:
                    groupfundict['grouppic'] = False
                    smsg = smsg + langport['success_disable'].format('<b>grouppic</b>')+'\n'
                    groupfundict['title'] = False
                    smsg = smsg + langport['success_disable'].format('<b>title</b>')+'\n'
                if admin['can_pin_messages'] == True:
                    groupfundict['pin'] = True
                    smsg = smsg + langport['success_enable'].format('<b>pin</b>')+'\n'
                else:
                    groupfundict['pin'] = False
                    smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
                if admin['can_invite_users'] == True:
                    groupfundict['export_link'] = True
                    smsg = smsg + langport['success_enable'].format('<b>export_link</b>')+'\n'
                else:
                    groupfundict['export_link'] = False
                    smsg = smsg + langport['success_disable'].format('<b>export_link</b>')+'\n'
            elif chat_type == 'group':
                clog('[Info] I am an admin in this chat,enabling admin functions without pin...')
                groupfundict['grouppic'] = True
                smsg = smsg + langport['success_enable'].format('<b>grouppic</b>')+'\n'
                groupfundict['pin'] = False
                smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
                groupfundict['title'] = True
                smsg = smsg + langport['success_enable'].format('<b>title</b>')+'\n'
                groupfundict['export_link'] = False
                smsg = smsg + langport['success_disable'].format('<b>export_link</b>')+'\n'
            function_list_data[str(chat_id)] = groupfundict
            write_function_list(function_list_data)
            if sendchat:
                dre = bot.sendMessage(chat_id,\
                    smsg,\
                    parse_mode='HTML',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
            return
    clog('[Info] I am not an admin in this chat.')
    groupfundict['grouppic'] = False
    smsg = smsg + langport['success_disable'].format('<b>grouppic</b>')+'\n'
    groupfundict['pin'] = False
    smsg = smsg + langport['success_disable'].format('<b>pin</b>')+'\n'
    groupfundict['title'] = False
    smsg = smsg + langport['success_disable'].format('<b>title</b>')+'\n'
    groupfundict['export_link'] = False
    smsg = smsg + langport['success_disable'].format('<b>export_link</b>')+'\n'
    function_list_data[str(chat_id)] = groupfundict
    write_function_list(function_list_data)
    if sendchat:
        dre = bot.sendMessage(chat_id,\
            smsg,\
            parse_mode='HTML',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return

def function_default(chat_id,msg,chat_type):
    global function_list_data
    bot_me=bot.getMe()
    function_set_default(chat_id)
    write_function_list(function_list_data)
    function_admincheck(chat_id,msg,chat_type,False)

    return

def function_set_default(chat_id):
    global function_list_data
    bot_me=bot.getMe()
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        groupfundict = {}
    groupfundict['a2z'] = True
    groupfundict['grouppic'] = True
    groupfundict['ping'] = True
    groupfundict['echo'] = True
    groupfundict['groupinfo'] = True
    groupfundict['pin'] = True
    groupfundict['title'] = True
    groupfundict['user'] = True
    groupfundict['numbersystem'] = True
    groupfundict['files'] = True
    groupfundict['lsadmins'] = True
    groupfundict['tag'] = True
    groupfundict['google_tts'] = True
    groupfundict['replace_str'] = True
    groupfundict['delete_message'] = True
    groupfundict['export_link'] = True
    function_list_data[str(chat_id)] = groupfundict
    return


def function_stats(chat_id,msg):
    global function_list_data
    bot_me=bot.getMe()
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        groupfundict = {}
    smsg = ''
    for funct in groupfundict:
        smsg = smsg + '<b>{0}</b> : <code>{1}</code>\n'.format(funct,str(groupfundict[funct]))
    dre = bot.sendMessage(chat_id,smsg,parse_mode='HTML',reply_to_message_id=msg["message_id"])
    log("[Debug] Raw sent data:"+str(dre))
    return

def help(chat_id,msg):
    langport=lang[chat_config[chat_id]["lang"]]["display"]['help']
    global function_list_data
    bot_me=bot.getMe()
    try:
        groupfundict = function_list_data[str(chat_id)]
    except:
        function_default(chat_id,msg,chat_type)
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
    dre = bot.sendMessage(chat_id,smsg,reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return
   
def helpp(chat_id,msg):
    dre = bot.sendMessage(chat_id,\
        '/ping\n/echo\n/getme\n/ns\n/getfile\n/gtts\n/exportblog\n/setlang\n/delmsg',\
        reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return
 
def pastebin(data,title):
    if pastebin_dev_key != "none" and pastebin_user_key != "none":
        pastebin_vars = {'api_dev_key': pastebin_dev_key,
            'api_option': 'paste', 'api_paste_code': data,
            'api_paste_private': '1',
            'api_user_key': pastebin_user_key,
            'api_paste_name': title}
        response = urllib.request.urlopen('http://pastebin.com/api/api_post.php',
                                bytes(urllib.parse.urlencode(pastebin_vars),'utf-8'))
        url = response.read()
        clog("[Pastebin]Uploaded to pastebin URL:"+str(url,'utf-8'))
        return(str(url,'utf-8'))
    else:
        return("invalid pastebin key")

#def pwrtg_getchat(chat_id):
#    req = Request('https://api.pwrtelegram.xyz/bot'+TOKEN+'/getChat?chat_id='+str(chat_id), headers={'User-Agent': 'Mozilla/5.0'})
#    true=True
#    false=False
#    try:
#        a = urlopen(req).read()
#    except urllib.error.HTTPError as error:
#        try:
#            a=eval(error.read())
#        except SyntaxError:
#            a = urlopen(req).read()
#        raise Exception("PWRTelegram API HTTP ERROR "+str(a['error_code'])+":"+a['description'])
#    fullresult=eval(a)
#    return fullresult['result']

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
    zh = zh.replace('1','ㄅ')
    zh = zh.replace('2','ㄉ')
    zh = zh.replace('3','ˇ')
    zh = zh.replace('4','ˋ')
    zh = zh.replace('5','ㄓ')
    zh = zh.replace('6','ˊ')
    zh = zh.replace('7','˙')
    zh = zh.replace('8','ㄚ')
    zh = zh.replace('9','ㄞ')
    zh = zh.replace('0','ㄢ')
    zh = zh.replace('-','ㄦ')
    zh = zh.replace('q','ㄆ')
    zh = zh.replace('w','ㄊ')
    zh = zh.replace('e','ㄍ')
    zh = zh.replace('r','ㄐ')
    zh = zh.replace('t','ㄔ')
    zh = zh.replace('y','ㄗ')
    zh = zh.replace('u','ㄧ')
    zh = zh.replace('i','ㄛ')
    zh = zh.replace('o','ㄟ')
    zh = zh.replace('p','ㄣ')
    zh = zh.replace('a','ㄇ')
    zh = zh.replace('s','ㄋ')
    zh = zh.replace('d','ㄎ')
    zh = zh.replace('f','ㄑ')
    zh = zh.replace('g','ㄕ')
    zh = zh.replace('h','ㄘ')
    zh = zh.replace('j','ㄨ')
    zh = zh.replace('k','ㄜ')
    zh = zh.replace('l','ㄠ')
    zh = zh.replace(';','ㄤ')
    zh = zh.replace('z','ㄈ')
    zh = zh.replace('x','ㄌ')
    zh = zh.replace('c','ㄏ')
    zh = zh.replace('v','ㄒ')
    zh = zh.replace('b','ㄖ')
    zh = zh.replace('n','ㄙ')
    zh = zh.replace('m','ㄩ')
    zh = zh.replace(',','ㄝ')
    zh = zh.replace('.','ㄡ')
    zh = zh.replace('/','ㄥ')
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
    zh = zh.replace('1','˙')
    zh = zh.replace('2','ˊ')
    zh = zh.replace('3','ˇ')
    zh = zh.replace('4','ˋ')
    zh = zh.replace('7','ㄑ')
    zh = zh.replace('8','ㄢ')
    zh = zh.replace('9','ㄣ')
    zh = zh.replace('0','ㄤ')
    zh = zh.replace('-','ㄥ')
    zh = zh.replace('=','ㄦ')
    zh = zh.replace('q','ㄟ')
    zh = zh.replace('w','ㄝ')
    zh = zh.replace('e','ㄧ')
    zh = zh.replace('r','ㄜ')
    zh = zh.replace('t','ㄊ')
    zh = zh.replace('y','ㄡ')
    zh = zh.replace('u','ㄩ')
    zh = zh.replace('i','ㄞ')
    zh = zh.replace('o','ㄛ')
    zh = zh.replace('p','ㄆ')
    zh = zh.replace('a','ㄚ')
    zh = zh.replace('s','ㄙ')
    zh = zh.replace('d','ㄉ')
    zh = zh.replace('f','ㄈ')
    zh = zh.replace('g','ㄐ')
    zh = zh.replace('h','ㄏ')
    zh = zh.replace('j','ㄖ')
    zh = zh.replace('k','ㄎ')
    zh = zh.replace('l','ㄌ')
    zh = zh.replace(';','ㄗ')
    zh = zh.replace("'",'ㄘ')
    zh = zh.replace('z','ㄠ')
    zh = zh.replace('x','ㄨ')
    zh = zh.replace('c','ㄒ')
    zh = zh.replace('v','ㄍ')
    zh = zh.replace('b','ㄅ')
    zh = zh.replace('n','ㄋ')
    zh = zh.replace('m','ㄇ')
    zh = zh.replace(',','之')
    zh = zh.replace('.','ㄔ')
    zh = zh.replace('/','ㄕ')
    return zh

def clog(text,colored_text = ""):
    if colored_text == "":
        colored_text = text
    if platform.system() == "Linux":
        print(colored_text+color.RESET)
    else:
        print(text)
    log(text)
    return

def log(text):
    if text[0:7] == "[Debug]":
        if Debug == True:
            logger= io.open(logpath+"-debug.log","a",encoding='utf8')
            logger.write("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"]"+text+"\n")
            logger.close()
        return
    logger= io.open(logpath+".log","a",encoding='utf8')
    logger.write(text+"\n")
    logger.close()
    return

if os.path.isdir("./logs") == False:
    os.mkdir("./logs")
logpath = "./logs/"+time.strftime("%Y-%m-%d-%H-%M-%S").replace("'","")
bot = telepot.Bot(TOKEN)
#bot = telepot.DelegatorBot(TOKEN,
#   pave_event_space()(
#        per_chat_id(), create_open, Player, timeout=20),
#]))
log("[Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug][Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug] Bot's TOKEN is "+TOKEN)
answerer = telepot.helper.Answerer(bot)

#bot.message_loop({'chat': on_chat_message})
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
read_function_list()
read_chatconfig()
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Bot has started",\
    color.GREEN+"["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"]"+color.BLUE+"[Info]"+color.GREEN+" Bot has started")
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Listening ...",\
    color.GREEN+"["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"]"+color.BLUE+"[Info] Listening...")

# Keep the program running.
while 1:
    time.sleep(10)