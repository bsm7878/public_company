from pydantic import BaseModel, HttpUrl, Field


class Company(BaseModel):
    uniq_key: str
    company_name: str

    class Config:
        orm_mode = True


class CompanyInfo(BaseModel):
    company_uniq_key: str
    img_url: HttpUrl
    foundation: str
    purpose: str = Field(..., title="설립목적")
    type: str
    authority: str
    homepage: HttpUrl
    location: str
    history: str
    role: str
    goal: str

    class Config:
        orm_mode = True
