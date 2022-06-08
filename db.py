import psycopg2
import psycopg2.extras as extras
import api_data

TABLE_CURRENT_FPL_TEAM = 'current_fpl_team'

dbconn = psycopg2.connect("dbname={} host={} port={} user={} password={}".format("fpl_predictor",
                                                                                 "localhost",
                                                                                 "5432",
                                                                                 "postgres",
                                                                                 "postgres"))



def execute_values(dbconn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    # SQL query to execute
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



if __name__ == '__main__':
    df = api_data.get_current_players_data()
    execute_values(dbconn,df,TABLE_CURRENT_FPL_TEAM)
