FROM python:3.13-slim

ENV TZ=Asia/Taipei
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y \
    tzdata wget gnupg ca-certificates \
    libnss3 libatk-bridge2.0-0 libxss1 libasound2 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /playwright-app

# ----- Step 1: Copy only requirements for faster cache -----
COPY pyproject.toml poetry.lock ./

# ----- Step 2: Install poetry + dependencies -----
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# ----- Step 3: Install playwright browser -----
RUN poetry run playwright install chromium

# ----- Step 4: Copy all source code -----
COPY . .

EXPOSE 9801

CMD ["poetry", "run", "python", "flask_app/trigger_automation.py"]
