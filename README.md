### Compare fuzzy matching libraries

Compares results from:

* thefuzz
* difflib
* fonetika / soundex
* fonetika / metaphone

Script output:

```shell
----------------------------------------
word: Pyotr
thefuzz: [('Piotr', 80), ('Petr', 67), ('Peter', 60)]
difflib: [('Piotr', 80), ('Petr', 67), ('Peter', 60)]
soundex: [('Petr', 100), ('Piotr', 100), ('Peter', 91)]
metaphone: [('Piotr', 80), ('Petr', 67), ('Peter', 60)]
----------------------------------------
word: Иван
thefuzz: [('Иванко', 90), ('Ваня', 75), ('Ванюша', 68)]
difflib: [('Иванко', 80), ('Ваня', 50), ('Ванюша', 40)]
soundex: [('Иванко', 83), ('Ваня', 60), ('Ванюша', 50)]
metaphone: [('Иванко', 90), ('Ваня', 75), ('Ванюша', 68)]
----------------------------------------
word: Vladimirovich
thefuzz: [('Wladymiryowich', 74), ('Wladimyrowitch', 74), ('Vladislavovich', 74)]
difflib: [('Wladymiryowich', 74), ('Wladimyrowitch', 74), ('Vladislavovich', 74)]
soundex: [('Vladislavovich', 81), ('Wladymiryowich', 78), ('Wladimyrowitch', 75)]
metaphone: [('Wladymiryowich', 74), ('Wladimyrowitch', 74), ('Vladislavovich', 74)]
----------------------------------------
word: Chelyabinsk, ul. Lenina, d.15, kv.33
thefuzz: [('Chelyabinsk, ul Lenina, 15-33', 95), ('Tchelabinsk Lenina 15-33', 86), ('Tchelabinsk ulitsa Lenina d 15 kv 33', 86)]
difflib: [('Chelyabinsk, ul Lenina, 15-33', 86), ('Tchelabinsk ulitsa Lenina d 15 kv 33', 78), ('Tchelabinsk Lenina 15-33', 70)]
soundex: [('Chelyabinsk, ul Lenina, 15-33', 95), ('Tchelabinsk Lenina 15-33', 86), ('Tchelabinsk ulitsa Lenina d 15 kv 33', 85)]
metaphone: [('Chelyabinsk, ul Lenina, 15-33', 95), ('Tchelabinsk Lenina 15-33', 86), ('Tchelabinsk ulitsa Lenina d 15 kv 33', 86)]
----------------------------------------
word: Харьков, Волонтерская 72, кв. 42
thefuzz: [('Харьков, ул. Волонтерская д.72, кв.42', 95), ('Волонтерская 72/42, Харьков', 95), ('Харьков, ул. Валонтерская 72-42', 86)]
difflib: [('Харьков, ул. Волонтерская д.72, кв.42', 90), ('Харьков, ул. Валонтерская 72-42', 79), ('Волонтерская 72/42, Харьков', 58)]
soundex: [('Харьков, ул. Волонтерская д.72, кв.42', 95), ('Харьков, ул. Валонтерская 72-42', 90), ('Волонтерская 72/42, Харьков', 69)]
metaphone: [('Харьков, ул. Волонтерская д.72, кв.42', 95), ('Волонтерская 72/42, Харьков', 95), ('Харьков, ул. Валонтерская 72-42', 90)]
```

### Running on the full set of data

```json
<function _calculate_similarity at 0x13c622e18> took 1:47:29.879752
```

This needs to be parallelized.