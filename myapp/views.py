from django.views.generic import ListView, DetailView
from .models import Question, Answer
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import QuestionForm
from .forms import AnswerForm 
from .forms import SignUpForm

class QuestionListView(ListView):
    model = Question
    template_name = 'myapp/question_list.html'
    context_object_name = 'questions'
    ordering = ['-created_at']

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'myapp/question_detail.html'
    context_object_name = 'question'

@method_decorator(login_required, name='dispatch')
class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'myapp/question_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
    
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('myapp:question_detail', pk=pk)
    else:
        form = AnswerForm()
    
    return render(request, 'myapp/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後、自動でログインさせる
            return redirect('/')  # 登録後に遷移したいURL名に変更
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})