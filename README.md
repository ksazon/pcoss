# Zastosowanie modelu szeregowania zadań częściowo zależnych w systemie otwartym w harmonogramowaniu danych tabelarycznych

## Kod źródłowy do pracy magisterskiej

### Sposób uruchomienia

* zainstalować interpreter Python w wersji nowszej niż 3.8
* zainstalować moduł `pcoss_scheduler_pkg`, na przykład za pomocą `pip install pcoss-scheduler-pkg-ksazon`
* uruchomić serwer (kod źródłowy w katalogu `mgr_server`, wybudowany projekt w `mgr_server\mgr_server\bin\Release\netcoreapp3.1\`), za pomocą:     
  * uruchomienia aplikacji IIS na systemie Windows Server (zgodnie z instrukcjami tutaj [Instrukcje IIS](https://docs.microsoft.com/pl-pl/aspnet/core/host-and-deploy/iis/?view=aspnetcore-3.1)),
  * za pomocą uruchomienia projektu z poziomu programu Visual Studio 2019 lub innego IDE obsługującego framework .Net Core w wersji 3.1
* przygotować plik TOML zgodnie z szablonem znajdującym się w `data\sample.toml` (można również skorzystać z gotowych plików z folderu `data\auto`)  
  jeżeli nie zostanie podany prawidłowy adres serwera, program zaproponuje uszeregowanie, ale nie będzie w stanie go wykonać
* uruchomić scheduler, na przykład z linii komend, za pomocą polecenia 
  `python -m pcoss_scheduler_pkg "[ścieżka do przygotowanego pliku w formacie TOML]"`  
  np  
  `python -m pcoss_scheduler_pkg "8j8m0.toml"`  
