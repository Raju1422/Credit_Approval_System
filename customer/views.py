from django.shortcuts import render
from .serializers import CustomerRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class CustomerRegisterView(APIView):
    def post(self,request):
        try :
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data.pop('first_name', None) 
                data.pop('last_name', None) 
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        