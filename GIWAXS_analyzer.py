import tkinter as tk
from tkinter import filedialog
import os
import pygix
import fabio
import numpy as np
import matplotlib.pyplot as plt
import PIL


"""Globals that the setup window will alter and then get deleted after use"""
sample_orientation_g = -1
incident_angle_g = -1.
cal_path_g = ''
data_path_g = ''


def main():
    Setup_Window().mainloop()

    pg = load_calibration()
    data = load_data()

    PIL.Image.fromarray(data).save('test.png')

    return data
    # line cuts and Plotting
    '''plt.rcParams.update({'mathtext.default':  'regular'})
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['text.usetex'] = False

    # this produces the line cuts using pygix
    i_oop, q = pg.profile_sector(data, npt=1000, chi_pos=0, chi_width=30,
                                 radial_range=(0, 2.5), unit='q_A^-1', correctSolidAngle=False, method="bbox")
    i_ip, q = pg.profile_sector(data, npt=1000, chi_pos=78, chi_width=10,
                                radial_range=(0, 2.5), unit='q_A^-1', correctSolidAngle=False, method="bbox")'''


def load_calibration():
    global cal_path_g, sample_orientation_g, incident_angle_g
    pg = pygix.Transform()
    pg.load(cal_path_g)
    pg.sample_orientation = sample_orientation_g
    pg.incident_angle = incident_angle_g
    print(pg)
    pg.title_angle = 0
    del sample_orientation_g
    del incident_angle_g
    del cal_path_g
    return pg


def load_data():
    global data_path_g
    data = fabio.open(data_path_g).data
    del data_path_g
    return data

def get_file(ftype='tif', init_dir=os.getcwd()):
    """Opens dialog box to get location of desired file"""
    if not ftype.lower() in ['tif', 'poni']:
        raise ValueError('invalid filetype to retrieve')
    filename = filedialog.askopenfilename(initialdir=init_dir, title=f'Select {ftype.upper()}',
                                          filetypes=((f'{ftype.upper()}', f'*.{ftype.lower()}',), ('all', '*.*')))
    return filename


class Setup_Window(tk.Tk):
    FONT_SIZE = 10
    FONT = 'Arial'
    default_angle = '0.12'      # degrees
    default_calibration_path = os.getcwd() + os.sep + 'calibrations'
    default_calibration_fname = 'cal.poni'
    default_data_path = os.getcwd() + os.sep + 'raw_data'
    default_data_fname = 'TT5mm-01-benzeneTPP_60min.tif'

    def __init__(self):
        """Set up Window"""

        tk.Tk.__init__(self)
        self.title('Setup')

        """Create and place labels"""
        columns = 3

        r = 0

        """Title Line"""
        tk.Label(self, text='Set up analysis',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r,
                                                                        column=0,
                                                                        columnspan=columns,
                                                                        sticky=tk.W)

        r += 1

        """Sample orientation"""
        tk.Label(self, text='Sample Orientation',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=0, sticky=tk.W)

        self.orientation_selection = tk.IntVar(self)

        self.orientation_selection.set(1)

        tk.Radiobutton(self, text='Horizontal', variable=self.orientation_selection, value=1,
                       font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=1)
        tk.Radiobutton(self, text='Vertical', variable=self.orientation_selection, value=2,
                       font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=2)

        tk.Label(self, text='                                                                  ',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=3, sticky=tk.W)

        r += 1

        """Incident Angle"""
        tk.Label(self, text='Incident Angle [\u00B0]',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=0, sticky=tk.W)
        self.angle_entry = tk.Entry(self, font=(Setup_Window.FONT, Setup_Window.FONT_SIZE))
        self.angle_entry.grid(row=r, column=1, columnspan=2, sticky=tk.E + tk.W)
        self.angle_entry.insert(0, Setup_Window.default_angle)

        r += 1

        """Calibration location"""

        tk.Label(self, text='Calibration',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=0, sticky=tk.W)
        self.calibration_path_entry = tk.Entry(self, font=(Setup_Window.FONT, Setup_Window.FONT_SIZE))
        self.calibration_path_entry.grid(row=r, column=1, columnspan=3, sticky=tk.E + tk.W)

        calibration_path = Setup_Window.default_calibration_path + os.sep + Setup_Window.default_calibration_fname
        self.calibration_path_entry.insert(0, calibration_path)

        tk.Button(self, text='...', font=(Setup_Window.FONT, Setup_Window.FONT_SIZE),
                  command=self.open_cal).grid(row=r, column=4, sticky=tk.E + tk.W)

        r += 1

        """Data location"""

        tk.Label(self, text='Data',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r, column=0, sticky=tk.W)
        self.data_path_entry = tk.Entry(self, font=(Setup_Window.FONT, Setup_Window.FONT_SIZE))
        self.data_path_entry.grid(row=r, column=1, columnspan=3, sticky=tk.E + tk.W)

        data_path = Setup_Window.default_data_path + os.sep + Setup_Window.default_data_fname
        self.data_path_entry.insert(0, data_path)

        tk.Button(self, text='...', font=(Setup_Window.FONT, Setup_Window.FONT_SIZE),
                  command=self.open_data).grid(row=r, column=4, sticky=tk.E + tk.W)

        r += 1

        """GO"""
        tk.Button(self, text='Analyze', font=(Setup_Window.FONT, Setup_Window.FONT_SIZE),
                  command=self.analyze).grid(row=r, column=columns-2, columnspan=2, sticky=tk.E + tk.W)

        r += 1
        tk.Label(self, text='2021 Teddy Tortorici',
                 font=(Setup_Window.FONT, Setup_Window.FONT_SIZE)).grid(row=r,
                                                                        column=0,
                                                                        columnspan=columns,
                                                                        sticky=tk.E + tk.W)

    def open_cal(self):
        calibration_path = get_file(ftype='poni', init_dir=Setup_Window.default_calibration_path)
        self.calibration_path_entry.delete(0, tk.END)
        self.calibration_path_entry.insert(0, calibration_path)

    def open_data(self):
        data_path = get_file(ftype='tif', init_dir=Setup_Window.default_data_path)
        self.data_path_entry.delete(0, tk.END)
        self.data_path_entry.insert(0, data_path)

    def analyze(self):
        global sample_orientation_g, incident_angle_g, cal_path_g, data_path_g
        """Get values from box"""
        sample_orientation_g = int(self.orientation_selection.get())
        incident_angle_g = float(self.angle_entry.get())
        cal_path_g = self.calibration_path_entry.get()
        data_path_g = self.data_path_entry.get()

        self.killWindow()

    def killWindow(self):
        self.destroy()


if __name__ == '__main__':
    main()
