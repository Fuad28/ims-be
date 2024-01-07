import datetime
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras



holding_costs  = np.random.uniform(0.2, 0.3, 33)
ordering_costs = np.random.uniform(2, 300, 33)
unit_costs     = np.random.uniform(1, 10, 33)


def create_date_features(df):
    df['month'] = df.date.dt.month
    df['day_of_month'] = df.date.dt.day
    df['day_of_year'] = df.date.dt.dayofyear
    df['week_of_year'] = df.date.dt.isocalendar().week.astype('int64')
    df['day_of_week'] = df.date.dt.dayofweek + 1
    df['year'] = df.date.dt.year
    df["is_wknd"] = df.date.dt.weekday // 4
    df["quarter"] = df.date.dt.quarter
    df['is_month_start'] = df.date.dt.is_month_start.astype(int)
    df['is_month_end'] = df.date.dt.is_month_end.astype(int)
    df['is_quarter_start'] = df.date.dt.is_quarter_start.astype(int)
    df['is_quarter_end'] = df.date.dt.is_quarter_end.astype(int)
    df['is_year_start'] = df.date.dt.is_year_start.astype(int)
    df['is_year_end'] = df.date.dt.is_year_end.astype(int)
    # 0: Winter - 1: Spring - 2: Summer - 3: Fall
    df["season"] = np.where(df.month.isin([12,1,2]), 0, 1)
    df["season"] = np.where(df.month.isin([6,7,8]), 2, df["season"])
    df["season"] = np.where(df.month.isin([9, 10, 11]), 3, df["season"])
    return df

def run_inference( product_id    : int|str,
                   encoder_path  : str,
                   scaler_path   : str,
                   scalerY_path  : str,
                   model_path    : str,
                   last_demand   : float,
                   onpromotion   : float,
                   oil_price     : float,
                   locale        : str            = 'no holiday',
                   data_save_dir : None|str       = None,
                   start_date    : None|list[int] = None,
                   end_date      : None|list[int] = None,
                   ) -> float:
    '''
    Performs inference on the given data over the specified time.
    PARAMS
    product
    '''
    keras.backend.clear_session()

    

    if end_date:
        end_date   = datetime.datetime(end_date[0], end_date[1],  end_date[2])
    else:
        end_date       = datetime.datetime(datetime.datetime.now().year, 12,  31)
        
        
    if start_date:
        start_date = datetime.datetime(start_date[0], start_date[1],  start_date[2])
    else:
        start_date     = datetime.datetime.now()
        
        
    current_date   = start_date

    days           = (end_date-start_date).days
    
    encoder        = joblib.load(encoder_path)
    scalerOPd      = joblib.load(scaler_path)
    scalerOut      = joblib.load(scalerY_path)
    model          = keras.models.load_model(model_path)

    tot_dems       = 0

    cols = ['family',
        'onpromotion',
        'dcoilwtico',
        'month',
        'day_of_month',
        'day_of_year',
        'week_of_year',
        'is_wknd',
        'is_month_start',
        'is_month_end',
        'is_quarter_start',	
        'is_quarter_end',
        'is_year_start',
        'is_year_end',
        'previous_demand',
        'locale_Local',
        'locale_National',
        'locale_Regional',
        'locale_no holiday',
        'day_of_week_1',
        'day_of_week_2',
        'day_of_week_3',	'day_of_week_4', 'day_of_week_5','day_of_week_6',	'day_of_week_7',
        'quarter_1',	'quarter_2',	'quarter_3',	'quarter_4',
        'season_0',	'season_1',	'season_2',	'season_3']
    

    data           = pd.DataFrame({ 'date'              : [start_date], 
                                    'family'            : [product_id], 
                                    'onpromotion'       : [onpromotion], 
                                    'dcoilwtico'        : [oil_price],
                                    'locale_Local'      : [0],
                                    'locale_National'   : [0],
                                    'locale_Regional'   : [0],
                                    'locale_no holiday' : [1],
                                    'day_of_week_1'     : [0],
                                    'day_of_week_2'     : [0],
                                    'day_of_week_3'     : [0],
                                    'day_of_week_4'     : [0],
                                    'day_of_week_5'     : [0],
                                    'day_of_week_6'     : [0],
                                    'day_of_week_7'     : [0],
                                    'quarter_1'         : [0],	
                                    'quarter_2'         : [0],	
                                    'quarter_3'         : [0],
                                    'quarter_4'         : [0],
                                    'season_0'          : [0],
                                    'season_1'          : [0],
                                    'season_2'          : [0],
                                    'season_3'          : [0],
                                   })

    if type(product_id) == str:
        product_id      = encoder.transform(np.array([[product_id]]).ravel())
        data['family']  = product_id


    if locale == 'Regional':
        data['locale_Regional']   = 1
        data['locale_no holiday'] = 0
        
    if locale == 'Local':
        data['locale_Local']      = 1
        data['locale_no holiday'] = 0
        
    if locale == 'National':
        data['locale_National']   = 1
        data['locale_no holiday'] = 0


    data          = create_date_features(data)
    data['previous_demand']      = last_demand
    
    print('===================== RUNNING MODEL ===============================')
    
    
    for day in range(days):
        # df = data.copy()
        dow           = data['day_of_week'].tolist()[0]
    
        if dow == 1:
            data['day_of_week_1']    = 1
    
        if dow == 2:
            data['day_of_week_2']    = 1
    
        if dow == 3:
            data['day_of_week_3']    = 1
    
        if dow == 4:
            data['day_of_week_4']    = 1
    
        if dow == 5:
            data['day_of_week_5']    = 1
    
        if dow == 6:
            data['day_of_week_6']    = 1
    
        season                       =  data['season'].tolist()[0]
        quarter                      =  data['quarter'].tolist()[0]
    
        match season:
            case 'season_0':
                data['season_0']     = 1
            case 'season_1':
                data['season_1']     = 1
            case 'season_2':
                data['season_2']     = 1
            case 'season_3':
                data['season_3']     = 1
    
        match quarter:
            case 'quarter_1':
                data['quarter_1']    = 1
            case 'quarter_2':
                data['quarter_2']    = 1
            case 'quarter_3':
                data['quarter_3']    = 1
            case 'quarter_4':
                data['quarter_4']    = 1
    
    
        data[['dcoilwtico','previous_demand']] = scalerOPd.transform(data[['dcoilwtico','previous_demand']])
        current_date                 = current_date + datetime.timedelta(days = 1)
        data['date']                 = current_date

        X                            = data[cols].values
        demand                       = scalerOut.inverse_transform(model.predict(X))
        
        
        print(f'demand predicted     = {demand}')
        # demand                       = np.abs(demand)
        
        data['onpromotion']          = np.random.uniform(0, 10,1).tolist()[0]
        data['dcoilwtico']           = np.random.uniform(60, 75,1).tolist()[0]
        data['previous_demand']      = np.random.uniform(0, demand.tolist()[0],1).tolist()[0]
        
        tot_dems+=demand
        
    print('===================== MODEL INFERENCE COMPLETED ===================')
    

    return tot_dems, product_id




def EOQ(D: (float),
        P: int,
        N: list[int,int] = [1,200]):

    """
    Economic Order Quantity

    Arguments:
    D: annual quantity demanded
    P: product ID

    Returns: [EOQ, total cost for 1 order, cost for n_orders and n_orders]

    """

    O = ordering_costs[P]
    S = O
    T = unit_costs[P] * D
    Total_price_for_1 = T
    H = holding_costs[P] *  D



    price = T
    num = 1

    # Validate that all function arguments are non-negative
    if(S>0 and D>0 and H>0):

        print('===================== RUNNING EOQ ===============================')
        


        '''
        HELP ME REVIEW FOR THIS Q THEN
        Q is the EOQ'''

        Q = (np.sqrt(2*S*D/H))

        for i in range(N[0], N[1]+1):
          demand = D//i
          T = unit_costs[P] * demand
          H = holding_costs[P] *  demand
          A = T/2

          C = 0.2*A

          total = C+H+O
          if total < price:
            price = total
            num = i
        print('===================== EOQ COMPLETED ===============================')
        

        return [Q, Total_price_for_1, price, num]

    else:
        print("Error. All function arguments must be non-negative.")


demand, pID = run_inference(     
                   product_id    = 'AUTOMOTIVE',
                   encoder_path  = 'fam encoder.joblib',
                   scaler_path   = 'oil_prevDem.joblib',
                   scalerY_path  = 'sales scaler.joblib',
                   model_path    = 'final model.h5',
                   last_demand   = 0,
                   onpromotion   = 0,
                   oil_price     = 68,
                   start_date    = [2023,1,1],
                   end_date      = [2023,1,31]
             )
# Run example
print(EOQ(demand,pID, [1,120]))