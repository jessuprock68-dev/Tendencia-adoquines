import pandas as pd
from pytrends.request import TrendReq
import sys

def ejecutar_analisis():
    print("🚀 Iniciando motor de búsqueda para Estrublock...")
    
    # Inicialización simplificada para máxima compatibilidad
    pytrends = TrendReq(hl='es-MX', tz=360)
    
    # Palabras clave estratégicas
    kw_list = ["adoquin romano", "adoquin hueso", "adoquin barrita"]
    
    try:
        print(f"🔎 Consultando tendencias en Jalisco para: {kw_list}")
        # Filtramos por Jalisco (MX-JAL) y últimos 3 meses
        pytrends.build_payload(kw_list, timeframe='today 3-m', geo='MX-JAL')
        
        df = pytrends.interest_over_time()
        
        nombre_archivo = "reporte_estrublock_final.xlsx"
        
        if df.empty:
            print("⚠️ Google no devolvió datos. Creando reporte de aviso.")
            df_vacio = pd.DataFrame({"Estado": ["Sin datos - IP bloqueada temporalmente"], "Sugerencia": ["Reintentar en unas horas"]})
            df_vacio.to_excel(nombre_archivo, index=False)
        else:
            # Limpieza de datos
            df = df.drop(columns=['isPartial'], errors='ignore')
            print("✅ Datos obtenidos con éxito.")
            df.to_excel(nombre_archivo)
            
        print(f"📂 Archivo generado exitosamente: {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error crítico detectado: {e}")
        # Generamos un log de error en Excel para diagnóstico
        pd.DataFrame({"Error": [str(e)]}).to_excel("reporte_estrublock_final.xlsx", index=False)

if __name__ == "__main__":
    ejecutar_analisis()
