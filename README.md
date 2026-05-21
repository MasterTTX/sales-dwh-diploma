# Sales Data Warehouse \& ETL Pipeline

# 

# First educational ETL/Data Warehouse project made during Data Engineering diploma study

# 

# Project Overview

# 

# Этот проект я делал как дипломную работу по направлению Data Engineering.

# Это мой первый полноценный проект, где я пытался самостоятельно построить ETL pipeline и небольшое аналитическое хранилище данных.

# 

# Главная цель проекта - понять базовую архитектуру Data Warehouse, попробовать работу с ETL и научиться строить простой data pipeline от CSV файла до BI dashboard.

# 

# В качестве источника данных использовался датасет supermarket\_sales.

# 

# Project Features

# PostgreSQL Data Warehouse

# ETL pipeline на Python

# staging / NDS / DDS / marts layers

# Apache Airflow orchestration

# Data Quality checks

# Tableau dashboard

# Docker infrastructure

# Architecture

# Data Flow

# CSV -> staging -> NDS -> DDS -> marts -> Tableau

# Layers

# Layer	Description

# staging	слой загрузки сырых данных

# nds	нормализованное хранилище

# dds	dimensional model (star schema)

# marts	аналитические представления

# etl	логирование и metadata

# Technology Stack

# 

# Во время проекта я использовал:

# 

# Python

# pandas

# PostgreSQL

# SQLAlchemy

# Apache Airflow

# Docker Compose

# Tableau Public

# 

# Некоторые технологии я изучал прямо по ходу разработки, потому что раньше не работал с полноценным ETL pipeline.

# 

# Data Warehouse Structure

# Staging

# staging.sales\_raw

# NDS

# nds.branches

# nds.product\_lines

# nds.customer\_segments

# nds.payment\_methods

# nds.sales

# DDS

# dds.dim\_date

# dds.dim\_time

# dds.dim\_store

# dds.dim\_product\_line

# dds.dim\_customer\_segment

# dds.dim\_payment\_method

# dds.fct\_sales

# Marts

# marts.v\_sales\_analytics

# ETL Pipeline

# ETL Flow

# CSV -> staging -> NDS -> DDS -> marts

# ETL Scripts

# src/etl/load\_to\_staging.py

# src/etl/load\_nds.py

# src/etl/load\_dds.py

# src/etl/load\_marts.py

# ETL Execution Order

# load\_to\_staging

# \-> dq\_staging

# \-> load\_nds

# \-> dq\_nds

# \-> load\_dds

# \-> dq\_dds

# \-> load\_marts

# Data Quality Checks

# 

# В проекте были добавлены простые проверки качества данных:

# 

# NULL checks

# duplicate invoice\_id checks

# foreign key checks

# numeric validation

# quantity validation

# revenue validation

# 

# Некорректные записи сохраняются в:

# 

# etl.dq\_rejected\_records

# 

# Так как это учебный проект, проверки сделаны в базовом варианте.

# 

# Metadata \& Logging

# 

# Для логирования ETL процессов были созданы таблицы:

# 

# etl.etl\_runs

# etl.etl\_run\_steps

# etl.dq\_rejected\_records

# 

# В них хранится:

# 

# история запусков

# статусы pipeline

# количество обработанных строк

# ошибки Data Quality

# Airflow Orchestration

# 

# Airflow DAG:

# 

# airflow/dags/sales\_dwh\_etl\_dag.py

# 

# Tasks:

# 

# load\_to\_staging

# run\_staging\_dq

# load\_nds

# run\_nds\_dq

# load\_dds

# run\_dds\_dq

# load\_marts

# 

# Airflow использовался для:

# 

# orchestration ETL pipeline

# task dependencies

# monitoring

# scheduling

# 

# Это был мой первый опыт работы с Apache Airflow, поэтому DAG сделан достаточно простым.

# 

# Tableau Dashboard

# 

# В Tableau был создан dashboard с основной аналитикой продаж.

# 

# Dashboard включает:

# 

# Revenue Trend by Date

# Revenue by Product Line

# Revenue by Branch

# 

# Также были добавлены KPI:

# 

# Total Revenue

# Total Sales

# Average Customer Rating

# 

# Workbook:

# 

# tableau/workbook/Sales\_Analytics\_Dashboard.twbx

# Architecture Decisions

# 

# Во время проекта были выбраны следующие решения:

# 

# использована star schema для аналитики

# ETL реализован как full refresh

# marts layer сделан через SQL views

# incremental loading пока не реализован

# SCD Type 2 не реализован

# 

# Некоторые вещи специально не усложнялись, потому что проект учебный и делался впервые.

# 

# Project Structure

# sales-dwh-diploma/

# ├── airflow/

# ├── data/

# ├── diagrams/

# ├── docker/

# ├── sql/

# ├── src/

# ├── tableau/

# ├── docker-compose.yml

# ├── requirements.txt

# └── README.md

# Running the Project

# 1\. Clone repository

# git clone <repository\_url>

# cd sales-dwh-diploma

# 2\. Start infrastructure

# docker compose build

# docker compose up -d

# 3\. Open Airflow

# http://localhost:8080

# 

# Login:

# 

# admin / admin

# 4\. Run ETL Pipeline

# 

# Запуск DAG:

# 

# sales\_dwh\_etl\_dag

# Validation Queries

# SELECT COUNT(\*) FROM staging.sales\_raw;

# 

# SELECT COUNT(\*) FROM nds.sales;

# 

# SELECT COUNT(\*) FROM dds.fct\_sales;

# 

# SELECT SUM(sales\_count)

# FROM marts.v\_sales\_analytics;







# Future Improvements

# Что можно улучшить в будущем:

# 

# incremental loading

# SCD Type 2

# CI/CD

# cloud deployment

# more Data Quality checks

# Result

# 

# Во время выполнения проекта я получил первый практический опыт:

# 

# построения ETL pipeline

# работы с PostgreSQL

# проектирования Data Warehouse

# работы с Apache Airflow

# создания BI dashboard

# реализации Data Quality checks

# 

# Проект помог мне лучше понять основы Data Engineering и архитектуру аналитических систем.

