# Web-Python-2024

This is a project on the subject of Modern technologies for developing WEB-applications using the Python language.

### Team: 02

Окаянченко Давид Олександрович ІА-13

Чурікова Орина Костянтинівна ІК-13

### Topic: Фінансова установа обміну валют

### Installation

1.Copy the repository

```sh
git clone https://github.com/mrEkso/Web-Python-2024.git
```

2.Copy the test environment file to .env

```sh
cp .env-test .env
```

3.Deploying the project

```sh
python -m venv .venv
.venv\Scripts\activate
```

4.Install the required packages

```sh
pip install -r requirements.txt
```

5.Run the project

```sh  
uvicorn app.main:app --reload
```