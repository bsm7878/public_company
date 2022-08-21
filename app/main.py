import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/company", response_model=schemas.Company)
def create_company(
    uniq_key: str = None, company_name: str = None, db: Session = Depends(get_db)
):

    params = {
        "apbaType": [],
        "jidtDptm": [],
        "area": [],
        "apbaId": "",
        "reportFormRootNo": "10101",
    }
    r = requests.post("https://www.alio.go.kr/item/itemOrganListJung.json", json=params)

    result = r.json()

    for data in result["data"]["apbaList"]:
        company = models.Company(uniq_key=data["apbaId"], company_name=data["apbaNa"])
        db.add(company)
        db.commit()

    return company


@app.post("/company/info", response_model=schemas.CompanyInfo)
def create_company_info(
    company_info: schemas.CompanyInfo, db: Session = Depends(get_db)
):

    # 공공기관에 등록되어 있지 않을 때 예외 처리
    existed_company = (
        db.query(models.Company)
        .filter_by(uniq_key=company_info.company_uniq_key)
        .first()
    )

    if not existed_company:
        raise HTTPException(status_code=400, detail="등록되지 않은 공공기관입니다.")

    # 이미 공공기관의 정보가 존재할 때 예외 처리
    register_company = (
        db.query(models.CompanyInfo)
        .filter_by(company_uniq_key=company_info.company_uniq_key)
        .first()
    )

    if register_company:
        raise HTTPException(status_code=400, detail="공공기관의 정보가 존재합니다.")

    company_info = models.CompanyInfo(
        company_uniq_key=company_info.company_uniq_key,
        img_url=company_info.img_url,
        foundation=company_info.foundation,
        purpose=company_info.purpose,
        type=company_info.type,
        authority=company_info.authority,
        homepage=company_info.homepage,
        location=company_info.location,
        history=company_info.history,
        role=company_info.role,
        goal=company_info.goal,
    )
    db.add(company_info)
    db.commit()

    return company_info
