from django.shortcuts import render, redirect
from .models import User, Travel
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, "travel_app/main.html")
def register(request):
    if request.method == 'GET':
        return redirect ('/main')
    newuser = User.objects.register(request.POST)
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each)
        return redirect('/main')
    if newuser[0] == True:
        # messages.success(request, 'Well done')
        request.session['id'] = newuser[1].id
        return redirect('/travels')

def travels(request):
    if 'id' not in request.session:
        return redirect ("/main")
    context = {
        "user": User.objects.get(id=request.session['id']),
        "travels" : Travel.objects.all(),
        "others": Travel.objects.all().exclude(join__id=request.session['id'])
    }
    return render(request, 'travel_app/travels.html', context)

def login(request):
    if request.method == 'GET':
        return redirect('/main')
    if 'id' in request.session:
        return redirect('/travels')
    else:
        user = User.objects.login(request.POST)
        if user[0] == False:
            for each in user[1]:
                messages.error(request, each)
            return redirect('/main')
        if user[0] == True:
            # messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['id'] = user[1].id
    return redirect('/travels')



def logout(request):
    if 'id' not in request.session:
        return redirect('/main')
    del request.session['id']
    return redirect('/main')

def addingplan(request):
    if 'id' not in request.session:
        return redirect ("/main")
    else:
        context= {
            "user":User.objects.get(id=request.session['id']),
        }
        return render(request, 'travel_app/addingplan.html', context)

def addplan(request):

    if request.method != 'POST':
        return redirect ("/travels/add")
    newplan= Travel.objects.travelPlan(request.POST, request.session["id"])
    if newplan[0] == True:
        return redirect('/travels')
    else:
        for message in newplan[1]:
            messages.error(request, message)
        return redirect('/travels/add')

def show(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/travels')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'travel_app/show.html', context)

def delete(request, id):
    try:
        target= Travel.objects.get(id=id)
    except Travel.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/travels')
    target.delete()
    return redirect('/travels')

def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"What trip?")
        return redirect('/travels')
    joiner= Travel.objects.join(request.session["id"], travel_id)
    print 80 * ('*'), joiner
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travels')
