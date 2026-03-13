import pandas as pd
from pytrends.request import TrendReq
import time
import sys

def ejecutar():
    print("🚀 Iniciando motor de búsqueda Estrublock...")
    
    # Añadimos un pequeño retraso inicial para no entrar "en seco"
    time.sleep(5)
    
    # Configuración de conexión más humana
    pytrends = TrendReq(hl='es-MX', tz=360, timeout=(10,25))
    
    kw_list = ["adoquin romano", "adoquin hueso", "adoquin barrita"]
    
    try:
        print(f"🔎 Consultando tendencias para: {kw_list}")
        # Reducimos un poco el periodo para asegurar que Google responda
        pytrends.build_payload(kw_list, timeframe='today 1-m', geo='MX-JAL')
        
        df = pytrends.interest_over_time()
        
        nombre_archivo = "reporte_estrublock_final.xlsx"
        
        if df.empty:
            print("⚠️ Google respondió pero sin datos. Reintentando...")
            pd.DataFrame({"Estado": ["Sin datos - Google Limit"], "Nota": ["Esperar 1 hora"]}).to_excel(nombre_archivo)
        else:
            df = df.drop(columns=['isPartial'], errors='ignore')
            print("✅ Datos obtenidos con éxito.")
            df.to_excel(nombre_archivo)
            
    except Exception as e:
        print(f"❌ Error detectado: {e}")
        pd.DataFrame({"Error": [str(e)]}).to_excel("reporte_estrublock_final.xlsx")

if __name__ == "__main__":
    ejecutar()
