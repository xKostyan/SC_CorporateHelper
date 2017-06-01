import urllib2
from bs4 import BeautifulSoup
import datetime
import time


def pr_debug(_data, _function, _dbg):
    # function that prints out debug data;
    # _data - text to print
    # _function - name of the function calling for debug
    # _dbg - flag (0 - disabled | 1 - enabled)
    if _dbg == 1:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print "[{0}] | [{1}:] {2}".format(st, _function, _data)
        print "=" * 50


def corp_api_call(clantag, _dbg):
    # function that calls 'iamogurchik's star conflict players database using provided corp tag
    # returns a list with all the members with corp tag

    # setting up the link for a corporation tag
    _dbg_name = 'corp_api_call'
    link = 'http://ts2.scorpclub.ru/api/v1/findusers.php?search=clanTag%3D%22' \
           + clantag + '%22&sort=nickname&DESC=&limit=400'

    # get data from a web page
    page = urllib2.urlopen(link)
    # process html with soup
    soup = BeautifulSoup(page, "html.parser")

    pr_debug(link, _dbg_name, _dbg)
    pr_debug(page, _dbg_name, _dbg)
    pr_debug(soup, _dbg_name, _dbg)

    table = soup.find("table")
    rows = table.find_all("tr")

    table_contents = []  # stores your table here
    for tr in rows:
        # processing data by html tags creating a 2d list containing each row as shorter list
        if rows.index(tr) == 0:
            row_cells = [th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '']
        else:
            row_cells = ([tr.find('th').getText()] if tr.find('th') else []) + [td.getText().strip() for td in
                                                                                tr.find_all('td') if
                                                                                td.getText().strip() != '']
        if len(row_cells) > 1:
            table_contents += [row_cells]
    pr_debug(table_contents, _dbg_name, _dbg)
    return table_contents


def lists_to_user_dict(list_of_users, _dbg):
    # this function creates a list of dictionaries
    # where each dictionary is a player with its id, name, and corpTag (corpTag is redundant but w/e)
    dict_tags = list_of_users[0]
    list_of_users_formatted = []
    pr_debug(dict_tags, 'lists_to_user_dict', _dbg)
    for i in list_of_users:
        if i != dict_tags:
            pr_debug(i, 'lists_to_user_dict', _dbg)
            temp_dict = dict(zip(dict_tags, i))
            pr_debug(temp_dict, 'lists_to_user_dict', _dbg)
            user_link = "http://ts2.scorpclub.ru/api/v1/userinfo.php?uid=" + str(temp_dict["uid"])
            user_link_dict = {"userLink": user_link}
            temp_dict.update(user_link_dict)
            list_of_users_formatted.append(temp_dict)
    pr_debug(list_of_users_formatted, 'lists_to_user_dict', _dbg)
    return list_of_users_formatted


def full_corp_dict(corptag, _dbg):
    # function that populates full dictionary with received data
    # returns a dict that is ready for conversion to json
    # datetime is "YYYY-MM-DD" format

    list_from_web = corp_api_call(corptag, _dbg)
    members = lists_to_user_dict(list_from_web, _dbg)
    corporation_dict = {"timeStamp": str(datetime.date.today()), "corpTag": corptag, "headCount": len(members),
                        "members": members}
    pr_debug(corporation_dict, "full_corp_dict", _dbg)
    return corporation_dict


