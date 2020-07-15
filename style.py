#   In each function, we need to first specify the class name of the corresponding widget (e.g.,QGroupBox)


def groupbox_style():
    return """
        QGroupBox {
        background-color:#fcc324;
        font: 15pt Times Bold;
        color: white;
        border: 2px solid gray;
        border-radius: 15px;
        }
    """


def progressbar_style():
    return """
       QProgressBar {
       border: 1px solid #bbb;
       background-color: white;
       height: 10px;
       border-radius: 6px;
       }
    """


def playlist_style():
    return """
        QListWidget {
        background-color: #fff;
        border-radius: 10px;
        border: 3px solid blue;
        }
    
    """