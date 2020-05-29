import psycopg2

#connect to transactions database
conn = psycopg2.connect(dbname='transactions', user='postgres', password='password', host='localhost')

cur = conn.cursor()
#define table structure
query = """CREATE TABLE fraud_predictions (
                        time_stamp CHAR(19) PRIMARY KEY,
                        body_length INT,
                        channels INT,
                        country CHAR(3), 
                        currency CHAR(3), 
                        delivery_method INT,
                        email_domain CHAR(50), 
                        event_id INT,
                        event_start INT, 
                        fb_published INT, 
                        has_analytics INT, 
                        has_logo INT, 
                        listed CHAR(1),
                        name CHAR(50),
                        name_length INT, 
                        num_order INT, 
                        num_payouts INT,
                        object_id INT, 
                        org_name CHAR(250), 
                        payee_name CHAR(75), 
                        payout_type CHAR(10), 
                        sale_duration REAL,
                        show_map INT, 
                        user_age INT, 
                        user_created BIGINT, 
                        user_type INT,
                        total_sales REAL, 
                        fraud CHAR(11),
                        f_prob REAL);"""
#create actual table
cur.execute(query)
#save table to db
conn.commit()

cur.close()
conn.close()