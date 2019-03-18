from django.core.files.base import ContentFile
from requests import request, ConnectionError
from lememe.models import UserProfile


def save_profile(backend, user, response, is_new, *args, **kwargs):
    """
    Get the user avatar (and any other details you're interested in)
    and save them to the userprofile
    """

    profile = UserProfile.objects.get_or_create(user=user,)[0]

    if backend.name == 'google-oauth2':
        if response.get('picture'):

            # split using "/" and get last character because the value for 'picture'
            # is something like this: https://lh6.googleusercontent.com/.../photo.jpg
            filename = response.get('picture').split("/")[-1]
            if profile.picture:
                # if existing avatar stick with it rather than google syncing
                pass
            else:
                try:
                    response = request('GET', response.get('picture'))
                    response.raise_for_status()
                except ConnectionError:
                    pass
                else:
                    # No avatar so sync it with the google one.
                    profile.picture.save(name=filename,
                                         content=ContentFile(response.content),
                                         save=False
                                         )
                    profile.save()

    elif backend.name == 'github':
        if response.get('avatar_url'):

            # split using "/" and get last character because the value for 'picture'
            # is something like this: https://lh6.googleusercontent.com/.../photo.jpg
            filename = response.get('avatar_url').split("/")[-1]
            if profile.picture:
                # if existing avatar stick with it rather than google syncing
                pass
            else:
                try:
                    response = request('GET', response.get('avatar_url'))
                    response.raise_for_status()
                except ConnectionError:
                    pass
                else:
                    # No avatar so sync it with the google one.
                    profile.picture.save(name=filename,
                                         content=ContentFile(response.content),
                                         save=False
                                         )
                    profile.save()


    # elif backend.name == 'facebook':  # and is_new:
    #     prof = user.userprofile
    #     if prof.avatar:
    #         pass
    #     else:
    #         url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    #
    #         try:
    #             response = request('GET', url, params={'type': 'large'})
    #             response.raise_for_status()
    #         except ConnectionError:
    #             pass
    #         else:
    #             prof.avatar.save(u'',
    #                              ContentFile(response.content),
    #                              save=False
    #                              )
    #             prof.save()
