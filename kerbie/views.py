from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import comment, post, userProfile, addImage
from forms import search_form, user_form, user_profile_form, addImage_form, post_form, comment_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def search(request):
	searched = False
	profiles = {}
	numProfiles = 0
	userId = 0
	n = ''
	if request.method == 'POST':
		form = search_form(request.POST)
		if form.is_valid():
			n = form.cleaned_data.get('name')
			all_profiles = userProfile.objects.all()
			profiles = all_profiles.filter(username=n)
			if len(profiles) != 0:
				numProfiles = len(profiles)
			searched = True
			request.session['from_method'] = 'search'
			request.session['search_for'] = n
		else:
			print form.errors
	else:
		form = search_form()
	return render(request, 'kerbie/search.html', {'form': form, 'username':n, 'searched':searched, 'numProfiles': numProfiles})
	
#def search(request, 

def index(request):
	#if request.session.get('last_visit'):
	#	last_visit_time = request.session.get('last_visit')
	#	request.session['last_visit'] = str(datetime.now())
	#else:
	#	request.session['last_visit'] = str(datetime.now())
	return render(request, 'kerbie/index.html', {})


def search_matches(request, u):
	return render(request, 'kerbie/search_results.html', {'users': u})

def register(request):
	registered = False
	users = userProfile.objects.all()
	counter = len(users)
	
	if request.method == 'POST':
		uform = user_form(request.POST)
		pform = user_profile_form(request.POST)
		
		if uform.is_valid() and pform.is_valid():
			counter += 1
			user = uform.save()
			user.set_password(user.password) #hashes the password
			user.save()
			profile = pform.save(commit=False)
			profile.user = user
			profile.userId = counter
			profile.joined = datetime.datetime.now()
			profile.username = user.get_username()
			profile.location = pform.cleaned_data.get('location')
			request.session['from_method'] = 'register'
			request.session['username'] = profile.username

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			profile.save()
			registered = True
				
		else:
			print uform.errors, pform.errors
			
	else:
		uform = user_form()
		pform = user_profile_form()
	
	return render(request, 'kerbie/register.html', {'user_form': uform, 'profile_form': pform, 'registered': registered})

def user_login(request):
	username = ""
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['username'] = username
				request.session['from_method'] = 'login'
				request.session['current_pro'] = username
				return HttpResponseRedirect('/kerbie/')
				
			else:
				return HttpResponse("Your account is inactive.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Uh oh! Watch out for typos!")
	else:
		return render(request, 'kerbie/login.html', {})

@login_required
def restricted(request):
	return HttpResponse("You are logged in. Woot!")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/kerbie/')
	
@login_required
def profile(request):
	is_user = False
	if request.session.get('search_for'):
		name = request.session.get('search_for')
		request.session['current_pro'] = name
		request.session['search_for'] = None
		request.session['from_method'] = 'profile'
	else:
		if request.session.get('current_pro') == request.session.get('username'):
			is_user = True
			name = request.session.get('username')
		else:
			name = request.session.get('current_pro')
	u = userProfile.objects.get(username=name)
	posts = post.objects.all()
	counter = len(posts)
	all_comments = comment.objects.all()
	if request.method == 'POST':
		form = post_form(request.POST)
		if form.is_valid():
			counter += 1
			newpost = form.save(commit=False)
			newpost.username = request.session.get('username') #username of the person posting
			newpost.user_wall = name #username of the wall being posted to
			newpost.date = datetime.datetime.now()
			newpost.messageId=counter
			newpost.save()
		else:
			print form.errors
	else:
		form = post_form()
	if u.photoId != 0:
		picture = addImage.objects.get(photoId=u.photoId)
	else:
		picture = None
	user_posts = posts.filter(user_wall=request.session.get('current_pro'))
	details = {'user_profile':name, 'location':u.location, 'picture': picture, 'joined':u.joined, 'birthday':u.birthday, 'current_pro':name,  'username':request.session.get('username'), 'posts':user_posts}
	if is_user:
		print "to user profile"
		return render(request, 'kerbie/user_profile.html', details)
	else:
		print "to other profile"
		return render(request, 'kerbie/profile.html', details)
		
def user_profile(request):
	request.session['current_pro']=request.session.get('username')
	print "user_profile current_pro: " + request.session.get('current_pro')
	return profile(request)
	
def get_posts(profile):
	posts = []
	posts += post.objects.filter(user_wall=profile)
	return posts

def comments(request, post_id):
	print 'comments'
	all_comments = comment.objects.all()
	main_post = post.objects.get(messageId=post_id)
	post_comments = comment.objects.filter(messageId=post_id)
	counter = len(all_comments)
	print 'counter= ' + str(counter)
	if request.method == 'POST':
		print 'if post comments'
		form = comment_form(request.POST)
		if form.is_valid():
			print 'form is valid comments'
			counter += 1
			newcomment = form.save(commit=False)
			newcomment.username = request.session.get('username')
			newcomment.messageId = post_id
			newcomment.date = datetime.datetime.now()
			newcomment.commentId = counter
			newcomment.save()
			print len(comment.objects.all())
		else:
			print "fml"+str(form.errors)
	else:
		print 'comment GET'
		form = comment_form()
	return render(request, 'kerbie/comment.html', {'post':main_post, 'comments':post_comments})
			
	
@login_required
def pictures(request):
	is_username = False
	user_profile = request.session.get('current_pro')
	username = request.session.get('username')
	user = userProfile.objects.get(username=user_profile)
	userId = user.userId
	if request.GET.get('setpic'):
		photoId = request.GET.get('profile_picture')
		print photoId
		user = userProfile.objects.get(username=request.session.get('username'))
		user.photoId=photoId
		print user.photoId+" " +user.username
		user.save()
	if username == user_profile:
		is_username = True
	pictures = addImage.objects.filter(userId__startswith=userId)
	return render(request, 'kerbie/pictures.html', {'pictures':pictures, 'user_profile':user_profile, 'is_user':is_username})
	
@login_required
def add_pictures(request):
	photos = addImage.objects.all()
	counter = len(photos)
	username = request.session.get('username')
	user = userProfile.objects.get(username=username)
	if request.method == 'POST':
		form = addImage_form(request.POST or None, request.FILES or None)
		if form.is_valid():
			counter += 1
			newpic = form.save(commit=False)
			newpic.userId = user.userId
			newpic.image = request.FILES['image']
			newpic.date = datetime.datetime.now()
			newpic.photoId = counter
			newpic.save()
		else:
			print form.errors
	else:
		form = addImage_form()
	
	return render(request, 'kerbie/add_pictures.html', {'form':form})#{'photos': photos, 'form':form})
	
	
	
	
	
	
	
	
