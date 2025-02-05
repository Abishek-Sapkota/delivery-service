class AttributeBasedDatabaseRouter:
    def db_for_read(self, model, **hints):
        # Use the model's custom database attribute if defined
        return getattr(model, "database_name", "default")

    def db_for_write(self, model, **hints):
        # Use the model's custom database attribute if defined
        return getattr(model, "database_name", "default")

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Prevent migrations on non-default databases
        return db == "default"
