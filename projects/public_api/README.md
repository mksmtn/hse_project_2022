# Public API for Music Recommender System

## Running the app

From `projects/public_api/` directory:

```bash
mkdir lfm-b2
# Copy tracks.tsv to projects/public_api/lfm-b2/tracks.tsv
cp ../../lfm-b2/tracks.tsv ./lfm-b2/tracks.tsv

# extract pickle files
unzip pickle.zip

docker build -t hse_project_2022_public_api .
docker run -p 127.0.0.1:8080:80 hse_project_2022_public_api
```

Wait till you see `Application startup complete` in your terminal. Then you can open [http://localhost:8080/users/1/predictions](http://localhost:8080/users/1/predictions) in your browser.

## Contributing

First, change directory to `projects/public_api`:

```bash
cd projects/public_api
```

### Starting the app in development mode

```bash
uvicorn --reload src.server:create_app
```

### Unit testing

```bash
python -m unittest
```
