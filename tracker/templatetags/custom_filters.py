import decimal

from django import template

register = template.Library()


@register.filter
def persianize_digits(value):
    if isinstance(value, (int, float, decimal.Decimal)):
        value = str(value)
    if not isinstance(value, str):
        return value
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"
    translation_table = str.maketrans(english_digits, persian_digits)
    return value.translate(translation_table)

@register.filter
def progress_percentage(weekly_hours, target_weekly_hours):
    try:
        percentage = (float(weekly_hours) / float(target_weekly_hours)) * 100
        return min(100, round(percentage))
    except (ValueError, ZeroDivisionError):
        return 0
