from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class RateModel(Model):
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=150)
    rate = fields.FloatField()

    class Meta:
        table = "rate"
        exclude = ["rate"]


PydanticM = pydantic_model_creator(RateModel, name="PydanticM")
RatePydantic = pydantic_model_creator(RateModel, name="RateModel",
                                                 exclude=("id", "rate"))
