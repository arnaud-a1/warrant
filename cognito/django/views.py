from django.conf import settings
from django.views.generic import FormView, TemplateView
from braces.views._access import AccessMixin,LoginRequiredMixin
from cognito import Cognito
from cognito.django.forms import ProfileForm


class TokenMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.access_token:
            return self.handle_no_permission(request)

        return super(TokenMixin, self).dispatch(
            request, *args, **kwargs)

class GetUserMixin(object):

    def get_user(self):
        c = Cognito(settings.COGNITO_USER_POOL_ID,
                    settings.COGNITO_APP_ID,
                    access_token=self.request.user.access_token)

class ProfileView(LoginRequiredMixin,TokenMixin,GetUserMixin,TemplateView):
    template_name = 'cognito/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context


class UpdateProfileView(LoginRequiredMixin,TokenMixin,GetUserMixin,FormView):
    template_name = 'cognito/update-profile.html'
    form_class = ProfileForm

    def get_initial(self):

        u = self.get_user()
        return {
            'name':u.name,
            'email':u.email,
            'gender':u.gender,
            'phone':u.phone,
            'address':u.address,
            'preferred_username':u.preferred_username
        }



