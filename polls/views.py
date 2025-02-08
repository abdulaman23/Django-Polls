from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from . models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404



def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    context = {

        "latest_question_list":latest_question_list,
    }

    return render(request, "polls/index.html", context)

    ''' if len(output)>0:
        return (HttpResponse(output))
    return (HttpResponse("No Questions present in the database at the moment"))'''
   
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Quesion does not exist")
    return render(request,"polls/detail.html",{"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})

def vote(request, question_id):

    question =  get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["Choice"])
    except (KeyError, Choice.DoesNotExist):   
        return render(request, "polls/detail.html",{"question":question,"error_message":"You did not select a choice",},)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# Create your views here.
