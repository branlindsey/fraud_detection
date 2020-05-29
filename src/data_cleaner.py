import pandas as pd
import pickle

def total_cost(ls):
    item_sum = []
    for i, cost in enumerate(ls):
        cost = ls[i]['cost'] * ls[i]['quantity_total']
        item_sum.append(cost)
    return sum(item_sum)

def clean_and_predict(df, data):
    
    df['total_sales'] = total_cost(data['ticket_types'])
    
    data['total_sales'] = df['total_sales'][0]
    data['event_id'] = data['ticket_types'][0]['event_id'] if data['ticket_types'] else -1
    data.pop('ticket_types', None)
    df.pop('ticket_types')
    #Fill NA values
    df.fillna(value={'has_header':-1, 
                     'delivery_method':-1, 
                     'country': '',  
                     'sale_duration': '46.87',  #this is the mean of our trained data (bad programming but hey we only have a day)
                     'num_order': 1,
                     'num_payouts':0},
                      inplace=True)
    df['sale_duration'] = df['sale_duration'].apply(lambda f: str(f))
    #FIX STRING FORMATTING ISSUES
    #df['org_name'] = df['org_name'].apply(lambda s: ''.join([l for l in s if l.isalpha()]))
    #df['name'] = df['name'].apply(lambda s: ''.join([l for l in s if l.isalpha()]))
    #bad programming but needs to be done for the model and SQL database
    df['delivery_method'] = int(df['delivery_method']) 
    data['delivery_method'] = int(df['delivery_method'])

    model = pickle.load(open('src/model.sav', 'rb'))
    
    probability = model.predict(df, prediction_type='Probability')[0,1]
    label = 'NO RISK'

    if probability > 0.9:
        label = 'HIGH RISK'
    elif probability > 0.3:
        label = 'MEDIUM RISK'
    elif probability > 0.001:
        label = 'LOW RISK'
        
    data['fraud'] = label
    data['f_prob'] = round(probability,5)

    return data
    