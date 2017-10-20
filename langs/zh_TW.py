{
  "cgp": {
    "all_member_are_admin": "所有人都是管理員的普通群組無法透過我來設置群組圖片",
    "help": "/cgp <PIC URL>\n或回覆一個圖片以更改群組圖片",
    "error": "設置群組圖片時發生錯誤\n\n{0}",
    "no_perm": "你沒有權限設置群組圖片",
    "reply_not_pic": "請回覆一個圖片信息"
  },
  "rgp": {
    "all_member_are_admin": "所有人都是管理員的普通群組無法透過我來設置群組圖片",
    "error": "移除群組圖片時發生錯誤\n\n{0}", 
    "no_perm": "你沒有權限設置群組圖片"
  },
  "ns": {
    "help": "/ns <todec|tobin|tooct|tohex> <number>\n提供的數字若不是十進位請在數字前面註明 <code>[bin:0b|oct:0o|hex:0x]</code>\n例如 : <code>0xabf</code>",
    "error": "發生錯誤\n\n{0}" 
  },
  "title": {
    "all_member_are_admin": "所有人都是管理員的普通群組無法透過我來設置群組標題",
    "help": "/title <String> 更改群組標題",
    "error": "設置群組標題時發生錯誤\n\n{0}", 
    "no_perm":"你沒有權限設置群組標題"
  },
  "lsadmins": {
    "error": "取得目標群組管理員時發生錯誤\n\n{0}",
    "everyone_is_admin": "群組內的每個人都是管理員",
    "admin_badge": "Admin"
  },
  "groupinfo": {
    "grouptype": "<b>群組類型</b>: {0}",
    "groupname": "<b>群組名稱</b>: {0}",
    "groupcount": "<b>群組人數</b>: {0}",
    "groupid": "<b>群組ID</b>: {0}"
  },
  "leavegroup": {
    "farewell": "Bye~",
    "no_perm": "你沒有辦法讓我離開喔"
  },
  "a2z": {
    "help": "/a2z <string>\n或回覆一個信息來將英文字母轉成注音",
    "not_text": "請回復一個文字信息"
  },
  "getuser": {
    "help": "/getuser [user_id]\n或回覆一個使用者來取得該用戶的資訊\n回覆時輸入 /getuser forward 可優先查詢轉寄來源的用戶資訊",
    "error": "取得該用戶資訊時發生錯誤 \n\n{0}",
    "nick": "<b>暱稱</b>: {0}",
    "userame": "<b>Username</b>: {0}",
    "userid": "<b>User id</b>: {0}",
    "status": "<b>目前職位</b>: {0}"
  },
  "pin": {
    "reply_help": "請回復一則訊息以將此訊息至頂",
    "group": "普通群組無法置頂訊息",
    "error": "置頂時發生錯誤\n\n{0}",
    "no_perm": "你沒有權限置頂訊息"
  },
  "replace": {
    "help_not_reply": "請回復一則訊息\n\n用法: /replace <要被取代的文字> <取代的文字>",
    "not_text": "請回復一個文字信息或有說明文字的任何檔案",
    "help": "/replace <要被取代的文字> <取代的文字>\n如果想要取代成空白可以使用<code>''</code>",
    "error": "發生錯誤\n\n{0}",
    "result": "{0} 認為 {1} 的意思是 {2}"
  },
  "getfile": {
    "help": "/getfile <file_id>",
    "error": "無法取得檔案\n\n{0}",
    "senderror": "傳送檔案時發生問題\n\n{0}"
  },
  "fileinfo": {
    "help": "回覆一個信息以取得檔案資訊",
    "istext": "這是文字訊息",
    "filetype": "<b>檔案類型</b> : {0}",
    "fileid": "<b>File id</b> : {0}"
  },
  "exportblog": {
    "no_perm": "你沒有權限",
    "debug_off": "Debug選項是關的",
    "debug": "若要取得Debug log請輸入 /exportblog -debug "
  },
  "tag": {
    "add": {
      "help": "/tag add <tag_name> <userid>\n或回覆該用戶以加入tag名單",
      "b_success": "已將下列用戶加到 {0} 清單:",
      "b_error": "將下列用戶加到 {0} 時發生問題:",
      "too_many": "請不要一次傳太多user,為避免卡死我只處理前50個",
      "already_exist": "此用戶已經在清單中了",
      "r_error": "將 {0} 加入 {1} 時發生問題: {2}",
      "r_success": "已將 {0} 加到 {1} 清單"
    },
    "remove": {
      "help": "/tag remove <tag_name> <userid>\n或回覆該用戶以將該用戶從指定名單移除\n或 /tag remove <tag> * 以移除這個tag",
      "no_list": "本群沒有任何清單",
      "remove_all": {
        "warn": "將<b>移除</b>本群組中的<b>所有</b>tag,此操作無法復原,確認執行請回復這則訊息並輸入 /confirm",
        "no_perm": "你沒有權限移除所有tag"
      },
      "list_not_exist": "清單 {0} 不存在",
      "list_removed": "已移除清單 {0}",
      "b_success": "已將下列用戶從 {0} 清單中移除:",
      "b_error": "將下列用戶從 {0} 移除時發生問題:",
      "too_many": "請不要一次傳太多user,為避免卡死我只處理前50個",
      "not_in_list": "此用戶不在清單中",
      "r_error": "將 {0} 從 {1} 移除時發生問題: {2}",
      "r_success": "已將 {0} 從 {1} 移除"
    },
    "confirm": {
      "donotknow_confirmabout": "我不知道你是在確認甚麼",
      "remove_all_success": "已移除本群組的所有tag"
    },
    "lstag": {
      "no_list": "此群組沒有任何 Tag 清單",
      "all": "清單 {0} ,有 {1} 人",
      "list_not_exist": "清單 {0} 不存在",
      "list_prefix": "清單 {0} ,共 {1} 人"
    },
    "tag": {
      "help": "/tag tag <tag_name>",
      "list_not_exist": "清單 {0} 不存在",
      "tag_prefix": "正在提及清單 {0} 的 {1} 個人"
    },
    "general": {
      "help": "/tag <add|remove|list|tag>",
      "PWRAPI": "此功能因為API終止服務暫時停用，詳情請到[pwrtelegram](https://t.me/pwrtelegram)"
    }
  },
  "gtts": {
    "help": "/gtts <lang_code> <txt>\nEx: /gtts en-GB Hello World!"
  },
  "function": {
    "general": {
      "help": "/function <enable|disable|chkadminf|stats|reset>",
      "reset_complete": "已重置功能狀態",
      "no_perm": "你沒有權限更改功能設定"
    },
    "enable": {
      "help": "/function enable <Function name|all>",
      "deploy": "偵測到本群組沒有設定且已初始化功能列表",
      "funct_not_exist": "找不到 {0}",
      "success": "已啟用 {0} 功能",
      "failed": "無法啟用功能 {0}\n\n{1}",
      "already_true": "此功能目前為啟用狀態",
      "all_member_are_admin": "所有人都是管理員的普通群組無法執行需要管理員的指令",
      "no_perm": "權限不足",
      "group_cant_pin": "普通群組無法置頂訊息"
    },
    "disable": {
      "help": "/function disable <Function name|all>",
      "deploy": "偵測到本群組沒有設定且已初始化功能列表",
      "funct_not_exist": "找不到 {0}",
      "success": "已停用 {0} 功能",
      "success_all": "已停用所有功能",
      "failed": "無法停用功能 {0}\n\n{1}",
      "already_false": "此功能目前為停用狀態"
    },
    "admin_check": {
      "all_member_are_admin": "所有人都是管理員的普通群組無法執行需要管理員的指令，因此有些功能已被停用",
      "success_enable": "已啟用 {0} 功能",
      "success_disable": "已停用 {0} 功能",
      "msg_checking_admin": "正在檢查我是否是管理員..."
    },
    "help": {
      "nofunction": "所有功能已被停用！若需要啟用，請使用 /function 指令"
    }
  }
}
