from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from starlette.routing import Mount

from typing import Callable, Any, Optional, List, Union
from functools import wraps

from .enums.request import HTTPMethods
from .response import ResponseInterface, ResponsesStructure

__all__ = (
    "BaseAPIRouter",
    "Documentation",
    "is_route_method"
)


class BaseAPIRouterMeta(type):
    def __new__(cls, name, bases, dct):
        self = super(BaseAPIRouterMeta, cls).__new__(cls, name, bases, dct)
        self.decorated_methods = [
            dct[attr]
            for attr in dct if callable(dct[attr]) and hasattr(dct[attr], 'is_decorated')
        ]
        return self


class BaseAPIRouter(metaclass=BaseAPIRouterMeta):
    """Базовый класс для роутеров"""

    group_name: str = "NoNameRoute"
    prefix: str = ""

    def __init__(self) -> None:
        self.router = APIRouter(prefix=self.prefix)
        self.interface = ResponseInterface()
        self._setup_routes()

    def _setup_routes(self):
        for router_method in self.decorated_methods:
            self.add_route(
                router_method.path,
                func=getattr(self, router_method.func.__name__),
                method=router_method.method,
                summary=router_method.summary,
                response=router_method.response,
                responses=router_method.responses,
                change=router_method.change,
                response_schema_exclude_node=router_method.response_schema_exclude_node
            )

    def _check_path_name(self, path: str) -> bool:
        """Метод проверяет существует-ли путь с таким же названием"""
        return self.prefix + path in [router.path for router in self.router.routes]

    def _check_path_method(self, path: str, method: HTTPMethods) -> bool:
        """Метод проверяет существует-ли путь с таким же методом"""
        return any([
            method.value in router.methods
            for router in self.router.routes if self.prefix + path == router.path
        ])

    def _valid_path(self, path: str, method: HTTPMethods, change: bool) -> bool:
        """Метод проверяет валидность пути в определенном порядке"""

        exist_name = self._check_path_name(path)
        exist_method = self._check_path_method(path, method)

        if change:
            if not exist_name:
                raise ValueError('Не существует пути для изменения')
            if not exist_method:
                raise ValueError('Не существует указанного метода у пути')
            return True

        return not exist_name or not exist_method

    def delete_route(self, path: str, method: HTTPMethods) -> None:
        """Метод позволяет удалить роут, по названию и методу"""

        for item in self.router.routes:

            if item.path == self.prefix + path and method.value in item.methods:
                self.router.routes.remove(item)
                return

        raise ValueError('Удаление не существующего пути')

    def add_route(self,
                  path: str,
                  *,
                  func: Callable[[], Any],
                  method: HTTPMethods,
                  summary: Optional[str] = None,
                  response: Any = Default(None),
                  responses: ResponsesStructure = None,
                  change: bool = False,
                  response_schema_exclude_node: bool = False
                  ) -> None:
        """
        Метод позволяет добавить новый роут путь.
        :param path: Путь
        :param func: Ссылка на функцию
        :param method: http метод. Все доступные прописаны в HTTPMethods
        :param summary: Описание, которое указывается после пути в /docs. Пример: GET /test/ {summary}
        :param response: Схема вывода, не обязательный параметр
        :param responses: Структура ответов
        :param change: Если вы хотите изменить существующий роут.
        :param response_schema_exclude_node: Отображать в ответе None значения
        """
        if not self._valid_path(path, method, change):
            return

        responses_structure = responses.generate() if responses else None

        if change:
            self.delete_route(path, method)

        self.router.add_api_route(
            path,
            func,
            methods=[method.value],
            response_model=response,
            summary=summary,
            responses=responses_structure,
            response_model_exclude_none=response_schema_exclude_node
        )


class Documentation(FastAPI):
    """Базовый класс для документации"""

    def __init__(
            self,
            documentation_path: str,
            *,
            title: str,
            version: Optional[str] = None,
            summary: Optional[str] = None,
            description: Optional[List[str]] = None,
            title_info_doc: str = "\n\n<h2>Существующие документации:</h2>",
            back_doc: str = "\n\n<a href='../docs'><-- Вернуться</a>"
    ) -> None:
        """
        Класс Документации
        :param documentation_path: Путь к документации.
        :param title: Название.
        :param summary: Краткое описание.
        :param description: Описание.
        :param title_info_doc: Заголовок перед выводом существующих документаций
        """

        if not description:
            description = []
        super().__init__(
            title=title, summary=summary, description="\n\n".join(description), version=version)
        self.documentation_path = documentation_path
        self.info_doc = title_info_doc
        self.back_doc = back_doc
        self.count = 1
        self.routers = []

        if self.back_doc in self.description:
            return

        if self.documentation_path == '/':
            return
        self.description += self.back_doc

    def __repr__(self) -> str:
        return f'<Документация о {self.title}>'

    def include_api_router(
            self, router: Union[BaseAPIRouter, List[BaseAPIRouter]]) -> None:
        if isinstance(router, List):
            self.routers.extend(router)
        else:
            self.routers.append(router)

    def push(self):
        for router in self.routers:
            router.router.routes = sorted(router.router.routes, key=lambda x: x.path)
            self.include_router(router.router, tags=[router.group_name])

    def include_documentation(self, doc: 'BaseDocumentation') -> None:
        if self.info_doc not in self.description:
            self.description += self.info_doc

        self.description += f"\n\n<a href='.{doc.documentation_path}/docs'>{self.count}. {doc.title} --> </a>"
        self.count += 1
        self.mount(doc.documentation_path, doc)
        if self.documentation_path == "/":
            return

        routers = []
        docs = []
        for i in doc.router.routes:
            if isinstance(i, APIRoute) and i.tags[0] not in routers:
                routers.append(i.tags[0])
            elif isinstance(i, Mount):
                docs.append(i.app.title)
        if routers:
            self.description += "\n\n**Содержит роуты на**:"
            for group_name in routers:
                self.description += f"\n * {group_name}"

        if docs:
            self.description += "\n\n**Содержит документации на**:"
            for title in docs:
                self.description += f"\n * {title}"


def is_route_method(
        path: str,
        *,
        method: HTTPMethods,
        summary: Optional[str] = None,
        response: Any = Default(None),
        responses: ResponsesStructure = None,
        change: bool = False,
        custom_key: Optional[str] = None,
        response_schema_exclude_node: bool = False
):
    """
    Декоратор позволяет добавить роут
    Предназначен только для методов класса BaseAPIRoute и его потомков

    :param path: Путь
    :param method: http метод. Все доступные прописаны в HTTPMethods
    :param summary: Описание, которое указывается после пути в /docs. Пример: GET /test/ {summary}
    :param response: Схема вывода, не обязательный параметр
    :param responses: Структура ответов
    :param change: Если вы хотите изменить существующий роут.
    :param custom_key: Ключ роута. Используется при проверках доступа.
    :param response_schema_exclude_node: Отображать в схеме ответа None значения
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self: BaseAPIRouter, *args, **kwargs):
            # Функция проверки доступа
            try:
                result = await func(self, *args, **kwargs)
            except RecursionError:
                return JSONResponse(
                    status_code=400,
                    content={
                        'message': None,
                        'detail': 'Произошло зацикливание',
                        'error': 'RecursionError'
                    }
                )
            return result

        wrapper.is_decorated = True
        wrapper.path = path
        wrapper.func = func
        wrapper.method = method
        wrapper.summary = summary
        wrapper.response = response
        wrapper.responses = responses
        wrapper.change = change
        wrapper.custom_key = custom_key
        wrapper.response_schema_exclude_node = response_schema_exclude_node
        return wrapper

    return decorator
