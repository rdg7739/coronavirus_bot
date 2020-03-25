# Coronavirus bot


## Blog Posts - More Information About Python Project Blueprint

You can find more information about this project/repository and how to use it in following blog post:

- [Ultimate Setup for Your Next Python Project](https://towardsdatascience.com/ultimate-setup-for-your-next-python-project-179bda8a7c2c)
- [Automating Every Aspect of Your Python Project](https://towardsdatascience.com/automating-every-aspect-of-your-python-project-6517336af9da)

## Quick Start

### Using Python Interpreter
```shell
~ $ make run
```

### Using Docker

Development image:
```console
~ $ make build-dev
~ $ docker images --filter "label=name=corobabot"
REPOSITORY                                                             TAG                 IMAGE ID            CREATED             SIZE
docker.pkg.github.com/rdg7739/coronavirus_bit/corobabot   3492a40-dirty       acf8d09acce4        28 seconds ago      967MB
~ $ docker run acf8d09acce4
```

Production (Distroless) image:
```console
~ $ make build-prod VERSION=0.0.5
~ $ docker images --filter "label=version=0.0.5"
REPOSITORY                                                             TAG                 IMAGE ID            CREATED             SIZE
docker.pkg.github.com/rdg7739/coronavirus_bit/corobabot   0.0.5               65e6690d9edd        5 seconds ago       86.1MB
~ $ docker run 65e6690d9edd
```

## Testing

Test are ran every time you build _dev_ or _prod_ image. You can also run tests using:

```console
~ $ make test
```

## Pushing to GitHub Package Registry

```console
~ $ docker login docker.pkg.github.com --username rdg7739
Password: ...
...
Login Succeeded
~ $ make push VERSION=0.0.5
```

## Cleaning

Clean _Pytest_ and coverage cache/files:

```console
~ $ make clean
```

Clean _Docker_ images:

```console
~ $ make docker-clean
```

## Setting Up Sonar Cloud
- Navigate to <https://sonarcloud.io/projects>
- Click _plus_ in top right corner -> analyze new project
- Setup with _other CI tool_ -> _other_ -> _Linux_
- Copy `-Dsonar.projectKey=` and `-Dsonar.organization=`
    - These 2 values go to `sonar-project.properties` file
- Click pencil at bottom of `sonar-scanner` command
- Generate token and save it
- Go to repo -> _Settings_ tab -> _Secrets_ -> _Add a new secret_
    - name: `SONAR_TOKEN`
    - value: _Previously copied token_
    
## Creating Secret Tokens
Token is needed for example for _GitHub Package Registry_. To create one:

- Go to _Settings_ tab
- Click _Secrets_
- Click _Add a new secret_
    - _Name_: _name that will be accessible in GitHub Actions as `secrets.NAME`_
    - _Value_: _value_

### Resources
- [Python Project Blueprint](https://github.com/MartinHeinz/python-project-blueprint)
- [COVID-19](https://github.com/pjt3591oo/covid-19)
- <https://realpython.com/python-application-layouts/>
- <https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6>
- <https://github.com/navdeep-G/samplemod/blob/master/setup.py>
- <https://github.com/GoogleContainerTools/distroless/blob/master/examples/python3/Dockerfile>
