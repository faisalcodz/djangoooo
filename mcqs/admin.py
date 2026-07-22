from django.contrib import admin

from .models import MCQOption, MCQQuestion


class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 4
    max_num = 4
    min_num = 4


class MCQQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [MCQOptionInline]
    list_display = ["question_text", "pub_date"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        options = obj.mcqoption_set.all()
        correct_count = options.filter(is_correct=True).count()
        if correct_count != 1:
            if correct_count == 0:
                from django.contrib import messages

                messages.warning(
                    request,
                    f'Question "{obj.question_text}" has no correct option selected. Please mark exactly one option as correct.',
                )
            elif correct_count > 1:
                from django.contrib import messages

                messages.warning(
                    request,
                    f'Question "{obj.question_text}" has {correct_count} correct options. Please mark exactly one option as correct.',
                )


admin.site.register(MCQQuestion, MCQQuestionAdmin)
