from example.app import api


def test_nested_fields_generation():
    """Check that nested data fields are correctly generated."""
    fields = api.serializers.TestModelDetailSerializer().get_fields()
    assert isinstance(
        fields["related_model_data"],
        api.serializers.RelatedTestModelSerializer,
    )
    assert fields["related_model_data"].read_only
    assert (
        fields["related_model_data"].allow_null
        == fields["related_model"].allow_null
    )
    fields = api.serializers.RelatedTestModelWithManyRelatedSerializer().get_fields()  # noqa: E501
    assert fields["test_models_data"].read_only
    assert fields["test_models_data"].many
