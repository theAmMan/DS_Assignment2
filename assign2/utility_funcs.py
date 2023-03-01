#A file for utility functions 
def get_link(port:int) -> str:
    base = "http://127.0.0.1:"
    base += str(port)
    base += "/"