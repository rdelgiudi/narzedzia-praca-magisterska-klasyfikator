# Repozytorium narzędzi użytych do realizacji pracy magisterskiej
Zestaw narzędzi użyty w mojej pracy magisterskiej.

## Realsense Recorder
Program nagrywający zsynchronizowany obraz koloru oraz głębi z kamery RealSense.

### Uruchamianie
Aby uruchomić, wystarczy wpisać w wiersz poleceń następującą komendę:
```
python recorder.py
```
~~UWAGA! Przed pierwszym uruchomieniem należy stworzyć folder o nazwie "videos" znajdujący się w tym samym folderze co skrypty. Do poprawienia w następnej iteracji programu.~~ Nieaktualne.

### Instalacja
Aby poprawnie działać, program wymaga bibliotek: NumPy, PyQt5, OpenCV, pyrealsense2 (wrapper oraz samo SDK).

Poprawność działania testowana jedynie w Ubuntu.

#### Uwagi przy kompilacji ze źródła:

Program testowany przy kompilacji realsense za pomocą następujących flag:

```
cmake -DBUILD_EXAMPLES=true -DBUILD_CV_EXAMPLES=true -DBUILD_PYTHON_BINDINGS:bool=true -DCMAKE_BUILD_TYPE=Release
```

##### Dotyczy tylko Linuxa (a dokładniej pochodne Debiana):
Problemy związane z kompilacją typu brak biblioteki X, można rozwiązać instalując libx-dev z apt. Przykład:

Otrzymujemy błąd braku biblioteki OpenCV, w shell wpisujemy:

```
sudo apt install libopencv-dev
```

#### Inne problemy:

TODO

## Data Extractor
Program do wydobywania klatek, aby zebrać dataset. Program wycina 120 kolejnych klatek obrazu oraz zapisuje w formie pliku .avi oraz jako seria obrazów .jpg.

## Model Training and Misc
Zestaw narzędzi zawierający skrypt trenujący oraz inne pomniejsze narzędzia.
