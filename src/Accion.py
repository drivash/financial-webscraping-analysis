class Accion:
    ''' Esta clase representa el campo de datos de una acción '''
    def __init__(self, nombre: str, rent_5a: str, rent_acu: str, margen_beneficios: str, valores:dict[str,str]):
        self.nombre: str = nombre
        self.rent_5a: str = rent_5a
        self.rent_acu:str = rent_acu
        self.margen_beneficios: str = margen_beneficios
        self.valores: dict = valores
    
    def __str__(self):
        ''' Devuelve un string con el conjunto de datos de la acción '''
        return f"{self.nombre}, {self.rent_5a}, {self.rent_acu}, {self.margen_beneficios}, {self.valores}"
    
    