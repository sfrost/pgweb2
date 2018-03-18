import json

from django import forms
from django.utils.http import urlencode

from . import Thing, ThingLookup
from ..compat import urlparse
from ..forms import widgets
from .base import BaseSelectableTestCase, parsed_inputs, parsed_widget_attributes

__all__ = (
    'AutoCompleteWidgetTestCase',
    'AutoCompleteSelectWidgetTestCase',
    'AutoComboboxWidgetTestCase',
    'AutoComboboxSelectWidgetTestCase',
    'AutoCompleteSelectMultipleWidgetTestCase',
    'AutoComboboxSelectMultipleWidgetTestCase',
)


class WidgetTestMixin(object):
    widget_cls = None
    lookup_cls = None

    def get_widget_instance(self, **kwargs):
        return self.__class__.widget_cls(self.__class__.lookup_cls, **kwargs)

    def test_init(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.lookup_class, self.__class__.lookup_cls)

    def test_dotted_path(self):
        """
        Ensure lookup_class can be imported from a dotted path.
        """
        dotted_path = '.'.join([self.__class__.lookup_cls.__module__, self.__class__.lookup_cls.__name__])
        widget = self.__class__.widget_cls(dotted_path)
        self.assertEqual(widget.lookup_class, self.__class__.lookup_cls)

    def test_invalid_dotted_path(self):
        """
        An invalid lookup_class dotted path should raise an ImportError.
        """
        with self.assertRaises(ImportError):
            self.__class__.widget_cls('that.is.an.invalid.path')

    def test_dotted_path_wrong_type(self):
        """
        lookup_class must be a subclass of LookupBase.
        """
        dotted_path = 'selectable.forms.widgets.AutoCompleteWidget'
        with self.assertRaises(TypeError):
            self.__class__.widget_cls(dotted_path)


class AutoCompleteWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoCompleteWidget
    lookup_cls = ThingLookup

    def test_rendered_attrs(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget)
        self.assertTrue('data-selectable-url' in attrs)
        self.assertTrue('data-selectable-type' in attrs)
        self.assertTrue('data-selectable-allow-new' in attrs)

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget)
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))


class AutoCompleteSelectWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoCompleteSelectWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoCompleteWidget)

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, forms.HiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[1])
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden')

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))

    def test_postdata_compatible_with_select(self):
        "Checks postdata for values that a select widget would generate."
        postdata = {'fruit': '1'}
        widget = self.get_widget_instance()
        widget_val = widget.value_from_datadict(postdata, [], 'fruit')
        self.assertEqual(widget_val, '1')


class AutoComboboxWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoComboboxWidget
    lookup_cls = ThingLookup

    def test_rendered_attrs(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget)
        self.assertTrue('data-selectable-url' in attrs)
        self.assertTrue('data-selectable-type' in attrs)
        self.assertTrue('data-selectable-allow-new' in attrs)

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget)
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget)
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))


class AutoComboboxSelectWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoComboboxSelectWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoComboboxWidget)

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, forms.HiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[1])
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden')

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))


class AutoCompleteSelectMultipleWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoCompleteSelectMultipleWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoCompleteWidget)

    def test_multiple_attr(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-multiple' in attrs)
        self.assertEqual(attrs['data-selectable-multiple'], 'true')

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, widgets.LookupMultipleHiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[1])
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden-multiple')

    def test_render_single(self):
        widget = self.get_widget_instance()
        val = 4
        rendered_value = widget.render('field_name', val)
        inputs = parsed_inputs(rendered_value)
        field = inputs['field_name_1'][0]
        self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
        self.assertEqual(field.attributes['type'].value, 'hidden')
        self.assertEqual(int(field.attributes['value'].value), val)

    def test_render_list(self):
        widget = self.get_widget_instance()
        list_val = [8, 5]
        rendered_value = widget.render('field_name', list_val)
        inputs = parsed_inputs(rendered_value)
        found_values = []
        for field in inputs['field_name_1']:
            self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
            self.assertEqual(field.attributes['type'].value, 'hidden')
            found_values.append(int(field.attributes['value'].value))
        self.assertListEqual(found_values, list_val)

    def test_render_qs(self):
        widget = self.get_widget_instance()
        t1 = self.create_thing()
        t2 = self.create_thing()
        qs_val = Thing.objects.filter(pk__in=[t1.pk, t2.pk])
        rendered_value = widget.render('field_name', qs_val)
        inputs = parsed_inputs(rendered_value)
        found_values = []
        found_titles = []
        for field in inputs['field_name_1']:
            self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
            self.assertEqual(field.attributes['type'].value, 'hidden')
            found_titles.append(field.attributes['title'].value)
            found_values.append(field.attributes['value'].value)
        self.assertListEqual(found_values, [str(t1.pk), str(t2.pk)])
        self.assertListEqual(found_titles, [t1.name, t2.name])

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))


class AutoComboboxSelectMultipleWidgetTestCase(BaseSelectableTestCase, WidgetTestMixin):
    widget_cls = widgets.AutoComboboxSelectMultipleWidget
    lookup_cls = ThingLookup

    def test_has_complete_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[0].__class__, widgets.AutoComboboxWidget)

    def test_multiple_attr(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-multiple' in attrs)
        self.assertEqual(attrs['data-selectable-multiple'], 'true')

    def test_has_hidden_widget(self):
        widget = self.get_widget_instance()
        self.assertEqual(widget.widgets[1].__class__, widgets.LookupMultipleHiddenInput)

    def test_hidden_type(self):
        widget = self.get_widget_instance()
        attrs = parsed_widget_attributes(widget.widgets[1])
        self.assertTrue('data-selectable-type' in attrs)
        self.assertEqual(attrs['data-selectable-type'], 'hidden-multiple')

    def test_render_single(self):
        widget = self.get_widget_instance()
        val = 4
        rendered_value = widget.render('field_name', val)
        inputs = parsed_inputs(rendered_value)
        field = inputs['field_name_1'][0]
        self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
        self.assertEqual(field.attributes['type'].value, 'hidden')
        self.assertEqual(field.attributes['value'].value, str(val))

    def test_render_list(self):
        widget = self.get_widget_instance()
        list_val = [8, 5]
        rendered_value = widget.render('field_name', list_val)
        inputs = parsed_inputs(rendered_value)
        found_values = []
        for field in inputs['field_name_1']:
            self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
            self.assertEqual(field.attributes['type'].value, 'hidden')
            found_values.append(int(field.attributes['value'].value))
        self.assertListEqual(found_values, list_val)

    def test_render_qs(self):
        widget = self.get_widget_instance()
        t1 = self.create_thing()
        t2 = self.create_thing()
        qs_val = Thing.objects.filter(pk__in=[t1.pk, t2.pk])
        rendered_value = widget.render('field_name', qs_val)
        inputs = parsed_inputs(rendered_value)
        found_values = []
        for field in inputs['field_name_1']:
            self.assertEqual(field.attributes['data-selectable-type'].value, 'hidden-multiple')
            self.assertEqual(field.attributes['type'].value, 'hidden')
            found_values.append(int(field.attributes['value'].value))
        self.assertListEqual(found_values, [t1.pk, t2.pk])

    def test_update_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance()
        widget.update_query_parameters(params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_limit_parameter(self):
        widget = self.get_widget_instance(limit=10)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertTrue('limit=10' in query)

    def test_initial_query_parameters(self):
        params = {'active': 1}
        widget = self.get_widget_instance(query_params=params)
        attrs = parsed_widget_attributes(widget.widgets[0])
        url = attrs['data-selectable-url']
        parse = urlparse(url)
        query = parse.query
        self.assertEqual(query, urlencode(params))

    def test_build_selectable_options(self):
        "Serialize selectable options as json in data attribute."
        options = {'autoFocus': True}
        widget = self.get_widget_instance(attrs={'data-selectable-options': options})
        attrs = parsed_widget_attributes(widget.widgets[0])
        self.assertTrue('data-selectable-options' in attrs)
        self.assertEqual(attrs['data-selectable-options'], json.dumps(options))
