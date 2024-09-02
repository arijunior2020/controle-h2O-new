from . import create_app  # Importa create_app do módulo atual (importação relativa)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
