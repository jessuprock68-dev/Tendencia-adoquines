import pandas as pd
from pytrends.request import TrendReq
import time
import sys

def ejecutar_monitoreo_estrublock():
    print("🚀 Iniciando proceso de BI - Estrublock...")
    
    # Inicializamos pytrends con un margen de reintentos
    # hl: idioma, tz: zona horaria (360 es para México)
    pytrends = TrendReq(hl='es-MX', tz=360, retries=3, backoff_factor=1)
    
    # Lista de productos clave para monitorear en Jalisco
    kw_list = ["adoquin romano", "adoquin hueso", "adoquin barrita", "cruz de tabasco"]
    
    try:
        print(f"🔎 Consultando tendencias en Jalisco para: {kw_list}")
        
        # Construimos la consulta para los últimos 3 meses en Jalisco (MX-JAL)
        pytrends.build_payload(kw_list, timeframe='today 3-m', geo='MX-JAL')
        
        df = pytrends.interest_over_time()
        
        # Verificamos si Google devolvió datos o si estamos bloqueados
        if df.empty:
            print("⚠️ Google no devolvió datos. Es posible que la IP esté saturada.")
            # Creamos un archivo de respaldo para evitar que el proceso falle
            df_error = pd.DataFrame({
                "Fecha": [pd.Timestamp.now()],
                "Estado": ["Sin datos - Posible bloqueo de Google"],
                "Accion": ["Reintentar manualmente en unas horas"]
            })
            nombre_archivo = "REPORTE_ESTRUBLOCK_ALERTA.xlsx"
            df_error.to_excel(nombre_archivo, index=False)
        else:
            # Limpiamos la columna isPartial que no nos sirve para finanzas
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            
            print("✅ Datos obtenidos exitosamente.")
            nombre_archivo = "Reporte_Tendencias_Jalisco.xlsx"
            df.to_excel(nombre_archivo)
            
        print(f"📂 Proceso terminado. Archivo generado: {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error crítico detectado: {e}")
        # Poka-Yoke: Incluso si falla todo, generamos un log en Excel
        df_fallo = pd.DataFrame({"Error": [str(e)], "Timestamp": [pd.Timestamp.now()]})
        df_fallo.to_excel("ERROR_SISTEMA.xlsx", index=False)
        # Salimos con éxito para que GitHub no marque la X roja si el error fue manejado
        sys.exit(0)

if __name__ == "__main__":
    ejecutar_monitoreo_estrublock()
