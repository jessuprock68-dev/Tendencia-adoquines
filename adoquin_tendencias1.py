import pandas as pd
from pytrends.request import TrendReq
import time
import sys

def ejecutar_analisis():
    print("🚀 Iniciando motor de inteligencia Estrublock...")
    
    # Pausa de seguridad para evitar bloqueos por IP
    time.sleep(10)
    
    # Configuración de conexión con tiempos de espera más amplios
    pytrends = TrendReq(hl='es-MX', tz=360, timeout=(15, 30))
    
    kw_list = ["adoquin romano", "adoquin hueso", "adoquin barrita"]
    
    try:
        print(f"🔎 Consultando demanda en Jalisco: {kw_list}")
        # Usamos un periodo de 1 mes para reducir la carga de datos y evitar el Error 429
        pytrends.build_payload(kw_list, timeframe='today 1-m', geo='MX-JAL')
        
        df = pytrends.interest_over_time()
        nombre_archivo = "reporte_estrublock_final.xlsx"
        
        if df.empty:
            print("⚠️ Google limitó la respuesta. Generando reporte de estado.")
            pd.DataFrame({"Estado": ["Límite de Google alcanzado"], "Sugerencia": ["No ejecutar más de una vez por hora"]}).to_excel(nombre_archivo, index=False)
        else:
            df = df.drop(columns=['isPartial'], errors='ignore')
            print("✅ Datos obtenidos exitosamente.")
            df.to_excel(nombre_archivo)
            
        print(f"📂 Archivo guardado: {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
        pd.DataFrame({"Error": [str(e)]}).to_excel("reporte_estrublock_final.xlsx", index=False)

if __name__ == "__main__":
    ejecutar_analisis()
