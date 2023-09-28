from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.home, name="home"),
    #    crud
    path("questions/", views.QuestionListView.as_view(), name="question_list"),
    path("questions/new/", views.QuestionCreateView.as_view(), name="question_create"),
    path(
        "questions/<slug:slug>/",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    path(
        "questions/<slug:slug>/update/",
        views.QuestionUpdateView.as_view(),
        name="question_update",
    ),
    path(
        "questions/<slug:slug>/delete/",
        views.QuestionDeleteView.as_view(),
        name="question_delete",
    ),
    path("questions/<slug:slug>/upvote/", views.upvote_question, name="upvote_question"),
    path("questions/<slug:slug>/downvote/", views.downvote_question, name="downvote_question"),

]
