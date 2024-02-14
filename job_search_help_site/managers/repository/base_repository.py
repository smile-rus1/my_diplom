class BaseRepository:
    """
    Base repository to any models.
    """
    instance = {}

    def __new__(cls, model):
        if cls.instance.get(model) is None:
            cls.instance[model] = super(BaseRepository, cls).__new__(cls)
            cls.instance[model].model = model

        return cls.instance[model]

    def create_model(self, **models_data):
        """
        Create a model
        """
        return self.model.objects.create(**models_data)

    def get_all(self) -> list:
        """
        Get all records from model.
        """
        return self.model.objects.all()

    def get_by_criteria(self, **criteria) -> list:
        """
        Get all records from model, by any criteria.
        """
        return self.model.objects.filter(**criteria).first()

    def delete_model_instance(self, **criteria):
        """
        Delete instance by any received parameters.
        """
        self.model.objects.filter(**criteria).delete()




