from __future__ import print_function
from django.shortcuts import render
from django.http import JsonResponse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from tapdashboard.settings import SCOPES


def getAllTAPGrades(request):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'classroom_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('classroom', 'v1', credentials=creds)

    # Additional Details

    # - Awarded grades
    # - Submission status(Submitted or yet to submit)
    # - Submission Time(Submitted before or after the Due date)

    # Dashboard

    # - Average grade
    # - % showing number of students submitting the assignment
    # - % showing submissions before due date and late submission

    courseWork = service.courses().courseWork().list(courseId=116777377623).execute().get('courseWork', [])
    students = service.courses().students().list(courseId=116777377623).execute().get('students', [])
    studentsubmissions = service.courses().courseWork().studentSubmissions().list(
        courseId=116777377623, # TAP My Art Project id
        courseWorkId = "-" # All TAP Assignments
    ).execute().get('studentSubmissions', [])
    return JsonResponse({
        "courseWork" : courseWork,
        "studentsubmissions" : studentsubmissions,
        "students" : students
    },safe=False)