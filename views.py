# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app
from schedule_api import *
import ast

@app.route('/')
def index():
    options = {}
    try:
        options['terms'] = get_terms()
    except:
        options['api_error'] = True

    return render_template('index.html', **options)

@app.route('/terms/<termCode>')
def viewSchools(termCode):
    options = {}
    try:
        options['schools'] = get_schools(termCode)
    except:
        options['api_error'] = True

    return render_template('term'+termCode+'.html', **options)

@app.route('/terms/<termCode>/schools/')
def viewSubjects(termCode):
    options = {}
    options['termcode'] = termCode
    options['schoolcode'] = request.args['school']
    try:
        options['subjects'] = get_subjects(termCode, request.args['school'])
    except:
        options['api_error'] = True

    return render_template('coreSearchHome.html', **options)

@app.route('/terms/<termCode>/<schoolCode>/<subjectCode>')
def test(termCode, schoolCode, subjectCode):
    options = {}
    try:
        options['catalogNumbers'] = get_catalogNumbers(termCode, schoolCode, subjectCode)
    except:
        options['api_error'] = True

    return render_template('test.html', **options)

@app.route('/terms/<termCode>/<schoolCode>/')
def viewClasses(termCode, schoolCode):
    test=[]
    options = {}
    options['i'] = 1
    options['termcode'] = termCode
    options['schoolcode'] = schoolCode
    options['subject'] = request.args['subject']
    options['catalogNumber'] = ''
    try:
        options['subjects'] = get_subjects(termCode, schoolCode)
    except:
        options['api_error'] = True
    try:
            options['catalogNumbers'] = get_catalogNumbers(termCode, schoolCode, request.args['subject'])
    except:
            options['api_error2'] = True
    if request.args['catalogNumber'] != '':
        options['catalogNumber'] = request.args['catalogNumber']
        for catalog in options['catalogNumbers']:
            test.append(catalog['CatalogNumber'])
        try:
            test.index(request.args['catalogNumber'])
        except ValueError:
            options['catalogNumber'] = -1
        options['className'] = get_className(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
        try:
            options['sections'] = get_classSections(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
        except:
            options['api_error1'] = True
    else:
        options['sections'] = {}
        for catalogNumber in options['catalogNumbers']:
            options['sections'][catalogNumber['CatalogNumber']] = get_className(termCode, schoolCode, 'EECS', '203')

    return render_template('coreSearch.html', **options)
