# Zastosowanie modelu szeregowania zadań częściowo zależnych w systemie otwartym w harmonogramowaniu danych tabelarycznych

## Kod źródłowy do pracy magisterskiej

### Sposób uruchomienia

* pobrać skrypty z folderu `mgr_client`
* uruchomić serwer (kod źródłowy w katalogu `mgr_server`, wybudowany projekt w `mgr_server\mgr_server\bin\Release\netcoreapp3.1\mgr_server.exe`), za pomocą:     
  * skorzystania z wymienionego pliku binarnego (zauważono pewne problemy z dostępem równoległym w ten sposób, perferowaną metodą jest uruchamianie za pomocą Visual Studio),
  * za pomocą uruchomienia aplikacji IIS (zgodnie z instrukcjami tutaj [Instrukcje IIS](https://docs.microsoft.com/pl-pl/aspnet/core/host-and-deploy/iis/?view=aspnetcore-3.1)),
  * za pomocą uruchomienia projektu z poziomu programu Visual Studio lub podobnego
* przygotować plik TOML zgodnie z szablonem znajdującym się w folderze `data` (można również skorzystać z gotowych plików z folderu `data\auto`)
  jeżeli nie zostanie podany prawidłowy adres serwera, program zaproponuje uszeregowanie, ale nie będzie w stanie go wykonać
* uruchomić scheduler, na przykład z linii komend, za pomocą polecenia  
  (ścieżka do folderu mgr_client)\main.py (ścieżka do przygotowanego pliku w formacie TOML)  
  np  
  `c:\git\mgr\mgr_linux\mgr_client\main.py ../data/auto/8j8m0.toml`  
