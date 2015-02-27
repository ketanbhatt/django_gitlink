from django.shortcuts import render
from gitlink.forms import UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from github import Github
from gitlink.models import UserProfile, Payload
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def gitlink(request):
    if request.user.is_authenticated():
        curr_user = UserProfile.objects.get(user = request.user)

        return render(request, 'gitlink/gitlink.html', {'github_linked' : curr_user.github_user_name, 'repo_selected' : curr_user.selected_repo})

    return render(request, 'gitlink/gitlink.html', {})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('gitlink'))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return HttpResponseRedirect(reverse('login'))

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'gitlink/register.html',
            {'user_form': user_form, 'profile_form': profile_form} )


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('gitlink'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('gitlink'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'gitlink/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('gitlink'))


@login_required
def sel_repo(request):
    if request.method == 'POST':
        selected_repo = request.POST['repo']
        curr_user = UserProfile.objects.get(user = request.user)
        curr_user.selected_repo = selected_repo
        curr_user.save()

        curr_user = UserProfile.objects.get(user = request.user)
        import pycurl, json
        github_url = 'https://api.github.com/repos/'+ curr_user.github_user_name + '/' + curr_user.selected_repo + '/hooks'
        data = json.dumps({"name": "web",  "active": "true",  "events": [    "push",    "pull_request"  ],  "config": {    "url": "http://gitlink.herokuapp.com/payload/",    "content_type": "json"  }})

        c = pycurl.Curl()
        c.setopt(pycurl.URL, github_url)
        c.setopt(pycurl.HTTPHEADER, ['Authorization: token ' + curr_user.access ,'Content-Type: application/json'])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.perform()

        return HttpResponseRedirect(reverse('gitlink'))

    else:
        curr_user = Github(UserProfile.objects.get(user = request.user).access)
        repos = curr_user.get_user().get_repos()

        return render(request, 'gitlink/sel_repo.html', {'repos' : repos})


from django.views.generic import View

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('This is GET request')
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('payload'))


@csrf_exempt
def payload(request):
    import json
    js = json.loads(request.body)
    uid = js['sender']['login']

    if 'pull_request' in js:
        message = js['pull_request']['title']
        url = js['pull_request']['url']

    else:
        message = js['commits'][0]['message']
        url = js['commits'][0]['url']

    payload = Payload.objects.get_or_create(for_user = UserProfile.objects.get(github_user_name=uid), message=message, url=url)

    return render(request, 'gitlink/payload.html', {})

@login_required
def view_payloads(request):
    user = UserProfile.objects.get(user = request.user)
    payloads = Payload.objects.filter(for_user=user)

    return render(request, 'gitlink/view_payloads.html', {'payloads' : payloads})
