from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StandardResponseModel(BaseModel):
    status: str
    status_code: int
    message: Optional[str] = None
    payload: Dict[str, Any]


class AuthorizeRequestModel(BaseModel):
    username: str
    password: str


class CheckAuthorizeResponseModel(BaseModel):
    message: str


class SearchByQueryRequestModel(BaseModel):
    query: Dict[str, Any]
    index: str
    skip: int
    take: int


class ParamsRowModel(BaseModel):
    id: str
    name: str
    russian_name: Optional[str] = None
    is_active: Optional[bool] = None
    required_document_types: Optional[List[str]] = None


class ParamsResponseModel(StandardResponseModel):
    payload: List[ParamsRowModel]


class GetProjectsRowModel(BaseModel):
    id: str
    title: str
    charge_code: Optional[str] = None


class GetProjectsBodyModel(BaseModel):
    items: List[GetProjectsRowModel]
    total: int
    page: Optional[int] = None
    page_size: Optional[int] = None


class GetProjectsResponseModel(StandardResponseModel):
    payload: GetProjectsBodyModel


class GetExpertsRowModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None


class GetExpertsBodyModel(BaseModel):
    items: List[GetExpertsRowModel]
    total: int
    page: Optional[int] = None
    page_size: Optional[int] = None


class GetExpertsResponseModel(StandardResponseModel):
    payload: GetExpertsBodyModel


class GetDocumentsRowModel(BaseModel):
    id: str
    title: str


class GetDocumentsBodyModel(BaseModel):
    items: List[GetDocumentsRowModel]
    total: int
    page: Optional[int] = None
    page_size: Optional[int] = None


class GetDocumentsResponseModel(StandardResponseModel):
    payload: GetDocumentsBodyModel


class MetadataRowModel(BaseModel):
    id: str
    name: str
    order_num: Optional[int] = None
    russian_name: Optional[str] = None
    is_editable: Optional[bool] = None
    external_id: Optional[str] = None
    parent_id: Optional[str] = None


class MetadataBodyModel(BaseModel):
    items: List[MetadataRowModel]
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class MetadataResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class IndustriesResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class FunctionsResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class GeographiesResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class SearchByQueryRowModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    index: str = Field(alias="_index")
    score: float = Field(alias="_score")
    source: Dict[str, Any] = Field(alias="_source")
    type: str = Field(alias="_type")
    inner_hits: Optional[Dict[str, Any]] = None


class SearchByQueryBodyModel(BaseModel):
    hits: List[SearchByQueryRowModel]
    total: int


class SearchByQueryResponseModel(StandardResponseModel):
    payload: SearchByQueryBodyModel
