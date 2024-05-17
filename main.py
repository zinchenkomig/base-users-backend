import os

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.cors import CORSMiddleware

from components.authentication.crud import get_user
from components.authentication.dependencies import CurrentUserDep
from components.authentication.router import auth_router
from components.superuser.router import superuser_router
from components.user.router import user_router
from dependencies import AsyncSessionDep
from starlette_exporter import PrometheusMiddleware, handle_metrics

from conf import settings

app = FastAPI(title=settings.APP_NAME, version='0.1.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('BASE_USERS_FRONTEND_URL')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware,
                   group_paths=True,
                   filter_unhandled_paths=True,
                   app_name=settings.APP_NAME)


app.include_router(router=auth_router,
                   prefix='/auth',
                   tags=['auth']
                   )

app.include_router(router=superuser_router,
                   prefix='/superuser',
                   tags=['superuser'])

app.include_router(router=user_router,
                   prefix='/user',
                   tags=['user'])

app.add_route("/metrics", handle_metrics)


@app.get('/ping')
async def ping():
    return 'pong'


@app.get('/email')
async def get_email(user: CurrentUserDep):
    return user.email


@app.get('/check/username')
async def check_username(username: str, async_session: AsyncSessionDep):
    user = await get_user(async_session, username=username)
    return user is not None


# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: settings.APP_NAME
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.JAEGER_BACKEND, insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)
