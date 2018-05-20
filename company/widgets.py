from django.core.validators import EMPTY_VALUES
from django.forms import widgets
from django.utils.html import format_html


class PreventRenderWidget(widgets.Input):
    # template_name = 'widgets/prevent_render.html'
    attrs = {}

    def render(self, name, value, attrs=None, renderer=None):
        return format_html('<!- not rendered ->')


class CheckboxSelectInlineLabelMultiple(widgets.CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_multiple_input.html'
    option_template_name = 'widgets/checkbox_input_option.html'
    css_class_name = 'form-field checkbox multi'

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs['class'] = self.attrs.get('class', self.css_class_name)


class CheckboxSelectMultipleIgnoreEmpty(CheckboxSelectInlineLabelMultiple):

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        if values:
            return [value for value in values if value not in EMPTY_VALUES]
