class Fondo_acciones:

    '''Esta clase define un elemento fondo'''

    def __init__(self, Nombre_Fondo: str, isin: str, Precio_accion: str, Comisiones: dict, Rentabilidad: dict, Volatilidad: str):
        self.Nombre_fondo : str = Nombre_Fondo
        self.isin : str = isin
        self.Precio_accion = Precio_accion
        self.Comisiones : dict = Comisiones
        self.Rentabilidad : dict =  Rentabilidad
        self.Volatilidad : str = Volatilidad
        
    def __str__(self):

        '''
        Devuelve una lista con primer elemento Nombre del fondo, segundo elemento ISIN,
        tercer elemento Comisiones y cuarto elemento rentabilidad
        ''' 
        return (self.Nombre_fondo, self.isin, self.Precio_accion, self.Comisiones, self.Rentabilidad, self.Volatilidad)