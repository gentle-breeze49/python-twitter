# encoding: utf-8
import mimetypes
import os
import re

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from twitter import TwitterError

TLDS = [
    "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar",
    "as", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg",
    "bh", "bi", "bj", "bl", "bm", "bn", "bo", "bq", "br", "bs", "bt", "bv",
    "bw", "by", "bz", "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl",
    "cm", "cn", "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz", "de", "dj",
    "dk", "dm", "do", "dz", "ec", "ee", "eg", "eh", "er", "es", "et", "eu",
    "fi", "fj", "fk", "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg",
    "gh", "gi", "gl", "gm", "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw",
    "gy", "hk", "hm", "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in",
    "io", "iq", "ir", "is", "it", "je", "jm", "jo", "jp", "ke", "kg", "kh",
    "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li",
    "lk", "lr", "ls", "lt", "lu", "lv", "ly", "ma", "mc", "md", "me", "mf",
    "mg", "mh", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt",
    "mu", "mv", "mw", "mx", "my", "mz", "na", "nc", "ne", "nf", "ng", "ni",
    "nl", "no", "np", "nr", "nu", "nz", "om", "pa", "pe", "pf", "pg", "ph",
    "pk", "pl", "pm", "pn", "pr", "ps", "pt", "pw", "py", "qa", "re", "ro",
    "rs", "ru", "rw", "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj",
    "sk", "sl", "sm", "sn", "so", "sr", "ss", "st", "su", "sv", "sx", "sy",
    "sz", "tc", "td", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to",
    "tp", "tr", "tt", "tv", "tw", "tz", "ua", "ug", "uk", "um", "us", "uy",
    "uz", "va", "vc", "ve", "vg", "vi", "vn", "vu", "wf", "ws", "ye", "yt",
    "za", "zm", "zw", "ελ", "бел", "мкд", "мон", "рф", "срб", "укр", "қаз",
    "հայ", "الاردن", "الجزائر", "السعودية", "المغرب", "امارات", "ایران", "بھارت",
    "تونس", "سودان", "سورية", "عراق", "عمان", "فلسطين", "قطر", "مصر",
    "مليسيا", "پاکستان", "भारत", "বাংলা", "ভারত", "ਭਾਰਤ", "ભારત",
    "இந்தியா", "இலங்கை", "சிங்கப்பூர்", "భారత్", "ලංකා", "ไทย",
    "გე", "中国", "中國", "台湾", "台灣", "新加坡", "澳門", "香港", "한국", "neric:",
    "abb", "abbott", "abogado", "academy", "accenture", "accountant",
    "accountants", "aco", "active", "actor", "ads", "adult", "aeg", "aero",
    "afl", "agency", "aig", "airforce", "airtel", "allfinanz", "alsace",
    "amsterdam", "android", "apartments", "app", "aquarelle", "archi", "army",
    "arpa", "asia", "associates", "attorney", "auction", "audio", "auto",
    "autos", "axa", "azure", "band", "bank", "bar", "barcelona", "barclaycard",
    "barclays", "bargains", "bauhaus", "bayern", "bbc", "bbva", "bcn", "beer",
    "bentley", "berlin", "best", "bet", "bharti", "bible", "bid", "bike",
    "bing", "bingo", "bio", "biz", "black", "blackfriday", "bloomberg", "blue",
    "bmw", "bnl", "bnpparibas", "boats", "bond", "boo", "boots", "boutique",
    "bradesco", "bridgestone", "broker", "brother", "brussels", "budapest",
    "build", "builders", "business", "buzz", "bzh", "cab", "cafe", "cal",
    "camera", "camp", "cancerresearch", "canon", "capetown", "capital",
    "caravan", "cards", "care", "career", "careers", "cars", "cartier",
    "casa", "cash", "casino", "cat", "catering", "cba", "cbn", "ceb", "center",
    "ceo", "cern", "cfa", "cfd", "chanel", "channel", "chat", "cheap",
    "chloe", "christmas", "chrome", "church", "cisco", "citic", "city",
    "claims", "cleaning", "click", "clinic", "clothing", "cloud", "club",
    "coach", "codes", "coffee", "college", "cologne", "com", "commbank",
    "community", "company", "computer", "condos", "construction", "consulting",
    "contractors", "cooking", "cool", "coop", "corsica", "country", "coupons",
    "courses", "credit", "creditcard", "cricket", "crown", "crs", "cruises",
    "cuisinella", "cymru", "cyou", "dabur", "dad", "dance", "date", "dating",
    "datsun", "day", "dclk", "deals", "degree", "delivery", "delta",
    "democrat", "dental", "dentist", "desi", "design", "dev", "diamonds",
    "diet", "digital", "direct", "directory", "discount", "dnp", "docs",
    "dog", "doha", "domains", "doosan", "download", "drive", "durban", "dvag",
    "earth", "eat", "edu", "education", "email", "emerck", "energy",
    "engineer", "engineering", "enterprises", "epson", "equipment", "erni",
    "esq", "estate", "eurovision", "eus", "events", "everbank", "exchange",
    "expert", "exposed", "express", "fage", "fail", "faith", "family", "fan",
    "fans", "farm", "fashion", "feedback", "film", "finance", "financial",
    "firmdale", "fish", "fishing", "fit", "fitness", "flights", "florist",
    "flowers", "flsmidth", "fly", "foo", "football", "forex", "forsale",
    "forum", "foundation", "frl", "frogans", "fund", "furniture", "futbol",
    "fyi", "gal", "gallery", "game", "garden", "gbiz", "gdn", "gent",
    "genting", "ggee", "gift", "gifts", "gives", "giving", "glass", "gle",
    "global", "globo", "gmail", "gmo", "gmx", "gold", "goldpoint", "golf",
    "goo", "goog", "google", "gop", "gov", "graphics", "gratis", "green",
    "gripe", "group", "guge", "guide", "guitars", "guru", "hamburg", "hangout",
    "haus", "healthcare", "help", "here", "hermes", "hiphop", "hitachi", "hiv",
    "hockey", "holdings", "holiday", "homedepot", "homes", "honda", "horse",
    "host", "hosting", "hoteles", "hotmail", "house", "how", "hsbc", "ibm",
    "icbc", "ice", "icu", "ifm", "iinet", "immo", "immobilien", "industries",
    "infiniti", "info", "ing", "ink", "institute", "insure", "int",
    "international", "investments", "ipiranga", "irish", "ist", "istanbul",
    "itau", "iwc", "java", "jcb", "jetzt", "jewelry", "jlc", "jll", "jobs",
    "joburg", "jprs", "juegos", "kaufen", "kddi", "kim", "kitchen", "kiwi",
    "koeln", "komatsu", "krd", "kred", "kyoto", "lacaixa", "lancaster", "land",
    "lasalle", "lat", "latrobe", "law", "lawyer", "lds", "lease", "leclerc",
    "legal", "lexus", "lgbt", "liaison", "lidl", "life", "lighting", "limited",
    "limo", "link", "live", "lixil", "loan", "loans", "lol", "london", "lotte",
    "lotto", "love", "ltda", "lupin", "luxe", "luxury", "madrid", "maif",
    "maison", "man", "management", "mango", "market", "marketing", "markets",
    "marriott", "mba", "media", "meet", "melbourne", "meme", "memorial", "men",
    "menu", "miami", "microsoft", "mil", "mini", "mma", "mobi", "moda", "moe",
    "mom", "monash", "money", "montblanc", "mormon", "mortgage", "moscow",
    "motorcycles", "mov", "movie", "movistar", "mtn", "mtpc", "museum",
    "nadex", "nagoya", "name", "navy", "nec", "net", "netbank", "network",
    "neustar", "new", "news", "nexus", "ngo", "nhk", "nico", "ninja", "nissan",
    "nokia", "nra", "nrw", "ntt", "nyc", "office", "okinawa", "omega", "one",
    "ong", "onl", "online", "ooo", "oracle", "orange", "org", "organic",
    "osaka", "otsuka", "ovh", "page", "panerai", "paris", "partners", "parts",
    "party", "pet", "pharmacy", "philips", "photo", "photography", "photos",
    "physio", "piaget", "pics", "pictet", "pictures", "pink", "pizza", "place",
    "play", "plumbing", "plus", "pohl", "poker", "porn", "post", "praxi",
    "press", "pro", "prod", "productions", "prof", "properties", "property",
    "pub", "qpon", "quebec", "racing", "realtor", "realty", "recipes", "red",
    "redstone", "rehab", "reise", "reisen", "reit", "ren", "rent", "rentals",
    "repair", "report", "republican", "rest", "restaurant", "review",
    "reviews", "rich", "ricoh", "rio", "rip", "rocks", "rodeo", "rsvp", "ruhr",
    "run", "ryukyu", "saarland", "sakura", "sale", "samsung", "sandvik",
    "sandvikcoromant", "sanofi", "sap", "sarl", "saxo", "sca", "scb",
    "schmidt", "scholarships", "school", "schule", "schwarz", "science",
    "scor", "scot", "seat", "seek", "sener", "services", "sew", "sex", "sexy",
    "shiksha", "shoes", "show", "shriram", "singles", "site", "ski", "sky",
    "skype", "sncf", "soccer", "social", "software", "sohu", "solar",
    "solutions", "sony", "soy", "space", "spiegel", "spreadbetting", "srl",
    "starhub", "statoil", "studio", "study", "style", "sucks", "supplies",
    "supply", "support", "surf", "surgery", "suzuki", "swatch", "swiss",
    "sydney", "systems", "taipei", "tatamotors", "tatar", "tattoo", "tax",
    "taxi", "team", "tech", "technology", "tel", "telefonica", "temasek",
    "tennis", "thd", "theater", "tickets", "tienda", "tips", "tires", "tirol",
    "today", "tokyo", "tools", "top", "toray", "toshiba", "tours", "town",
    "toyota", "toys", "trade", "trading", "training", "travel", "trust", "tui",
    "ubs", "university", "uno", "uol", "vacations", "vegas", "ventures",
    "vermögensberater", "vermögensberatung", "versicherung", "vet", "viajes",
    "video", "villas", "vin", "vision", "vista", "vistaprint", "vlaanderen",
    "vodka", "vote", "voting", "voto", "voyage", "wales", "walter", "wang",
    "watch", "webcam", "website", "wed", "wedding", "weir", "whoswho", "wien",
    "wiki", "williamhill", "win", "windows", "wine", "wme", "work", "works",
    "world", "wtc", "wtf", "xbox", "xerox", "xin", "xperia", "xxx", "xyz",
    "yachts", "yandex", "yodobashi", "yoga", "yokohama", "youtube", "zip",
    "zone", "zuerich", "дети", "ком", "москва", "онлайн", "орг", "рус", "сайт",
    "קום", "بازار", "شبكة", "كوم", "موقع", "कॉम", "नेट", "संगठन", "คอม",
    "みんな", "グーグル", "コム", "世界", "中信", "中文网", "企业", "佛山", "信息",
    "健康", "八卦", "公司", "公益", "商城", "商店", "商标", "在线", "大拿", "娱乐",
    "工行", "广东", "慈善", "我爱你", "手机", "政务", "政府", "新闻", "时尚", "机构",
    "淡马锡", "游戏", "点看", "移动", "组织机构", "网址", "网店", "网络", "谷歌", "集团",
    "飞利浦", "餐厅", "닷넷", "닷컴", "삼성", "onion"]

URL_REGEXP = re.compile(r'(?i)((?:https?://|www\\.)*(?:[\w+-_]+[.])(?:' + r'\b|'.join(TLDS) + r'\b|(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))+(?:[:\w+\/]?[a-z0-9!\*\'\(\);:&=\+\$/%#\[\]\-_\.,~?])*)', re.UNICODE)


def calc_expected_status_length(status, short_url_length=23):
    replaced_chars = 0
    status_length = len(status)
    match = re.findall(URL_REGEXP, status)
    if len(match) >= 1:
        replaced_chars = len(''.join(match))
    status_length = status_length - replaced_chars + (short_url_length * len(match))
    return status_length


def is_url(text):
    if re.findall(URL_REGEXP, text):
        return True
    else:
        return False


def parse_media_file(passed_media):
    img_formats = ['image/jpeg',
                   'image/png',
                   'image/gif',
                   'image/bmp',
                   'image/webp']
    video_formats = ['video/mp4']

    # If passed_media is a string, check if it points to a URL, otherwise,
    # it should point to local file. Create a reference to a file obj for
    #  each case such that data_file ends up with a read() method.
    if not hasattr(passed_media, 'read'):
        if passed_media.startswith('http'):
            filename = os.path.basename(passed_media)
            data_file = urlopen(passed_media)
            file_size = data_file.length
        else:
            with open(os.path.realpath(passed_media), 'rb') as f:
                filename = os.path.basename(passed_media)
                data_file = f
                data_file.seek(0, 2)
                file_size = data_file.tell()

    # Otherwise, if a file object was passed in the first place,
    # create the standard reference to media_file (i.e., rename it to fp).
    else:
        filename = passed_media.name
        data_file = passed_media
        data_file.seek(0, 2)
        file_size = data_file.tell()

    try:
        data_file.seek(0)
    except:
        pass

    media_type = mimetypes.guess_type(os.path.basename(filename))[0]
    if media_type in img_formats and file_size > 5 * 1048576:
        raise TwitterError({'message': 'Images must be less than 5MB.'})
    elif media_type in video_formats and file_size > 15 * 1048576:
        raise TwitterError({'message': 'Videos must be less than 15MB.'})
    elif media_type not in img_formats and media_type not in video_formats:
        raise TwitterError({'message': 'Media type could not be determined.'})

    return data_file, filename, file_size, media_type
