### Compare fuzzy matching libraries

Compares results from:

* thefuzz
* difflib

Script output:

```shell
----------------------------------------
item: Pyotr
thefuzz:
[('Pyotr', 100), ('Piotr', 80), ('Petr', 67), ('Peter', 60)]
difflib:
[('Pyotr', 100), ('Piotr', 80), ('Petr', 67), ('Peter', 60)]
----------------------------------------
item: Petr
thefuzz:
[('Petr', 100), ('Peter', 89), ('Pyotr', 67), ('Piotr', 67)]
difflib:
[('Petr', 100), ('Peter', 89), ('Pyotr', 67), ('Piotr', 67)]
----------------------------------------
item: Peter
thefuzz:
[('Peter', 100), ('Petr', 89), ('Pyotr', 60), ('Piotr', 60)]
difflib:
[('Peter', 100), ('Petr', 89), ('Pyotr', 60), ('Piotr', 60)]
----------------------------------------
item: Piotr
thefuzz:
[('Piotr', 100), ('Pyotr', 80), ('Petr', 67), ('Peter', 60)]
difflib:
[('Piotr', 100), ('Pyotr', 80), ('Petr', 67), ('Peter', 60)]
----------------------------------------
item: Иван
thefuzz:
[('Иван', 100), ('Иванко', 90), ('Ваня', 75), ('Ванюша', 68)]
difflib:
[('Иван', 100), ('Иванко', 80), ('Ваня', 50), ('Ванюша', 40)]
----------------------------------------
item: Иванко
thefuzz:
[('Иванко', 100), ('Иван', 90), ('Ваня', 68), ('Ванюша', 50)]
difflib:
[('Иванко', 100), ('Иван', 80), ('Ваня', 40), ('Ванюша', 33)]
----------------------------------------
item: Ваня
thefuzz:
[('Ваня', 100), ('Иван', 75), ('Иванко', 68), ('Ванюша', 68)]
difflib:
[('Ваня', 100), ('Ванюша', 60), ('Иван', 50), ('Иванко', 40)]
----------------------------------------
item: Ванюша
thefuzz:
[('Ванюша', 100), ('Иван', 68), ('Ваня', 68), ('Иванко', 50)]
difflib:
[('Ванюша', 100), ('Ваня', 60), ('Иван', 40), ('Иванко', 33)]
----------------------------------------
item: Vladimirovich
thefuzz:
[('Vladimirovich', 100),
 ('Wladymiryowich', 74),
 ('Wladimyrowitch', 74),
 ('Vladislavovich', 74)]
difflib:
[('Vladimirovich', 100),
 ('Wladymiryowich', 74),
 ('Wladimyrowitch', 74),
 ('Vladislavovich', 74)]
----------------------------------------
item: Wladymiryowich
thefuzz:
[('Wladymiryowich', 100),
 ('Wladimyrowitch', 79),
 ('Vladimirovich', 74),
 ('Vladislavovich', 57)]
difflib:
[('Wladymiryowich', 100),
 ('Wladimyrowitch', 79),
 ('Vladimirovich', 74),
 ('Vladislavovich', 57)]
----------------------------------------
item: Wladimyrowitch
thefuzz:
[('Wladimyrowitch', 100),
 ('Wladymiryowich', 79),
 ('Vladimirovich', 74),
 ('Vladislavovich', 57)]
difflib:
[('Wladimyrowitch', 100),
 ('Wladymiryowich', 79),
 ('Vladimirovich', 74),
 ('Vladislavovich', 57)]
----------------------------------------
item: Vladislavovich
thefuzz:
[('Vladislavovich', 100),
 ('Vladimirovich', 74),
 ('Wladymiryowich', 57),
 ('Wladimyrowitch', 57)]
difflib:
[('Vladislavovich', 100),
 ('Vladimirovich', 74),
 ('Wladymiryowich', 57),
 ('Wladimyrowitch', 57)]
----------------------------------------
item: Chelyabinsk, ul. Lenina, d.15, kv.33
thefuzz:
[('Chelyabinsk, ul. Lenina, d.15, kv.33', 100),
 ('Chelyabinsk, ul Lenina, 15-33', 95),
 ('Tchelabinsk Lenina 15-33', 86),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 86)]
difflib:
[('Chelyabinsk, ul. Lenina, d.15, kv.33', 100),
 ('Chelyabinsk, ul Lenina, 15-33', 86),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 78),
 ('Tchelabinsk Lenina 15-33', 70)]
----------------------------------------
item: Chelyabinsk, ul Lenina, 15-33
thefuzz:
[('Chelyabinsk, ul Lenina, 15-33', 100),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 95),
 ('Tchelabinsk Lenina 15-33', 87),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 83)]
difflib:
[('Chelyabinsk, ul Lenina, 15-33', 100),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 86),
 ('Tchelabinsk Lenina 15-33', 83),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 74)]
----------------------------------------
item: Tchelabinsk Lenina 15-33
thefuzz:
[('Tchelabinsk Lenina 15-33', 100),
 ('Chelyabinsk, ul Lenina, 15-33', 87),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 86),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 86)]
difflib:
[('Tchelabinsk Lenina 15-33', 100),
 ('Chelyabinsk, ul Lenina, 15-33', 83),
 ('Tchelabinsk ulitsa Lenina d 15 kv 33', 77),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 70)]
----------------------------------------
item: Tchelabinsk ulitsa Lenina d 15 kv 33
thefuzz:
[('Tchelabinsk ulitsa Lenina d 15 kv 33', 100),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 86),
 ('Tchelabinsk Lenina 15-33', 86),
 ('Chelyabinsk, ul Lenina, 15-33', 83)]
difflib:
[('Tchelabinsk ulitsa Lenina d 15 kv 33', 100),
 ('Chelyabinsk, ul. Lenina, d.15, kv.33', 78),
 ('Tchelabinsk Lenina 15-33', 77),
 ('Chelyabinsk, ul Lenina, 15-33', 74)]
----------------------------------------
item: Харьков, Волонтерская 72, кв. 42
thefuzz:
[('Харьков, Волонтерская 72, кв. 42', 100),
 ('Харьков, ул. Волонтерская д.72, кв.42', 95),
 ('Волонтерская 72/42, Харьков', 95),
 ('Харьков, ул. Валонтерская 72-42', 86)]
difflib:
[('Харьков, Волонтерская 72, кв. 42', 100),
 ('Харьков, ул. Волонтерская д.72, кв.42', 90),
 ('Харьков, ул. Валонтерская 72-42', 79),
 ('Волонтерская 72/42, Харьков', 58)]
----------------------------------------
item: Харьков, ул. Волонтерская д.72, кв.42
thefuzz:
[('Харьков, ул. Волонтерская д.72, кв.42', 100),
 ('Харьков, Волонтерская 72, кв. 42', 95),
 ('Волонтерская 72/42, Харьков', 95),
 ('Харьков, ул. Валонтерская 72-42', 88)]
difflib:
[('Харьков, ул. Волонтерская д.72, кв.42', 100),
 ('Харьков, Волонтерская 72, кв. 42', 90),
 ('Харьков, ул. Валонтерская 72-42', 85),
 ('Волонтерская 72/42, Харьков', 59)]
----------------------------------------
item: Харьков, ул. Валонтерская 72-42
thefuzz:
[('Харьков, ул. Валонтерская 72-42', 100),
 ('Харьков, ул. Волонтерская д.72, кв.42', 88),
 ('Харьков, Волонтерская 72, кв. 42', 86),
 ('Волонтерская 72/42, Харьков', 86)]
difflib:
[('Харьков, ул. Валонтерская 72-42', 100),
 ('Харьков, ул. Волонтерская д.72, кв.42', 85),
 ('Харьков, Волонтерская 72, кв. 42', 79),
 ('Волонтерская 72/42, Харьков', 55)]
----------------------------------------
item: Волонтерская 72/42, Харьков
thefuzz:
[('Волонтерская 72/42, Харьков', 100),
 ('Харьков, Волонтерская 72, кв. 42', 95),
 ('Харьков, ул. Волонтерская д.72, кв.42', 95),
 ('Харьков, ул. Валонтерская 72-42', 86)]
difflib:
[('Волонтерская 72/42, Харьков', 100),
 ('Харьков, Волонтерская 72, кв. 42', 64),
 ('Харьков, ул. Волонтерская д.72, кв.42', 59),
 ('Харьков, ул. Валонтерская 72-42', 55)]
n=10000, thefuzz: 0.723324883, difflib: 0.5580252579999999
n=10000, thefuzz: 1.053837108, difflib: 0.3932262620000002
n=10000, thefuzz: 0.722236037, difflib: 1.0575971510000004
n=10000, thefuzz: 1.6385437390000002, difflib: 2.0771567740000005
n=10000, thefuzz: 1.0495511209999986, difflib: 1.6632040000000003
```