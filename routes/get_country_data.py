from flask import Blueprint, render_template
import json
from google.cloud import datastore
from collections import defaultdict

get_country_data_bp = Blueprint('get_country_data', __name__)

@get_country_data_bp.route('/population-table')
def country_population():
    client = datastore.Client()
    countries = []
    for country_code in ['MY', 'VN', 'PH', 'TH', 'SG', 'KH', 'MM', 'BN', 'LA', 'ID']:
        query = client.query(kind='population')
        query.add_filter('country_code', '=', country_code)
        query.order = ['-timestamp']
        query.limit = 1
        result = list(query.fetch())
        if result:
            country = {
                'code' : result[0]['country_code'],
                'name': result[0]['country_name'],
                'population': result[0]['population'],
                'timestamp': result[0]['timestamp']
            }
            countries.append(country)
    return render_template('country_population_table.html', countries=countries)

@get_country_data_bp.route('/population-chart')
def country_population_chart():
    # get_pop_change_by_year()
    return render_template('country_population_chart.html', countries=get_country_population(), year_countries = get_population_by_year(), year_rate=get_pop_change_by_year())

def get_country_population():
    client = datastore.Client()
    countries = []
    for country_code in ['MY', 'VN', 'PH', 'TH', 'SG', 'KH', 'MM', 'BN', 'LA', 'ID']:
        query = client.query(kind='population')
        query.add_filter('country_code', '=', country_code)
        query.order = ['-timestamp']
        query.limit = 1
        result = list(query.fetch())
        if result:
            country = {
                'code' : result[0]['country_code'],
                'name': result[0]['country_name'],
                'population': result[0]['population'],
                'timestamp': result[0]['timestamp']
            }
            countries.append(country)
    return countries

def get_population_by_year():
    client = datastore.Client()
    year_countries = []
    for country_code in ['MY', 'VN', 'PH', 'TH', 'SG', 'KH', 'MM', 'BN', 'LA', 'ID']:
        query = client.query(kind='population')
        query.add_filter('country_code', '=', country_code)
        query.add_filter('year', '>=', 2000)
        query.add_filter('year', '<=', 2022)
        query.order = ['year']
        result = list(query.fetch())
        if result:
            population_data = []
            for entity in result:
                population_data.append({
                    'year': entity['year'],
                    'population': entity['population']
                })
            country = {
                'code': result[0]['country_code'],
                'name': result[0]['country_name'],
                'data': population_data
            }
            year_countries.append(country)
    return year_countries

def get_pop_change_by_year():
    client = datastore.Client()
    year_rate = []
    for country_code in ['MY', 'VN', 'PH', 'TH', 'SG', 'KH', 'MM', 'BN', 'LA', 'ID']:
        last_yr_pop = 0
        curr_yr_pop = 0
        query = client.query(kind='population')
        query.add_filter('country_code', '=', country_code)
        query.add_filter('year', '>=', 2000)
        query.add_filter('year', '<=', 2022)
        query.order = ['year']
        result = list(query.fetch())
        if result:
            population_data = []
            for entity in result:
                curr_yr_pop = entity['population']
                year = entity['year']
                rate = ((curr_yr_pop - last_yr_pop) / curr_yr_pop) * 100
                if last_yr_pop == 0 : 
                    rate = 0

                population_data.append({
                    'year': year,
                    'population': curr_yr_pop,
                    'rate' : rate
                })

                last_yr_pop = curr_yr_pop
                # print (f'year = {year} country = {country_code} rate = {rate}')
            country = {
                'code': result[0]['country_code'],
                'name': result[0]['country_name'],
                'data': population_data
            }
            year_rate.append(country)
    return year_rate
    