# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app
from schedule_api import *
<<<<<<< HEAD
import time
=======
import ast
>>>>>>> origin/master

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
<<<<<<< HEAD
    help = []
=======
>>>>>>> origin/master
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
<<<<<<< HEAD
            return render_template('coreSearch.html', **options)
        options['className'] = get_className(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
        try:
            help = get_classSections(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
            if type(help) == type([]):
                options['sections'] = help
            elif type(help) == type({}):
                options['sections'] = []
                options['sections'].append(help)
        except:
            options['api_error1'] = True
    else:
        options['sections'] = []
        i = 0
        change = True
        for catalogNumber in options['catalogNumbers']:
            if change:
                t1 = time.time()
                change = False
            help = get_basicClassInfo(termCode, schoolCode, request.args['subject'], catalogNumber['CatalogNumber'])
            options['sections'].append(help)
            i += 1
            if i == 29:
                i = 0
                t2 = time.time()
                time.sleep(61 - (t2 - t1))
                change = True

        '''options['sections'] = []
        if request.args['courseLevel'] == '' and request.args['credit'] == '':
            for catalogNumber in options['catalogNumbers']:
                help = get_classSections(termCode, schoolCode, request.args['subject'], catalogNumber['CatalogNumber'])
                if type(help) == type([]):
                    help1['SectionNumber'] = catalogNumber['CatalogNumber']
                    help1['SectionName'] = catalogNumber['CourseDescr']
                    help1['sectionType'] = help[0]['SectionType']
                    help1['CreditHours'] = help[0]['CreditHours']
                    options['sections'].append(help1)
                elif type(help) == type({}):
                    help1['SectionNumber'] = catalogNumber['CatalogNumber']
                    help1['SectionName'] = catalogNumber['CourseDescr']
                    help1['sectionType'] = help['SectionType']
                    help1['CreditHours'] = help['CreditHours']
                    options['sections'].append(help1)


        elif request.args['courseLevel'] == '':
            for catalogNumber in options['catalogNumbers']:
                help = get_classSections(termCode, schoolCode, request.args['subject'], catalogNumber['CatalogNumber'])
                if type(help) == type([]):
                    if int(help[0]['CreditHours'][0]) == int(request.args['credit']):
                        options['sections'].append(catalogNumber)
                elif type(help) == type({}):
                    if int(help['CreditHours'][0]) == int(request.args['credit']):
                        options['sections'].append(catalogNumber)

        elif request.args['credit'] == '':
            for catalogNumber in options['catalogNumbers']:
                if int(request.args['courseLevel']) != 5:
                    if int(catalogNumber['CatalogNumber'][0]) == int(request.args['courseLevel']):
                        options['sections'].append(catalogNumber)
                else:
                    if int(catalogNumber['CatalogNumber'][0]) >= int(request.args['courseLevel']) :
                        options['sections'].append(catalogNumber)
        else:
            for catalogNumber in options['catalogNumbers']:
                help = get_classSections(termCode, schoolCode, request.args['subject'], catalogNumber['CatalogNumber'])
                if type(help) == type([]):
                    if int(help[0]['CreditHours'][0]) == int(request.args['credit']) and int(catalogNumber['CatalogNumber'][0]) == int(request.args['courseLevel']):
                        options['sections'].append(catalogNumber)
                elif type(help) == type({}):
                    if int(help['CreditHours'][0]) == int(request.args['credit']) and int(catalogNumber['CatalogNumber'][0]) == int(request.args['courseLevel']):
                        options['sections'].append(catalogNumber)'''
=======
        options['className'] = get_className(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
        try:
            options['sections'] = get_classSections(termCode, schoolCode, request.args['subject'], request.args['catalogNumber'])
        except:
            options['api_error1'] = True
    else:
        options['sections'] = {}
        for catalogNumber in options['catalogNumbers']:
            options['sections'][catalogNumber['CatalogNumber']] = get_className(termCode, schoolCode, 'EECS', '203')
>>>>>>> origin/master

    return render_template('coreSearch.html', **options)
