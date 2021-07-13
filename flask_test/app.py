from flask import Flask, render_template, request, jsonify, redirect, session
from flask_wtf import FlaskForm
from wtforms import SelectField

import dash
import dash_core_components as dcc 
from dash.dependencies import Input, Output
import dash_html_components as html 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

class Form(FlaskForm):
    input_1 = SelectField('input1', choices=[(1, 1), (2, 2), (3, 3)])
    input_2 = SelectField('input2', choices=[(4, 4), (5, 5), (6, 6)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    if request.method == "POST":
        session['input_1'] = form.input_1.data
        session['input_2'] = form.input_2.data
        return redirect("/dash/")

    return render_template('index.html', form=form)


dash_app = dash.Dash(
        __name__,
        server=app,
        url_base_pathname='/dash/'
)

dash_app.layout = html.Div(id='dash-container', 
                        children = [
                            html.H1(id = 'main_h1', style={'text-align':'center'}, children = "Test"),
                            dcc.Slider(id = 'slider', min=0, max=20, step=0.5, value=10)
                            ])


@dash_app.callback(
    Output(component_id='main_h1', component_property='children'),
    Input(component_id='slider', component_property='value')
)
def update_h1(slider_data):

    return f"Input 1: {session.get('input_1', None)}\nInput 2: {session.get('input_2', None)}"

if __name__ == '__main__':
    app.run(debug=True)