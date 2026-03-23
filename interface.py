import os
def logo(v):
    os.system("cls" if os.name == "nt" else "clear")
    print(rf"""
  _____ _      _____  ____  _____ _______ 
 |  __ (_)    / ____|/ __ \|  __ \__   __|
 | |__) |__ _| (___ | |  | | |__) | | |   
 |  ___/ \ \ / \___ \| |  | |  _  /  | |   
 | |   | |>  < ____) | |__| | | \ \  | |   
 |_|   |_/_/\_\_____/ \____/|_|  \_\ |_|   
        MODULAR ENGINE v{v} | LOCKED CORE
    """)
