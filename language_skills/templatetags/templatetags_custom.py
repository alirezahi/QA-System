from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_answer(context, id):
    if 'answers' in context:
        answers = context['answers']
        return answers.objects.filter(order=id).last()
    return ''


@register.simple_tag
def question_format(format_string):
    format_string = format_string.replace('/&&__question__&&/', '**')
    return format_string
