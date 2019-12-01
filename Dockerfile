FROM continuumio/miniconda3

# clean up impage
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Do not run as root
RUN groupadd -r myuser && useradd -r -g myuser myuser

WORKDIR /app

# Install requirements
COPY environment.yml /app/environment.yml
RUN conda config --add channels conda-forge \
    && conda env create -n ecsdemo -f environment.yml \
    && rm -rf /opt/conda/pkgs/* 

EXPOSE 80

# activate the classifierTools environment
ENV PATH /opt/conda/envs/ecsdemo/bin:$PATH

# copy over python files and dataset
COPY . .

CMD ["bash", "conda activate ecsdemo"]
CMD [ "python3", "src/model/fit_model.py" ]
CMD [ "python3", "src/server/app.py" ]

#  docker build -t oli5679/ecsdemo .

# docker run  -p 5000:5000 oli5679/ecsdemo