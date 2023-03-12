from sqlalchemy.orm import Session


class BaseDAO:
    def __init__(self, session: Session):
        self.session = session

    def add(self, model_instance):
        self.session.add(model_instance)
        self.session.commit()

    def add_all(self, model_instances):
        self.session.add_all(model_instances)
        self.session.commit()

    def update(self, model_instance):
        self.session.commit()

    def delete(self, model_instance):
        self.session.delete(model_instance)
        self.session.commit()

    def get_by_id(self, model, id_):
        return self.session.query(model).get(id_)

    def get_all(self, model):
        return self.session.query(model).all()
