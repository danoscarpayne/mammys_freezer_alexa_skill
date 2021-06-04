
# imports
import pandas as pd
import numpy as np


from sqlalchemy import create_engine

import flask
from flask import request, jsonify, make_response, abort

import json

from datetime import datetime, date
from dateutil.relativedelta import *

con_url = 'postgresql://kvofwgoepabkir:31da4c48a8799ea4fb77248112f24e169cf4d87b912e2f3cde929dfc4c732f93@ec2-79-125-30-28.eu-west-1.compute.amazonaws.com:5432/djkug1lfqo41t'

engine = create_engine(con_url)

# Set up app
app = flask.Flask(__name__)

@app.route('/v1.0/show_freezer')
def show_table():

    sql_query = '''select * from freezer_table '''

    df = pd.read_sql(sql_query, con=engine)

    return jsonify(df.to_dict('records'))

@app.route('/v1.0/freezer/<name>')
def search_for_freezer_item(name):

    sql_query = '''select * from freezer_table where name ILIKE '%%{}%%' '''.format(name)

    df = pd.read_sql(sql_query, con=engine)

    return jsonify(df.to_dict('records'))

## define function
@app.route('/v1.0/freezer/find_oldest_items')
def find_oldest_items():

    drawer = request.args.get('location', None)
    no_items = request.args.get('limit', None)

    # conditions
    if drawer is None:

        WHERE_CLAUSE = ''
    else:
        WHERE_CLAUSE = '''where location = {}'''.format(drawer)

    print(no_items)

    # limit
    if no_items == None:

        LIMIT_CLAUSE = '''order by 9 desc limit 3'''
    else:
        LIMIT_CLAUSE = '''order by 9 desc limit {}'''.format(no_items)

    # sql statement
    stem = '''select *, (CURRENT_DATE - cast(date_entered as date)) as age from freezer_table '''

    sql_script = stem + WHERE_CLAUSE + LIMIT_CLAUSE

    # create dataframe
    df = pd.read_sql(sql_script, engine)

    return jsonify(df.to_dict('records'))

@app.route('/v1.0/freezer/add_item', methods = ['POST'])
def add_food_item():

    data = request.form

    name = data.get('name')
    location = data.get('location')
    insert_date = data.get('date')
    expiry = data.get('expiry', 3)
    item_no = data.get('qty', 1)
    notes = data.get('notes', '')

    if any(x is None for x in [name, location]):
        abort(400)

    else:

        max_client = pd.read_sql('select max(food_id) as client_no from freezer_table', engine)

        cand_no = max_client.loc[0, 'client_no'] + 1

        # Populate values
        if insert_date is None:

            date_entered = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            date_entered = insert_date

        # Make dict object
        fdict = {}

        fdict['food_id'] = cand_no
        fdict['name'] = name
        fdict['date_entered'] = date_entered
        fdict['expiry_date'] = (date.today() + relativedelta(months=expiry)).strftime('%Y-%m-%dT%H:%M:%SZ')
        fdict['location'] = location
        fdict['months_to_expire'] = expiry
        fdict['notes'] = notes
        fdict['qty'] = item_no

        new_df = pd.DataFrame([fdict])


        new_df.to_sql('freezer_table', con=engine, index=False, if_exists='append')

        msg = 'Successfully Added'

        return make_response(msg, 201)

@app.route('/v1.0/freezer/move_item', methods = ['PUT'])
def move_food_item():

    data = request.form

    food_id = data.get('id')
    location = data.get('location')

    if any(x is None for x in [food_id, location]):
        abort(400)

    else:

        chg_sql = '''
        UPDATE freezer_table
        SET location = {}
        WHERE food_id = {}'''.format(location, food_id)

        with engine.connect() as con:

            con.execute(chg_sql)

        msg = 'Successfully Moved'

        return make_response(msg, 200)

@app.route('/v1.0/freezer/update_food_qty', methods = ['PUT'])
def update_food_qty():

    data = request.form

    food_id = data.get('id')
    qty = data.get('qty')

    if any(x is None for x in [food_id, qty]):
        abort(400)

    else:

        chg_sql = '''
        UPDATE freezer_table
        SET qty = {}
        WHERE food_id = {}'''.format(qty, food_id)

        with engine.connect() as con:

            con.execute(chg_sql)

        msg = 'Successfully Updated'

        return make_response(msg, 200)

@app.route('/v1.0/freezer/delete_item/<food_id>', methods = ['DELETE'])
def delete_food_item(food_id):


    del_sql = '''DELETE FROM freezer_table WHERE food_id={};'''.format(food_id)

    with engine.connect() as con:

        con.execute(del_sql)

    msg = 'Successfully Moved'

    return make_response(msg, 200)


if __name__ == '__main__':
    app.run(debug = True)
