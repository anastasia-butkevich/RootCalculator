import json
import sympy as sp
import numpy as np


x = sp.symbols("x")


def root_intervals(func: sp.Expr) -> list[tuple]:
    """
    Identify intervals where the function may have a root by detecting sign changes between critical points.

    Args:
        func (sp.Expr): The function as a Sympy expression.

    Returns:
        list[tuple]: A list of intervals (a, b) where the function changes sign.

    Raises:
        TypeError: if the function is not a valid Sympy expression.
    """
    if not isinstance(func, sp.Basic):
        raise TypeError("Function must be a Sympy expression.")

    f_diff = sp.diff(func, x)
    try:
        crit_points = [p.evalf() for p in sp.nroots(f_diff) if p.is_real]
    except Exception:
        crit_points = []
    crit_points = sorted(set(crit_points))
    if not crit_points:
        return []
 
    crit_points = [-sp.oo] + crit_points + [sp.oo]
    intervals = []
    f_num = sp.lambdify(x, func, "numpy")
    
    for i in range(len(crit_points) - 1):
        a, b = crit_points[i], crit_points[i + 1]
        if a == -sp.oo:
            try:
                a = find_finite_bound(func, b, direction=-1)
            except Exception:
                continue
        if b == sp.oo:
            try:
                b = find_finite_bound(func, a, direction=1)
            except Exception:
                continue
        try:
            if f_num(a) * f_num(b) < 0:
                intervals.append((a, b))
        except Exception:
            continue
    return intervals


def find_finite_bound(func: sp.Expr, start: float, direction: int, max_iter: int = 1000) -> float:
    """
    Find a finite bound from a given start in the specified direction where the function's sign changes.

    Args:
        func (sp.Expr): The function as a Sympy expression.
        start (float): Starting point for the search.
        direction (int): Search direction (1 for increasing, -1 for decreasing).
        max_iter (int): Maximum iterations to search.

    Returns:
        float: A finite bound where a sign change relative to the start is detected.

    Raises:
        ValueError: If no sign change is found within max_iter steps.
    """
    f_num = sp.lambdify(x, func, "numpy")
    f_start = f_num(start)
    current = start
    for _ in range(max_iter):
        current += direction
        f_current = f_num(current)
        if f_start * f_current < 0:
            return current
    raise ValueError("Could not find a valid finite bound with sign change.")


def bisection(func, interval: tuple, eps: float, max_iter=1000) -> float:
    """
    Find a root of `func` in the given interval using the bisection method.

    Args:
        func (sp.Expr): A sympy expression representing the function.
        interval (tuple): A tuple (a, b) such that func(a)*func(b) < 0.
        eps (float): Precision for convergence.
        max_iter (int): Maximum number of iterations.

    Returns:
        float: The approximate root.

    Raises:
        ValueError: If func(a) and func(b) do not have opposite signs.
    """
    a, b = interval
    f_num = sp.lambdify(x, func, "numpy")
    f_a, f_b = f_num(a), f_num(b)

    if f_a * f_b > 0:
        raise ValueError("The function must have opposite signs at the endpoints.")

    for _ in range(max_iter):
        mid = (a + b) / 2.0
        f_mid = f_num(mid)
        if abs(f_mid) < eps or abs(b - a) < 2 * eps:
            return mid
        if f_mid * f_a < 0:
            b, f_b = mid, f_mid
        else:
            a, f_a = mid, f_mid

    raise RuntimeError("Bisection method did not converge.")


def newton(func, interval: tuple, eps: float, max_iter=1000) -> float:
    """
    Use Newton's method to find a root of `func` within the specified interval.

    Args:
        func (sp.Expr): A sympy expression representing the function.
        interval (tuple): A tuple (a, b) to confine the search.
        eps (float): Precision for convergence.
        max_iter (int): Maximum number of iterations.

    Returns:
        float: The approximate root.

    Raises:
        ZeroDivisionError: If the derivative becomes too small.
        ValueError: If the iterates leave the given interval.
    """
    f_num = sp.lambdify(x, func, "numpy")
    f_diff_num = sp.lambdify(x, sp.diff(func, x), "numpy")
    
    a, b = interval
    guess = (a + b) / 2.0

    for _ in range(max_iter):
        f_val = f_num(guess)
        f_diff_val = f_diff_num(guess)
        if abs(f_val) < eps:
            return guess
        if abs(f_diff_val) < eps:
            raise ZeroDivisionError("Derivative too small; Newton's method fails.")
        guess_new = guess - f_val / f_diff_val
        if not (a <= guess_new <= b):
            raise ValueError("Newton's method went out of bounds.")
        guess = guess_new

    raise RuntimeError("Newton's method did not converge.")


def calculate(func, eps):
    """
    Calculate roots for intervals where `func` changes sign using Newton's and the bisection methods.

    This function first determines candidate intervals (using a sign-change detection strategy)
    and then applies both root-finding methods on each interval.

    Args:
        func (sp.Expr): The sympy expression for the function.
        tol (float): Tolerance for root convergence.

    Returns:
        dict: A dictionary mapping each interval (as a string) to a tuple (newton_root, bisection_root).
    """
    intervals = root_intervals(func)
    results = {}
    
    for interval in intervals:
        try:
            res1 = newton(func, interval, eps)
        except Exception as e:
            res1 = str(e)
        
        try:
            res2 = bisection(func, interval, eps)
        except Exception as e:
            res2 = str(e)
        
        results[str(interval)] = (res1, res2)
    
    return results
