import json
import uvicorn

import settings


from fastapi import (FastAPI,
                     UploadFile,
                     File,
                     HTTPException)
from tortoise.contrib.fastapi import register_tortoise

from models.models import (RateModel,
                           RatePydantic,
                           PydanticM)

app = FastAPI()


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    """
    Функция отвечает за загрузку json файла и сохранение его данных в базу
    данных postgresql.<br>
    :param в качестве параметра передается класс Upload, отвечающий за
    загрузку файла json.<br>
    :return в случае передачи корректного json, возвращает содержимое json
    файла.
    """
    content = await file.read()
    try:
        data = json.loads(content.decode("utf-8"))
        for key, value in data.items():
            for val in value:
                rate = RateModel(date=key, cargo_type=val['cargo_type'],
                                 rate=val['rate'])
                await rate.save()
    except json.JSONDecodeError:
        return {"message": "Загружаемый файл имеет неподдерживаемый тип!"}
    return {"filename": data}


@app.post('/cost_calculate')
async def cost_calculate(rate: RatePydantic, cost: int) -> float():
    """
    Функция отвечает за расчет стоимости страхования в зависимости от
    указанного в запросе типа груза и даты.<br>
    :param в качестве параметра передается pydantic модель RatePydantic,
    согласно которой указывается в запросе имеющиеся в базе данных дата и
    тип груза.<br>
    :param отдельной строкой передается объявленная стоимость груза.<br>
    :return возвращается стоимость.
    """
    param = await RateModel.filter(date=rate.date,
                                   cargo_type=rate.cargo_type)
    if param:
        result = param[0].rate * cost
        return {"Стоимость": format(result, ".2f")}
    else:
        raise HTTPException(status_code=400, detail="Проверьте передаваемые "
                                                    "параметры!")


@app.get('/get_rate')
async def get_records():
    """
    Функция возвращает все записи, имеющие в базе данных касаемо даты и
    тарифов (просто для проверки).<br>
    :param в качестве параметра передается pydantic модель PydanticM.<br>
    :return возвращается имеющиеся записи.
    """
    param = await RateModel.all()
    return param


register_tortoise(
    app=app,
    config=settings.DATABASE_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True
)
