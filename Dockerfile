FROM cgr.dev/chainguard/wolfi-base

# Instalar Python y UV
RUN apk add --no-cache python-3.12 py3.12-pip && \
    pip install uv

WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias con UV
RUN uv sync --frozen --no-cache --no-dev

# Copiar codigo
COPY main.py ./

EXPOSE 3000

CMD ["uv", "run", "python", "main.py"]