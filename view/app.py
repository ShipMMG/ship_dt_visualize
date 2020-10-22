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

    ship_type = request.form.get('ship_type', 'ship')
    ship_box_real_color = request.form.get('ship_box_real_color', '0XFF00FF')
    ship_box_virtual_color = request.form.get('ship_box_virtual_color', '0XDCF8FF')
    animation_speed = request.form.get('animation_speed', 1.0)
    init_camera_position_x = request.form.get('init_camera_position_x', 0.0)
    init_camera_position_y = request.form.get('init_camera_position_y', 0.0)
    init_camera_position_z = request.form.get('init_camera_position_z', 15.0)
    init_camera_look_at_x = request.form.get('init_camera_look_at_x', 0.0)
    init_camera_look_at_y = request.form.get('init_camera_look_at_y', 0.0)
    init_camera_look_at_z = request.form.get('init_camera_look_at_z', 0.0)
    grid_visualizing = request.form.get('grid_visualizing', 'off')
    grid_helper_size = request.form.get('grid_helper_size', 100.0)
    grid_helper_step = request.form.get('grid_helper_step', 100.0)
    axis_visualizing = request.form.get('axis_visualizing', 'off')
    axis_length = request.form.get('axis_length', 1000.0)
    water_visualizing = request.form.get('water_visualizing', 'off')
    sun_color = request.form.get('sun_color', '0xffffff')
    water_color = request.form.get('water_color', '0x334B3F')
    sky_visualizing = request.form.get('sky_visualizing', 'off')

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
        ship_type=ship_type,
        ship_box_real_color=ship_box_real_color, ship_box_virtual_color=ship_box_virtual_color,
        animation_speed=animation_speed,
        init_camera_position_x=init_camera_position_x,
        init_camera_position_y=init_camera_position_y,
        init_camera_position_z=init_camera_position_z,
        init_camera_look_at_x=init_camera_look_at_x,
        init_camera_look_at_y=init_camera_look_at_y,
        init_camera_look_at_z=init_camera_look_at_z,
        grid_visualizing=grid_visualizing, grid_helper_size=grid_helper_size, grid_helper_step=grid_helper_step,
        axis_visualizing=axis_visualizing, axis_length=axis_length,
        water_visualizing=water_visualizing, sun_color=sun_color, water_color=water_color,
        sky_visualizing=sky_visualizing,
    )


if __name__ == "__main__":
    app.run(debug=True)
