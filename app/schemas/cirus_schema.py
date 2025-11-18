from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class ContinentStatsBase(BaseModel):
    sno: int
    continent: str
    internet_subscribers: Optional[int] = None
    population: Optional[int] = None
    literacy: Optional[Decimal] = None
    meta_fb_users: Optional[int] = None
    linkedin_users: Optional[int] = None
    twitter_users: Optional[int] = None
    internet_pct_population: Optional[Decimal] = None
    internet_pct_literate: Optional[Decimal] = None
    fb_pct_literate: Optional[Decimal] = None
    fb_pct_internet: Optional[Decimal] = None
    linkedin_pct_literate: Optional[Decimal] = None
    linkedin_pct_internet: Optional[Decimal] = None
    twitter_pct_literate: Optional[Decimal] = None
    twitter_pct_internet: Optional[Decimal] = None

    class Config:
        from_attributes = True


class CountryStatsBase(BaseModel):
    sno: int
    country: str
    continent: str
    internet_subscribers: Optional[int] = None
    population: Optional[int] = None
    literacy: Optional[Decimal] = None
    meta_fb_users: Optional[int] = None
    linkedin_users: Optional[int] = None
    twitter_users: Optional[int] = None
    internet_pct_population: Optional[Decimal] = None
    internet_pct_literate: Optional[Decimal] = None
    fb_pct_literate: Optional[Decimal] = None
    fb_pct_internet: Optional[Decimal] = None
    linkedin_pct_literate: Optional[Decimal] = None
    linkedin_pct_internet: Optional[Decimal] = None
    twitter_pct_literate: Optional[Decimal] = None
    twitter_pct_internet: Optional[Decimal] = None

    class Config:
        from_attributes = True


class ContinentResponse(BaseModel):
    continent: str
    country_count: int


class CountryListResponse(BaseModel):
    countries: List[str]


class SelectedCountriesRequest(BaseModel):
    countries: List[str]