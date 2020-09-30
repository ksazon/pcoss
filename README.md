# Zastosowanie modelu szeregowania zadań częściowo zależnych w systemie otwartym w harmonogramowaniu danych tabelarycznych

## Kod źródłowy do pracy magisterskiej

### Sposób uruchomienia

* zainstalować interpreter języka `Python` w wersji nowszej niż `3.8`
* zainstalować prezentowany tutaj moduł `pcoss_scheduler_pkg`, na przykład za pomocą `pip install pcoss-scheduler-pkg-ksazon`
* przygotować plik `TOML` z problemem, zgodnie z szablonem znajdującym się w `data\sample.toml` lub skorzystać z gotowych plików z folderu `data\auto`
* uruchomić prezentowany moduł z linii komend za pomocą polecenia:  
  `python -m pcoss_scheduler_pkg "[ścieżka do przygotowanego pliku w formacie TOML]"`  
  na przykład znajdując się w katalogu `data\auto` wpisać w linii komend:
  `python -m pcoss_scheduler_pkg "8j8m0.toml"`  

Jeżeli w pliku konfiguracyjnym `TOML` opcje
* `show_conflict_graph`
* `show_result_schedule_graph`
* `show_gantt_plot`
mają wartość `true`, w trakcie działania blokująco zostaną wyświetlone, odpowiednio graf konfliktu, graf uszeregowania i wykres Gantta (ten ostatni otwiera okno przeglądarki)
