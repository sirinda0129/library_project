# CONTRIBUTE

## Подготовка к работе

### Подготовка к работе через `pipenv`

1. Установить необходимые пакеты Python в систему 
    ```bash
    pip install pipenv
    ```
1. Активировать виртуальное окружение
    ```bash
    pipenv shell
    ```
1. Установить зависимости (включая зависимости времени разработки)
    ```bash
    pipenv install --dev
    ```
1. Обновить зависимости (используются при сборке контейнера)
    ```bash
    pipenv lock -r > requirements.txt
    pipenv lock -r --dev > requirements_dev.txt
    ```
1. Настроить IDE для работы с виртуальным окружением. Так как `pipenv`
создает вируальное окружение за пределами проекта, то его можно найти командой
    ```
   pipenv --venv
    ```

### Подготовка к работе через `virtualenv`

TODO

## Развертывание на сервере

Разветывание выполняется с использованием `Ansible`. В процессе выполнения
потребуется установка зависимостей времени разработки (файл `requirements_dev`).
На сервере развертывается копия `git` репозитория и собирается новый Docker-образ.
После чего Docker-контейнер с приложением перезапускается. В процессе развертывания
будет запрошен пароль для зашифрованных файлов, содержащих секретную информацию.
Пароль необходимо ввести с клавиатуры.

```bash
cd .deploy/
ansible-playbook -i inventory playbook.yml
```