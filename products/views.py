from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Gun,Product,Transport,Tool,Armor
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from users.models import User
from .serializers import ProductSerializer


@api_view(['POST'])
def Publish_Product(request):
    
    data = ProductSerializer(data=request.data)
    if data.is_valid():
        data.save()
        return Response({'message':'product successfully published'}, status=201)
    
    return Response(data.errors, status=400)
        


@csrf_exempt
def Delete_product(request, id, username):
    
    if request.method != 'DELETE':
        return JsonResponse({'Error':'only DELETE method acepted'})
    
    
    
    try:
        
        product_exists = Product.objects.get(id=id)
        
        if product_exists.seller != username:
            return JsonResponse({'Error':'user without permissions'})
        
        product_exists.delete()
        return JsonResponse({'message':'product successfully deleted'})
        
        
    except Product.DoesNotExist:
        return JsonResponse({'Error':'product does not exists'})    
        
    except Exception as a:
        return JsonResponse({'Error':str(a)})
        
        
        
@csrf_exempt
def Get_product(request, id, username):
    if request.method != 'GET':
        JsonResponse({'Error': 'only GET method acepted'})
        
      
    try:  
        product = Product.objects.get(id = id)
        return JsonResponse({
            "Product": 
                {
                    "name": product.name,
                    "id": id,
                    "category": product.category,   
                    "price" : product.price,
                    "used": product.used,
                    "recommendedFor": product.recommendedFor,
                    "description": product.description,
                    "seller": product.seller
            }   
        })
        

        
    except Product.DoesNotExist:
        return JsonResponse({'Error':'product does not exists'})
    except Exception as e:
        return JsonResponse({'Error':str(e)})
    
    
@csrf_exempt 
def Get_Publications(Request, username):
    if Request.method != 'GET':
        JsonResponse({'Error': 'only GET method acepted'})

    
    try:
        publications = Product.objects.all().values()

        return JsonResponse({"Publications": list(publications)})
        
        
    except Product.DoesNotExist:
        return JsonResponse({'Error':'product does not exists'})
    except Exception as e:
        return JsonResponse({'Error':str(e)})
        
    
 

@csrf_exempt 
def Buy_Product(Request, username, id):
    if Request.method != 'POST':
        JsonResponse({'Error': 'only POST method acepted'})

    
    try:
        user = User.objects.filter(userName = username).first()
        product = Product.objects.filter(id = id).first()
        seller = User.objects.filter(userName = product.seller).first()
        
        if user.money < product.price :
            return JsonResponse({'Error':'User dont have enought money'})
        
        else:
            user.money = user.money - product.price
            seller.money = seller.money + product.price
            product.delete()
            user.save()
            seller.save()
            return JsonResponse({'message':'Product successfully bought'})
            
    
   
    except User.DoesNotExist:
        return JsonResponse({'Error':'product does not exists'})
        
    except Product.DoesNotExist:
        return JsonResponse({'Error':'product does not exists'})
    
    
    except Exception as e:
        return JsonResponse({'Error':str(e)})   

    
    
