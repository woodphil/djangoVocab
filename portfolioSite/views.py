from django.shortcuts import render
from django.http import HttpResponse

from django.template import RequestContext, loader

# Create your views here.
def index(request):
	#template = loader.get_template('portfolioSite/index.html')
	#return HttpResponse(template.render())
	#return HttpResponse('blah');
	return render(request, 'portfolioSite/base_main.html');
	
def resume(request):
	return render(request, 'portfolioSite/base_resume.html');
	
def projects(request):
	return render(request, 'portfolioSite/base_projects.html');
	
def contact(request):
	return render(request, 'portfolioSite/base_contact.html');