# TCP Logger

Программа на Python, которая собирает информацию о трафике и количестве подключений.

## Установка

```bash
git clone https://github.com/Eldar-Z/tcplogger
```

## Использование

Используя make:
```bash
запуск программы--
make run

запуск тестирования--
make test
```

Без использования make:
```bash
запуск программы (аргументы берутся из файла config.txt)--
python3 main.py

запуск программы со своими аргументами--
python3 main.py <период> <название_файла.csv>

запуск тестирования--
python3 test.py <период> <количество_отправляемых_байт>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
