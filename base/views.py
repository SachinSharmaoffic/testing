from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Question, Comment
from users.models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.
def home(request):
    return render(request, "home.html")


# crud function

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Question
from users.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def home(request):
    return render(request, "home.html")


# crud function
class QuestionListView(ListView):
    model = Question

    context_object_name = "questions"
    ordering = ["-date_created"]
    paginate_by = 2  # Number of questions per page

    def get_queryset(self):
        # Get the queryset for the questions
        questions = super().get_queryset()
        # Prefetch the related Profile objects to avoid N+1 queries
        questions = questions.select_related("user__profile")
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Paginate the questions queryset
        questions = self.get_queryset()
        paginator = Paginator(questions, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        context["questions"] = questions
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'base/question_detail.html'  # Use your question detail template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object  # Get the question object from the view
        comments = Comment.objects.filter(question=question).select_related('user__profile')
        comment_form = CommentForm()  # Create a new instance of the comment form
        # context['comments'] = comments
        # context['comment_form'] = comment_form
        
        upvotes = question.upvotes.count()
        downvotes = question.downvotes.count()
        difference = upvotes - downvotes

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['upvotes'] = upvotes
        context['downvotes'] = downvotes
        context['difference'] = difference
        return context

    def post(self, request, *args, **kwargs):
        question = self.get_object()  # Get the question object
        comment_form = CommentForm(request.POST)  # Bind the form data to the CommentForm

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = self.request.user
            comment.question = question
            comment.save()
        

            # Redirect to the same page after a successful comment submission
            return HttpResponseRedirect(self.request.path_info)

        # If the form is not valid, re-render the question detail page with errors
        context = self.get_context_data(**kwargs)
        context['comment_form'] = comment_form
        return self.render_to_response(context)

class QuestionCreateView(CreateView):
    model = Question
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    model = Question
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False


class QuestionDeleteView(UserPassesTestMixin, DeleteView):
    model = Question
    success_url = "/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False

# class CommentDetailView(CreateView):
class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'base/comment_form.html'  # Use your custom HTML template


    def form_valid(self, form):
        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        form.instance.question = question
        form.instance.user = self.request.user
        form.save()
        return redirect('base:question_detail', slug=self.kwargs['slug'])


def upvote_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.user in question.downvotes.all():
        question.downvotes.remove(request.user)
    if request.user not in question.upvotes.all():
        question.upvotes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

def downvote_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.user in question.upvotes.all():
        question.upvotes.remove(request.user)
    if request.user not in question.downvotes.all():
        question.downvotes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
