from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect

from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Photo,Comment
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})



class MyGallery(LoginRequiredMixin, ListView):
    template_name = 'account/my_gallery.html'

    def get_queryset(self):
        query_set = None
        profile = Profile.objects.get(user = self.request.user)
        profile.clean_photosCount()
        self.extra_context = {'section' : 'gallery', 'count' : profile.photosCount}
        if profile is not None:
            query_set = profile.photo_set.all().order_by('-updated','-timestamp')
        return query_set


class Feed(LoginRequiredMixin, ListView):
    template_name = 'account/feed.html'
    extra_context = {'section' : 'feed', }

    def get_queryset(self):
        photos = Photo.objects.all().order_by('-updated','-timestamp')
        queryset = []
        index = 1
        for pic in photos:
            comments = Comment.objects.all().filter(photo=pic).order_by('-updated')
            queryset.append({'photo' : pic, 'comments' : comments, 'index' : index })
            index = index + 1
        return queryset

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        formData = self.request.POST
        print(formData)
        pic = Photo.objects.get(pk=int(formData['photo_id']))
        c =Comment(user = profile,photo = pic,text=formData['text'])
        c.save()
        return HttpResponseRedirect(reverse_lazy('feed'))






class AddImageView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['name',]
    template_name = 'account/add_image.html'
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = Profile.objects.get(user = self.request.user)
        instance.user.clean_photosCount()
        return super(AddImageView,self).form_valid(form)