# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app
from schedule_api import *
<<<<<<< HEAD
import time
=======
<<<<<<< HEAD
import time
=======
import ast
>>>>>>> origin/master
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

<<<<<<< HEAD
@app.route('/<abb>')
def test(abb):
    options = {}
    try:
        options['catalogNumbers'] = get_location(abb)
=======
@app.route('/terms/<termCode>/<schoolCode>/<subjectCode>')
def test(termCode, schoolCode, subjectCode):
    options = {}
    try:
        options['catalogNumbers'] = get_catalogNumbers(termCode, schoolCode, subjectCode)
>>>>>>> origin/master
    except:
        options['api_error'] = True

    return render_template('test.html', **options)

@app.route('/terms/<termCode>/<schoolCode>/')
def viewClasses(termCode, schoolCode):
    test=[]
<<<<<<< HEAD
    help = []
=======
<<<<<<< HEAD
    help = []
=======
>>>>>>> origin/master
>>>>>>> origin/master
    options = {}
    options['i'] = 1
    options['termcode'] = termCode
    options['schoolcode'] = schoolCode
    options['subject'] = request.args['subject']
    options['catalogNumber'] = ''
<<<<<<< HEAD
    options['Credits'] = request.args['credit']
    options['CourseLevel'] = request.args['courseLevel']
=======
>>>>>>> origin/master
    try:
        options['subjects'] = get_subjects(termCode, schoolCode)
    except:
        options['api_error'] = True
<<<<<<< HEAD
    if options['subject'] == '':
        return render_template('coreSearch.html', **options)
=======
>>>>>>> origin/master
    try:
            options['catalogNumbers'] = get_catalogNumbers(termCode, schoolCode, request.args['subject'])
    except:
            options['api_error2'] = True
<<<<<<< HEAD
    if type(options['catalogNumbers']) == type({}):
        help.append(options['catalogNumbers'])
        options['catalogNumbers'] = help
        help = []
=======
>>>>>>> origin/master
    if request.args['catalogNumber'] != '':
        options['catalogNumber'] = request.args['catalogNumber']
        for catalog in options['catalogNumbers']:
            test.append(catalog['CatalogNumber'])
        try:
            test.index(request.args['catalogNumber'])
        except ValueError:
            options['catalogNumber'] = -1
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> origin/master
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
<<<<<<< HEAD
            help = get_basicClassInfo(termCode, schoolCode, request.args['subject'], catalogNumber['CatalogNumber'])
            options['sections'].append(help)

    return render_template('coreSearch.html', **options)

@app.route('/terms/<termCode>/<schoolCode>/<subjectCode>/<catalogNumber>/<sectionNumber>')
def viewDetailOfCourse(termCode, schoolCode, subjectCode, catalogNumber, sectionNumber):
    options = {}
    help = []
    help1 = []
    options['termcode'] = termCode
    options['schoolcode'] = schoolCode
    options['subjectcode'] = subjectCode
    options['catalognumber'] = catalogNumber
    options['chosenSection'] = sectionNumber
    options['i'] = 1
    try:
        options['Sections'] = get_classSections(termCode, schoolCode, subjectCode, catalogNumber)
    except:
        options['api_error'] = True
    if type(options['Sections']) == type({}):
        help.append(options['Sections'])
        options['Sections'] = help
    options['className'] = get_className(termCode, schoolCode, subjectCode, catalogNumber)
    options['classDescr'] = get_classDescr(termCode, schoolCode, subjectCode, catalogNumber)
    for section in options['Sections']:
        teachers = get_instructorName(termCode, schoolCode, subjectCode, catalogNumber, section['SectionNumber'])
        books = get_textbook(termCode, schoolCode, subjectCode, catalogNumber, section['SectionNumber'])
        section['Meeting'] = get_sectionInfo(termCode, schoolCode, subjectCode, catalogNumber, section['SectionNumber'])['Meeting']
        if type(section['Meeting']) == type({}):
            help1.append(section['Meeting'])
            section['Meeting'] = help1
            help1 = []
        for meeting in section['Meeting']:
            address = get_location(meeting['Location'][(meeting['Location'].rfind(' '))+1:])
            meeting['Address'] = address
        section['Textbooks'] = books
        section['Instructors'] = teachers

    return render_template('particularCourse.html', **options)
=======
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
>>>>>>> origin/master
