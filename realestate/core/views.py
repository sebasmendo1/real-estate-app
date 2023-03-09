from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SearchSerializer
from .models import Search

# Create your views here.
def usrealestate(request):
    zip_code = "75204"
    url = "https://us-real-estate.p.rapidapi.com/v2/for-sale-by-zipcode"

    querystring = {"zipcode":{zip_code}
                   ,"offset":"0"
                   ,"limit":"42"}

    headers = {
        "X-RapidAPI-Key": "14a1e513e4mshb66fc223dcedc01p154082jsn5afd3b8b6581",
        "X-RapidAPI-Host": "us-real-estate.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # Return the response as JSON
    return JsonResponse(response.json())

def front(request):
    context = { }
    return render(request, "index.html", context)

def homeValue(rent, rentalSqft, listingSqft, listingPrice): 
    closingCosts = 15000
    rentalPricePerSqft = rent // listingSqft
    avgRentalPricePerSqft = avg(rentalPricePerSqft)
    PVAR = avgRentalPricePerSqft * listingSqft
    bruteNegotiationPrice = (PVAR * 100)/0.6 
    maxOffer = bruteNegotiationPrice - closingCosts
    minOffer = maxOffer*0.85

    return maxOffer, minOffer; 

@csrf_exempt
def searchListings(request):
    if request.method == "POST":
        zipCode = request.POST.get("zipCode")
        return JsonResponse({"zipCode": zipCode})
    

@api_view(['GET', 'POST'])
def search(request):

    if request.method == 'GET':
        search = Search.objects.all()
        serializer = SearchSerializer(search, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def search_detail(request, pk):
    try:
        zip_code = Search.objects.get(pk=pk)
    except Search.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        Search.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)