from django.shortcuts import render
from rest_framework.views import APIView , Response , status
from .serializers import QuoteSerializer , TagSerializer
from .models import Quote , Tag
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema ,OpenApiParameter
import requests
from .tasks import get_random_quote
from django.db.models import Q
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
import random


# Create your views here.

class QuoteAllView(APIView):
    serializer_class = QuoteSerializer

    @extend_schema(tags=["quote"],parameters=[
            OpenApiParameter(
                name='Author',
                type=str,
                location=OpenApiParameter.QUERY,
                description="Author full name (default: None)",
                required=False,
            ),
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description="limit for count of item you see (default: 1)",
                required=False,
            ),
            OpenApiParameter(
                name='Term',
                location=OpenApiParameter.QUERY,
                type=str,
                description="Term query to filter contents (default: None)",
                required=False,
            ),
            OpenApiParameter(
                name='Tags',
                location=OpenApiParameter.QUERY,
                type=str,
                description="Tags query to filter by tags (default: None)",
                required=False,
            ),
            OpenApiParameter(
                name='Sort',
                location=OpenApiParameter.QUERY,
                type=bool,
                description="if this query set True results return order by date create (default: False)",
                required=False,
            ),])
    
    def get(self,request):
        author = request.query_params.get("Author","")
        limit = int(request.query_params.get("limit",1))
        search_query = request.query_params.get("Term", "")
        tags = request.query_params.get("Tags", None)
        sort_by_date_create = request.query_params.get("Sort", False)
        if tags:
            tags = tags.split(',') 
            tag_list = Tag.objects.filter(name__in=tags)

        if sort_by_date_create:
            queryset = Quote.objects.all().order_by('-dateadded')
        else:
            queryset = Quote.objects.all().order_by('?')

        get_random_quote.delay()

        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query))
        if author:
            queryset = queryset.filter(author = author)
        if tags:
            queryset = queryset.filter(tags__in=tag_list)
        if limit :
            queryset = queryset[:limit]
        else:
            queryset = queryset[0]



        ser_data = QuoteSerializer(instance=queryset,many=True)
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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

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