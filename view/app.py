#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import pandas as pd
from werkzeug.datastructures import FileStorage

app = Flask(__name__)  # Flask setting

ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    title = "Ship Digital Twin Visualization"
    return render_template('index.html', title=title)  # rendering 'index.html'


@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    title = 'Visualize'
    L = request.form.get('L', 2.1)
    B = request.form.get('B', 0.3)
    d = request.form.get('d', 0.1)

    ship_real_color = request.form.get('ship_real_color', '0XFF00FF')
    ship_virtual_color = request.form.get('ship_virtual_color', '0XDCF8FF')
    animation_speed = request.form.get('animation_speed', 1.0)
    init_camera_position_x = request.form.get('init_camera_position_x', 0.0)
    init_camera_position_y = request.form.get('init_camera_position_y', 0.0)
    init_camera_position_z = request.form.get('init_camera_position_z', 15.0)
    init_camera_look_at_x = request.form.get('init_camera_look_at_x', 0.0)
    init_camera_look_at_y = request.form.get('init_camera_look_at_y', 0.0)
    init_camera_look_at_z = request.form.get('init_camera_look_at_z', 0.0)
    grid_helper_size = request.form.get('grid_helper_size', 100.0)
    grid_helper_step = request.form.get('grid_helper_step', 100.0)

    send_data = request.files['send_data']
    if isinstance(send_data, FileStorage) and send_data.content_type == 'text/csv':
        df = pd.read_csv(send_data)
        num_of_ships = int((len(list(df.columns)) - 1) / 3)
        print(num_of_ships)

        time = df['TIME']
        ship_results = []
        for number in range(num_of_ships):
            ship = df[['psi' + str(number), 'x' + str(number), 'y' + str(number)]].values.tolist()
            ship_results.append(ship)

    else:
        raise ValueError('File type is not CSV')

    return render_template(
        'visualize.html',
        title=title,
        time=time,
        ship_results=ship_results,
        L=L, B=B, d=d,
        ship_real_color=ship_real_color, ship_virtual_color=ship_virtual_color,
        animation_speed=animation_speed,
        init_camera_position_x=init_camera_position_x,
        init_camera_position_y=init_camera_position_y,
        init_camera_position_z=init_camera_position_z,
        init_camera_look_at_x=init_camera_look_at_x,
        init_camera_look_at_y=init_camera_look_at_y,
        init_camera_look_at_z=init_camera_look_at_z,
        grid_helper_size=grid_helper_size, grid_helper_step=grid_helper_step,
    )


if __name__ == "__main__":
    app.run(debug=True)
