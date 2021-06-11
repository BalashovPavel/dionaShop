from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)


class ProductFilterForm(forms.Form):
    ordering = forms.ChoiceField(label="Сортировка", required=False, choices=[
        ["title", "По алфавиту"],
        ["price", "Сначало дешевле"],
        ["-price", "Сначало дороже"],
    ])
