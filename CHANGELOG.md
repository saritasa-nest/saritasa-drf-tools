# Version history

We follow [Semantic Versions](https://semver.org/).

## Unreleased

## 0.3.0

- Confirm support for python 3.14
- Add secondary sorting feature for getting deterministic results in `OrderingFilterBackend` (and `SARITASA_DRF_ORDERING_ADD_PK_TO_ORDERING` setting)
- Add `capture_on_commit` to `ApiActionTester`

## 0.2.2

- Fix warnings in `OrderingFilterBackend`.

## 0.2.1

- Fix order of ordering fields in `OrderingFilterBackend`.

## 0.2.0

- Make `OrderingFilterBackend`/`SearchFilterBackend` show `action` with openapi warnings
- Add `NestedFieldsMixin` for serializers
- Add ability to add extra kwargs for ordering fields in `OrderingFilterBackend`.
Also add new settings `SARITASA_DRF_ORDERING_IS_NULL_FIRST` and `SARITASA_DRF_ORDERING_IS_NULL_LAST`.
- Add ability serialize multiple objects in `ApiActionTester.serialize_data` method via `many=True`.

## 0.1.0

- Beta release
