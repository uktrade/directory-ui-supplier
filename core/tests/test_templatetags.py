from django.template import Context, Template


def test_add_anchors():
    template = Template(
        '{% load add_anchors from cms_tags %}'
        '{{ html|add_anchors|safe }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_table_of_contents():
    template = Template(
        '{% load table_of_contents from cms_tags %}'
        '{% for anchor, label in html|table_of_contents %}'
        '    <a href="#{{ anchor }}">{{ label }}</a>'
        '{% endfor %}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '    <a href="#title-one-section">Title one</a>'
        '    <a href="#title-two-section">Title two</a>'
    )
