from flask import Flask, render_template, request
from lexer import analizar_lexico      # Importamos nuestra función del lexer
from parser import analizar_sintactico # Importamos nuestra función del parser

def Crear_app():
    app = Flask(__name__)
    
    @app.route('/', methods=["GET", "POST"])
    def index():
        tipo_analisis = None
        resultado_lexico = []
        resultado_sintactico = None
        errores = []
        
        if request.method == "POST":
            texto = request.form.get('texto')
            accion = request.form.get('accion')

            if texto:
                if accion == 'lexico':
                    tipo_analisis = 'lexico'
                    resultado_lexico = analizar_lexico(texto)
                
                elif accion == 'sintactico':
                    tipo_analisis = 'sintactico'
                    resultado, lista_errores = analizar_sintactico(texto)
                    resultado_sintactico = resultado
                    errores = lista_errores

        return render_template("index.html", 
                            tipo_analisis=tipo_analisis,
                            resultado_lexico=resultado_lexico,
                            resultado_sintactico=resultado_sintactico,
                            errores=errores)
    return app

if __name__ == "__main__":
    app = Crear_app()
    app.run(debug=True, port=5001)
