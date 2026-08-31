# Setup hyaup-backend

## Developer Setup

1. Clone the repository
2. Switch to the mbiarrambang branch

```bash
cd hyaup-backend
git checkout mbiarrambang
```

## Setup environment variables

Copy the `.env.example` file to `.env` and fill in the values.

```bash
cp .env.example .env
```

## Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate || .venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python main.py
```