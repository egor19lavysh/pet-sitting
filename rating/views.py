from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Review, ReviewImage
from .forms import ReviewForm, ReviewImageForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

def update_user_rating(user):
    reviews = Review.objects.filter(user=user).values_list('score')
    total = sum(item[0] for item in reviews)
    quantity = len(reviews)

    user.rating = total/quantity
    user.save()

class ReviewCreateView(CreateView):
    model = Review
    template_name = "rating/review_form.html"
    form_class = ReviewForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = ReviewImageForm()
        return context
    
    def post(self, request, user_id, *args, **kwargs):
        form = self.get_form()
        image_form = ReviewImageForm(request.POST, request.FILES)
        user = get_object_or_404(User, id=user_id)

        if form.is_valid() and image_form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.user = user
            review.save()

            for img in request.FILES.getlist("images"):
                ReviewImage(image=img, review=review).save()
            
            update_user_rating(user)
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def review_update_view(request, pk):
    review = get_object_or_404(Review, id=pk)
    images = ReviewImage.objects.filter(review=review)
    print(images)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        review_image_form = ReviewImageForm(request.POST, request.FILES)
        if review_form.is_valid() and review_image_form.is_valid():

            review = review_form.save()

            for image in images:
                if request.POST.get(str(image)):
                    image.delete()

            for img in request.FILES.getlist("images"):
                ReviewImage(image=img, review=review).save()

            return redirect('/')
    else:
        return render(request, "rating/review_update_form.html", {'form': ReviewForm(instance=review), 'images': images, 'review_image_form': ReviewImageForm()})


class ReviewDeleteView(DeleteView):
    model=Review
    success_url=reverse_lazy("main:index")
    template_name="rating/review_delete_form.html"

