# MedLink PMG-2026 Analytics — контейнер для віддаленого запуску стенду
# Збірка:  docker build -f deploy/Dockerfile -t medlink-pmg .
# Запуск:  docker run -p 8085:8085 -v pmg-data:/app/App_Data medlink-pmg
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY src/MedLink.Pmg.Module/MedLink.Pmg.Module.csproj src/MedLink.Pmg.Module/
RUN dotnet restore src/MedLink.Pmg.Module/MedLink.Pmg.Module.csproj
COPY src/MedLink.Pmg.Module src/MedLink.Pmg.Module
RUN dotnet publish src/MedLink.Pmg.Module/MedLink.Pmg.Module.csproj -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
ENV ASPNETCORE_URLS=http://0.0.0.0:8085 \
    DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false \
    Pmg__SeedPath=/app/seed \
    Pmg__WebRootPath=/app/web \
    Pmg__SampleReportsPath=/app/samples \
    Pmg__UploadsPath=/app/App_Data/uploads \
    ConnectionStrings__PmgSqlite="Data Source=/app/App_Data/pmg_medlink.sqlite"
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends libicu72 curl && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/publish .
COPY seed /app/seed
COPY src/MedLink.Pmg.Web /app/web
COPY ["Вересень 26.xlsx", "02000334_SF_2026_08_20260910.xlsx", "/app/samples/"]
COPY docs /app/docs
VOLUME ["/app/App_Data"]
EXPOSE 8085
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s CMD curl -fs http://localhost:8085/api/v1/system/health || exit 1
ENTRYPOINT ["dotnet", "MedLink.Pmg.Module.dll"]
