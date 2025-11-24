from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from allaboutmovies.models import Movie_details
# Create your views here.
def basic(request):
    return HttpResponse("hello world")
   
@csrf_exempt
def movie(request):
    if request.method=="POST":
        data=json.loads(request.body)
        rating_value=int(data.get("rating",0))
        rating_stars="*"* rating_value
        movie_details =Movie_details.objects.create(
            movie_name = data.get('movie_name'),
            release_date = data.get('release_date'),
            budget = data.get('budget'),
            rating = rating_value,
        )
        return JsonResponse({"status": "success", "data":data},status=200)
    
    elif request.method=="GET":
        result=list(Movie_details.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        movie_id=data.get("id")#getting id
        if not movie_id:
            return JsonResponse({"error": "Movie ID is required"}, status=400)
        try:
            Movie_details.objects.get(id=movie_id)
        except Movie_details.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
        # Update only fields provided in the PUT request
        Movie_details.objects.filter(id=movie_id).update(
            movie_name = data.get("movie_name"),
            release_date = data.get("release_date"),
            budget = data.get("budget"),
            rating = data.get("rating"))
        updated_data = Movie_details.objects.filter(id=movie_id).values().first()
        return JsonResponse({"status":"Movie updated successfully","updated_data":updated_data},status=200)
    
    elif request.method == "DELETE":
        data = json.loads(request.body)
        movie_id = data.get("id")
        if not movie_id:
           return JsonResponse({"error": "Movie ID is required"}, status=400)
        try:
           movie = Movie_details.objects.get(id=movie_id)
           movie.delete()
           return JsonResponse({"status": "Movie deleted successfully"}, status=200)
        except Movie_details.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)
        
