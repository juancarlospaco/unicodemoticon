#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pkgutil


AUTOSTART_DESKTOP_FILE = pkgutil.get_data('unicodemoticon',
                                          'unicodemoticon.desktop')


CODES = tuple("""aa ab ae af ak am an ar as av ay az ba be bg bh bi bm bn bo
bo br bs ca ce ch co cr cs cs cu cv cy cy da de de dv dz ee el el en eo es et
eu eu fa fa ff fi fj fo fr fr fy ga gd gl gn gu gv ha he hi ho hr ht hu hy hy
hz ia id ie ig ii ik io is is it iu ja jv ka kg ki kj kk kl km kn ko kr ks ku
kv kw ky la lb lg li ln lo lt lu lv mg mh mi mi mk mk ml mn mr ms ms mt my my
na nb nd ne ng nl nl nn no nr nv oc oj om or os pa pi pl ps pt qu rm rn ro ro
ru rw sa sc sd se sg si sk sk sl sm sn so sq sq sr ss st su sv sw ta te tg th
ti tk tl tn to tr ts tt tw ty ug uk ur uz ve vi vo wa wo xh yi yo za zh zh zu
""".split())


STD_ICON_NAMES = tuple(sorted(set("""emblem-default emblem-documents start-here
emblem-downloads emblem-favorite emblem-important emblem-mail emblem-photos
emblem-readonly emblem-shared emblem-symbolic-link emblem-synchronized
emblem-system emblem-unreadable face-angel face-angry face-crying face-devilish
face-embarrassed face-cool face-kiss face-laugh face-monkey face-plain
face-raspberry face-sad face-sick face-smile face-smile-big face-smirk
face-surprise face-tired face-uncertain face-wink face-worried go-home
insert-image insert-link insert-object insert-text list-add edit-copy
edit-find-replace edit-paste tools-check-spelling accessories-character-map
accessories-dictionary accessories-text-editor preferences-desktop-font
preferences-desktop-keyboard applications-other applications-utilities
preferences-other user-bookmarks application-x-executable image-missing
""".split())))  # use your themes icons


UNICODEMOTICONS = {
    "faces":
        "😀😬😁😂😃😄😅😆😇😉😊🙂☺😋😌😍😘😗😙😚😜😝😛😎😏😶😐😑😒😳😞😟😠😡😔😕🙁☹😣😖😫😩😤😮😱😨😰😯😦😧😢😥😪😓😭😵😲😷😴💤💩😈👿👹👺💀👻👽😺😸😹😻😼😽🙀😿😾☻👀🙌👏👋👍👎👊✊✌👌✋👐💪🙏☝👆👇👈👉🖕🖐🤘🖖✍💅👄👅👂👃👁👀👤👥🗣👶👦👧👨👩👱👴👵👲👳👮👷💂🕵🎅👼👸👰🚶🏃💃👯👫👬👭🙇💁🙅🙆🙋🙎🙍💇💆💑👩‍❤️‍👩👨‍❤️‍👨💏👩‍❤️‍💋‍👩👨‍❤️‍💋‍👨👪👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👩‍👦👩‍👩‍👧👩‍👩‍👧‍👦👩‍👩‍👦‍👦👩‍👩‍👧‍👧👨‍👨‍👦👨‍👨‍👧👨‍👨‍👧‍👦👨‍👨‍👦‍👦👨‍👨‍👧‍👧👚👕👖👔👗👙👘💄💋👣👠👡👢👞👟👒🎩🎓👑⛑🎒👝👛👜💼👓🕶💍🌂",

    "symbols":
        "𝒜𝒞𝒟𝒢𝒥𝒦𝒩𝒪𝒫𝒬𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝔅𝔇𝔉𝔐ℵαβγδελμψ^@½⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ₐₑₒₓₔₕₖₗₘₙₚₛₜ⋙⋘™✔©®€℅№∗√∞≋≡≢⊕⊖⊗⊛☆🜀★⏧⌖☎♀♂✓✗⦿⧉⩸*¢£¥×¤ж—†•π℗Ω≬⊹✠⩐∰§´»«@θ¯⋄∇♥✗☦☧☨☩☪☫☬☭☯࿊࿕☥✟✠✡⛤‼⁉…❓✔✗☑☒➖➗❌™®©Ω℮₤₧❎✅➿♿☠☯☮☘💲💯🚭🚮💤㋡🔞🚼🛀🚬🚭🌀⇉⇇⇈⇊➺⇦⇨⇧⇩↔↕↖↗↘↙↯↰↱↲↳↴↵↶↷↺↻➭🔄⏪⏩⏫⏬①②③④⑤⑥⑦⑧⑨⑩➊➋➌➍➎➏➐➑➒➓½¾∞⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓨⓩ■●▲▼▓▒░◑◐〇◈▣▨▧▩◎◊□◕☉♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♲♻♳♴♵♶♷♸♹♺♼♽♾",

    "feelings":
        "❤💛💚💙💜💔❣💕💞💓💗💖💘💝💟☮🆔⚛📴📳🆚🉑🆑🅾🆘⛔🚫❌⭕💢♨🚷🚯🚳🚱🔞📵❗❕❓❔‼⁉💯🔅🔆⚜⚠🚸🔰💠🌀➿🌐Ⓜ🏧🚹🚺🚼🚮🆗🆙🆒🆕🆓🔚🔙🔛🔝🔜☑🔘⚪⚫🔴🔵🔸🔹🔶🔷🔺▪▫⬛⬜🔻◼◻🃏💭🗯💬♥♡❤❦☙❣💌💘💞💖💓💗💟💝💑🌹💋💔💕✵✪✬✫✻✴☆✨✶✩★✾❄❀✿🃏⚝⚹⚜🌟🌠💫💥♀♂⚢⚣⚤⚥⚧☿👭👬👫",

    "nature":
        "🌋🌌🌁🐶🐱🐭🐹🐰🐻🐼🐨🐯🐮🐷🐽🐸🐙🐵🙈🙉🙊🐒🐔🐧🐦🐤🐣🐥🐺🐗🐴🦄🐝🐛🐌🐞🐜🕷🐍🐢🐠🐟🐡🐬🐳🐋🐊🐆🐅🐃🐂🐄🐪🐫🐘🐐🐏🐑🐎🐖🐀🐁🐓🦃🕊🐕🐩🐈🐇🐿🐾🐉🐲🌵🎄🌲🌳🌴🌱🌿☘🍀🎍🎋🍃🍂🍁🌾🌺🌻🌹🌷🌼🌸💐🍄🌰🎃🐚🕸🌎🌍🌏🌕🌖🌗🌘🌑🌒🌓🌔🌚🌝🌛🌜🌞🌙⭐🌟💫✨☄☀🌤⛅🌥🌦☁🌧⛈🌩⚡🔥💥❄🌨☃⛄🌬💨🌪🌫☂☔💧💦🌊",

    "culture":
        "🏠🏡🏫🏢🏣🏥🏪🏩🏨💒⛪🏬🏤🌇🌆🏯🏰⛺🏭🗼🗻🌄🌅🌃🗽🌉🎠🎡⛲🎢🚢🗽🎍🎎🎒🎓🎏🎃👻🎅🎄🎁🎋🎉🎊🎈🎌🌎💩⚙⚖⚔⚒🔐🔗🔩♫♪♭♩🎶🎵🎼🎨🎬🎤🎧🎹🎻🎺🎷🎸🏁⚽🏀🏈⚾🎾🏐🏉🎱⛳🏌🎿⛷🏂⛸🏹🎣🚣🏊🏄🛀⛹🏋🚴🚵🏇🕴🏆🎽🏅🎖🎗🏵🎫🎟🎭🎨🎪🎤🎧🎼🎹🎷🎺🎸🎻🎬🎮👾🎯🎲🎰🎳",

    "food":
        "🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🍍🍅🍆🌶🌽🍠🍯🍞🧀🍗🍖🍤🍳🍔🍟🌭🍕🍝🌮🌯🍜🍲🍥🍣🍱🍛🍙🍚🍘🍢🍡🍧🍨🍦🍰🎂🍮🍬🍭🍫🍿🍩🍪🍺🍻🍷🍸🍹🍾🍶🍵☕🍼🍴🍽",

    "tech":
        "⌚📱📲⌨🖥🖨🖱🖲🕹🗜💽💾💿📀📼📷📸📹🎥📽🎞📞☎📟📠📺📻🎙🎚🎛⏱⏲⏰🕰⏳⌛📡🔋🔌💡🔦🕯🗑🛢💸💵💴💶💷💰💳💎⚖🔧🔨⚒🛠⛏🔩⚙⛓🔫💣🔪🗡⚔🛡🚬☠⚰⚱🏺🔮📿💈⚗🔭🔬🕳💊💉🌡🏷🔖🚽🚿🛁🔑🗝🛋🛌🛏🚪🛎🖼🗺⛱🗿🛍🎈🎏🎀🎁🎊🎉🎎🎐🎌🏮✉📩📨📧💌📮📪📫📬📭📦📯📥📤📜📃📑📊📈📉📄📅📆🗓📇🗃🗳🗄📋🗒📁📂🗂🗞📰📓📕📗📘📙📔📒📚📖🔗📎🖇✂📐📏📌📍🚩🏳🏴🔐🔒🔓🔏🖊🖋✒📝✏🖍🖌🔍🔎📛🔊🔉🔇🔔🔕☢☣☤✇✆⛵🚤🚣⚓🚀✈💺🚁🚂🚊🚆🚈🚇🚋🚎🚌🚍🚙🚕🚖🚛🚚🚓🚔🚒🚑🚐🚲🚡🚟🚜",

    "multichar":
        ("d-( ʘ‿ʘ )_m", "d-(✿ ʘ‿ʘ)_m", "ಠ_ಠ", "ಢ_ಢ", "┌П┐(⌣د̲⌣)┌П┐", "(￣(工)￣)", "⊙_ʘ",
         "ಡ_ಡ", "⊙_⊙", "⊙▃⊙", "¯\_(ツ)_/¯", "(づ｡◕‿‿◕｡)づ", "⊂(ʘ‿ʘ)つ",
         "ლ(ಠ_ಠ ლ)", "≖_≖", "⊂(`･ω･´)つ", "Ծ_Ծ", "¯\＼(⊙_ʘ)/¯", "ʕ•ᴥ•ʔ",
         "͡° ͜ʖ﻿ ͡°", "ᕦ(ò_óˇ)ᕤ", "(¬▂¬)", "█▄▄ ███ █▄▄", "(⌐■_■)",
         "✌.|•͡˘‿•͡˘|.✌", "[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]", "\(｡◕‿‿◕｡)/", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
         "٩(｡͡•‿•｡)۶", "∩(°︶▽°︶)∩", "☜(ﾟヮﾟ☜)", "Ƹ̵̡Ӝ̵̨̄Ʒ", "┐(;´༎ຶД༎ຶ`)┌",
         "(✿つ°ヮ°)つ  └⋃┘", "(つ°ヮ°)つ  （。Y。）", "(✿ ◕‿◕) ᓄ✂╰⋃╯",
         "(つ°ヮ°)つ  (‿|‿)",  "▄︻̷̿┻̿═━一", "(｡♥‿‿♥｡)", "╭∩╮（︶︿︶）╭∩╮",
         "<('()))}><{", "┐(´～`；)┌", "(╯°□°）╯︵ ┻━┻", "(ง'̀-'́)ง", "ᕙ(⇀‸↼‶)ᕗ",
         "ლ(=ↀωↀ=)ლ", "ヾ(*ΦωΦ)ﾉ", "m_༼ ༎ຶ ෴ ༎ຶ༽_m", "\(•⊙ω⊙•)/",
         "o(╥﹏╥)o", "╭∩╮_(҂≖̀‿≖́)_╭∩╮", "💞 ╭∩╮_(✿ -༗‿༗-)_╭∩╮ 💕",
         "(－‸ლ)", "(͠≖ ͜ʖ͠≖)", "╭∩╮( ͡⚆ ͜ʖ ͡⚆)╭∩╮", "ლ(╹◡╹ლ)", "(๑˃̵ᴗ˂̵)و",
         "(V) (°,,,°) (V)", "( ͠° ͟ʖ ͡°)", "ಠ_ರೃ", "🌀_🌀", "♥‿♥",
         "₍₍ ᕕ( ･᷄ὢ･᷅ )ᕗ⁾⁾",  "*｡٩(ˊωˋ*)و✧*｡",  "(•ิ_•ิ)?",
         "(　-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷄◞ω◟-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷅ )",
         "(つ°ヮ°)つ  (≬)", "┻━┻ ︵ \(°□°)/ ︵ ┻━┻",
         "¸.·´¯`·.´¯`·.¸¸.·´¯`·.¸><(((º>", "ᶠᶸᶜᵏ♥ᵧₒᵤ", "\,,/(◣_◢)\,,/",
         "(⌐■_■)--︻╦╤─ - - - (╥﹏╥)", "\m/_(>_<)_\m/", "Yᵒᵘ Oᶰˡʸ Lᶤᵛᵉ Oᶰᶜᵉ",
         "(つ -‘ _ ‘- )つ", "^⨀ᴥ⨀^", "ლ(́◕◞Ѿ◟◕‵ლ)", "┌∩┐(⋟﹏⋞)┌∩┐",
         "ˁ˚ᴥ˚ˀ", "ヽ(￣(ｴ)￣)ﾉ", "(⋟﹏⋞)", "⊂(✰‿✰)つ",
         "(づ ￣ ³￣)づ ⓈⓂⓄⓄⓉⒽ", "❚█══█❚ ▐━━━━━▌",
         "/( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ", "(ง⌐□ل͜□)ง", " ─=≡Σ((( つ◕ل͜◕)つ",
         " ┬──┬◡ﾉ(° -°ﾉ)", "(•̀ᴗ•́)و ̑̑", "（。Y。）ԅ(≖‿≖ԅ)", "(っ˘з(˘⌣˘ )",
         "(ᗒᗣᗕ)՞", "¯\_( ʘ‿ʘ)人(ʘ‿ʘ )_/¯", "ฅ(⌯͒• ɪ •⌯͒)ฅ❣", "ฅ(≚ᄌ≚) ",
         "o(≧∇≦o)", "ฅ ̳͒•ˑ̫• ̳͒ฅ", "(=｀ェ´=)", "₍˄ุ.͡˳̫.˄ุ₎ฅ˒˒", "༼༭ຶཬ༤ຶ༽", "૮(ㅍ◞◟ㅍ)ა",
         "(〓￣(∵エ∵)￣〓)", "૮(꒦ິཅ꒦ິ)ა", "✲ﾟ｡✧٩(･ิᴗ･ิ๑)۶✲ﾟ｡✧", "٩(๑ơలơ)۶♡",
         "- =͟͟͞͞ ( ꒪౪꒪)ฅ✧", "୧( ॑ധ ॑)୨", "(Ɔ ˘⌣˘)♥(˘⌣˘ C)", "(ʃƪ ˘ ³˘)",
         "♡ლ(-༗‿༗-)ლ♡", "\(≚ᄌ≚)/", "＼⍩⃝／", "(ಠ .̫.̫ ಠ)",
         "( • Y • )ԅ(‾⌣‾ԅ)", "૮(⋆❛ہ❛⋆)ა", "/(　-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷄◞ω◟-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷅ )", "૮(꒦ິཅ꒦ິ)ა",
         "\(¬ω¬)/", "¯\_(҂⌣̀_⌣́)_/¯", "ლ(´﹏`ლ)", "\( ༎ຶŎ༎ຶ )/",
         "ღ╰⋃╯ღ•̥̑ .̮ •̥̑)", "⊂(^(工)^)⊃", "|'''\ (Ⓘ.Ⓘ) /'''|",
         "ヽ(´ー`)人(´∇｀)人(`Д´)ノ", "ʕʘ̅͜ʘ̅ʔ", "¯\_(❤‿❤)_/¯", "┣┓웃┏♨❤♨┑유┏┥",
         "|ʘ‿ʘ)╯", "ƪ(`▿▿´ ƪ)", "\(○’ω’○)/", "◎ヽ(^･ω･^=)~", "\(◦'⌣'◦)/",
         "(⌣́_⌣̀)\('́⌣'̀ )", "(ఠ_ఠ)", "\(☉_☉)/", "¯\_(⌣̯̀⌣́)_/¯",
         "ƪ(˘⌣˘)┐ ƪ(˘⌣˘)ʃ ┌(˘⌣˘)ʃ", "〜(￣▽￣〜)(〜￣▽￣)〜", "B==✊==D 💦")
}
