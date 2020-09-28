# Zastosowanie modelu szeregowania zadań częściowo zależnych w systemie otwartym w harmonogramowaniu danych tabelarycznych

## Kod źródłowy do pracy magisterskiej

### Sposób uruchomienia

* pobrać skrypty z folderu `mgr_client`
* uruchomić serwer (kod źródłowy w katalogu `mgr_server`, wybudowany program w ), albo za pomocą uruchomienia IIS serwera, zgodnie z instrukcjami tutaj https://docs.microsoft.com/pl-pl/aspnet/core/host-and-deploy/iis/?view=aspnetcore-3.1, lub też za za pomocą uruchomienia aplikacji z poziomu progamu Visual Studio lub podobnego
* przygotować plik TOML zgodnie z szablonem znajdującym się w
* uruchomić scheduler, na przykłąd z linii komend, za pomocą polecenie
  (ścieżka do folderu mgr_client)\main.py (nazwa przygotowanego pliku w formacie TOML)
