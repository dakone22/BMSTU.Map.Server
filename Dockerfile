FROM python:3.9-slim

ADD ./ /BMSTU.Map.Server
WORKDIR /BMSTU.Map.Server/

CMD exec apt-get update
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "-m", "src"]
