import TkEasyGUI as eg

# Create window
layout = [
    [eg.Text("file:")],
    [
        eg.Input(key="-file-"),
        eg.FileBrowse(),  # FileBrowse button
        eg.Button("Copy", key="-copy-file-"),
    ],
    [eg.CloseButton()],
]

if __name__=="__main__":
    window = eg.Window("FileBrowse Test", layout, size=(500, 300))

    # Event loop
    while window.is_running():
        # get window event
        event, values = window.read()
        print("@@@", event, values)
        if event == "-copy-file-":
            eg.set_clipboard(values["-file-"])
            eg.print("Copied to clipboard:\n", values["-file-"])
    window.close()