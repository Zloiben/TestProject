FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN if [ "$MODE" != "PROD" ]; then \
        pip install --no-cache-dir -r requirements-test.txt; \
    fi

CMD ["sh", "build.sh"]