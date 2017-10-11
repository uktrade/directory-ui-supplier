from django.forms import widgets
from django.utils.html import format_html, mark_safe


class PreventRenderWidget(widgets.Input):
    # template_name = 'widgets/prevent_render.html'
    attrs = {}

    def render(self, name, value, attrs=None, renderer=None):
        return format_html('<!- not rendered ->')


class CheckboxWithInlineLabel(widgets.CheckboxInput):
    template = """
        <div class="form-field checkbox">
            {input_html}
            <label for="{id}">{label}</label>
        </div>
    """

    def __init__(self, label='', *args, **kwargs):
        self.label = label
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input_html = super().render(name, value, attrs)
        wrapper_html = self.template.format(
            input_html=input_html, label=self.label, id=attrs['id']
        )
        return mark_safe(wrapper_html)


class CheckboxSelectInlineLabelMultiple(widgets.CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_multiple_input.html'
    option_template_name = 'widgets/checkbox_input_option.html'
    css_class_name = 'form-field checkbox multi'

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs['class'] = self.attrs.get('class', self.css_class_name)
