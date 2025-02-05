class MultiDbSchemaRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    user_app_labels = {"user", }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.user_app_labels:
            return "user_management"
        return None

    def db_for_write(self, model, **hints):
        return None