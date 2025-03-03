from example.app import api


def test_custom_fields__override():
    """Check that custom field will be used instead of CharField."""
    fields = api.serializers.TestModelDetailSerializer().get_fields()
    assert isinstance(fields["text_field"], api.fields.CustomCharField)
