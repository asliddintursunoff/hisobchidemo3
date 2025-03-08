from .models import *
import pandas as pd
def main_to_excell():
    workers = Worker.objects.all()
    main = pd.DataFrame({"ishchilar":[f"{worker.last_name} {worker.name}"for worker in workers]})
    main.to_excel("excell/main.xlsx",sheet_name = "data",index = True)
    print("halo")
