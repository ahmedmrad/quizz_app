import mysql.connector
import yaml
import random
import itertools
from data_manipulation import convert
from itertools import chain

def get_creds(db_name):
    """
    Get MySQL credentials
    :return host: host address
    :return user: user name
    :return password: database password
    :return database: database name
    """
    with open('config.yaml', 'r') as config:
        cfg = yaml.load(config, Loader=yaml.FullLoader)
    host = cfg[db_name]['host']
    user = cfg[db_name]['user']
    password = cfg[db_name]['password']
    database = cfg[db_name]['database']
    return host, user, password, database


def connect(host, user, password, database):
    """
    Connect to MySQL database
    :param host: host address
    :param user: user name
    :param password: database password
    :param database: database name
    :return: Connection Object or none
    """
    conn = None
    try:
        conn = mysql.connector.connect(host=host,
                                       user=user,
                                       password=password,
                                       database=database,
                                       autocommit=True)
        if conn.is_connected():
            print('Connected to MySQL database')

    except Exception as e:
        print(e)
    return conn


def check_condition(conn):
    '''
    check if we viewed every idea at least 10 times
    :param conn:
    :return list_results:
    '''
    mycursor = conn.cursor()
    sql = """ SELECT idea_view FROM ideas_ """
    mycursor.execute(sql)
    results = mycursor.fetchall()
    list_results = list(itertools.chain(*results))
    return list_results


def get_SampleIdeas(conn, max_val, sample):
    '''
    Get ideas to be displayed
    :param conn: mysql connector object
    :param max_val: maximum round to be allowed
    :param sample: sample size
    :return results: sampled tables in the form of tuples
    return sample_list: list ids
    '''
    mycursor = conn.cursor()
    sql_1 = """SELECT id, view_count  FROM ideas_ """
    mycursor = conn.cursor()
    mycursor.execute(sql_1)
    results = mycursor.fetchall()
    dict_sampleIdeas = convert(results, {})
    ids_ideasNotViewedEnough = [key for key, val in dict_sampleIdeas.items() if val != max_val]
    if ids_ideasNotViewedEnough != 0:
        sample_list = random.sample(ids_ideasNotViewedEnough, sample)
        if len(sample_list) >= sample:
            sql_2 = """SELECT ideas FROM ideas_ WHERE id IN {}""".format(tuple(sample_list))
            mycursor.execute(sql_2)
            results = [item[0] for item in mycursor.fetchall()]
        elif 0 < len(sample_list) < sample:
            first_elem = """SELECT ideas FROM ideas_ WHERE id IN {}""".format(tuple(sample_list))
            rest_sampleIds = [key for key, val in dict_sampleIdeas.items() if key not in sample_list]
            rest_sample = random.sample(ids_ideasNotViewedEnough, sample - len(sample_list))
            second_elem = """SELECT ideas FROM ideas_ WHERE id IN {}""".format(tuple(rest_sample))
            mycursor.execute(sql_2)
            results = [item[0] for item in mycursor.fetchall()]
        else:
            pass
    else:
        ids = [key for key, val in dict_sampleIdeas.items()]
        id_list = random.sample(ids_ideasNotViewedEnough, sample)
        sql_2 = """SELECT ideas FROM ideas_ WHERE id IN {}""".format(tuple(id_list))
        mycursor.execute(sql_2)
        results = [item[0] for item in mycursor.fetchall()]
    return results, sample_list

def get_randomSample(conn, sample):
    """
    Create random sample list for the form
    this will only be displayed in the case all the ideas in the round
    are circuled through -will not be recorded.
    :param conn: mysql connector object
    :return result: sampled tables in the form of tuples
    """
    sql = """ SELECT id FROM ideas_ """
    mycursor = conn.cursor()
    mycursor.execute(sql)
    ids = [item[0] for item in mycursor.fetchall()]
    sample_list = tuple(random.sample(ids, sample))
    sql_2 = ("""SELECT ideas FROM ideas_ WHERE id IN {}""".format(sample_list))
    mycursor.execute(sql_2)
    results = mycursor.fetchall()
    data_list = list(chain.from_iterable(results))
    return data_list


def update_novel(conn, sample_list):
    '''
    update novel count if answer was yes
    :param conn: mysql connector object
    :param sample_list: list of ideas to be updated
    '''
    if len(sample_list) == 1:
        sql = """UPDATE ideas_ SET novel = novel+1  WHERE ideas IN '{0}'""".format(str(sample_list))
        mycursor = conn.cursor()
        print(sql)
        mycursor.execute(sql)
        conn.commit()
    else:
        sql = """UPDATE ideas_ SET novel = novel+1  WHERE ideas IN {}""".format(tuple(sample_list))
        mycursor = conn.cursor()
        print(sql)
        mycursor.execute(sql)
        conn.commit()


def update_original(conn, sample_list):
    '''
    update original count if answer was yes
    :param conn: mysql connector object
    :param sample_list: list of ideas to be updated
    '''
    if len(sample_list) == 1:
        sql = """UPDATE ideas_ SET original = original+1  WHERE ideas IN '{0}'""".format(str(sample_list))
        mycursor = conn.cursor()
        mycursor.execute(sql)
        conn.commit()
    else:
        sql = """UPDATE ideas_ SET original = original+1  WHERE ideas IN {}""".format(tuple(sample_list))
        mycursor = conn.cursor()
        mycursor.execute(sql)
        conn.commit()


def update_feasible(conn, sample_list):
    '''
    update feasible count if answer was yes
    :param conn: mysql connector object
    :param sample_list: list of ideas to be updated
    '''
    if len(sample_list) == 1:
        sql = """UPDATE ideas_ SET feasible = feasible+1  WHERE ideas IN '{0}'""".format(str(sample_list))
        mycursor = conn.cursor()
        mycursor.execute(sql)
        conn.commit()
    else:
        sql = """UPDATE ideas_ SET feasible = feasible+1  WHERE ideas IN {}""".format(tuple(sample_list))
        mycursor = conn.cursor()
        mycursor.execute(sql)
        conn.commit()


def update_ViewCount(conn, sample_list):
    """
    update the view_count_temp column
    :param conn: mysql connector object
    :param sample_list: list of tuple ids to be updated
    :return: updated view_count_temp columns
    """
    sql = """UPDATE ideas_ SET view_count = view_count+1  WHERE ideas IN {}""".format(tuple(sample_list))
    mycursor = conn.cursor()
    mycursor.execute(sql)
    conn.commit()


def get_userCode(conn):
    '''
    generate the user passcode to receive payment
    :param conn: mysql connector object
    :return : return user_passcode
    '''
    sql = '''SELECT user_code, view_count FROM password'''
    mycursor = conn.cursor()
    mycursor.execute(sql)
    passcode = mycursor.fetchall()
    dict_userPasscode = convert(passcode, {})
    list_userPasscode = [key for key, val in dict_userPasscode.items() if val == 0]
    secure_random = random.SystemRandom()
    user_passcode = secure_random.choice(list_userPasscode)
    return user_passcode


def update_UserCode(conn, user_code):
    '''
    Make sure the user code is only viewed once
    :param conn: mysql connector object
    :param user_code:  user code selected
    '''
    mycursor = conn.cursor()
    sql = ''' UPDATE password SET view_count = view_count + 1 WHERE user_code = '{0}' '''.format(str(user_code))
    mycursor.execute(sql)
    conn.commit()


def update_ratings(conn, difficulty, certainty, user_code):
    '''
    Update the rating system difficult/certainty
    :param conn: mysql connector object
    :param ratings_list: user code, and measure of difficulty and certainty
    '''
    mycursor = conn.cursor()
    sql = '''UPDATE password SET rating_difficulty = '{0}', rating_certainty ='{1}' where user_code = '{2}' '''.format(difficulty, certainty, str(user_code))
    print(sql)
    mycursor.execute(sql)
    conn.commit()

def update_success(conn,user_code):
    '''
    Flag the user if he answered the english test correctly
    :param conn: mysql connector object
    :param user_code:  user code selected
    '''
    mycursor = conn.cursor()
    sql = ''' UPDATE password SET english_test = 'success' WHERE user_code = '{0}' '''.format(str(user_code))
    mycursor.execute(sql)
    conn.commit()

def update_failed(conn, user_code):
    '''
    Flag the user if he answered the english test incorrectly
    :param conn: mysql connector object
    :param user_code:  user code selected
    '''
    mycursor = conn.cursor()
    sql = ''' UPDATE password SET english_test = 'failed' WHERE user_code = '{0}' '''.format(str(user_code))
    mycursor.execute(sql)
    conn.commit()
