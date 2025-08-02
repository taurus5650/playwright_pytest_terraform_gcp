FROM python:3.13-slim

# Set timezone
RUN apt update && apt install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
    echo "Asia/Taipei" > /etc/timezone

# Install browser deps
RUN apt install -y wget gnupg ca-certificates && \
    apt install -y libnss3 libatk-bridge2.0-0 libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0

# Set workdir
WORKDIR /app

# Install poetry and deps
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Copy source
COPY . .

# Install Playwright browser
RUN poetry run playwright install chromium

## Container will keep running for inspection
#CMD ['tail', '-f', '/dev/null']
