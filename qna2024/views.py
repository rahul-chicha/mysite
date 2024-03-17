from django.http import HttpResponse, JsonResponse
from ultralytics import YOLO
from roboflow import Roboflow
import json

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from . import textsplit
# download content of google doc file
import io
from googleapiclient.http import MediaIoBaseDownload

import re
#which
SCOPES = ['https://www.googleapis.com/auth/drive']


def send_object(request):
    print("home page requested")
    friends = ["ram", "shyam", "raju"]
    return HttpResponse(friends)

def send_json(request):
    print("home page requested")
    friends = ["ram", "shyam", "raju"]
    return JsonResponse(friends, safe=False)

def question_detection(request):
    print(request)
    # "D:\project2024\qna2024\best (1).pt"
    # model = YOLO(model='../best.pt')  # load a pretrained model (recommended for training)
    model = YOLO(model= './best.pt' )  # load a pretrained model (recommended for training)
    results = model('E://myproject2024/qna2024/history-0081.png', save=True, save_crop=True,  conf=0.50, iou=0.50, line_width=3, project='e:/myproject2024/runs/detect')
    # for result in results:
    #     print(result[0].names)
    print(results[0].__len__())
    return JsonResponse(results[0].tojson(normalize=False), safe=False)

    
def deploy(request):
    rf = Roboflow(api_key="VAcp69rkEQ0XVvoLxLGD")
    project = rf.workspace().project("qna-rslvg")
    project.version(8).deploy(model_type='yolov8', model_path='C://Users/WIN11_2024/Downloads', filename='best.pt')
    return HttpResponse("deployed")

def upload_for_active_learning(request):
    rf = Roboflow(api_key="VAcp69rkEQ0XVvoLxLGD")
    project = rf.workspace().project("qna-rslvg")

def drive_upload(request):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": "download.doc", "mimeType": "application/vnd.google-apps.document",}
        media = MediaFileUpload("runs\detect\predict5\crops\Questions\history-00022.jpg", mimetype="application/vnd.google-apps.document")
        
        # create drive file
        file = (service.files().create(body=file_metadata, media_body=media, fields="id").execute())                
        print(f'File ID: {file.get("id")}')
        file_id = file.get("id")

        # download content of google doc file
        request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
        result = file.getvalue().decode('utf-8')
        print(result)
        #delete uploaded file after ocr
        service.files().delete(fileId=file_id).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    #result = split_paragraph(file.getvalue().decode('utf-8'))
    result_final = textsplit.extract_info(result)
    print (result_final)
    return JsonResponse(result_final, safe=False)

    

# Your input paragraph
input_paragraph = "_______________ 08. * नवपाषाण युग में भारतीय उपमहाद्वीप के उत्तर-पश्चिमी क्षेत्र में निम्नलिखित में से किस स्थान पर कृषि के अभ्युदय के प्रारंभिक प्रमाण प्राप्त हुए हैं? (A) मुंडिगक (C) दम्ब सादत (E) अमरी (B) मेहरगढ (D) बालाकोट उत्तर - (B) मेहरगढ़ [CG PSC (Pre) 2017] मेहरगढ़ पाकिस्तान के बलूचिस्तान में स्थित है जहां से कृषि और कृषक बस्तियों के साक्ष्य प्राप्त हुए । यह स्थल भारतीय उपमहाद्वीप का प्रथम कृषि संबंधी साक्ष्य वाला स्थल है।"

# Function to split the paragraph into different parts
def split_paragraph(input_string):
    # Define a pattern to capture different sections
    input_paragraph = "_______________ 08. * नवपाषाण युग में भारतीय उपमहाद्वीप के उत्तर-पश्चिमी क्षेत्र में निम्नलिखित में से किस स्थान पर कृषि के अभ्युदय के प्रारंभिक प्रमाण प्राप्त हुए हैं? (A) मुंडिगक (C) दम्ब सादत (E) अमरी (B) मेहरगढ (D) बालाकोट उत्तर - (B) मेहरगढ़ [CG PSC (Pre) 2017] मेहरगढ़ पाकिस्तान के बलूचिस्तान में स्थित है जहां से कृषि और कृषक बस्तियों के साक्ष्य प्राप्त हुए । यह स्थल भारतीय उपमहाद्वीप का प्रथम कृषि संबंधी साक्ष्य वाला स्थल है।"
    #print(input_paragraph)
    #pattern = re.compile(r'(\d+\.)\s*\*\s*(.*?)(?:\((A|B|C|D|E)\)\s*(.*?)(?=\([A-E]\)|\[|$))?\s*(\[.*?\])?\s*(.*)')
    pattern = re.compile(r'(\d)')
    # Extract information using the pattern
    match = pattern.match(input_paragraph)
    print(match)
    output_data = {}

    if match:
        output_data["QuestionNumber"] = match.group(1)
        
    #output_json = json.dumps(extract_info(example_string), ensure_ascii=False, indent=2)
    return JsonResponse(output_data, safe=False)