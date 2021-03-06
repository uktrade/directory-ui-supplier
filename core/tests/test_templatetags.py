from django.template import Context, Template


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


def test_first_paragraph():
    template = Template(
        '{% load first_paragraph from cms_tags %}'
        '{{ html|first_paragraph|safe }}'

    )
    context = Context({
        'html': '<p>The first paragraph</p><p></p>'
    })
    html = template.render(context)

    assert html == '<p>The first paragraph</p>'


def test_grouper():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 10)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '        <li>6</li>'
        '    </ul>'
        '<ul>'
        '        <li>7</li>'
        '        <li>8</li>'
        '        <li>9</li>'
        '    </ul>'
    )


def test_grouper_remainder():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 6)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '    </ul>'
    )


def test_add_href_target(rf):
    request = rf.get('/', HTTP_HOST='www.example.com')
    template = Template(
        '{% load add_href_target from cms_tags %}'
        '{{ html|add_href_target:request|safe }}'

    )
    context = Context({
        'request': request,
        'html': (
            '<a href="http://www.google.com"></a>'
            '<a href="https://www.google.com"></a>'
            '<a href="http://www.example.com"></a>'
            '<a href="https://www.example.com"></a>'
        )
    })
    html = template.render(context)

    assert html == (
        '<a href="http://www.google.com" target="_blank"></a>'
        '<a href="https://www.google.com" target="_blank"></a>'
        '<a href="http://www.example.com"></a>'
        '<a href="https://www.example.com"></a>'
    )
