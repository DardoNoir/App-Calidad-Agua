
# Subindice ICA del pH
def subindice_ph(valor_ph: float) -> float:
    if 6.5 <= valor_ph <= 8.5:
        return 100.0    
    elif 6.0 <= valor_ph < 6.5 or 8.5 < valor_ph <= 9.0:
        return 70.0
    else:
        return 30.0
    
# Subindice ICA del Oxígeno Disuelto
def subindice_oxigeno_disuelto(valor_od: float) -> float:
    if 5.0 <= valor_od <= 12.0:
        return 100.0
    elif 4.0 <= valor_od < 5.0 or 12.0 < valor_od <= 15.0:
        return 70.0
    else:
        return 30.0 

# Subindice ICA de DBO5
def subindice_dbo5(valor_dbo5: float) -> float:
    if 2.9 <= valor_dbo5 <= 3.1:
        return 100.0
    elif 2.75 <= valor_dbo5 < 2.9 or 3.1 < valor_dbo5 <= 3.25:
        return 70.0
    else:
        return 30.0
    
# Subindice ICA de Sólidos Coliformes Totales
def subindice_coliformes_totales(valor_ct: float) -> float:
    if 4800.0 <= valor_ct <= 5200.0:
        return 100.0
    elif 4500.0 <= valor_ct < 4800.0 or 5200.0 < valor_ct <= 5500.0:
        return 70.0
    else:
        return 30.0

