import warnings
import math
import numpy as np
import sympy as sp
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource, TextInput, RadioButtonGroup, Div, Toggle, Legend
from bokeh.plotting import curdoc, figure

curdoc().theme = 'caliber'
conversion_list = ['^   = **', 
           'e^x = exp(x)', 
           '√   = sqrt()',
           'arcsin = asin',
           'Everything else is intuitive...',
           'Be aware of centering ln/log @ 0 as the derivative is infinity',
           'The error area graphs for any form of ln/log are weird']

format_widget = '<a>Formatting Guide:</a><ul>{}</ul>'.format(''.join(f'<li>{item}</li>' for item in conversion_list))

title = Div(text='<h1 style="font-family: Times">Taylor Polynomial Visualizer</h1>')
list_text = Div(text=format_widget)
a_text = Div(text="The center value (a) will be in terms of...")
step_size_radio = RadioButtonGroup(labels = ["Integers", "Pi Approximations"], active = 0, width=240)
equation_input = TextInput(title="Enter the equation you want to use (default is sin(x)):", value = "")
equation_output = Div(text=r"$$\sin{\left(x \right)}\approx$$")
link = Div(text='<span>Made by </span><a href="https://www.linkedin.com/in/naren-manikandan/" target="_blank">Naren Manikandan</a><span>. Check out the code </span><a href="https://github.com/Naren219/taylor-webapp" target="_blank">here</a><span>')

h_size_int = 10
pi_step = 1.571
h_size_pi = pi_step * 4
int_step = 1
current_step = int_step

x = np.linspace(-h_size_int, h_size_int, 500)
a_marker = np.zeros_like(x)

x_sp = sp.Symbol('x')
y_sp = sp.sin(x_sp)

y_np = sp.lambdify(x_sp, y_sp, modules="numpy")
y = y_np(x)

def taylor2latex(f, n, a):
    if a == 0:
        taylor_series = f.series(n=n+1).removeO()
    else:
        taylor_series = f.series(x_sp, a, n+1).removeO()
    return sp.latex(taylor_series)
def get_coeff(y_sp, a, n=0):
    rev_y = taylor2latex(y_sp, n, a)
    rev_y = '{' + rev_y + '}'
    equation_output.text = '$$' + sp.latex(y_sp) + r'\approx' + rev_y + '$$'
    for _ in range(n):
        y_sp = sp.diff(y_sp, x_sp)
    deriv_sp = y_sp.subs(x_sp, a)
    deriv_np = sp.lambdify(x_sp, deriv_sp, 'numpy')
    deriv = deriv_np(a)
    return deriv * np.power(x - a, n) / math.factorial(n)

y_init = get_coeff(y_sp, 0)

source = ColumnDataSource(data=dict(x=x, y=y))
taylor_coords = ColumnDataSource(data=dict(x=x, y=y_init))
marker_source = ColumnDataSource(data=dict(x=a_marker, y=x))
ROC_source_left = ColumnDataSource(data=dict(x=a_marker-np.ones_like(a_marker), y=x))
ROC_source_right = ColumnDataSource(data=dict(x=a_marker+np.ones_like(a_marker), y=x))

plot = figure(title="Graph with Taylor Polynomial Approximation", y_range=(-10, 10), width=500, height=500)
plot.aspect_ratio = 1.2
plot.line('x', 'y', source=source, line_width=3, line_alpha=1)
plot.line('x', 'y', source=taylor_coords, line_width=3, line_alpha=0.6, line_color="purple")
plot.line('x', 'y', source=marker_source, line_width=3, line_color="gold", line_dash="dashed")
l_b = plot.line('x', 'y', source=ROC_source_left, line_width=3, line_color="orange", line_dash="dotted", legend_label="Left Bound")
r_b = plot.line('x', 'y', source=ROC_source_right, line_width=3, line_color="orange", line_dash="solid", line_alpha=0.3, legend_label="Right Bound")
area_plot = plot.varea(x=x, y1=y_init, y2=y, fill_alpha=0.4)

l_b.visible, r_b.visible = False, False
plot.legend.background_fill_color = "white"
plot.legend.background_fill_alpha = 0.5
ROC_bool = False

a_slider = Slider(title="Choose a Center Value (a)", start=-h_size_int, end=h_size_int, step=int_step, value=0, width=500)
deg_input = Slider(title="Degree of the Taylor Polynomial", start=0, end=20, step=1, value=0)
toggle_ROC = Toggle(label='Toggle Radius of Convergence Lines', button_type='default', active=True, width=240)
toggle_error = Toggle(label='Toggle Error Area', button_type='default', active=True, width=240)

def get_ROC(expr):
    global l_b, r_b, ROC_bool
    if expr == sp.ln(x_sp+1) or expr == sp.ln(1+x_sp) or expr == 1/(1-x_sp):
        ROC_bool = True
        l_b.visible, r_b.visible = True, True
        ROC_source_left.data = { 'x' : np.full_like(x, a_slider.value-1), 'y' : x}
        ROC_source_right.data = { 'x' : np.full_like(x, a_slider.value+1), 'y' : x}
    else:
        ROC_bool = False
        l_b.visible, r_b.visible = False, False
def update_view(attr, old, new):
    global l_b, r_b
    selectedValue = a_slider.value

    newStart = selectedValue - h_size_int
    newEnd = selectedValue + h_size_int

    plot.x_range.start = newStart
    plot.x_range.end = newEnd

    marker_source.data = { 'x': np.full_like(x, a_slider.value), 'y' : x }
    get_ROC(y_sp)
def compute_error(x, y1, y2):
    global area_plot, ROC_bool
    area_plot.data_source.data['x'] = np.linspace(a_slider.value, h_size_int, 500) if ROC_bool else x
    area_plot.data_source.data['y1'] = y1
    area_plot.data_source.data['y2'] = y2
def compute_taylor(attr, old, new):
    global y
    degree = int(deg_input.value)
    new_y = np.zeros_like(x)
    for n in range(degree + 1):
        val = get_coeff(y_sp, a_slider.value, n)
        new_y = np.add(new_y, val, out=new_y, casting="unsafe")
    taylor_coords.data = { 'x': x, 'y': new_y }
    compute_error(x, new_y, y)
def choose_step_size(attr, old, new):
    a_slider.value = 0
    if (new == 1):
        a_slider.step = pi_step
        a_slider.start = -h_size_pi
        a_slider.end = h_size_pi
    else:
        a_slider.step = int_step
        a_slider.start = -h_size_int
        a_slider.end = h_size_int
def set_equation(attr, old, new):
    global x_sp
    global y_sp
    global source
    global y
    global l_b, r_b

    y_sp = sp.sympify(new)
    new_np = sp.lambdify(x_sp, y_sp, 'numpy')

    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            new_eq = new_np(x)
        except RuntimeWarning:
            print("RuntimeWarning occurred!")
            y_sp = sp.Pow(x_sp, 2)
            new_np = sp.lambdify(x_sp, y_sp, 'numpy')
            new_eq = new_np(x)
        finally:
            warnings.resetwarnings()

    y = new_eq
    source.data = {'x': x, 'y': new_eq}
    y_init = get_coeff(y_sp, a_slider.value)
    taylor_coords.data = {'x': x, 'y': y_init}
    get_ROC(y_sp)
    compute_error(x, y_init, new_eq)
    if l_b is None and r_b is None:
        l_b.visible, r_b.visible = False, False
def toggle_ROC_lines(attr, old, new):
    if l_b is not None and r_b is not None:
      if ROC_bool:
        l_b.visible = toggle_ROC.active
        r_b.visible = toggle_ROC.active
def toggle_error_CB(attr, old, new):
    area_plot.visible = toggle_error.active

equation_input.on_change('value', set_equation)
a_slider.on_change('value', update_view)
deg_input.on_change('value', compute_taylor)
step_size_radio.on_change('active', choose_step_size)
toggle_ROC.on_change('active', toggle_ROC_lines)
toggle_error.on_change('active', toggle_error_CB)

layout = column(title, list_text, equation_input, plot, equation_output, toggle_ROC, toggle_error, a_text, step_size_radio, a_slider, deg_input, link)
curdoc().add_root(layout)