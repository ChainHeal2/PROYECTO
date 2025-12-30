"""Funciones"""
def campos_limpios(variable1,variable2):
    """quita espacios"""
    if len(variable1) >= 8 and len(variable2) >= 8 :
        if not variable1[0] in "1234567890":
            variable1 = " ".join(variable1.split())
            variable2 = " ".join(variable2.split())
            if "@" in variable1 and "." in variable1:
                return variable1.lower(), variable2.replace(" ","")
    else:
        return None
        
def devolver_espacios(variable):
    """Regresa los espacios"""
    if variable:
        resultado = variable.replace("_"," ")
        return resultado.title()
    return None