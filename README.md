# Постановка на расписание задачи парсинга сайта и заполнения БД 

В рамках задания поднят docker-compose [файл](https://github.com/PolarJaba/1st_airflow_dag/blob/main/docker-compose.yml), содержащий контейнеры postgres и airflow.

При подключении к контейнеру postgres написан запрос на создание таблицы для сбора данных:
![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/create_table.PNG)

Создан [dag](https://github.com/PolarJaba/1st_airflow_dag/blob/main/airflow/dags/rates.py) для получения курсов биткоина к рублю каждые 10 минут и записи значений в таблицу базы данных postgres.

В результате получена таблица:

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/table.PNG)

<i>Прим. согласно третьему пункту задания, в Dag'е также предусмотрен таск, выводящий фразу "Good morning, my diggers!", при помощи BashOperator.</i> 
