from django.shortcuts import render
from rest_framework.views import APIView , Response , status
from .serializers import QuoteSerializer , TagSerializer
from .models import Quote , Tag
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
import requests
from .tasks import get_random_quote

# Create your views here.

class QuoteAllView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"])
    def get(self,request):
        get_random_quote.delay()
        query = Quote.objects.all()
        ser_data = QuoteSerializer(instance=query,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
    
class QuoteDetailView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"])
    def get(self,request,pk):
        query = get_object_or_404(Quote,quote_id=pk)
        ser_data = QuoteSerializer(instance=query)
        return Response(ser_data.data,status=status.HTTP_200_OK)
    
class QuoteCreateView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"])
    def post(self,request):
        data = request.data
        deserdata = QuoteSerializer(data=data)
        if deserdata.is_valid():
            deserdata.save()
            return Response(deserdata.data,status=status.HTTP_201_CREATED)
        return Response(deserdata.errors,status=status.HTTP_400_BAD_REQUEST)
    
class QuoteUpdateView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"])
    def put(self, request, pk):
        query_set = get_object_or_404(Quote,id=pk)
        ser_data = QuoteSerializer(instance=query_set,data=request.data,partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuoteDeleteView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"])
    def delete(self,request,pk):
        query_set = get_object_or_404(Quote,id=pk)
        query_set.delete()
        return Response({"message":"question delete"},status=status.HTTP_200_OK)
    
class CreatTagView(APIView):
    serializer_class = TagSerializer

    @extend_schema(tags=["tag"])
    def post(self,request):
        deserdata = TagSerializer(data=request.data)
        if deserdata.is_valid():
            deserdata.save()
            return Response(deserdata.data,status=status.HTTP_201_CREATED)
        return Response(deserdata.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TagAllView(APIView):
    serializer_class = TagSerializer

    @extend_schema(tags=["tag"])
    def get(self,request):
        query_set = Tag.objects.all()
        ser_data = TagSerializer(instance=query_set,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


class TagDetailView(APIView):
    serializer_class = TagSerializer

    @extend_schema(tags=["tag"])
    def get(self,request,pk):
        query_set = get_object_or_404(Tag,id=pk)
        ser_data = TagSerializer(instance=query_set)
        return Response(ser_data.data,status=status.HTTP_200_OK)