import psycopg2
import psycopg2.extras as extras
import api_data

TABLE_CURRENT_FPL_TEAM = 'current_fpl_team'

dbconn = psycopg2.connect("dbname={} host={} port={} user={} password={}".format("fpl_predictor",
                                                                                 "localhost",
                                                                                 "5432",
                                                                                 "postgres",
                                                                                 "postgres"))


def insert_dataframe(dbconn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = dbconn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        dbconn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        dbconn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


def get_week():
    cursor = dbconn.cursor()
    try:
        query = """select max(week) from %s""" % TABLE_CURRENT_FPL_TEAM
        cursor.execute(query)
        week = cursor.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
    cursor.close()
    week=1 if week == None else week+1
    return week


if __name__ == '__main__':
    df = api_data.get_current_players_data()
    insert_dataframe(dbconn,df,TABLE_CURRENT_FPL_TEAM)
