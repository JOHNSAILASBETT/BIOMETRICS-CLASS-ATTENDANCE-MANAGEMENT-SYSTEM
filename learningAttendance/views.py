from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .models import School, Department, Unit, Course # RegisterSubjects
from django.views.generic import (TemplateView, DetailView,
                                  ListView, FormView, CreateView, UpdateView, DeleteView)
# from .forms import CommentForm, LessonForm, ReplyForm, SubjectRegisterForm  # SubjectRegisterForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class SchoolsListView(ListView):
    context_object_name = 'schools'
    model = School
    template_name = "school_list_view.html"


class DepartmentsListView(DetailView):
    context_object_name = 'schools'
    model = School
    template_name = "department_list_view.html"


    # def get_context_data(self, **kwargs):
    #     context = super(DepartmentListView, self).get_context_data(**kwargs)
    #     if self.user.is_student:
    #         for subjects_available in self.standard.subjects.all:
    #             if self.user.semester == self.subject.semester and self.user.year == self.subject.year:
    #                 context = {
    #                     'subjects_available': subjects_available
    #                 }
    #             else:
    #                 return HttpResponse("You are not legible to register units please visit Admin or your lecturer")
    #     return self, 'subject_list_view.html', context


# to get the lessons of a subject we will use detailview of that subject
class CoursesListView(DetailView):
    context_object_name = 'departments'
    model = Department
    template_name = "courses_list_view.html"

class UnitsListView(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = "units_list_view.html"

class LecturesListView(DetailView):
    context_object_name = 'units'
    model = Unit
    template_name = "lectures_list_view.html"
"""
# to get the chapters of a lesson we will use detailview of that lesson
class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = "lesson_detail_view.html"

    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print('Comment form is returned')
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            print('Reply form is returned')
            return self.form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail', kwargs={'standard': standard.slug,
                                                                'subject': subject.slug,
                                                                'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'subject'
    model = Subject
    template_name = "lesson_create.html"

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('lesson_list', kwargs={'standard': standard.slug,
                                                   'slug': self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonUpdateView(UpdateView):
    fields = ('name', 'position', 'video', 'ppt', 'notes')
    model = Lesson
    template_name = 'lesson_update.html'
    context_object_name = 'lessons'


class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_list', kwargs={'standard': standard.slug, 'slug': subject.slug})


# to get the chapters of a lesson we will use detail view of that lesson
class SubjectRegisterView(DetailView, FormView):
    context_object_name = 'subjects'
    model = Standard
    template_name = "attendance_register/subject_to_register.html"

    form_class = SubjectRegisterForm

    def get_context_data(self, **kwargs):
        context = super(SubjectRegisterView, self).get_context_data(**kwargs)
        if self.user.is_student:
            for subjects_available in self.standard.subject.all:
                if self.user.semester == self.subject.semester and self.user.year == self.subject.year:
                    context = {
                        'subjects_available': subjects_available
                    }
                else:
                    return HttpResponse("You are not legible to register units please visit Admin or your lecturer")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'subjects_available' in request.POST:
            form_class = self.get_form_class()
            form_name = 'subjects_available'

        form = self.get_form(form_class)

        if form_name == 'subjects_available' and form.is_valid():
            return self.form_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail', kwargs={'standard': standard.slug,
                                                                'subject': subject.slug,
                                                                'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.student = self.request.user
        fm.subject_name = self.object.subject.name
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
"""