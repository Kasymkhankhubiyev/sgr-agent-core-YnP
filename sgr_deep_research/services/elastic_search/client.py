from __future__ import annotations

from sgr_deep_research.services.base import HTTPClient
from sgr_deep_research.settings import get_config

from . import models

config = get_config()


class ElasticSearchClient(HTTPClient):
    service_name = "elastic_search"
    service_url = config.elastic.know2_api_base_url.rstrip("/")
    username = config.elastic.know2_auth_login_username
    password = config.elastic.know2_auth_login_password

    @classmethod
    def _url(cls, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{cls.service_url}{path}"

    @classmethod
    async def authorize(
        cls, body: models.AuthorizeRequestModel | None = None
    ) -> models.StandardResponseModel:
        payload = await cls.request(
            method="post",
            url=cls._url("/api/v1/auth/login"),
            data=(
                body
                or models.AuthorizeRequestModel(
                    username=cls.username, password=cls.password
                )
            ).model_dump(),
        )
        return models.StandardResponseModel(**payload)

    @classmethod
    async def check_authorize(cls) -> models.CheckAuthorizeResponseModel:
        payload = await cls.request(method="get", url=cls._url("/api/v1/auth/check"))
        return models.CheckAuthorizeResponseModel(**payload)

    @classmethod
    async def get_experts_availability_statuses(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_availability_statuses"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_experts_contract_statuses(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_contract_statuses"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_experts_subdivisions(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_subdivisions"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_experts_types(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_types"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_experts_staff_categories(cls) -> models.MetadataResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_staff_categories"),
        )
        return models.MetadataResponseModel(**payload)

    @classmethod
    async def get_experts_jobs(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/expert_jobs"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_projects(cls) -> models.GetProjectsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/projects/minimal"),
            params={"order_by": "created_at", "order": "desc"},
        )
        return models.GetProjectsResponseModel(**payload)

    @classmethod
    async def get_experts(cls) -> models.GetExpertsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/experts/minimal"),
            params={"order_by": "created_at", "order": "desc"},
        )
        return models.GetExpertsResponseModel(**payload)

    @classmethod
    async def get_documents(cls) -> models.GetDocumentsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/documents/minimal"),
            params={"order_by": "created_at", "order": "desc"},
        )
        return models.GetDocumentsResponseModel(**payload)

    @classmethod
    async def get_projects_statuses(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/projects/metadata/project-statuses"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_projects_types(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/projects/metadata/project-types"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_documents_availabilities(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/documents/metadata/document-availabilities"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_documents_sources(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/documents/metadata/document-sources"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_metadata_document_types(cls) -> models.MetadataResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/metadata/document-types"),
            params={"order_by": "order_num", "order": "asc"},
        )
        return models.MetadataResponseModel(**payload)

    @classmethod
    async def get_metadata_languages(cls) -> models.ParamsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/metadata/languages"),
        )
        return models.ParamsResponseModel(**payload)

    @classmethod
    async def get_metadata_functions(cls) -> models.FunctionsResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/metadata/functions"),
            params={"order_by": "name", "order": "asc"},
        )
        return models.FunctionsResponseModel(**payload)

    @classmethod
    async def get_metadata_industries(cls) -> models.IndustriesResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/metadata/industries"),
            params={"order_by": "name", "order": "asc"},
        )
        return models.IndustriesResponseModel(**payload)

    @classmethod
    async def get_metadata_geographies(cls) -> models.GeographiesResponseModel:
        payload = await cls.request(
            method="get",
            url=cls._url("/api/v1/metadata/geographies"),
            params={"order_by": "name", "order": "asc"},
        )
        return models.GeographiesResponseModel(**payload)

    @classmethod
    async def search_by_query(
        cls, body: models.SearchByQueryRequestModel
    ) -> models.SearchByQueryResponseModel:
        payload = await cls.request(
            method="post",
            url=cls._url("/api/v1/search/search-by-query"),
            data=body.model_dump(),
        )
        return models.SearchByQueryResponseModel(**payload)
