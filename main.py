import tkinter as tk
from audio_data_model import AudioDataModel
from audio_data_view import AudioDataView
from audio_data_controller import AudioController

if __name__ == "__main__":
    # Create the model, view, and controller objects
    model = AudioDataModel()
    root = tk.Tk()
    view = AudioDataView(root, controller=None)
    controller = AudioController(model, view)
    view.controller = controller  # Set the controller for the view
    root.mainloop()
