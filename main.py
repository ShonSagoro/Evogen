import warnings

from views.ChromosomaGui import ChromosomaGui

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    app = ChromosomaGui()
    app.mainloop()