from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Review, ReviewImage, Reply
from .forms import ReviewForm, ReviewImageForm, ReplyForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from notifications.views import create_notification

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
            create_notification(type="review", message=f"Добавлен новый отзыв от пользователя {review.reviewer.username}", user_id=user.id)
            
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

            update_user_rating(review.user)
            create_notification(type="review", message=f"Пользователь {review.reviewer.username} изменил свой отзыв на вашей странице", user_id=review.user.id)

            return redirect('/')
    else:
        return render(request, "rating/review_update_form.html", {'form': ReviewForm(instance=review), 'images': images, 'review_image_form': ReviewImageForm()})


class ReviewDeleteView(DeleteView):
    model=Review
    success_url=reverse_lazy("main:index")
    template_name="rating/review_delete_form.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        update_user_rating(self.user)
        create_notification(type="review", message=f"Пользователь {self.reviewer.username} удалил свой отзыв на вашей странице", user_id=self.user.id)
        return response

class ReplyCreateView(CreateView):
    model=Reply
    form_class=ReplyForm
    template_name="rating/reply_create_form.html"

    def post(self, request, pk):

        existing_reply = Reply.objects.filter(review__id=pk).first()
        published_review = get_object_or_404(Review, id=pk)

        if existing_reply :
            return HttpResponse("Вы уже оставили ответ на этот отзыв.<br>Удалите либо измените существующий ответ.", status=400)

        if not published_review.published:
            return HttpResponse("Отзыв еще на модерации.", status=400)

        form = self.get_form()

        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = get_object_or_404(Review, id=pk)
            reply.save()

            create_notification(type="review", message=f"Пользователь {reply.review.user.username} оставил ответ на ваш отзыв", user_id=reply.review.reviewer.id)

            return redirect("main:user_profile", username=request.user.username)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, pk, *args, **kwargs):
        review = get_object_or_404(Review, id=pk)
        if request.user != review.user:
            return HttpResponse("У вас нет права доступа.", status=400) 
        return super().dispatch(request, pk, *args, **kwargs)

class ReplyUpdateView(UpdateView):
    model=Reply
    fields=["text"]
    template_name="rating/reply_update_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:user_profile", kwargs={"username": self.request.user.username})

    def dispatch(self, request, pk, *args, **kwargs):
        reply = get_object_or_404(Reply, id=pk)
        if request.user != reply.review.user:
            return HttpResponse("У вас нет права доступа.", status=400) 
        return super().dispatch(request, pk, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        create_notification(type="review", message=f"Пользователь {self.object.review.user.username} изменил ответ на ваш отзыв", user_id=self.object.review.reviewer.id)
        return response


class ReplyDeleteView(DeleteView):
    model=Reply
    template_name="rating/reply_delete_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:user_profile", kwargs={"username": self.request.user.username})

    def dispatch(self, request, pk, *args, **kwargs):
        reply = get_object_or_404(Reply, id=pk)
        if request.user != reply.review.user:
            return HttpResponse("У вас нет права доступа.", status=400) 
        return super().dispatch(request, pk, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        create_notification(type="review", message=f"Пользователь {self.object.review.user.username} удалил ответ на ваш отзыв", user_id=self.object.review.reviewer.id)
        return response