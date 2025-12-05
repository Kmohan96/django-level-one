from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import movie_details
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def basic(requset):
    return HttpResponse("hello world")

def movie_info(request):
    movie=request.GET.get("movie") #movie-og.date-oct 25
    date=request.GET.get("date")
    return JsonResponse({"status":"success","result":{"movie_name":movie,"release_date":date}},status=200)



@csrf_exempt
def movies(request):
    if request.method=="POST":
        #data=json.loads(request.body)
        data=request.POST
        movie=movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"movie record inserted successfully","data":data},status=200)
    elif request.method=="GET":
        movie_info=movie_details.objects.all()
        movie_list=[]
        rating_filter=request.GET.get("rating")
        min_bud_filter=request.GET.get("min_budget")
        max_bud_filter=request.GET.get("max_budget")
        if rating_filter:
            movie_info=movie_info.filter(rating__gte=float(rating_filter))
        for i in movie_info:
            if min_bud_filter or max_bud_filter:
                budget_str=i.budget.lower().replace("cr","")
                budget_val=float(budget_str)
                if min_bud_filter and budget_val<=float(min_bud_filter):
                    continue
                if max_bud_filter and budget_val>=float(max_bud_filter):
                    continue
            movie_list.append({
                "movie_name":i.movie_name,
                "release_date":i.release_date,
                "budget":i.budget,
                "rating":i.rating
            })

        if len(movie_list)==0:
            return JsonResponse({"status":"success","message":"no movies found matching the criteria"},status=200)
        return JsonResponse({"status":"success","data":movie_list},status=200)
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        existing_movie=movie_details.objects.get(id=ref_id)
        if data.get("movie_name"):
            new_movie=data.get("movie_name")
            existing_movie.movie_name=new_movie
            existing_movie.save()
        elif data.get("release_date"):
            new_release_date=data.get("release_date")
            existing_movie.release_date=new_release_date
            existing_movie.save()
        elif data.get("budget"):           
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
        elif data.get("rating"):
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        return JsonResponse({"status":"success","message":"movie record updated successfully","data":data},status=200) 
    elif request.method=="DELETE":
        data=request.GET.get("id")
        ref_id=int(data)
        existing_movie=movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({"status":"success","message":"movie record deleted successfully"},status=200)

    return JsonResponse({"error":"error occured"},status=400)



# @csrf_exempt
# def rating_get(request):
#     if request.method=="GET":
#         result_list=[]
#         result=movie_details.objects.all()
#         for i in result:
#             if i.rating>3.5:
#                  result_list.append({
#                 "movie_name":i.movie_name,
#                 "release_date":i.release_date,
#                 "budget":i.budget,
#                 "rating":i.rating
#                  })
#         return JsonResponse({"status":"success","data":result_list},status=200)
    

# @csrf_exempt
# def budget_get(request):
#     if request.method == "GET":
#         result_list = []
#         movies = movie_details.objects.all()
#         for m in movies:
#             budget_number = int(m.budget[:-2])  
#             if 25 <= budget_number <= 45:
#                 result_list.append({
#                     "movie_name": m.movie_name,
#                     "release_date": m.release_date,
#                     "budget": m.budget,
#                     "rating": m.rating
#                 })

#         return JsonResponse({"status": "success", "data": result_list}, status=200)




