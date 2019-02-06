from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import random
import datetime
import time
import tweepy
from tweepy import OAuthHandler
import pickle
import re
from textblob import TextBlob 




from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

def home(request):
	return  render(request,'authenticate/home.html',{})

def login_user(request):
	if request.method == 'POST':	
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(username=username, password=password)
	
		if user is not None:
			login(request,user)
			messages.success(request,('You Have Be Successfully Logged In!'))
			return redirect('home')

    		# A backend authenticated the credentials
		else:
			messages.success(request,('Error In Logging In-Please Try Again'))
			
			return redirect('login')
    		# No backend authenticated the credentials
	else:
		return  render(request,'authenticate/login.html',{})

def logout_user(request):
	logout(request)
	messages.success(request,('Logged-Out Successfully!'))
	return redirect('home')

def register(request):
	if request.method == 'POST':
		form=UserCreationForm(request.POST)
	else:
		form=UserCreationForm()
	context={'form' : form}
	return  render(request,'authenticate/register.html', context)

def datapassing(request):
	username=request.POST['moviename']
	
	consumer_key = 'yoIwFkjZGYDa49aO16XqSNqcN'
	consumer_secret = 'gl4LQOItV7Z1aFwNrlvaiKJ3t8o8h99blMIAmnmdHxYjzjRAxO' 
	access_token = '624310916-E7fDF2IE8P6bfY1oVFglASf6F8RnxMd3vgSXFqnZ'
	access_secret ='ID9JcoXHsDcKtvNcnmBGcCQhUlO0wmwAxBJ6LCesiUAas'

	'''consumer_key = 'zEzzMLu8t2fWgdgYzj2IdaXQF'
	consumer_secret = 'V3MCoZ6R0ykwJdA9cd5kiVg9LPNjDvE8SGZLZ4b4BQYXudncJZ' 
	access_token = '970671991526105090-KZHusqgiW5KvVDaVnWw2eadGvSh1W7x'
	access_secret ='YC4YH6KU0RiS5exvUaVv6karRcFrfaI5E01tMFmmZHdgv'''



	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	args = [username];
	api = tweepy.API(auth,wait_on_rate_limit=True)

	# Fetching the tweets
	list_tweets = []

	query = args[0]
	if len(args) == 1:
		for status in tweepy.Cursor(api.search,q=query+" -filter:retweets",lang='en',result_type='recent',geocode="22.1568,89.4332,500km").items(20):
			list_tweets.append(status.text)

	with open('authenticate/classifier.pickle','rb') as f:
    		classifier = pickle.load(f)
    
	with open('authenticate/tfidfmodel.pickle','rb') as f:
    		tfidf = pickle.load(f)    
    
	total_pos = 0
	total_neg = 0
	total_neutral=0

	for tweet in list_tweets:
    		tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    		tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    		tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", tweet)
    		tweet = tweet.lower()
    		tweet = re.sub(r"that's","that is",tweet)
    		tweet = re.sub(r"there's","there is",tweet)
    		tweet = re.sub(r"what's","what is",tweet)
    		tweet = re.sub(r"where's","where is",tweet)
    		tweet = re.sub(r"it's","it is",tweet)
    		tweet = re.sub(r"who's","who is",tweet)
    		tweet = re.sub(r"i'm","i am",tweet)
    		tweet = re.sub(r"she's","she is",tweet)
    		tweet = re.sub(r"he's","he is",tweet)
    		tweet = re.sub(r"they're","they are",tweet)
    		tweet = re.sub(r"who're","who are",tweet)
    		tweet = re.sub(r"ain't","am not",tweet)
    		tweet = re.sub(r"wouldn't","would not",tweet)
    		tweet = re.sub(r"shouldn't","should not",tweet)
    		tweet = re.sub(r"can't","can not",tweet)
    		tweet = re.sub(r"couldn't","could not",tweet)
    		tweet = re.sub(r"won't","will not",tweet)
    		tweet = re.sub(r"\W"," ",tweet)
    		tweet = re.sub(r"\d"," ",tweet)
    		tweet = re.sub(r"\s+[a-z]\s+"," ",tweet)
    		tweet = re.sub(r"\s+[a-z]$"," ",tweet)
    		tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    		tweet = re.sub(r"\s+"," ",tweet)
    		analysis=TextBlob(tweet)
    		if(analysis.sentiment.polarity>0):
    			total_pos=total_pos+1
    		elif(analysis.sentiment.polarity == 0):
    			total_neutral=total_neutral+1
    		else:
    			total_neg=total_neg+1
    			



	mylist=['brij','charusat','patel']
		
	return  render(request,'authenticate/result.html',{'data':username,'list':list_tweets,'positive':total_pos,'negative':total_neg,'neutral':total_neutral})


def get_data(request):
	data = {
	   "sales": 100,
	   "customers":10,
	} 
	return JsonResponse(data)
