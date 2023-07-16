#### **Project description:**
This application is designed to automate functions and
increasing the speed of decision-making by a specialist conducting
calculations of the predicted power shortage in the energy district,
limited to a certain number of transmission lines. 
---
#### **Initial data:**
Hourly values of the forecast consumption of the energy district
and possible transfers of power to neighboring power systems (located
specialist in the folder initial_data), the value of the planned generation of power plants
generating companies and industrial enterprises and the planned network layout
(entered by a specialist through the graphical interface of the application).
Tables of values for the maximum allowable power flows along the lines supplying
energy district (contain the dependences of the values ​​of permissible flows on the network scheme
and outdoor temperature in 5°C increments). For application access to tables
dependencies, a database is created using the SQLite DBMS.
___
#### **Forecast period:**
Day x-1, x-2 (tomorrow, the day after tomorrow).
___
#### **Calculation mechanism:**
The calculation of the predicted power deficit values is carried out on the basis of
raw data received from the user and hourly temperature forecasts
outside air obtained through the API. Additionally, interpolation is carried out
values of the maximum allowable flows with the transition to a temperature change step of 1°C.
The calculation is carried out for each hour of the planned day.
___
#### **Results:**
As a result, the specialist receives a table with hourly values
power deficit in the energy district for the planned day. Based on table data
the specialist makes decisions on further planning of the electric
power system networks (such as: increasing the generation capacity of power plants by
the planned period, a ban on putting power transmission lines into repair,
change in the composition of points of the normal section with adjacent power systems, etc.).
