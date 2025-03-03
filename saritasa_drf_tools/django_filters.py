from django import forms
from django.template import loader
from django_filters import rest_framework


class DjangoFilterBackend(rest_framework.DjangoFilterBackend):
    """Customized DjangoFilterBackend to reduce queries count."""

    def to_html(
        self,
        request,  # noqa: ANN001
        queryset,  # noqa: ANN001
        view,  # noqa: ANN001
    ) -> str | None:
        """Convert ModelChoiceField's widget to TextInput."""
        filterset: rest_framework.FilterSet | None = self.get_filterset(
            request=request,
            queryset=queryset,
            view=view,
        )
        if filterset is None:
            return None

        form: forms.Form = filterset.form
        for field in form.fields.values():
            if isinstance(field, forms.ModelChoiceField):
                field.widget = forms.TextInput()
        template = loader.get_template(template_name=self.template)
        context = {
            "filter": filterset,
        }
        return template.render(context, request)
