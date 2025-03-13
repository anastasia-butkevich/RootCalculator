import json
import re

import sympy as sp

from django.shortcuts import render, redirect
from .models import EquationModel
from . import calculations as calc
from .forms import InputForm
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "app/index.html")


def from_db(request):
    entries_names = EquationModel.objects.values_list("name", flat=True)
    return render(request, "app/from_db.html", {"entries_names": entries_names})


def manual(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("from_db")
    else:
        form = InputForm()
    return render(request, "app/manual.html", {"form": form})


def results(request):
    if request.method == "POST":
        selected_name = request.POST.get("selected_name")

        if not selected_name:
            messages.error(request, "Please select an entry from a dropdown.")
            return redirect("from_db")

        equation = EquationModel.objects.get(name=selected_name)
        if equation.results is None:
            f = sp.sympify(equation.function)
            equation.results = calc.calculate(f, equation.eps)

            equation.save()

        f = sp.sympify(equation.function)

        func_latex_html = sp.latex(f)

        func_latex_desmos = func_latex_html.replace("^", "^")
        func_latex_desmos = re.sub(
            r"(\w+)\^(\{[\d]+\}|\d+)", r"\1^{\2}", func_latex_desmos
        )

        res = json.loads(equation.results)

        return render(
            request,
            "app/results.html",
            {
                "name": equation.name,
                "function_latex_html": f"\\({func_latex_html}\\)",
                "function_latex_desmos": func_latex_desmos,
                "results": res,
            },
        )
    return redirect("index")
