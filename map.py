import sys
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkintermapview import TkinterMapView
import run as r
import weight_dialog as wd


class App(tkinter.Tk):

    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3)
        self.grid_rowconfigure(1, weight=1)

        self.search_bar = tkinter.Entry(self, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tkinter.Button(
            master=self, width=8, text="Search", command=self.search)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tkinter.Button(
            master=self, width=8, text="Clear", command=self.clear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        self.map_widget = TkinterMapView(
            width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(
            row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(
            row=2, column=1, sticky="nsew", columnspan=2)

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        self.save_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="save current marker",
                                                 command=self.save_marker)
        self.save_marker_button.grid(row=0, column=0, pady=10, padx=10)

        self.clear_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="clear marker list",
                                                  command=self.clear_marker_list)
        self.clear_marker_button.grid(row=1, column=0, pady=10, padx=10)

        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="connect marker with path",
                                                    command=self.connect_marker)
        self.connect_marker_button.grid(row=2, column=0, pady=10, padx=10)

        self.map_widget.set_address("NYC")

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        self.current_marker = 1

        btn = tkinter.Button(self, text="Click Me",
                             bg="black", fg="white", command=self.run)
        btn.grid(column=1, row=3)

    def run(self):
        r.calculate_shortest_path()

    def add_marker_event(self, coords):
        inputDialog = wd.MyDialog(self)
        self.wait_window(inputDialog.top)
        print('weight: ', inputDialog.weight)
        print("Add marker:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="Customer"+str(self.current_marker), command=self.assign_weight("C"+str(self.current_marker), inputDialog.weight))
        r.customer_locations.append(
            ["C"+str(self.current_marker), (coords[0], coords[1])])
        print(r.customer_locations)
        self.current_marker += 1
        self.marker_list.append(new_marker)
        self.search_marker = new_marker

    def assign_weight(self, customer, weight):
        r.products_weights.append([customer, int(weight)])
        print(r.products_weights)

    def search(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(
                address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def save_marker(self):
        if self.search_marker is not None:
            self.marker_list_box.insert(
                tkinter.END, f" {len(self.marker_list)}. {self.search_marker.text} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        self.connect_marker()
        self.current_marker = 1

    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
