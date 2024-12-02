import tkinter as tk
from audio_data_model import AudioDataModel
from audio_data_view import AudioDataView
from audio_data_controller import AudioController

if __name__ == "__main__":
    #Creates the model, view, and controller objects
    model = AudioDataModel()
    root = tk.Tk()
    view = AudioDataView(root, controller=None)
    controller = AudioController(model, view)
    view.controller = controller  #Sets the controller
    root.mainloop()
