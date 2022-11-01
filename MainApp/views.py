from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status
from MainApp.models import File
from  MainApp.serializers import FileUploadSerializer,SaveFileSerializer
from datetime import datetime
import json
# remember to import the FileUploadSerializer and SaveFileSerializer
class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']

        timeFrame = serializer.validated_data['timeFrame']
        reader = pd.read_csv(file)
        reader['DATE']= pd.to_datetime(reader['DATE'], format='%Y%m%d') 
        reader['DATE'] = reader['DATE'].astype(str)
        #print( reader['DATE'])
        #reader["TIME"] = pd.to_timedelta(reader["TIME"])
        #reader["TIME"] = pd.to_datetime(reader["TIME"]).dt.time
        reader["TIME"] = pd.to_datetime(reader["TIME"]).dt.strftime('%H:%M')

        #print(reader["TIME"])
        reader["DateTime"] = reader["DATE"] + ' ' + reader["TIME"]
        reader["DateTime"] = pd.to_datetime(reader["DateTime"], format="%Y%m%d %H:%M")
        #print( reader["DateTime"])
        reader = reader.set_index("DateTime")

        dataFrame = reader.resample(f'{timeFrame}T',origin='start').agg({"OPEN": "first", 
                                             "CLOSE": "last", 
                                             "LOW": "min", 
                                             "HIGH": "max"})

        dataFrame2 = dataFrame.to_json(orient = 'table') 
        #print(dataFrame2)

        with open("JsonOutput.json", "w") as media:
                    json.dump(dataFrame2, media)

       
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)