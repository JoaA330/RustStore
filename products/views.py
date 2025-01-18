from django.shortcuts import render
from .models import Gun,Product,Transport,Tool,Armor
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from users.models import User
import json

@csrf_exempt
def Publish_Product(request):
    if request.method != 'POST' :
        return JsonResponse({'Error':'only method POST acepted'}) 
    
    try:
        #PRODUCT--
        data = json.loads(request.body)
        username = data.get('userName')
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        description = data.get('description')
        used = data.get('used')
        author = data.get('author')
        type = data.get('type')
        maxspeed = data.get('maxSpeed')
        charge = data.get('chargeLevel')
        promagic = data.get('protectionForMagic')
        proCourts = data.get('protectionForCouts')
        proHits = data.get('protectionForHits')
        agricult = data.get('agricultural')
        
        name_exists = Product.objects.filter(name = name, seller=username).first()
        
        if name_exists:
            return JsonResponse({'Error':'the product already exists'}) 
        
        
        if not all([username, name, category, price]):
            return JsonResponse({'Error':'data incomplete'})
        
        
        #GUN--
        if category == 'Guns':
            
            if not all([author,type]):
                return JsonResponse({'Error':'data incomplete'})
            
            
            if type == 'Archer':
                recommend = 'Archer'
                
            elif type == 'Magical':
                recommend = 'Wizard'
            
            else:
                recommend = 'Warrior'
                
            
            p = Gun.objects.create(
                name = name,
                category = category,
                price = price,
                description = description,
                used = used,
                author = author,
                type = type,
                seller= username,
                recommendedFor = recommend
            )
            
            
        #TRANSPORT--
        elif category == 'Transport':
            
            if not all([maxspeed, charge]):
                return JsonResponse({'Error':'data incomplete'})
            
            p = Transport.objects.create(
                name = name,
                category = category,
                price = price,
                description = description,
                maxSpeed = maxspeed,
                chargeLevel = charge,
                seller= username
            )
          
        #TOOL--    
        elif category == 'Tools':  
            
            if not all([agricult]):
                return JsonResponse({'Error':'data incomplete'})
            
            p = Tool.objects.create(
                name = name,
                category = category,
                price = price,
                description = description,
                used = used,
                agricultural = agricult,
                seller= username
            )
            
        #ARMOR--    
        else:
            if not all([proCourts, proHits, promagic]):
                return JsonResponse({'Error':'data incomplete'})
            
            p = Armor.objects.create(
                name = name,
                category = category,
                price = price,
                description = description,
                used = used,
                protectionForMagic = promagic,
                protectionForCourts = proCourts,
                protectionForHits = proHits,
                seller= username
            )
            
        p.save()
        return JsonResponse({'message':'successfully published'})
        
        
                 
    except json.JSONDecodeError:
        return JsonResponse({'Error':'JSON incorrect format'})
    
    except Exception as e:
        return JsonResponse({'Error':str(e)})
        


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

    
    
