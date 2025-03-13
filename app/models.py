import json
from django.db import models


class EquationModel(models.Model):
    name = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    eps = models.FloatField()
    results = models.JSONField(null=True, default=None)

    def __str__(self):
        if self.results is not None:
            results_data = json.loads(self.results)
            intervals = list(results_data.keys())
            roots = list(results_data.values())
            return f"{self.name}: f(x) = {self.function}, eps = {self.eps}, intervals: {intervals}, results: {roots}"
        else:
            return f"{self.name}: f(x) = {self.function}, eps = {self.eps}. Results are not calculated yet."
