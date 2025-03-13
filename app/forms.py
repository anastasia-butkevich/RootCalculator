from .models import EquationModel
from django.core.exceptions import ValidationError
from django import forms
from sympy import sympify, symbols
from sympy.core.sympify import SympifyError


from django import forms
from django.core.exceptions import ValidationError
from app.models import EquationModel
from sympy import sympify, symbols
from sympy.core.sympify import SympifyError


class InputForm(forms.ModelForm):
    class Meta:
        model = EquationModel
        fields = ["name", "function", "eps"]
        labels = {"name": "Name", "function": "Polynomial", "eps": "Precision"}
        widgets = {
            "eps": forms.NumberInput(attrs={"step": "0.0001", "min": "0", "max": "1"})
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.Meta.model.objects.filter(name=name).exists():
            raise ValidationError("This name already exists in the database.")
        return name

    def clean_eps(self):
        eps = self.cleaned_data.get("eps")
        if eps < 0 or eps > 1:
            raise ValidationError("Precision must take a value from 0 to 1.")
        return eps

    def clean_function(self):
        function_str = self.cleaned_data.get("function")

        if "," in function_str:
            raise ValidationError("Function should use dots, not commas.")

        try:
            expr = sympify(function_str)
        except SympifyError:
            raise ValidationError(
                "Function is not a valid expression. Please read the instructions."
            )

        variables = expr.free_symbols
        if variables != {symbols("x")}:
            raise ValidationError("Function should only contain the variable 'x'.")

        if not expr.is_polynomial():
            raise ValidationError("Function must be a polynomial only.")

        return function_str
