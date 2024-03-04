from django.shortcuts import render
from rest_framework.views import APIView , Response , status
from .serializers import QuoteSerializer
from .models import Quote
from django.shortcuts import get_object_or_404

# Create your views here.

class QuoteAllView(APIView):

    def get(self,request):
        query = Quote.objects.all()
        ser_data = QuoteSerializer(query,many=True)
        return Response(instance=ser_data.data,status=status.HTTP_200_OK)
    
class QuoteCreateView(APIView):

    def post(self,request):
        data = request.data
        deserdata = QuoteSerializer(data=data)
        if deserdata.is_valid():
            deserdata.save()
            return Response(deserdata.data,status=status.HTTP_201_CREATED)
        return Response(deserdata.errors,status=status.HTTP_400_BAD_REQUEST)
    
class QuoteUpdateView(APIView):
    def put(self, request, pk):
        query_set = get_object_or_404(Quote,id=pk)
        ser_data = QuoteSerializer(instance=query_set,data=request.data,partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuoteDeleteView(APIView):
    def delete(self,request,pk):
        query_set = get_object_or_404(Quote,id=pk)
        query_set.delete()
        return Response({"message":"question delete"},status=status.HTTP_200_OK)