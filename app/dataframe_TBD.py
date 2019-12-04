import pandas as pd
from DateTime import datetime


#types: 0:static, 1:linear, 2:dynamic
T=12

#EnvironmentInput

popBerlin = EnvironmentInput(name="User Population", value_default=3644000, type=1, growth_factor=30000/12)


#ControlInput
berlinCoveredArea = ControlInput(name="Covered Area Berlin", type=0, value_min=35, value_max=50, value_default=45, steps=5)




timeHorizon = pd.Series([range(T)])


print(timeHorizon)


 ControlInput | EnvironmentInput

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000))
    sources = db.Column(db.String(500))
    model_id = db.Column(db.Integer, db.ForeignKey('sim_model.id'), nullable=False)

    value_min = db.Column(db.Integer)
    value_max = db.Column(db.Integer)
    value_default = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    type = db.Column(db.Integer, nullable=False) #0:static, 1:linear, 2:dynamic

    growth_factor = db.Column(db.Integer) #allows to differentiate between static and dynamic/growth inputs
