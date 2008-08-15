"""Some useful function for the stats middleware."""

def is_feed(path):
    """is a feed requested?"""
    feeds = ('/feed/', '/rss/', '/atom/', '.rss', '.atom')
    for f in feeds:
        if f.lower() in path.lower():
            return True

def is_search(refer, return_query=False):
    """check if the visitor comes from a search engine. refer must be urlparsed"""
    searchs = {'google': 'q', 'yahoo': 'p', 'aol': 'q', 'aolsvc': 'q', 'search.msn': 'q', 'gmx': 'search', 'suche.web': 'su', 't-online': 'q', 'suche.lycos': 'query', 'altavista': 'q', 'alltheweb': 'q', 'search.live': 'q', 'technorati.com': 'q', 'localhost': 'q',}
    for s in searchs.keys():
        if s in refer[1].lower():
            if return_query:
                try:
                    # split get arguments of the url
                    params = {}
                    for p in refer[4].split("&"):
                        params[p.split("=", 1)[0]] = p.split("=", 1)[1]
                    # return the search string
                    return params[searchs[s]].replace('+', ' ')
                except:
                    return False
            return True

def is_bot(useragent):
    """is the visitor a bot?"""
    bots = ('aipbot', 'amfibibot', 'appie', 'ask jeeves/teoma', 'aspseek', 'axadine', 'baiduspider', 'becomebot', 'blogcorpuscrawler', 'blogpulse', 'blogsnowbot', ' bot ', 'boitho.com', 'bruinbot', 'cerberian', 'cfnetwork', 'check_http', 'cipinetbot', 'claymont', 'crawler', 'cometsearch@cometsystems.com', 'converacrawler', 'cydralspider', 'digger', 'es.net_crawler', 'eventax', 'everyfeed-spider', 'exabot', 'faxobot', 'findlinks', 'fireball', 'friendfeedbot', 'feedparser', 'feedburner', 'francis', 'gaisbot', 'gamekitbot', 'gazz@nttr.co.jp', 'geonabot', 'getrax crawler', 'gigabot', 'girafa.com', 'goforitbot', 'googlebot', 'grub-client', 'holmes', 'houxoucrawler', 'almaden.ibm.com', 'istarthere.com', 'relevantnoise', 'httrack', 'ia_archiver', 'ichiro', 'iltrovatore-setaccio', 'inelabot', 'infoseek', 'inktomi.com', 'irlbot', 'jetbot', 'jobspider_ba', 'kazoombot', 'larbin', 'libwww', 'linkwalker', 'lmspider', 'mackster', 'mediapartners-google', 'microsoft url control', 'mj12bot', 'moreoverbot', 'mozdex', 'msnbot', 'msrbot', 'naverbot', 'netresearchserver', 'ng/2.0', 'np(bot)', 'nutch', 'objectssearch', 'ocelli', 'omniexplorer_bot', 'openbot', 'overture', 'patwebbot', 'php', 'phpdig', 'pilgrim html-crawler', 'pipeliner', 'pompos', 'psbot', 'python-urllib', 'quepasacreep', 'robozilla', 'rpt-httpclient', 'rss-suchmaschine', 'savvybot', 'scooter', 'search.ch', 'seekbot', 'semager', 'seznambot', 'sherlock', 'shelob', 'sitesearch', 'snapbot', 'snappreviewbot', 'speedy spider', 'sphere scout', 'soup', 'stackrambler', 'steeler', 'surveybot', 'szukacz', 'technoratibot', 'telnet', 'themiragorobot', 'thesubot', 'thumbshots-de-bot', 'topicblogs', 'turnitinbot', 'tutorgigbot', 'tutorial crawler', 'twingly', 'vagabondo', 'versus', 'voilabot', 'w3c_css_validator', 'w3c_validator', 'w3c-checklink', 'web downloader', 'webcopier', 'webcrawler', 'webfilter robot', 'west wind internet protocols', 'wget', 'webalta', 'wwweasel robot', 'wwwster', 'xaldon webspider', 'xenu', 'xfruits', 'yahoo! slurp', 'yahoofeedseeker', 'yahoo-mmcrawler', 'zao', 'zipppbot', 'zyborg')
    for bot in bots:
        if bot.lower() in useragent.lower():
            return True

def chart_relation(splitter, *args):
    """return the percentage of each arg on all args"""
    base = 0
    for i in range(len(args)):
        base = base + float(args[i-1])
    plist = ""
    for i in range(len(args)):
        if not args[i]: args[i] = 0
        if i == len(args) - 1: splitter = ""
        plist = plist + str(int((float(args[i]) / base)*100)) + splitter
    return plist
