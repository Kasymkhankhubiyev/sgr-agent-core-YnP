import asyncio
from typing import Any, Callable, Coroutine, Union

import aiohttp
from pydantic import BaseModel, Field

KNOW2_API_BASE_URL = "https://know-two-api-dev.yakov.partners"

KNOW2_AUTH_LOGIN_USERNAME = "devuser_rniadmin"
KNOW2_AUTH_LOGIN_PASSWORD = "Pvj1kVm*F}J"


class StandardResponseModel(BaseModel):
    status: str
    status_code: int
    message: str | None = None
    payload: dict


class AuthorizeRequestModel(BaseModel):
    username: str
    password: str


class CheckAuthorizeResponseModel(BaseModel):
    message: str


class SearchByQueryRequestModel(BaseModel):
    query: dict
    index: str
    skip: int
    take: int


class ParamsRowModel(BaseModel):
    id: str
    name: str
    russian_name: str | None = None
    is_active: bool | None = None
    required_document_types: list[str] | None = None


class ParamsResponseModel(BaseModel):
    status: str
    status_code: int
    message: str | None = None
    payload: list[ParamsRowModel]


class GetProjectsRowModel(BaseModel):
    id: str
    title: str
    charge_code: str | None = None


class GetProjectsBodyModel(BaseModel):
    items: list[GetProjectsRowModel]
    total: int
    page: int | None = None
    page_size: int | None = None


class GetProjectsResponseModel(StandardResponseModel):
    payload: GetProjectsBodyModel


class GetExpertsRowModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    patronymic: str | None = None


class GetExpertsBodyModel(BaseModel):
    items: list[GetExpertsRowModel]
    total: int
    page: int | None = None
    page_size: int | None = None


class GetExpertsResponseModel(StandardResponseModel):
    payload: GetExpertsBodyModel


class GetDocumentsRowModel(BaseModel):
    id: str
    title: str


class GetDocumentsBodyModel(BaseModel):
    items: list[GetDocumentsRowModel]
    total: int
    page: int | None = None
    page_size: int | None = None


class GetDocumentsResponseModel(StandardResponseModel):
    payload: GetDocumentsBodyModel


class MetadataRowModel(BaseModel):
    id: str
    name: str
    order_num: int | None = None
    russian_name: str | None = None
    is_editable: bool | None = None
    external_id: str | None = None
    parent_id: str | None = None


class MetadataBodyModel(BaseModel):
    items: list[MetadataRowModel]
    total: int | None = None
    page: int | None = None
    page_size: int | None = None


class MetadataResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class IndustriesResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class FunctionsResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class GeographiesResponseModel(StandardResponseModel):
    payload: MetadataBodyModel


class SearchByQueryRowModel(BaseModel):
    id: str = Field(alias="_id")
    index: str = Field(alias="_index")
    score: float = Field(alias="_score")
    source: dict = Field(alias="_source")
    type: str = Field(alias="_type")
    inner_hits: dict | None = None

    class Config:
        populate_by_name = True


class SearchByQueryBodyModel(BaseModel):
    hits: list[SearchByQueryRowModel]
    total: int


class SearchByQueryResponseModel(StandardResponseModel):
    payload: SearchByQueryBodyModel


class KnowTwoApiWorker:
    session: aiohttp.ClientSession

    experts_availability_statuses: dict = {}
    experts_contract_statuses: dict = {}
    experts_subdivisions: dict = {}
    experts_types: dict = {}
    experts_staff_categories: dict = {}
    experts_jobs: dict = {}
    projects: dict = {}
    experts: dict = {}
    documents: dict = {}
    projects_statuses: dict = {}
    projects_types: dict = {}
    documents_availabilities: dict = {}
    documents_sources: dict = {}
    metadata_document_types: dict = {}
    metadata_languages: dict = {}
    metadata_functions: dict = {}
    metadata_industries: dict = {}
    metadata_geographies: dict = {}

    def __init__(
        self,
        refresh_token: str = None,
        access_token: str = None,
        is_admin: bool = False,
        is_classification: bool = False,
    ):
        if (not refresh_token or not access_token) and not is_admin:
            raise NotImplementedError("Invalid initial parameters")
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.is_admin = is_admin
        self.is_classification = is_classification

    async def __fetch_and_store_data__(
        self,
        target_function: Callable[
            [],
            Coroutine[
                Any,
                Any,
                Union[
                    ParamsResponseModel,
                    MetadataResponseModel,
                    GetProjectsResponseModel,
                    GetExpertsResponseModel,
                    GetDocumentsResponseModel,
                ],
            ],
        ],
        target_attr: dict,
    ):
        response = await target_function()
        if isinstance(response, IndustriesResponseModel) or isinstance(
            response, FunctionsResponseModel
        ):
            data = {
                row.id: row.name for row in response.payload.items if not row.parent_id
            }
        elif isinstance(response, GeographiesResponseModel):
            first_level_ids = [
                row.id for row in response.payload.items if not row.parent_id
            ]
            data = {
                row.id: row.name
                for row in response.payload.items
                if row.parent_id in first_level_ids
            }
        if isinstance(response, ParamsResponseModel):
            if response.payload[0].russian_name:
                data = {row.russian_name: row.id for row in response.payload}
            else:
                data = {row.name: row.id for row in response.payload}
        elif isinstance(response, MetadataResponseModel):
            data = {row.russian_name: row.id for row in response.payload.items}
        elif isinstance(response, GetProjectsResponseModel) or isinstance(
            response, GetDocumentsResponseModel
        ):
            data = {row.id: row.title for row in response.payload.items}
        elif isinstance(response, GetExpertsResponseModel):
            data = {
                row.id: f"{row.first_name} {row.last_name} {row.patronymic}"
                for row in response.payload.items
            }
        target_attr.clear()
        target_attr.update(data)

    async def __collect_data__(self):
        task_list = [
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_availability_statuses,
                    target_attr=self.experts_availability_statuses,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_contract_statuses,
                    target_attr=self.experts_contract_statuses,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_subdivisions,
                    target_attr=self.experts_subdivisions,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_types,
                    target_attr=self.experts_types,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_staff_categories,
                    target_attr=self.experts_staff_categories,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts_jobs, target_attr=self.experts_jobs
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_projects, target_attr=self.projects
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_experts, target_attr=self.experts
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_documents, target_attr=self.documents
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_projects_statuses,
                    target_attr=self.projects_statuses,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_projects_types,
                    target_attr=self.projects_types,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_documents_availabilities,
                    target_attr=self.documents_availabilities,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_documents_sources,
                    target_attr=self.documents_sources,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_metadata_document_types,
                    target_attr=self.metadata_document_types,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_metadata_functions,
                    target_attr=self.metadata_functions,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_metadata_languages,
                    target_attr=self.metadata_languages,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_metadata_industries,
                    target_attr=self.metadata_industries,
                )
            ),
            asyncio.create_task(
                self.__fetch_and_store_data__(
                    target_function=self.get_metadata_geographies,
                    target_attr=self.metadata_geographies,
                )
            ),
        ]
        await asyncio.gather(*task_list)

    async def __aenter__(self):

        self.session = await self.authorize(
            body=AuthorizeRequestModel(
                username=KNOW2_AUTH_LOGIN_USERNAME,
                password=KNOW2_AUTH_LOGIN_PASSWORD,
            )
        )

        await self.__collect_data__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def authorize(self, body: AuthorizeRequestModel) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession()
        async with session.post(
            url=f"{KNOW2_API_BASE_URL}/api/v1/auth/login",
            json=body.model_dump(),
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return session

    async def check_authorize(self) -> CheckAuthorizeResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/auth/check",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return CheckAuthorizeResponseModel(**(await response.json()))

    async def get_experts_availability_statuses(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_availability_statuses",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_experts_contract_statuses(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_contract_statuses",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_experts_subdivisions(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_subdivisions",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_experts_types(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_types",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_experts_staff_categories(self) -> MetadataResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_staff_categories",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return MetadataResponseModel(**(await response.json()))

    async def get_experts_jobs(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/expert_jobs",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_projects(self) -> GetProjectsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/projects/minimal?order_by=created_at&order=desc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return GetProjectsResponseModel(**(await response.json()))

    async def get_experts(self) -> GetExpertsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/experts/minimal?order_by=created_at&order=desc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return GetExpertsResponseModel(**(await response.json()))

    async def get_documents(self) -> GetDocumentsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/documents/minimal?order_by=created_at&order=desc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return GetDocumentsResponseModel(**(await response.json()))

    async def get_projects_statuses(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/projects/metadata/project-statuses",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_projects_types(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/projects/metadata/project-types",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_documents_availabilities(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/documents/metadata/document-availabilities",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_documents_sources(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/documents/metadata/document-sources",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_metadata_document_types(self) -> MetadataResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/metadata/document-types?order_by=order_num&order=asc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return MetadataResponseModel(**(await response.json()))

    async def get_metadata_languages(self) -> ParamsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/metadata/languages",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return ParamsResponseModel(**(await response.json()))

    async def get_metadata_functions(self) -> FunctionsResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/metadata/functions?order_by=name&order=asc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return FunctionsResponseModel(**(await response.json()))

    async def get_metadata_industries(self) -> IndustriesResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/metadata/industries?order_by=name&order=asc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return IndustriesResponseModel(**(await response.json()))

    async def get_metadata_geographies(self) -> GeographiesResponseModel:
        async with self.session.get(
            url=f"{KNOW2_API_BASE_URL}/api/v1/metadata/geographies?order_by=name&order=asc",
        ) as response:
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            return GeographiesResponseModel(**(await response.json()))

    async def search_by_query(
        self, body: SearchByQueryRequestModel
    ) -> SearchByQueryResponseModel:

        async with self.session.post(
            url=f"{KNOW2_API_BASE_URL}/api/v1/search/search-by-query",
            json=body.model_dump(),
        ) as response:
            print(body.model_dump_json())
            if response.status != 200:
                raise NotImplementedError("unlucky network request")
            result = await response.json()
            return SearchByQueryResponseModel(**result)


if __name__ == "__main__":
    know_two_api_worker = KnowTwoApiWorker(is_classification=True, is_admin=True)

    query_fields = (
        "doc_name^6",
        "doc_name.stemmed^6",
        "project.title",
        "attributes.summary^3",
        "attributes.document_type",
        "attributes.availability",
        "attributes.industry",
        "attributes.function",
        "attributes.external_authors",
        "attributes.user",
        "attributes.geography",
        "attributes.poc",
        "attributes.tags^5",
        "attributes.related_document^2.5",
    )

    queries = {
        "multi_match": {
            "query": "Геннадий Масквов",
            "fields": ["last_name", "first_name", "patronymic", "full_name"],
            "type": "best_fields",
            "boost": 3.0,
            "tie_breaker": 0.3,
            "minimum_should_match": "100%",
        }
    }

    async def run():

        async with know_two_api_worker:
            a = await know_two_api_worker.search_by_query(
                SearchByQueryRequestModel(
                    query=queries, skip=0, take=10, index="experts"
                )
            )

        print(a)

    asyncio.run(run())
