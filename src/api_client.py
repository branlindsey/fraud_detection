"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
import pymongo
import pandas as pd
from collections import defaultdict
import psycopg2
import datetime
from .data_cleaner import clean_and_predict

class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key='vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db=None,
                 interval=30):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        self.db = self.connect_to_database()
        self.interval = 30

    def connect_to_database(self):
        conn = psycopg2.connect(dbname='transactions', user='postgres', password='password', host='localhost')
        return conn
    
    def make_predictions(self, data):

        #put data into format that model can recognize
        df = pd.DataFrame(data=None, columns=['body_length', 'channels', 'country', 'currency', 'delivery_method',
                                               'email_domain', 'event_start', 'fb_published', 'has_analytics',
                                               'has_logo', 'listed', 'name', 'name_length', 'num_order', 'num_payouts',
                                               'object_id', 'org_name', 'payee_name', 'payout_type', 
                                               'sale_duration', 'show_map', 'user_age', 'user_created', 'user_type',
                                               'ticket_types', 'total_sales'])


        out = defaultdict() #need a dictionary with only our needed columns. is there a better way todo this? YES!!
        for col in df.columns:
            if col in data:
                df.loc[0, col] = data[col] 
                out[col] = data[col]

        out['time_stamp'] = data['time_stamp']
        #see data_cleaner.py for function details
        #returns dictionary with fraud label and probability key, values
        data = clean_and_predict(df, out) 

        return data 
        
        
    def save_to_database(self, data):
        """Save a data row to the database."""
       # print("Received data:\n" + repr(row) + "\n") 
    
        clean_data = self.make_predictions(data)
        cur = self.db.cursor() #cursify our connection object
        
        placeholders = ', '.join(['%s'] * len(clean_data))
        columns = ', '.join(clean_data.keys())
        sql = "INSERT INTO {} ( {} ) VALUES ( {} )".format('fraud_predictions', columns, placeholders)
        row_values = [str(v).replace(' ', '').replace(',', '') if type(v) == str else v for v in clean_data.values()]

        print (sql)
        print (row_values)
        cur.execute(sql, row_values)

        self.db.commit() #save the insertion
        cur.close() #close for posterity
        
    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        #create empty dictionary to cleanly store messy json data
        dic = defaultdict()
        #create timestamp
        dic['time_stamp'] = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        #put all data in separately
        for item in data['data']:
            for k, v in item.items():
                dic[k] = v

        self.next_sequence_number = data['_next_sequence_number']
        
        return dic

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            if len(data) > 1:
                print("Saving...")
                self.save_to_database(data)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)


def main():
    """Collect events every 30 seconds."""
    client = EventAPIClient()
    client.collect()


if __name__ == "__main__":
    main()
