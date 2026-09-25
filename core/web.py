def init_app(app):
    @app.context_processor
    def inject_installed_modes():
        return {"installed_modes": frozenset(app.blueprints)}
