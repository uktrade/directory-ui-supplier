from django.forms import widgets
from django.utils.html import format_html


class PreventRenderWidget(widgets.Input):
    attrs = {}
    
    def render(name, value, attrs=None):
        return format_html('<!- not rendered ->')

    def value_from_datadict(data, files, name):
        return data.get(name, None)

