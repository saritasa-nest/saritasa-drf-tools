# Version history

We follow [Semantic Versions](https://semver.org/).

## Unreleased

## 0.2.0

- Make `OrderingFilterBackend`/`SearchFilterBackend` show `action` with openapi warnings
- Add `NestedFieldsMixin` for serializers
- Add ability to add extra kwargs for ordering fields in `OrderingFilterBackend`.
Also add new settings `SARITASA_DRF_ORDERING_IS_NULL_FIRST` and `SARITASA_DRF_ORDERING_IS_NULL_LAST`.
- Add ability serialize multiple objects in `ApiActionTester.serialize_data` method via `many=True`.

## 0.1.0

- Beta release
