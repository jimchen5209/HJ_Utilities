#-*-coding:UTF-8-*-
import sys
import time
import telepot
import urllib
import urllib.request
import os
import io
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
try:
    fs = open("./config.json","r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading config.json:"+str(val).split(',')[0].replace('(','').replace("'",""))
    programPause = input("Press any key to stop...\n")
    exit()

#load config
config = eval(fs.read())
fs.close()
TOKEN = config["TOKEN"]
pastebin_dev_key = config["pastebin_dev_key"]
pastebin_user_key = config["pastebin_user_key"]
Debug = config["Debug"]
confirmsg = None

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    log("[Debug] Raw message:"+str(msg))
    dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info]"
    try:
        dlog=dlog+"[EDITED"+msg['edit_date']+"]"
    except:
        time.sleep(0)
    fuser= bot.getChatMember(chat_id,msg['from']['id'])
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
    if chat_type == 'private':
        dlog = dlog + "[Private]["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
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
                dlog = dlog + "( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) sent a "+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
            clog(flog)
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
            clog(flog)
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
            clog(flog)
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
            clog(flog)
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
            clog(flog)
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
            clog(flog)
        #command_detect
        if content_type == 'text':
            cmd = msg['text'].split()
            if cmd[0] == '/start':
                startc(chat_id,msg)
        dre = bot.sendMessage(chat_id,'本機器人在私訊中沒有功能，請將我加入到群組',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    elif chat_type == 'group' or chat_type == 'supergroup':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
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
                dlog = dlog + "( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
        elif content_type == 'new_chat_member':
            if msg['new_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been added to ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
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
        elif content_type == 'left_chat_member':
            if msg['left_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been kicked from ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
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
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
            clog(flog)
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
            clog(flog)
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
            clog(flog)
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
            clog(flog)
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
            clog(flog)
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
            clog(flog)
        #command_detect
        if content_type == 'text':
            cmd = msg['text'].split()
            if cmd[0] == '/start' or cmd[0] == '/start@'+username:
                startc(chat_id,msg)
            if cmd[0] == '/cgp' or cmd[0] == '/cgp@'+username:
                cgp(chat_id,msg,chat_type)
            if cmd[0] == '/rgp' or cmd[0] == '/rgp@'+username:
                rgp(chat_id,msg,chat_type)
            if cmd[0] == '/echo' or cmd[0] == '/echo@'+username:
                echo(chat_id,msg)
            if cmd[0] == '/ns' or cmd[0] == '/ns@'+username:
                ns(chat_id,msg,cmd)
            if cmd[0] == 'ping' or cmd[0] == 'Ping':
                ping(chat_id,msg)
            if cmd[0] == '/ping' or cmd[0] == '/ping@'+username:
                ping(chat_id,msg)
            if cmd[0] == '/title' or cmd[0] == '/title@'+username:
                title(chat_id,msg,chat_type)
            if cmd[0] == '/lsadmins' or cmd[0] == '/lsadmins@'+username:
                lsadmins(chat_id,msg,cmd)
            if cmd[0] == '/groupinfo' or cmd[0] == '/groupinfo@'+username:
                groupinfo(chat_id,msg,chat_type)
            if cmd[0] == '/leavegroup' or cmd[0] == '/leavegroup@'+username:
                leavegroup(chat_id,msg,chat_type)
            if cmd[0] == '/a2z' or cmd[0] == '/a2z@'+username:
                a2zc(chat_id,msg)
            if cmd[0] == '/getuser' or cmd[0] == '/getuser@'+username:
                getuser(chat_id,msg,cmd)
            if cmd[0] == '/getme' or cmd[0] == '/getme@'+username:
                getme(chat_id,msg)
            if cmd[0] == '/pin' or cmd[0] == '/pin@'+username:
                pin(chat_id,msg,chat_type)
            if cmd[0] == '/replace' or cmd[0] == '/replace@'+username:
                replace(chat_id,msg,cmd)
            if cmd[0] == '/getfile' or cmd[0] == '/getfile@'+username:
                getfile(chat_id,msg,cmd)
            if cmd[0] == '/tag' or cmd[0] == '/tag@'+username:
                tag(chat_id,msg,cmd,chat_type)
            if cmd[0] == '/confirm' or cmd[0] == '/confirm@'+username:
                confirm(chat_id,msg)
            if cmd[0] == '/gtts' or cmd[0] == '/gtts@'+username:
                gtts(chat_id,msg)
            if cmd[0] == '/help' or cmd[0] == '/help@'+username:
                help(chat_id,msg)

def startc(chat_id,msg):
    dre = bot.sendMessage(chat_id,'JUST a utility bot\n/help',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def cgp(chat_id,msg,chat_type):
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,\
            '所有人都是管理員的普通群組無法透過我來設置群組圖片',\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        reply_to = msg['reply_to_message']
    except:
        url = msg['text'].split(' ',1)
        log("[Debug] Attemping to download "+url[1])
        try:
            urllib.request.urlretrieve (url[1],"image.jpg")
        except:
            dre = bot.sendMessage(chat_id,'/cgp <PIC URL>\n或回覆一個圖片以更改群組圖片',reply_to_message_id=msg['message_id'])
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
                    '設置群組圖片時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                    parse_mode = 'Markdown',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                    +str(val).split(',')[0].replace('(','').replace("'",""))
            else:
                clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
            fo.close()
            os.remove('image.jpg')
    else:
        try:
            photo_array=msg['reply_to_message']['photo']
            log("[Debug] File_id to set:"+str(photo_array))
        except:
            dre = bot.sendMessage(chat_id,'請回覆一個圖片信息',reply_to_message_id=msg['message_id'])
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
                    '設置群組圖片時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                    parse_mode = 'Markdown',\
                    reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                clog('[ERROR] Unable to change the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
            else:
                clog('[Info] Sucessfully changed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
            fo.close()
            os.remove('image.jpg')
    return

def rgp(chat_id,msg,chat_type):
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,\
            '所有人都是管理員的普通群組無法透過我來設置群組圖片',\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    try:
        bot.deleteChatPhoto(chat_id)
    except:
        tp, val, tb = sys.exc_info()
        sval=str(val)
        bot.sendChatAction(chat_id,'typing')
        dre = bot.sendMessage(chat_id,\
            '移除群組圖片時發生錯誤 :(\n\n' +str(val).split(',')[0].replace('(','').replace("'","`"),\
            parse_mode = 'Markdown',\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        clog('[ERROR] Unable to remove the Group photo in '+msg['chat']['title']+'('+str(chat_id)+') : '\
            +str(val).split(',')[0].replace('(','').replace("'",""))
    else:
        clog('[Info] Sucessfully removed the Group photo in '+msg['chat']['title']+'('+str(chat_id)+')')
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
    try:
        log("[Info] Number to transfer :"+txt[2])
    except:
        dre = bot.sendMessage(chat_id,\
            "/ns <todec|tobin|tooct|tohex> <number>\n"+\
            "提供的數字若不是十進位請在數字前面註明 `[bin:0b|oct:0o|hex:0x]`\n"+\
            "例如 : `0xabf`",\
            parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    if txt[1] == "todec":
        try:
            result = int(txt[2],0)
        except:
            tp, val, tb = sys.exc_info()
            bot.sendChatAction(chat_id,'typing')
            dre = bot.sendMessage(chat_id,\
                '發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
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
                '發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
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
                '發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
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
                '發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
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
        dre = bot.sendMessage(chat_id,\
            "/ns <todec|tobin|tooct|tohex> <number>\n提供的數字若不是十進位請在數字前面註明 `[bin:0b|oct:0o|hex:0x]`\n例如 : `0xabf`",\
            parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return
  
def ping(chat_id,msg):
    dre = bot.sendMessage(chat_id,'Pong',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def title(chat_id,msg,chat_type):
    cmd=msg['text'].split(' ',1)
    try:
        title=cmd[1]
    except:
        if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
            dre = bot.sendMessage(chat_id,\
                '所有人都是管理員的普通群組無法透過我來設置群組標題',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            dre = bot.sendMessage(chat_id,'/title <String>',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        return
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,\
            '所有人都是管理員的普通群組無法透過我來設置群組標題',\
            reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                print('[Info] Admin Matched for \n[Info] '+ str(admin))
                log('[Info] Admin Matched for \n[Info] '+ str(admin))
                try:
                    bot.setChatTitle(chat_id,title)
                except:
                    tp, val, tb = sys.exc_info()
                    sval=str(val)
                    bot.sendChatAction(chat_id,'typing')
                    dre = bot.sendMessage(chat_id,\
                        '設置群組標題時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] Unable to change the Group title in '+msg['chat']['title']+'('+str(chat_id)+') : '\
                        +str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    clog('[Info] Sucessfully changed the Group title in '+msg['chat']['title']+'('+str(chat_id)+')')
                return
        clog('[Info] No admins matched with' + msg['from']['username']+'('+str(msg['from']['id'])+ ')')
        bot.sendMessage(chat_id,'你沒有權限設置群組標題',reply_to_message_id=msg['message_id'])
        return
    return

def lsadmins(chat_id,msg,cmd):
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
                '取得目標群組管理員時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`")+'\n\n將以目前群組繼續',\
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
            adminmsg=adminmsg + "\n創群者："+nickname+"\n"
            if group_type == 'group' and target_group['all_members_are_administrators'] == True:
                adminmsg = adminmsg + '\n群組內的每個人都是管理員:D'
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
                adminmsg = adminmsg + "Admin - "
            adminmsg = adminmsg +nickname
    dre = bot.sendMessage(chat_id,adminmsg,parse_mode = 'HTML',disable_web_page_preview=True,reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    print('[Info]Admin list for ',target_group['title'],' ( ',str(target_group['id']), ' ): ')
    log("[Info]")
    clog(adminmsg)
    return

def groupinfo(chat_id,msg,chat_type):
    dre = bot.sendMessage(chat_id,\
        "*群組類型*: "+chat_type+"\n"+\
        "*群組名稱*: "+msg['chat']['title']+"\n"+\
        "*群組人數*: " + str(bot.getChatMembersCount(chat_id)) +"\n"+\
        "*群組ID*: `" +str(chat_id) + "`",\
        parse_mode = 'Markdown',\
        reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def leavegroup(chat_id,msg,chat_type):
    if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
        dre = bot.sendMessage(chat_id,'Bye~',reply_to_message_id=msg['message_id'])
        bot.leaveChat(chat_id)
        log("[Debug] Raw sent data:"+str(dre))
    else:
        clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
        for admin in bot.getChatAdministrators(chat_id):
            if msg['from']['id'] == admin['user']['id']:
                clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                dre = bot.sendMessage(chat_id,'Bye~',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                bot.leaveChat(chat_id)
                return
        clog('[Info] No admins matched with' + msg['from']['username'],'('+msg['from']['id']+ ')')
        dre = bot.sendMessage(chat_id,'你沒有辦法讓我離開喔',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
        return
    return

def a2zc(chat_id,msg):
    try:
        reply_to = msg['reply_to_message']
    except:
        alpt = msg['text'].split(' ',1)
        try:
            tcm=alpt[1]
        except:
            dre = bot.sendMessage(chat_id,'/a2z <string>\n或回覆一個信息來將英文字母轉成注音',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            string=a2z(tcm)
            dre = bot.sendMessage(chat_id,string,reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    else:
        try:
            tcm = reply_to['text']
        except:
            dre = bot.sendMessage(chat_id,'請回復一個文字信息',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            string=a2z(tcm)
            dre = bot.sendMessage(chat_id,string,reply_to_message_id=reply_to['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    return

def getuser(chat_id,msg,txt):
    try:
        reply_to = msg['reply_to_message']
    except:
        try:
            uuser_id = int(txt[1])
        except:
            dre = bot.sendMessage(chat_id,\
                "/getuser [user_id]\n"+\
                "或回覆一個使用者來取得該用戶的資訊",\
                parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                user = bot.getChatMember(chat_id,uuser_id)
            except:
                tp, val, tb = sys.exc_info()
                bot.sendChatAction(chat_id,'typing')
                dre = bot.sendMessage(chat_id,\
                    '取得該用戶資訊時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
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
                    nickname = '['+ firstname + ' ' + lastname + '](https://t.me/' + user['user']['username'] + ')'
                except:
                    uusername = 'Undefined'
                    nickname = firstname + ' ' + lastname
                userid = str(user['user']['id'])
                dre = bot.sendMessage(chat_id, \
                    '*暱稱*: ' + nickname + '\n'+\
                    '*Username*: ' + uusername + '\n' +\
                    '*User id*: `' + userid +'`'+ '\n' +\
                    '*目前職位*: ' + user['status'],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
    else:
        user = bot.getChatMember(chat_id,reply_to['from']['id'])
        firstname = user['user']['first_name']
        try:
            lastname = user['user']['last_name']
        except:
            lastname = ''
        try:
            uusername = '@' + user['user']['username']
            nickname = '['+ firstname + ' ' + lastname + '](https://t.me/' + user['user']['username'] + ')'
        except:
            uusername = 'Undefined'
            nickname = firstname + ' ' + lastname
        userid = str(user['user']['id'])
        dre = bot.sendMessage(chat_id, \
            '*暱稱*: ' + nickname + '\n'+\
            '*Username*: ' + uusername + '\n' +\
            '*User id*: `' + userid +'`'+ '\n' +\
            '*目前職位*: ' + user['status'],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    return

def getme(chat_id,msg):
    user= bot.getChatMember(chat_id,msg['from']['id'])
    firstname = user['user']['first_name']
    try:
        lastname = user['user']['last_name']
    except:
        lastname = ''
    try:
        uusername = '@' + user['user']['username']
        nickname = '['+ firstname + ' ' + lastname + '](https://t.me/' + user['user']['username'] + ')'
    except:
        uusername = 'Undefined'
        nickname = firstname + ' ' + lastname
    userid = str(user['user']['id'])
    dre = bot.sendMessage(chat_id, \
        '*暱稱*: ' + nickname + '\n'+\
        '*Username*: ' + uusername + '\n' +\
        '*User id*: `' + userid +'`'+ '\n' +\
        '*目前職位*: ' + user['status'],parse_mode = 'Markdown',reply_to_message_id=msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    return

def pin(chat_id,msg,chat_type):
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,'請回復一則訊息以將此訊息至頂',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        if chat_type == 'group':
            dre = bot.sendMessage(chat_id,'普通群組無法置頂訊息',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
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
                            '置頂時發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                            parse_mode = 'Markdown',\
                            reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        clog('[ERROR] Unable to pin the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+chat_id+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
                    else:
                        clog('[Info] Sucessfully pinned the message '+str(reply_to['message_id'])+' in '+msg['chat']['title']+'('+chat_id+')')
                    return
            clog('[Info] No admins matched with' + msg['from']['username']+'('+msg['from']['id']+ ')')
            dre = bot.sendMessage(chat_id,'你沒有權限置頂訊息',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            return
    return

def replace(chat_id,msg,cmd):
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,'請回復一則訊息\n\n用法: /replace <要被取代的文字> <取代的文字>',reply_to_message_id=msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            rstring=reply_to['text']
        except:
            dre = bot.sendMessage(chat_id,'請回復一個文字信息',reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                test=cmd[1]
                test=cmd[2]
            except:
                dre = bot.sendMessage(chat_id,"/replace <要被取代的文字> <取代的文字>\n如果想要取代成空白可以使用`''`",\
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
                        '發生錯誤 :(\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                        parse_mode = 'Markdown',\
                        reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    clog('[ERROR] ERROR when replacing '+cmd[1]+' to ' + cmd[2]+msg['chat']['title']+'('+str(chat_id)+') : '\
                        +str(val).split(',')[0].replace('(','').replace("'",""))
                else:
                    dre = bot.sendMessage(chat_id,rstring,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
    return

def getfile(chat_id,msg,cmd):
    bot.sendChatAction(chat_id,"upload_document")
    try:
        file_id = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,"/getfile <file_id>")
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            dre = bot.sendDocument(chat_id,file_id,reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        except:
            tp, val, tb = sys.exc_info()
            dre = bot.sendMessage(chat_id,\
                '無法取得檔案\n\n'+str(val).split(',')[0].replace('(','').replace("'","`"),\
                parse_mode = 'Markdown',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[ERROR] Unable to fetch the file '+file_id+' in '+msg['chat']['title']+'('+str(chat_id)+') : '+str(val).split(',')[0].replace('(','').replace("'",""))
    return

def readtag():
    clog("[Info] Reading data...")
    if os.path.isfile("./tagdata.json") == False:
        fs = open("./tagdata.json","w")
        fs.write("{}")
        fs.close
    fs = open("./tagdata.json","r")
    data = eval(fs.read())
    fs.close
    return(data)

def writetag(data):
    clog("[Info] Writing data...")
    fs = open("./tagdata.json","w")
    fs.write(str(data))
    fs.close
    return

def addtag(chat_id,msg,cmd):
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
            dre = bot.sendMessage(chat_id,"/tag add <tag_name> <userid>\n或回覆該用戶以加入tag名單",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                testcmduser = cmd[3]
            except:
                dre = bot.sendMessage(chat_id,"/tag add <tag_name> <userid>\n或回覆該用戶以加入tag名單",reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                successmsg = "已將下列用戶加到 <b>" + cmd[2] + "</b> 清單:\n"
                successcount = 0
                errmsg = "將下列用戶加到 <b>" + cmd[2] + "</b> 時發生問題:\n"
                errcount = 0
                nousername = "下列用戶沒有設置 username ,屆時無法tag他們:\n"
                nousernamecount = 0
                if len(cmd) >= 54:
                    dre = bot.sendMessage(chat_id,"請不要一次傳太多user,為避免卡死我只處理前50個",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
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
                            errmsg = errmsg +"<b>"+ a + "</b> : <code>此用戶已經在清單中了</code>\n"
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
                            nousername = nousername + "<b>" + nickname + "</b> (<i>"+a+"</i>) \n"
                            nousernamecount = nousernamecount + 1
                            clog("[WARN] " +firstname + ' ' + lastname+ " ( " + str(userid)+ ") has no username!")
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
                if nousernamecount == 0:
                    nousername = ""
                dre = bot.sendMessage(chat_id,successmsg+errmsg+nousername,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
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
            smsg = "將 <b>" + str(userid) + "</b> 加入 <b>" + cmd[2] +"</b> 時發生問題: <code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>\n"
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
                smsg = "將 <b>" + str(userid) + "</b> 加入 <b>" + cmd[2] +"</b> 時發生問題: <code>此用戶已經在清單中了</code>\n"
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
                smsg= "用戶 <b>" + nickname + "</b> (<i>"+str(userid)+"</i>) 沒有設置 username ,屆時無法tag他\n\n"
                clog("[WARN] " +firstname + ' ' + lastname+ " ( " + str(userid)+ ") has no username!")
            smsg = smsg + "已將 " + nickname + " 加到 <b>" + cmd[2] + "</b>清單"
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
            dre = bot.sendMessage(chat_id,"/tag remove <tag_name> <userid>\n或回覆該用戶以將該用戶從指定名單移除\n"+\
                "或 /tag remove <tag> * 以移除這個tag",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if tagname == "*":
                global confirmsg
                if grouptagdict == {}:
                    dre = bot.sendMessage(chat_id,"本群沒有任何清單",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
                if chat_type == 'group' and msg['chat']['all_members_are_administrators'] == True:
                    dre = bot.sendMessage(chat_id,"將移除本群組中的所有tag,此操作無法復原,確認執行請回復這則訊息並輸入 /confirm",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    confirmsg = dre
                    return
                else:
                    clog('[Info] Searching admins in '+msg['chat']['title']+'('+str(chat_id)+ ')')
                    for admin in bot.getChatAdministrators(chat_id):
                        if msg['from']['id'] == admin['user']['id']:
                            clog('[Info] Admin Matched for \n[Info] '+ str(admin))
                            dre = bot.sendMessage(chat_id,"將移除本群組中的所有tag,此操作無法復原,確認執行請回復這則訊息並輸入 /confirm",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                            confirmsg = dre
                            log("[Debug] Raw sent data:"+str(dre))
                            return
                    clog('[Info] No admins matched with' + msg['from']['username'],'('+msg['from']['id']+ ')')
                    dre = bot.sendMessage(chat_id,'你沒有權限移除所有tag',reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
            try:
                testcmduser = cmd[3]
            except:
                dre = bot.sendMessage(chat_id,"/tag remove <tag_name> <userid>\n或回覆該用戶以將該用戶從指定名單移除\n"+\
                "或 /tag remove <tag> * 以移除這個tag",reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                if cmd[3] == "*":
                    if temptaglist == []:
                        clog("[ERROR] List "+cmd[2]+ "not found.")
                        dre = bot.sendMessage(chat_id,"清單"+cmd[2]+"不存在",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                        log("[Debug] Raw sent data:"+str(dre))
                        return
                    del grouptagdict[cmd[2]]
                    clog("[Info] Cleared the list "+cmd[2])
                    data[str(chat_id)]=grouptagdict
                    writetag(data)
                    dre = bot.sendMessage(chat_id,"已移除清單 <b>"+cmd[2]+"</b>",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    return
                successmsg = "已將下列用戶從 <b>" + cmd[2] + "</b> 清單中移除:\n"
                successcount = 0
                errmsg = "將下列用戶從 <b>" + cmd[2] + "</b> 移除時發生問題:\n"
                errcount = 0
                if len(cmd) >= 54:
                    dre = bot.sendMessage(chat_id,"請不要一次傳太多user,為避免卡死我只處理前50個",parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
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
                            errmsg = errmsg +"<b>"+ a + "</b> : <code>此用戶不在清單中</code>\n"
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
                            nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
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
            smsg = "將 <b>" + userid + "</b> 從 <b>" + cmd[2] +"</b> 移除時發生問題: <code>"+str(val).split(',')[0].replace('(','').replace("'","")+"</code>\n"
            dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            try:
                temptaglist.index(userid)
            except:
                clog("[ERROR] Errored when remving user " + str(userid) + " from "+cmd[2]+" :The user is not in the list")
                smsg = "將 <b>" + str(userid) + "</b> 從 <b>" + cmd[2] +"</b> 移除時發生問題: <code>此用戶不在清單中了</code>\n"
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
            smsg = smsg + "已將 " + nickname + " 從 <b>" + cmd[2] + "</b>移除"
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
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    try:
        reply_to = msg['reply_to_message']
    except:
        dre = bot.sendMessage(chat_id,"我不知道你是在確認甚麼",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        global confirmsg
        if confirmsg == None:
            dre = bot.sendMessage(chat_id,"我不知道你是在確認甚麼",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        if reply_to["message_id"] == confirmsg["message_id"]:
            if msg['from']['id'] != confirmsg['reply_to_message']['from']['id']:
                dre = bot.sendMessage(chat_id,"我不知道你是在確認甚麼",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            ccmd = confirmsg['reply_to_message']['text'].split()
            if ccmd[0] == '/tag' or ccmd[0] == '/tag@'+username:
                if ccmd[1] == 'remove' and ccmd[2] == "*":
                    data=readtag()
                    del data[str(chat_id)]
                    writetag(data)
                    dre = bot.sendMessage(chat_id,"已移除本群組的所有tag",disable_web_page_preview=True,reply_to_message_id=confirmsg['reply_to_message']["message_id"])
                    log("[Debug] Raw sent data:"+str(dre))
                    confirmsg = None
        else:
            dre = bot.sendMessage(chat_id,"我不知道你是在確認甚麼",disable_web_page_preview=True,reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return

    return

def lstag(chat_id,msg,cmd):
    data=readtag()
    smsg = ""
    try:
        grouptagdict = data[str(chat_id)]
    except:
        dre = bot.sendMessage(chat_id,"此群組沒有任何 Tag 清單",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    try:
        listname = cmd[2]
    except:
        for ttag in data[str(chat_id)]:
            temptaglist = data[str(chat_id)][ttag]
            smsg = smsg + "清單 <b>"+ttag+"</b> ,有 <b>" + str(len(temptaglist)) +"</b> 人\n"
    else:
        try:
            temptaglist = data[str(chat_id)][listname]
        except:
            dre = bot.sendMessage(chat_id,"清單 <b>"+listname+"</b> 不存在",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            smsg = smsg +"清單 <b>"+listname+"</b> ,共 <b>" + str(len(temptaglist)) +"</b> 人\n"
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
    data=readtag()
    smsg = ""
    nousername = "無法tag下列用戶,因為他們沒有username:\n"
    nousernamecount = 0
    try:
        listname = cmd[2]
    except:
        dre = bot.sendMessage(chat_id,"/tag tag <tag_name>",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    else:
        try:
            temptaglist = data[str(chat_id)][listname]
        except:
            dre = bot.sendMessage(chat_id,"清單 <b>"+listname+"</b> 不存在",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            if temptaglist == []:
                dre = bot.sendMessage(chat_id,"清單 <b>"+listname+"</b> 不存在",reply_to_message_id=msg["message_id"])
                log("[Debug] Raw sent data:"+str(dre))
                return
            count = 0
            for userid in temptaglist:
                adduser = bot.getChatMember(chat_id,int(userid))
                firstname = adduser['user']['first_name']
                try:
                    lastname = adduser['user']['last_name']
                except:
                    lastname = ''
                try:
                    uusername = adduser['user']['username']
                    nickname = '<a href="https://t.me/' + adduser['user']['username'] + '">'+firstname + ' ' + lastname+'</a>'
                except:
                    nickname = firstname + ' ' + lastname
                    nousername = nousername + nickname + "\n"
                    nousernamecount = nousernamecount+1
                else:
                    smsg = smsg + "@"+uusername+" "
                count = count +1
                if count >= 2:
                    smsg = smsg + "\n"
                    count = 0
    print(smsg)
    dre = bot.sendMessage(chat_id,smsg,parse_mode="HTML",reply_to_message_id=msg["message_id"])
    log("[Debug] Raw sent data:"+str(dre))
    if nousernamecount != 0:
        dre = bot.sendMessage(chat_id,nousername,parse_mode="HTML",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
    return

def tag(chat_id,msg,cmd,chat_type):
    try:
        testsubcmd = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,"/tag <add|remove|list|tag>",reply_to_message_id=msg["message_id"])
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
        else:
            dre = bot.sendMessage(chat_id,"/tag <add|remove|list|tag>",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))

    return

def gtts(chat_id,msg):
    cmd = msg['text'].split(' ',2)
    try:
        lang = cmd[1]
    except:
        dre = bot.sendMessage(chat_id,"/gtts <lang_code> <txt>\nEx: /gtts en-GB Hello World!",reply_to_message_id=msg["message_id"])
        log("[Debug] Raw sent data:"+str(dre))
        return
    else:
        try:
            txt = cmd[2]
        except:
            dre = bot.sendMessage(chat_id,"/gtts <lang_code> <txt>\nEx: /gtts en-GB Hello World!",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
            return
        else:
            smsg = '[Link](https://translate.google.com.tw/translate_tts?ie=UTF-8&q='+txt+'&tl='+lang+'&client=tw-ob)'
            dre = bot.sendMessage(chat_id,smsg,parse_mode="Markdown",reply_to_message_id=msg["message_id"])
            log("[Debug] Raw sent data:"+str(dre))
    return

def help(chat_id,msg):
    dre = bot.sendMessage(chat_id,\
        '/a2z\n/cgp\n/rgp\n/ping\n/echo\n/groupinfo\n/pin\n/getme\n/title\n/ns\n/getuser\n/replace\n/getfile\n/lsadmins\n/tag\n/gtts',\
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

def clog(text):
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
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Bot has started")
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Listening ...")

# Keep the program running.
while 1:
    time.sleep(10)