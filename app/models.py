from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Company(Base):
    __tablename__ = "company"

    """
        - uniq_key: 회사 고유 번호
        - company_name: 회사이름
    """

    uniq_key = Column(String(255), primary_key=True, unique=True, index=True)
    company_name = Column(String(255))

    company_info = relationship("CompanyInfo", back_populates="company")


class CompanyInfo(Base):
    __tablename__ = "company_info"

    """
        - img_url: 로고 이미지 주소
        - foundation: 기관설립일
        - purpose: 설립목적
        - type: 기관유형
        - authority: 주무기관
        - homepage: 홈페이지
        - location: 소재지
        - history: 기관연혁
        - role: 주요 기능 및 역할
        - goal: 경영목표 및 전략
    """
    id = Column(Integer, primary_key=True, index=True)
    company_uniq_key = Column(String(255), ForeignKey("company.uniq_key"))

    img_url = Column(String(255))
    foundation = Column(String(20))
    purpose = Column(String(255))
    type = Column(String(20))
    authority = Column(String(20))
    homepage = Column(String(255))
    location = Column(String(20))
    history = Column(String(255))
    role = Column(String(255))
    goal = Column(String(255))

    company = relationship("Company", back_populates="company_info")
