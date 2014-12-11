# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app
from schedule_api import *
import time

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

@app.route('/<abb>')
def test(abb):
    options = {}
    try:
        options['catalogNumbers'] = get_location(abb)
    except:
        options['api_error'] = True

    return render_template('test.html', **options)

@app.route('/terms/<termCode>/<schoolCode>/')
def viewClasses(termCode, schoolCode):
    test=[]
    help = []
    options = {}
    options['i'] = 1
    options['termcode'] = termCode
    options['schoolcode'] = schoolCode
    options['subject'] = request.args['subject']
    options['catalogNumber'] = ''
    options['Credits'] = request.args['credit']
    options['CourseLevel'] = request.args['courseLevel']
    try:
        options['subjects'] = get_subjects(termCode, schoolCode)
    except:
        options['api_error'] = True
    if options['subject'] == '':
        return render_template('coreSearch.html', **options)
    try:
            options['catalogNumbers'] = get_catalogNumbers(termCode, schoolCode, request.args['subject'])
    except:
            options['api_error2'] = True
    if type(options['catalogNumbers']) == type({}):
        help.append(options['catalogNumbers'])
        options['catalogNumbers'] = help
        help = []
    if request.args['catalogNumber'] != '':
        options['catalogNumber'] = request.args['catalogNumber']
        for catalog in options['catalogNumbers']:
            test.append(catalog['CatalogNumber'])
        try:
            test.index(request.args['catalogNumber'])
        except ValueError:
            options['catalogNumber'] = -1
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