from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AgentState(BaseModel):
    prompt: str
    classification: List[str] = Field(default_factory=list)
    route_plan: List[str] = Field(default_factory=list)
    route_taken: List[str] = Field(default_factory=list)
    lookup_result: Optional[LookupState] = None
    news_result: Optional[NewsState] = None
    sector_result: Optional[SectorState] = None


class LookupState(BaseModel):
    prompt: Optional[str] = None
    company: Optional[str] = None
    period: Optional[str] = None
    interval: Optional[str] = None
    error: Optional[str] = None
    symbol: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    marketCap: Optional[int] = None
    trailingPE: Optional[float] = None
    forwardPE: Optional[float] = None
    dividendYield: Optional[float] = None
    beta: Optional[float] = None
    fiftyTwoWeekLow: Optional[float] = None
    fiftyTwoWeekHigh: Optional[float] = None
    avgVolume: Optional[float] = None
    sharesOutstanding: Optional[int] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    lastPrice: Optional[float] = None
    period_return_pct: Optional[float] = None
    ann_vol_pct: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    atr_14: Optional[float] = None
    tail_ohlcv: Optional[dict] = None


class NewsState(BaseModel):
    prompt: Optional[str] = None
    company: Optional[str] = None
    items: Optional[int] = None
    rows: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class SectorState(BaseModel):
    prompt: Optional[str] = None
    sectors: Optional[List[str]] = None
    raw_rows: Optional[List[Dict[str, Any]]] = None
    structured_view: Optional[Dict[str, Any]] = None
    interpreted_results: Optional[str] = None
    error: Optional[str] = None
