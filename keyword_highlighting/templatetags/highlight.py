from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def highlight_yellow(text, value):
    if text is not None and value != "":
        ori_text = str(text)
        lowered_text = ori_text.lower()
        ori_value = value
        lowered_value = ori_value.lower()

        offset = 0
        if x := re.finditer(lowered_value, lowered_text):
            for occurence in x:
                ori_text = (
                    ori_text[: occurence.start() + offset]
                    + f'<span class="highlight">{ori_text[occurence.start() + offset: occurence.end() + offset]}</span>'
                    + ori_text[occurence.end() + offset :]
                )
                offset += 31
        str_replaced = ori_text
    else:
        str_replaced = text

    return mark_safe(str_replaced)
