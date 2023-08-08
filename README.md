# Постановка на расписание задачи парсинга сайта и заполнения БД 

В рамках задания поднят docker-compose [файл](https://github.com/PolarJaba/1st_airflow_dag/blob/main/docker-compose.yml), содержащий контейнеры postgres и airflow.

Через веб-интерфейс airflow созданно подключение:

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/conn.PNG)

Со следующими параметрами:

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/conn_parameters.PNG)

Создан [dag](https://github.com/PolarJaba/1st_airflow_dag/blob/main/airflow/dags/rates.py) для получения курсов биткоина к рублю каждые 10 минут и записи значений в таблицу базы данных postgres, в коде предусмотрено создание переменной:

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/variables.PNG)

В результате получена таблица:

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/table.PNG)

<i>Прим. согласно третьему пункту задания, в Dag'е также предусмотрен таск, выводящий фразу "Good morning, my diggers!", при помощи BashOperator.</i> 

<i>Прим.2. создание таблицы в БД вынесено как отдельный таск внутри питоновского скрипта.</i>

![image](https://github.com/PolarJaba/1st_airflow_dag/blob/main/3-3/graph.PNG)
