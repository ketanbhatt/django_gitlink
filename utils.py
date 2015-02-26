from gitlink.models import UserProfile

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        git_user = UserProfile.objects.get(user=user)
        git_user.access = response.get('access_token')
        git_user.github_user_name =  response.get('login')
        git_user.user_github_id = response.get('id')
        git_user.save()
