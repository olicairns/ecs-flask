# flask nginx miniconda
FROM cameroncruz/flask-nginx-uwsgi-miniconda:python3.6

# clean up impage
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Do not run as root
RUN groupadd -r myuser && useradd -r -g myuser myuser
WORKDIR /app

# Install conda environment and add to path
COPY environment.yml /app/environment.yml
RUN conda config --add channels conda-forge \
    && conda env create -n ecsdemo -f environment.yml \
    && rm -rf /opt/conda/pkgs/* 
ENV PATH /opt/conda/envs/ecsdemo/bin:$PATH

# expose on port 80
EXPOSE 80

# activate conda environment
CMD ["bash", "conda activate ecsdemo"]

## needed to follow convention of flask nginx miniconda 
# /etc/supervisor/conf.d/supervisord.conf and /app/main.py paths
COPY src/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY src/server/main.py /app/main.py
COPY src/server/config.py /app/config.py

# copy model and explainer binaries
COPY bin/market-invoice-lgb.pkl bin/market-invoice-lgb.pkl

CMD [ "python3", "/app/main.py" ]

