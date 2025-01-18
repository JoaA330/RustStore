from django.shortcuts import render
from .models import User, Status
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def Sign_in(request):
    if request.method != 'POST':
        return JsonResponse({'Error': 'This Endpoint only use POST'})
    
    try:
        data = json.loads(request.body)
        userName = data.get('userName')
        password = data.get('password')
        name = data.get('name')
        lastname = data.get('lastname')
        location = data.get('location')
        role = data.get('u_status')
        
        
        if not all([userName, password, name, lastname, location, role]):
            return JsonResponse({'Error' : 'the data is not completed to create the user'})
          
        user_exist = User.objects.filter(userName = userName).first()
        
        if user_exist :
            return JsonResponse({'Error' : 'The username already exists'})
    
    
        user = User.objects.create(
            userName = userName,
            password = password,
            money = 0,
            name = name,
            online = False,
            lastname = lastname,
            u_status = role,
            location = location
            )
        
        user.save()
    
        return JsonResponse({'message' : 'user created successfully'})
    
    
    except json.JSONDecodeError:
        return JsonResponse({'Error' : 'Json out of syntaxis'})
    
    except Exception as k:
        return JsonResponse({'Error' : str(k)})
    


@csrf_exempt
def Log_in(request):
    if request.method != 'POST':
        JsonResponse({'Error' : 'only POST accepted'})
    
    try:
        data = json.loads(request.body)
        userName = data.get('userName')
        password = data.get('password')
        
        user = User.objects.filter(userName=userName, password=password).first()
        
        if user and user.online == False:
            user.online = True
            return JsonResponse({'message': 'Successfully login'})
        
        else:
            return JsonResponse({'Error': 'data incorrect'})
            
            
            
    except json.JSONDecodeError:
        return JsonResponse({'Error': 'JSON incorrect'})
    
    except Exception as e:
        return JsonResponse({'Error': str(e)})
        
        

def Logout(request, username):
    
    if request.method != 'POST':
        JsonResponse({'Error' : 'only POST accepted'})
      
    try:
        user = User.objects.filter(userName = username).first()
        
        if user.online == True:
            user.online = False
            JsonResponse({'message':'Successfully logout'})
            
        else:
            JsonResponse({'Error':'User stay offline'})
          
            
        
        
    except User.DoesNotExist:
        JsonResponse({'Error':'User dont exists'})
        
    except Exception as e:
        return JsonResponse({'Error': str(e)})

        
        
def Get_user(request,username):
    if request.method != 'GET':
        JsonResponse({'Error' : 'only GET accepted'})
        
        
    try:
        user = User.objects.get(userName = username)
        return user
        
        
    except User.DoesNotExist:
        JsonResponse({'Error':'User dont exists'})
    
    except Exception as e:
        return JsonResponse({'Error': str(e)})
             
