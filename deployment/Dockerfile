FROM python:3.13-slim

# Set environment variables
ENV TZ=Asia/Taipei
ENV PYTHONUNBUFFERED=1

# Install system & browser dependencies
RUN apt update && apt install -y \
    tzdata wget gnupg ca-certificates \
    libnss3 libatk-bridge2.0-0 libxss1 libasound2 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /playwright-app

# Install Poetry & dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy source code
COPY . .

# Install Playwright browsers (chromium only)
RUN poetry run playwright install chromium

EXPOSE 9801

CMD ["poetry", "run", "python", "-m", "flask_app.trigger_automation"]