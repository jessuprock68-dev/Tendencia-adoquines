import pandas as pd
from pytrends.request import TrendReq
import time
import random
from datetime import datetime
import os

def ejecutar_monitor():
    # Configuración de reintentos para mayor robustez
    pytrends = TrendReq(hl='es-MX', tz=360, retries=3, backoff_factor=0.5)
    
    geometrias = ["adoquin romano", "adoquin hueso", "adoquin barrita", "cruz de tabasco", "adoquin hexagonal"]
    
    print(f"🚀 Monitor Estrublock Cloud - {datetime.now().strftime('%H:%M:%S')}")

    try:
        # En la nube consultamos de uno en uno para máxima seguridad
        all_data = []
        for geo in geometrias:
            print(f"🔎 Analizando: {geo}")
            time.sleep(random.randint(20, 30)) # Pausa larga profesional
            
            pytrends.build_payload([geo], timeframe='today 3-m', geo='MX-JAL')
            df = pytrends.interest_over_time()
            if not df.empty:
                df = df.drop(columns=['isPartial'])
                all_data.append(df)

        if all_data:
            df_final = pd.concat(all_data, axis=1).fillna(0)
            nombre_archivo = f"Tendencias_Estrublock_{datetime.now().strftime('%Y-%m')}.xlsx"
            df_final.to_excel(nombre_archivo)
            print(f"✅ Reporte generado: {nombre_archivo}")
        else:
            print("⚠️ No se recuperaron datos, pero el script finalizó.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    ejecutar_monitor()