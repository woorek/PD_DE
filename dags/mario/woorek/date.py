from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
import pendulum

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
	'owner': 'pd24',
	'depends_on_past': True,
	'start_date': datetime(year=2023, month=6, day=1, hour=0, minute=0, tzinfo=local_tz),
	'retries':0,
}

dag = DAG(
	dag_id = 'date-test',
	description = 'pd24 date test',
	tags = ['sqoop', 'hive'],
	schedule_interval = '10 8 * * *',
	user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
	default_args = default_args
)

check_execute_task = BashOperator(
    task_id='check.execute',
    bash_command="""
        echo "date                            => `date`"
        echo "logical_date                    => {{logical_date}}"
        echo "execution_date                  => {{execution_date.strftime("%Y-%m-%d %H:%M:%S")}}"
        echo "next_execution_date             => {{next_execution_date.strftime("%Y-%m-%d %H:%M:%S")}}"
        echo "prev_execution_date             => {{prev_execution_date.strftime("%Y-%m-%d %H:%M:%S")}}"
        echo "local_dt(execution_date)        => {{local_dt(execution_date)}}"
        echo "local_dt(next_execution_date)   => {{local_dt(next_execution_date)}}"
        echo "local_dt(prev_execution_date)   => {{local_dt(prev_execution_date)}}"
        echo "===================================================================="
        echo "data_interval_start             => {{data_interval_start}}"
        echo "data_interval_end               => {{data_interval_end}}"
        echo "ds => {{ds}}"
        echo "ds_nodash => {{ds_nodash}}"
        echo "ds_nodash => {{ds_nodash}}"
        echo "ts  => {{ts}}"
        echo "ts_nodash_with_tz  => {{ts_nodash_with_tz}}"
        echo "prev_data_interval_start_success  => {{prev_data_interval_start_success}}"
        echo "prev_data_interval_end_success => {{prev_data_interval_end_success}}"
        echo "prev_data_interval_end_success => {{prev_data_interval_end_success}}"
        echo "prev_start_date_success => {{prev_start_date_success}}"
        echo "dag => {{dag}}"
        echo "task => {{task}}"
        echo "macros => {{macros}}"
        echo "task_instance => {{task_instance}}"
        echo "ti => {{ti}}"
        echo "====================================================================="
        echo "dag_run.logical_date => {{dag_run.logical_date}}"
        echo "execution_date => {{execution_date}}"
        echo "====================================================================="
        #2020-11-11 형식의 날짜 반환
        echo "exe_kr = {{execution_date.add(hours=9).strftime("%Y-%m-%d")}}"
        #20201212 형식의 날짜 반환
        echo "exe_kr_nodash = {{execution_date.add(hours=9).strftime("%Y%m%d")}}"
        #2020-11-11 형식의 날짜 반환 + 한달 더하기
        echo "exe_kr_add_months = {{execution_date.add(hours=9).add(months=1).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 + 하루 더하기
        echo "exe_kr_add_days = {{execution_date.add(hours=9).add(days=1).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 - 일주일 빼기
        echo "exe_kr_a_week_ago = {{execution_date.add(hours=9).add(days=-7).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 - 한달 빼기
        echo "exe_kr_a_month_ago = {{execution_date.add(hours=9).add(months=-1).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 - 1년 빼기
        echo "exe_kr_1_year_ago = {{execution_date.add(hours=9).add(years=-1).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 - 2년 빼기
        echo "exe_kr_2_year_ago = {{execution_date.add(hours=9).add(years=-2).strftime("%Y-%m-%d")}}"
        #2020-11-11 형식의 날짜 반환 - 하루 빼기
        echo "exe_kr_yesterday = {{execution_date.add(hours=9).add(days=-1).strftime("%Y-%m-%d")}}"
        echo "====================================================================="

        """
    ,
    dag=dag
)

check_execute_task

