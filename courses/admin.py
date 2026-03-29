from django.contrib import admin
from .models import (
    Course, Enrollment, Module, Lesson, Question, QuestionOption,
    Quiz, QuizQuestion, StudentProgress, QuizAttempt, StudentAnswer,
    Turma, PresenceSession, PresenceRecord
)


# ============================================================================
# INLINE ADMIN CLASSES
# ============================================================================

class ModuleInline(admin.TabularInline):
    """Inline for modules in course admin."""
    model = Module
    extra = 1
    fields = ['title', 'order', 'is_published']
    ordering = ['order']


class LessonInline(admin.TabularInline):
    """Inline for lessons in module admin."""
    model = Lesson
    extra = 1
    fields = ['title', 'duration_minutes', 'order', 'is_published']
    ordering = ['order']


class QuizInline(admin.TabularInline):
    """Inline for quizzes in module admin."""
    model = Quiz
    extra = 0
    fields = ['title', 'passing_score', 'max_attempts', 'order', 'is_published']
    ordering = ['order']


class QuestionOptionInline(admin.TabularInline):
    """Inline for question options."""
    model = QuestionOption
    extra = 4
    fields = ['option_text', 'is_correct', 'order']
    ordering = ['order']


class QuizQuestionInline(admin.TabularInline):
    """Inline for quiz questions."""
    model = QuizQuestion
    extra = 1
    fields = ['question', 'order']
    ordering = ['order']
    autocomplete_fields = ['question']


class StudentAnswerInline(admin.TabularInline):
    """Inline for student answers in quiz attempt."""
    model = StudentAnswer
    extra = 0
    fields = ['question', 'selected_option', 'text_answer', 'is_correct', 'points_earned']
    readonly_fields = ['question', 'selected_option', 'text_answer', 'is_correct', 'points_earned']
    can_delete = False


# ============================================================================
# MODEL ADMIN CLASSES
# ============================================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin for Course model."""
    list_display = ['name', 'price', 'is_active', 'created_at', 'module_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'image_url')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def module_count(self, obj):
        """Display number of modules."""
        return obj.modules.count()
    module_count.short_description = 'Modules'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin for Enrollment model."""
    list_display = ['user', 'course', 'source', 'acquired_at']
    list_filter = ['source', 'acquired_at']
    search_fields = ['user__email', 'course__name']
    readonly_fields = ['acquired_at']
    autocomplete_fields = ['user', 'course']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin for Module model."""
    list_display = ['title', 'course', 'order', 'is_published', 'lesson_count', 'quiz_count']
    list_filter = ['is_published', 'course']
    search_fields = ['title', 'description', 'course__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline, QuizInline]
    autocomplete_fields = ['course']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
    
    def lesson_count(self, obj):
        """Display number of lessons."""
        return obj.lessons.count()
    lesson_count.short_description = 'Lessons'
    
    def quiz_count(self, obj):
        """Display number of quizzes."""
        return obj.quizzes.count()
    quiz_count.short_description = 'Quizzes'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin for Lesson model."""
    list_display = ['title', 'module', 'order', 'duration_minutes', 'is_published']
    list_filter = ['is_published', 'module__course']
    search_fields = ['title', 'content', 'module__title']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['module']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('module', 'title', 'content', 'order')
        }),
        ('Media', {
            'fields': ('video_url', 'duration_minutes'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
    
    class Media:
        css = {
            'all': ('https://cdn.ckeditor.com/4.20.1/standard/ckeditor.css',)
        }
        js = (
            'https://cdn.ckeditor.com/4.20.1/standard/ckeditor.js',
            'https://cdn.ckeditor.com/4.20.1/standard/adapters/jquery.js',
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin for Question model."""
    list_display = ['question_preview', 'course', 'question_type', 'points', 'created_at']
    list_filter = ['question_type', 'course', 'created_at']
    search_fields = ['question_text', 'course__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionOptionInline]
    autocomplete_fields = ['course']
    
    fieldsets = (
        ('Question Details', {
            'fields': ('course', 'question_text', 'question_type', 'points')
        }),
        ('Feedback', {
            'fields': ('explanation',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        """Display shortened question text."""
        return obj.question_text[:60] + '...' if len(obj.question_text) > 60 else obj.question_text
    question_preview.short_description = 'Question'


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """Admin for QuestionOption model."""
    list_display = ['option_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct']
    search_fields = ['option_text', 'question__question_text']
    autocomplete_fields = ['question']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin for Quiz model."""
    list_display = ['title', 'module', 'passing_score', 'max_attempts', 'order', 'is_published', 'question_count']
    list_filter = ['is_published', 'module__course']
    search_fields = ['title', 'description', 'module__title']
    readonly_fields = ['created_at', 'updated_at', 'total_points']
    inlines = [QuizQuestionInline]
    autocomplete_fields = ['module']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('module', 'title', 'description', 'order')
        }),
        ('Quiz Settings', {
            'fields': ('passing_score', 'max_attempts', 'time_limit_minutes')
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at', 'total_points')
        }),
    )
    
    def question_count(self, obj):
        """Display number of questions."""
        return obj.quiz_questions.count()
    question_count.short_description = 'Questions'


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    """Admin for QuizQuestion model."""
    list_display = ['quiz', 'question', 'order']
    list_filter = ['quiz__module__course']
    search_fields = ['quiz__title', 'question__question_text']
    autocomplete_fields = ['quiz', 'question']


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    """Admin for StudentProgress model."""
    list_display = ['user', 'get_item', 'completed', 'score', 'completed_at']
    list_filter = ['completed', 'completed_at']
    search_fields = ['user__email', 'lesson__title', 'quiz__title']
    readonly_fields = ['completed_at']
    autocomplete_fields = ['user', 'lesson', 'quiz']
    
    def get_item(self, obj):
        """Display lesson or quiz."""
        return obj.lesson or obj.quiz
    get_item.short_description = 'Item'


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin for QuizAttempt model."""
    list_display = ['user', 'quiz', 'attempt_number', 'score', 'passed', 'started_at', 'submitted_at']
    list_filter = ['passed', 'started_at', 'quiz__module__course']
    search_fields = ['user__email', 'quiz__title']
    readonly_fields = ['started_at', 'submitted_at']
    inlines = [StudentAnswerInline]
    autocomplete_fields = ['user', 'quiz']
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('user', 'quiz', 'attempt_number')
        }),
        ('Results', {
            'fields': ('score', 'passed')
        }),
        ('Timing', {
            'fields': ('started_at', 'submitted_at')
        }),
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    """Admin for StudentAnswer model."""
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'attempt__quiz__module__course']
    search_fields = ['attempt__user__email', 'question__question_text']
    readonly_fields = ['attempt', 'question', 'selected_option', 'text_answer', 'is_correct', 'points_earned']
    autocomplete_fields = ['attempt', 'question']


# ============================================================================
# TURMA / PRESENCE CONTROL ADMIN
# ============================================================================

class PresenceSessionInline(admin.TabularInline):
    """Inline for presence sessions within a turma."""
    model = PresenceSession
    extra = 0
    fields = ['date', 'is_open', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-date']


class PresenceRecordInline(admin.TabularInline):
    """Inline for presence records within a session."""
    model = PresenceRecord
    extra = 0
    fields = ['student', 'registered_at']
    readonly_fields = ['student', 'registered_at']
    can_delete = False


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    """Admin for Turma model."""
    list_display = ['name', 'professor', 'student_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'professor__email']
    readonly_fields = ['created_at']
    filter_horizontal = ['students']
    autocomplete_fields = ['professor']
    inlines = [PresenceSessionInline]

    fieldsets = (
        ('Informações da Turma', {
            'fields': ('name', 'professor', 'is_active', 'created_at')
        }),
        ('Alunos', {
            'fields': ('students',),
        }),
    )

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Alunos'


@admin.register(PresenceSession)
class PresenceSessionAdmin(admin.ModelAdmin):
    """Admin for PresenceSession model."""
    list_display = ['turma', 'date', 'is_open', 'present_count', 'created_at']
    list_filter = ['is_open', 'date']
    search_fields = ['turma__name']
    readonly_fields = ['created_at']
    autocomplete_fields = ['turma']
    inlines = [PresenceRecordInline]

    fieldsets = (
        ('Sessão', {
            'fields': ('turma', 'date', 'is_open', 'created_at')
        }),
    )

    def present_count(self, obj):
        return obj.records.count()
    present_count.short_description = 'Presenças'


@admin.register(PresenceRecord)
class PresenceRecordAdmin(admin.ModelAdmin):
    """Admin for PresenceRecord model."""
    list_display = ['student', 'session', 'registered_at']
    list_filter = ['registered_at']
    search_fields = ['student__email', 'session__turma__name']
    readonly_fields = ['registered_at']
    autocomplete_fields = ['session', 'student']

