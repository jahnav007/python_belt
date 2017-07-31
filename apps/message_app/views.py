from django.shortcuts import render, redirect
from .models import User, Quote, Fav
from django.contrib import messages
from django.db.models import Count

def quotes(request):
    if not 'loggedUser' in request.session:
        return redirect ('/')
    else:
        quotes=Quote.quoteManager.all().annotate(num_fav=Count('fav_quote'))
        user=User.userManager.all()

        context= {
        "user": user,
        "quotes":quotes,
        }
        return render (request, 'message_app/quotes.html', context)

def sub_quote(request):
    if not 'loggedUser' in request.session:
        return redirect ('/')
    else:
        user= Quote.quoteManager.postquote(request.POST["quoted_by"], request.session["loggedUserID"], request.POST['text'] )
        if user[0] == False:
            for error in user[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/quotes')
        else:
            "all goood"
            return redirect ('/quotes')


def add_fav(request, quoteID):
    if not 'loggedUser' in request.session:
        return redirect ('/')
    else:
        favs= Fav.favManager.fav(request.session["loggedUserID"], quoteID)
        if favs[0] == False:
            messages.add_message(request, messages.ERROR, favs[1])
            return redirect('/quotes')
        else:
            print favs
            return redirect('/quotes')

def delete_fav(request, quoteID):
    if not 'loggedUser' in request.session:
        return redirect ('/')
    else:
        Fav.favManager.delete(quoteID)
        return redirect('/quotes')

def indv_user(request, userID):
    if not 'loggedUser' in request.session:
        return redirect ('/')
    else:
        indv_user=userID

        quotes=Quote.quoteManager.filter(user_id= indv_user).annotate(num=Count('text'))
        poster =User.userManager.filter(id= indv_user)
        user=User.userManager.all()

        context= {
        "user": user,
        "quotes":quotes,
        "poster": poster
        }
        return render (request,'message_app/users.html', context )
