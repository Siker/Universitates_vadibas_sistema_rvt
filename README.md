# Universitates_vadibas_sistema_rvt
Mēs izstrādāsim konsoles programmu, kas simulē skolas vadības sistēmu, kur var pārvaldīt studentus, pasniedzējus un kursus. Lietotāji varēs reģistrēties kursos, apskatīt grafiku un saņemt vērtējumus. Sistēma ļaus organizēt mācību procesu un uzglabāt pamatinformāciju par studijām.

## Funkcionalitāte
  
- Studenta pievienošana
- Paskatīt visus studentus
- Skatīt informāciju par studentu
- Rediģet studentu
- Dzēst studentu
- Pieveinot pasniedzēju
- Skatīt visus pasniedzējus
- Dzēst pasniedzēju
- Pievienot kursu
- Skatīt visus kursus
- Rediģēt kursu
- Meklēt kursu pēc nosaukuma
- Reģistrēt studentu kursā
- Dzēst kursu
- Pievienot atzīmi
- Rediģēt atzīmi
- Aprēķināt vidējo atzīmi
- Pievienot grafiku
- Skatīt grafiku
- Skatīt datus
- Iziet

## Datu bāze

Ir izmantota MySql

tiek glabāti:

 - studenta dati
 - pasniedzēja dati
 - kursi
 - atzimes 
 - grafiki

 ## Tehnoloģijas

 - GitHub
 - Python
 - MySql
 - Trello
 - Visual Studio Code

 ## Svarīgi

 1. Instalēt pedejo python versiju uz datoru
 2. Parbaudīt, ka kopā ar python ir instalēta pip sistēma(Lai parbaudīt : "pip help"). Ja būs kļuda tad jāinstalēt ar komandu "python3 get-pip.py" 
 3. Instalēt MySql pip install mysql-connector-python

## Ka atvērt programmu

1. Lejupladēt no Github visus failus vienā mapē
2. Atvērt mapi VSCode vai terminalā
3. Uzrakstīt "python main.py" vai "python3 main.py"

## Ka izmantot programmu

Būs uzraksīts, ka atrast informāciju par visu

### Studenti

1. Uzspiediet "1" un "ENTER"
    - 1. Pievienot studentu
    - 2. Skatīt visus studentus
    - 3. Skatīt studenta info (kursi + atzīmes)
    - 4. Rediģēt studentu
    - 5. Dzēst studentu
    - 0. Atpakaļ
    Lai izdarītu darbību jāuzspiediet ciparu un "ENTER"

### Pasniedzēji

2. Uzspiediet "2" un "ENTER"
    - 1. Pievienot pasniedzēju
    - 2. Skatīt visus pasniedzējus
    - 3. Dzēst pasniedzēju
    - 0. Atpakaļ
    Lai izdarītu darbību jāuzspiediet ciparu un "ENTER"

### Kursi
3. Uzspiediet "3" un "ENTER"
    - 1. Pievienot kursu
    - 2. Skatīt visus kursus
    - 3. Rediģēt kursu
    - 4. Meklēt kursu pēc nosaukuma
    - 5. Reģistrēt studentu kursā
    - 6. Dzēst studentu
    - 0. Atpakaļ
    Lai izdarītu darbību jāuzspiediet ciparu un "ENTER"

### Atzīmes

4. Uzspiediet "4" un "ENTER"
    - 1. Pievienot atzīmi
    - 2. Rediģēt atzīmi
    - 3. Aprēķināt vidējo atzīmi
    - 0. Atpakaļ
    Lai izdarītu darbību jāuzspiediet ciparu un "ENTER"

### Grafiks

5. Uzspiediet "5" un "ENTER"
    - 1. Pievienot grafiku
    - 2. Skatīt grafiku
    - 0. Atpakaļ
    Lai izdarītu darbību jāuzspiediet ciparu un "ENTER"

### Saglabāt datus

    Lai saglabātu datus jāuzspiediet "6" un "ENTER"

### Iziet

    Lai izietu jāuzspiediet "0" un "ENTER"
