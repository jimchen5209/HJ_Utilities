{
  "cgp": {
    "all_member_are_admin": "A group which all members are admins is not able to be set group picture by me.",
    "help": "/cgp <PIC URL>\nor reply to a picture to change group picture.",
    "error": "An error occured when setting group picture.\n\n{0}",
    "no_perm": "You don't have permission to change group picture.",
    "reply_not_pic": "Reply to a picture,please."
  },
  "rgp": {
    "all_member_are_admin": "A group which all members are admins is not able to be set group picture by me.",
    "error": "An error occured when removing group picture.\n\n{0}",
    "no_perm": "You don't have permission to change group picture."
  },
  "ns": {
    "help": "/ns <todec|tobin|tooct|tohex> <number>\nIf the number you provided is not in Decimal,type `[bin:0b|oct:0o|hex:0x]` before the number.\nEx : `0xabf`",
    "error": "An error occured.\n\n{0}"
  },
  "title": {
    "all_member_are_admin": "A group which all members are admins is not able to be set group title by me.",
    "help": "/title <String> Change group title",
    "error": "An error occured when setting group title.\n\n{0}",
    "no_perm": "You don't have permission to change group title."
  },
  "lsadmins": {
    "error": "An error occured when fetching admins list from the target group.\n\n{0}\n\nI'll continue with this group.",
    "everyone_is_admin": "All members in this group are admins.",
    "creator":"Creator：{0}",
    "admin_badge": "Admin"
  },
  "groupinfo": {
    "grouptype": "<b>Group type</b>: {0}",
    "groupname": "<b>Group title</b>: {0}",
    "groupcount": "<b>Members</b>: {0}",
    "groupid": "<b>Group ID</b>: {0}"
  },
  "leavegroup": {
    "farewell": "Bye~",
    "no_perm": "You cannot let me leave."
  },
  "a2z": {
    "help": "/a2z <string>\nor reply to a text message to replace all alphabets to zuyings.",
    "not_text": "Reply to a text message,please."
  },
  "getuser": {
    "help": "/getuser [user_id]\nor reply to a user to get the informations of this user.\nType <code>/getuser forward</code> so as to get the informations of the sender of the forwared message.",
    "error": "An error occured when fetching the informations of this user. \n\n{0}",
    "nick": "<b>Nickname</b>: {0}",
    "username": "<b>Username</b>: {0}",
    "userid": "<b>User id</b>: {0}",
    "status": "<b>Status</b>: {0}"
  },
  "pin": {
    "reply_help": "Reply to a message to pin this message.",
    "group": "A group is not able to pin messages.",
    "error": "An error occured when pinning this message.\n\n{0}",
    "no_perm": "You don't have permission to pin the message."
  },
  "replace": {
    "help_not_reply": "Reply to a message,please.\n\nUsage: /replace <string to be replaced> <string to replace>",
    "not_text": "Reply to a text message,please.",
    "help": "/replace <string to be replaced> <string to replace>\nIf you want to replace with blank,use `''`",
    "error": "An error occured.\n\n{0}",
    "result": "{0} thinks that the meaning of {1} is {2}",
    "result_self": "{0} means {1}"
  },
  "getfile": {
    "help": "/getfile <file_id>",
    "error": "Unable to fetch the file.\n\n{0}",
    "senderror": "An error occured when sending the file.\n\n{0}"
  },
  "fileinfo": {
    "help": "Reply to a message to get the infomations of the file.",
    "istext": "This is a text message.",
    "filetype": "<b>File type</b> : {0}",
    "fileid": "<b>File id</b> : {0}"
  },
  "exportblog": {
    "no_perm": "You don't have permission.",
    "debug_off": "Debug option is off",
    "debug": "If you want to get Debug log,use /exportblog -debug "
  },
  "tag": {
    "add": {
      "help": "/tag add <tag_name> <userid>\nor reply to a user to add this user to a list",
      "b_success": "Successfully added the following user(s) to {0} :",
      "b_error": "Error(s) occured when adding the following user(s) to {0}:",
      "too_many": "Don't send too many users in once, I'll only use 50 users in order not to block.",
      "already_exist": "The user is already in this list.",
      "r_error": "An error occured when adding {0} to {1} : {2}",
      "r_success": "Successfully added {0} to {1} ."
    },
    "remove": {
      "help": "/tag remove <tag_name> <userid>\nor reply to a user to remove this user from a list.\nor use /tag remove <tag> * to remove the whole tag",
      "no_list": "There is no list in this group.",
      "remove_all": {
        "warn": "This will <b>remove all</b> of the tags in this group.It cannot be undone.If you want to continue,reply to this message and type /confirm .",
        "no_perm": "You don't have permission to remove all of the tags in this group."
      },
      "list_not_exist": "{0} is not exist.",
      "list_removed": "Removed the list {0}",
      "b_success": "Successfully removed the following user(s) from {0}:",
      "b_error": "Error(s) occured when removing the following user(s) from {0} :",
      "too_many": "Don't send too many users in once, I'll only use 50 users in order not to block.",
      "not_in_list": "The user is not in this list",
      "r_error": "An error occured when removing {0} from {1} : {2}",
      "r_success": "Successfully removed {0} from {1} ."
    },
    "confirm": {
      "donotknow_confirmabout": "I have no idea what you are confirming about.",
      "remove_all_success": "Removed all of the tags in this group."
    },
    "lstag": {
      "no_list": "There is no list in this group.",
      "all": "List {0} ,has {1} member(s).",
      "list_not_exist": "{0} is not exist.",
      "list_prefix": "List {0} ,has {1} member(s)."
    },
    "tag": {
      "help": "/tag tag <tag_name>",
      "list_not_exist": "{0} is not exist.",
      "tag_prefix": "Mentioning {1} member(s) in {0}."
    },
    "tagadmin": {
        "all_member_are_admin":"A group with all members are admin enabled,I will only mention the creator.",
        "tag_prefix": "Mentioning {0} admin(s) in this group."
    },
    "general": {
      "help": "/tag <add|remove|list|tag|admin>",
      "PWRAPI": "The function is temporarily unavailable because the API is down.For further information: [pwrtelegram](https://t.me/pwrtelegram)"
    }
  },
  "gtts": {
    "help": "/gtts <lang_code> <txt>\nEx: /gtts en-GB Hello World!"
  },
  "function": {
    "general": {
      "help": "/function <enable|disable|chkadminf|stats|reset>",
      "reset_complete": "Reseted the status of functions",
      "no_perm": "You don't have permission to change the function settings."
    },
    "enable": {
      "help": "/function enable <Function name|all>",
      "deploy": "Detected there is no function settings in this group and deployed successfully.",
      "funct_not_exist": "{0} not found.",
      "success": "{0} has been enabled.",
      "failed": "Unable to enable {0}\n\n{1}",
      "already_true": "This function has already enabled.",
      "all_member_are_admin": "A group which all members are admins is not able to execute functions that need admin.",
      "no_perm": "I have no permission.",
      "group_cant_pin": "A group is not able to pin messages."
    },
    "disable": {
      "help": "/function disable <Function name|all>",
      "deploy": "Detected there is no function settings in this group and deployed successfully.",
      "funct_not_exist": "{0} not found.",
      "success": "{0} has been disabled.",
      "success_all": "All functions are disabled.",
      "failed": "Unable to disable {0}\n\n{1}",
      "already_false": "This function has already disabled."
    },
    "admin_check": {
      "all_member_are_admin": "A group which all members are admins is not able to execute functions that need admin, so some of functions are disabled.",
      "success_enable": "{0} has been enabled.",
      "success_disable": "{0} has been disabled.",
      "msg_checking_admin": "Checking if I am an admin in this group..."
    }
  },
  "exportchatlink":{
      "no_perm": "You don't have permission to export chat link.",
      "error":"A problem occured when exporting chat link\n\n{0}"
  },
  "help": {
    "nofunction": "All functions are disabled!Use /function if you need to enable."
  },
  "config":{
    "langsuccess":"Set language to {0}",
    "langexist":"The language has already been {0}",
    "lang_noperm":"You don't have permission to change my language."
  }
}