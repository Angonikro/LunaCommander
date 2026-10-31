# Changelog

## 0.6.57
- Sortiermodus (Kriterium und auf-/absteigend) wird jetzt dauerhaft für linkes und rechtes Dateifenster separat gespeichert und nach einem Neustart wiederhergestellt.

## 0.6.56

- Sortiermodus wird für jedes Dateifenster separat beibehalten. Aktualisieren sortiert nicht mehr automatisch wieder nach Name.
- Markierte lokale Dateien und Ordner können per Drag-and-drop aus beiden Dateifenstern in andere Dateimanager oder auf den Desktop gezogen werden.
- Mehrfachauswahl wird als gemeinsamer Datei-URL-Transfer exportiert; Archivansichten und Remote-Verbindungen bleiben vom lokalen Drag-and-drop ausgeschlossen.
- Standardaktion ist Kopieren; das Zielprogramm kann je nach Dateimanager und Modifikatortaste eine passende Aktion anbieten.


## 0.6.54
- Das Kontextmenü „Öffnen mit“ schlägt passende installierte Programme automatisch abhängig vom Dateityp vor.
- Gespeicherte Programmwahl wird pro Dateiendung zuerst vorgeschlagen; die Zuordnung bleibt in den LunaCommander-Einstellungen erhalten.
- „Andere Anwendung auswählen…“ bleibt jederzeit verfügbar; die systemweiten Dateizuordnungen werden nicht verändert.
- Versionsangaben und Installationsanleitung für ZIP und DEB aktualisiert.

## 0.6.53
- Added browser-style mouse Back/Forward side-button navigation with separate history per pane.

0.6.52
- Added a localized “Open with” submenu to the right-click menu for local files. Choose an executable from the system to open the selected file.
- Updated the new menu labels in German, English, French, Italian and Dutch.

## 0.6.51
- Ergänzt eigene, kompakte Symbole für Audio-, Video-, Dokument-, Tabellen-, Präsentations-, Disc-Image-, Code-, Untertitel-, Paket- und Torrent-Dateien.
- Bestehende Bild-Miniaturen sowie Archiv- und DEB-Symbole bleiben unverändert.
- Versionsanzeige in der Anwendung und Paketmetadaten aktualisiert.

## 0.6.50
- Eigenes rotes DEB-Symbol für `.deb`-Installationspakete ergänzt.
- Das Symbol erscheint in beiden Dateifenstern und bleibt auch bei aktivierten Foto-Miniaturen sichtbar.
- Kein zusätzliches Icon-Paket erforderlich.

## 0.6.49
- Auf Basis der vom Nutzer bereitgestellten Version 0.6.47 neu aufgebaut.
- Startordner-Wiederherstellung und Standardpfadlogik aus 0.6.47 unverändert übernommen.
- Foto-Miniaturen werden in Hintergrund-Threads dekodiert und skaliert.
- Fehler beim Lesen einzelner Dateimetadaten brechen das Laden eines gesamten Ordners nicht mehr ab.
- Veraltete Miniatur-Aufträge werden beim Ordnerwechsel verworfen.

## 0.6.48
- Laden und Skalieren der Foto-Miniaturen in Hintergrund-Threads verlegt.
- Die Dateiliste zeigt zunächst Platzhalter; Vorschaubilder erscheinen nach und nach, ohne die Bedienoberfläche während der Bilddecodierung zu blockieren.
- Veraltete Miniatur-Aufträge werden nach einem Ordnerwechsel ignoriert.
- Verzeichnis-Metadaten werden pro Eintrag nur einmal gelesen, statt Dateigröße und Änderungszeit mehrfach separat abzufragen.

## 0.6.47
- Foto-Vorschau vollständig in die Dateiliste verlegt: Bilder erscheinen als erkennbare 72×72-Pixel-Miniaturen direkt neben dem Dateinamen.
- Separate Vorschaufläche unter der Dateiliste entfernt.
- Einstellung zum Ein-/Ausschalten bleibt erhalten und ist in Deutsch, Englisch, Französisch, Italienisch und Niederländisch beschriftet.
- Ordner- und Archivsymbole bleiben erhalten und werden bei aktivierten Miniaturen kompakt in der größeren Symbolfläche zentriert.

## 0.6.46
- Optionale Foto-Vorschau unter Einstellungen ergänzt.
- Bei Auswahl eines Bildes wird im jeweiligen Dateifenster unter der Dateiliste eine skalierte Vorschau angezeigt.
- Unterstützte Formate: JPG, JPEG, PNG, GIF, BMP, WebP, TIFF und AVIF (abhängig von den Qt-Bildplugins).
- Vorschau ist standardmäßig ausgeschaltet und wird in den Einstellungen dauerhaft gespeichert.
- Beschriftungen in Deutsch, Englisch, Französisch, Italienisch und Niederländisch.

## 0.6.45
- Einstellung zum Ein- und Ausblenden versteckter Dateien und Ordner ergänzt.
- Versteckte Einträge (Namen mit Punkt am Anfang) sind standardmäßig ausgeblendet.
- Die Einstellung wird gespeichert und aktualisiert beide Dateifenster sofort nach dem Ändern.
- Beschriftung in Deutsch, Englisch, Französisch, Italienisch und Niederländisch.

## 0.6.44
- Eigene Symbole für ZIP, RAR, 7Z und TAR-Archive ergänzt; alle TAR-Kompressionsvarianten verwenden dasselbe Symbol.
- Archivsymbole erscheinen in beiden Dateifenstern und beim Durchsuchen von Archiven.
- Symbole werden direkt mit Qt gezeichnet; keine zusätzlichen Bilddateien oder Icon-Themes erforderlich.

## 0.6.43
- Mehrfach-Löschen arbeitet jetzt als ein einzelner Batch-Hintergrundjob statt mehrere Löschjobs über die Warteschlange zu verketten.
- Alle markierten Einträge werden nacheinander abgearbeitet; Fehler bei einzelnen Einträgen verhindern die übrigen Löschversuche nicht.
- Fortschritt bezieht sich auf die gesamte Auswahl; nach Abschluss wird das Dateifenster neu geladen.

## 0.6.42
- Mehrfach-Löschen repariert: alle markierten Einträge werden gesammelt und mit einer einzigen Bestätigungsabfrage gelöscht.
- Fenster- und Info-Version auf 0.6.42 aktualisiert.

## 0.6.41\n- Löschen verarbeitet jetzt alle mit STRG/SHIFT markierten Dateien und Ordner statt nur des aktuellen Eintrags.\n- Vor dem Löschen mehrerer Einträge erscheint eine gemeinsame Bestätigungsabfrage mit Anzahl.\n- Mehrfach markierte Untereinträge werden beim Löschen eines ebenfalls markierten übergeordneten Ordners nicht doppelt eingeplant.\n\n## 0.6.40
- README neu strukturiert: klarer, direkt kopierbarer `sudo apt install`-Befehl für die ZIP-Installation.
- ZIP-Installation mit konkreten Entpack-, Verzeichniswechsel- und Startbefehlen dokumentiert.
- DEB-Installation und Start separat und eindeutig beschrieben.

## 0.6.39\n- README vollständig überarbeitet: Voraussetzungen sowie Installation und Start direkt aus dem ZIP-Quellcode ohne DEB ergänzt.\n- Veraltete und widersprüchliche Installationshinweise entfernt.\n\n## 0.6.38\n- Infofenster ergänzt: Unter „LunaCommander 0.6.38 – Qt6“ wird zentriert „Goldisoft 2026“ angezeigt.\n\n## 0.6.37
- Vollständiges, scrollbar aufgebautes Hilfefenster statt der bisherigen Platzhalteranzeige.
- Hilfe vollständig auf Deutsch, Englisch, Französisch, Italienisch und Niederländisch.
- Erläutert Dateifenster, STRG-/SHIFT-Auswahl, Dateiaktionen, Archive, FTP/FTPS/SFTP, Einstellungen und Funktionstasten.

## 0.6.36
- STRG-/SHIFT-Auswahl korrigiert: Modifier werden beim Mausdruck erfasst und beim Klick zusätzlich über Qt abgefragt.
- Modifier-Klick öffnet auch bei Einfachklick-Modus keine Datei oder keinen Ordner.
- Mehrfachauswahl bleibt beim Rechtsklick auf bereits markierte Einträge erhalten.

## 0.6.35
- STRG- und SHIFT-Klick markieren Dateien und Ordner auch bei aktivem Einfachklick-Öffnen, ohne den Eintrag versehentlich zu öffnen.
- Rechtsklick auf eine bereits markierte Zeile erhält die Mehrfachauswahl für Aktionen wie gemeinsames Packen.
- Tabellenzeilen werden als ganze Zeile markiert.

## 0.6.34
- Korrektur: In den Einstellungen gibt es nur noch eine gemeinsame TAR-Programmzeile für TAR, TAR.GZ, TAR.XZ und TAR.BZ2.
- Versionsanzeige in der Anwendung auf 0.6.34 korrigiert.

## 0.6.33
- Einstellungen vereinfacht: TAR, TAR.GZ, TAR.XZ und TAR.BZ2 teilen sich eine gemeinsame TAR-Programmzeile.
- Alle TAR-Formate verwenden denselben konfigurierten TAR-Programmpfad.

## 0.6.32
- Archiv-Erstellung ausschließlich über externe Programme: ZIP, RAR, 7-Zip, TAR, TAR.GZ, TAR.XZ und TAR.BZ2.
- Alle Archivprogramme zentral in den Einstellungen konfigurierbar; Programmpfade werden gespeichert und Installationsstatus angezeigt.
- Keine interne Python-Archiv-Erstellung mehr für neue Archive.

## 0.6.30
- RAR executable is auto-detected and can be configured manually in Settings.
- Added RAR archive creation through the configured RARLAB binary; no hard RAR package dependency is added.

# Changelog

## 0.6.31
- Fixed RAR archive paths: creation now runs in the selected item’s parent directory and passes only the item basename.
- Prevents absolute paths such as `/home/pi/...` from being stored inside newly created RAR archives.
- Updated application, VERSION, README, changelog and Debian package version to 0.6.31.


## 0.6.29
- Fixed startup crash: initialize the default interface language before translating the initial window title.
- Load the saved interface language only after configuration is read; then refresh all translated UI elements as before.
- Updated application, VERSION, README, changelog and Debian package version to 0.6.29.


## 0.6.28
- Vollständige Überarbeitung der sichtbaren Benutzeroberflächen-Texte für Deutsch, Englisch, Französisch, Italienisch und Niederländisch.
- Archiv-Kontextmenü, Entpack-Aktionen, Suchdialoge, Verbindungsdialoge, Löschbestätigung, Konfliktdialoge, Statusmeldungen und Übertragungswarteschlange lokalisiert.
- Sortiermenü (Name, Datum, Größe, Typ sowie auf-/absteigend) in allen fünf Sprachen.
- Einstellungen: Programmbeschreibungen und RAR-Hinweise verwenden die gewählte Sprache.
- Versionsnummer in App-Fenster, VERSION, Changelog, README und Debian-Paket auf 0.6.28 aktualisiert.

## 0.6.27
- Fixed the Settings dialog buttons: OK/Cancel captions are now set explicitly for each interface language, so the German interface no longer inherits English Qt button labels.

- Name sorting now keeps normal folders first, dot-folders next, and files last; ascending/descending applies within each group.

# Changelog

## 0.6.23
- Fixed F2 so it opens the File menu instead of only focusing the menu bar.
- Fixed F5/F6 function-key handling when a file pane has focus.
- Active pane now follows keyboard selection, focus, and mouse interaction.
- Added a clear status message when copy/move is invoked without a selected entry.

# LunaCommander 0.6.22

- Replaced the width-by-size-hint top QToolBar layout with 14 equal-stretch Qt tool buttons.
- The top action row now fills the full available width at all window sizes; no empty right-hand gap remains.
- Preserved the 24 px icons, existing button height, labels, translations and action callbacks.
- Kept the 0.6.21 three permanently visible transfer queue rows and navigation controls.

# Changelog

## 0.6.19
- Restore the original 0.6.17 toolbar icon size and button proportions.
- Slightly reduce only toolbar spacing and horizontal button padding so Settings fits; labels and icons remain full-size.
- Keep the F1–F10 row and all other layout dimensions unchanged.

0.6.16
- Added German/English text labels to all top toolbar actions.
- Changed the toolbar layout to show icons above their bilingual labels.

# Changelog

## 0.6.15
- Replaced emoji toolbar and function-key symbols with consistent native Qt icons.
- Kept the exact F1–F10 mapping and improved button spacing and legibility.
- Reduced the transfer queue from four to three visible entries.
- Each transfer now occupies one compact row with its label and progress bar side by side.
- Reserved all three queue rows at startup so the complete queue area is visible immediately.

# Changelog

## 0.6.14
- Redesigned the Qt6 toolbar with clearer action symbols and improved spacing.
- Reworked the F1–F10 function-key bar with the correct mapping: F1 Help, F2 Menu, F3 View, F4 Edit, F5 Copy, F6 Move, F7 New Folder, F8 Delete, F9 Settings, F10 Exit.
- Moved the transfer queue below the function-key bar to match the requested layout.
- Increased the default window size and improved button styling for better readability.


## 0.6.13
- Archive deletion now runs as a background queue task instead of blocking the main window.
- F5/F6 transfers support copy and move between archives and normal folders, including archive-to-archive transfers for supported formats.
- Move operations remove the source only after the destination copy succeeds.
- Archive operations continue to refresh the affected panes when complete.

# Changelog

## 0.6.12
- Added deletion of selected files and complete folders directly inside ZIP and TAR/TAR.GZ/TAR.XZ/TAR.BZ2 archives.
- Archive contents are rewritten safely to a temporary file; all other entries are preserved.
- Added 7z entry deletion through the installed 7-Zip command. RAR modification remains unsupported with Debian's free tools.
- After deletion, the current archive folder is refreshed in place.


## 0.6.11
- Added copying local files and folders into an archive opened in the destination pane (F5).
- ZIP archives are extended directly; TAR/TAR.GZ/TAR.XZ/TAR.BZ2 archives are safely rebuilt while preserving existing entries.
- Prevents accidental replacement of existing archive entries and keeps the archive view open after copying.
- Delete confirmation now uses explicit German buttons „Ja“ and „Nein“ instead of system-default English labels.
- Deleting entries from inside an archive is blocked with a German explanation.

## 0.6.10
- Fixed copying files and folders directly from an open archive to the other pane.
- Archive member paths are now read from ZIP/TAR streams (and 7z extraction streams), not treated as ordinary filesystem paths.
- Preserves the archive view after a successful transfer. Moving archive contents is rejected with a clear message; copy is supported.

# Changelog

## 0.6.2
- Dateifenster nutzen den verfügbaren Platz; größere Dateisymbole und Zeilen.
- Einfach- oder Doppelklick zum Öffnen wieder in Einstellungen auswählbar und gespeichert.

# Changelog

## 0.6.1
- Restored the Midnight Commander-style F1–F10 function bar.
- Restored the full toolbar actions and added Settings and Help menus.
- Added F1–F10 application-wide shortcuts.
- Added basic local filename search and a theme settings dialog.

## 0.6.3
- Recursive folder transfers between local folders and FTP/FTPS/SFTP locations.
- Increased transfer queue display height by one row.

## 0.6.4
- Run local and FTP/FTPS/SFTP folder and file transfers in a background worker so the Qt interface remains responsive.
- Add queued transfer status rows and increase the transfer queue area by one row.
- Merge copied folders into an existing destination folder instead of failing with Errno 17.

## 0.6.5
- Fixed transfer queue growth by retaining only the four most recent task rows.
- Ask before overwriting existing destinations: merge, replace, skip or cancel.
- FTP/FTPS/SFTP connection dialog now labels its action button 'Verbinden'.

## 0.6.5
- Keep the transfer queue at a fixed height and show only the four most recent jobs.
- Ask what to do when a destination already exists: merge, replace, skip or cancel.
- Run clipboard paste/cut operations in the background as well as pane-to-pane transfers.
- Use an explicit "Verbinden" button in FTP, FTPS and SFTP dialogs.

## 0.6.6
- Added live percentage progress bars to each visible transfer queue entry.
- Progress is calculated from total file sizes for local, FTP, FTPS and SFTP transfers, including recursive folder copies.

## 0.6.7
- Context-menu archive creation: ZIP, TAR.GZ, TAR.XZ and TAR.BZ2.
- Integrated extraction for ZIP and TAR formats with path traversal protection.
- Optional RAR/7z extraction through installed 7zip/unar/unrar backend.
- Settings show the default text application and archive handling backends.


## 0.6.9
- Added Debian Trixie runtime dependencies for 7zip, unar and unrar-free.
- Added 7z archive creation.
- Prefer unar/unrar-free for RAR extraction because Debian's free 7zip build omits the proprietary RAR decoder.
- Updated README with exact APT dependencies and RAR support notes.

## 0.6.9
- Archive files open inside the active LunaCommander pane according to the configured single-/double-click setting.
- ZIP and TAR-family contents are browsable in the pane; folders inside archives can be navigated without launching an archive manager.
- 7z contents are listed internally through the installed 7-Zip command-line backend.
- Opening a file member extracts it to the LunaCommander cache and opens that file with its associated viewer/editor.

## 0.6.17
- Replaced the mixed German/English toolbar captions with a real interface language selector.
- Added separate German, English, French, Italian and Dutch labels.
- Switching language updates toolbar actions, menus, F1–F10, pane headers, navigation buttons and archive context menus immediately.
- The selected language is saved in the user configuration.


## 0.6.21
- The transfer queue now displays three permanent rows from application startup, even when no operation is running.
- Queue rows are reused for later operations instead of being created only after a transfer starts.
- Reworked both panes' navigation controls with consistent Qt back, up and home icons, compact button sizing and localized tooltips.
- Preserved the existing dual-pane layout, toolbar sizing and F1–F10 function bar.

## 0.6.24
- Einstellungen: getrennte Standardordner für linkes und rechtes Dateifenster.
- Optionales Wiederherstellen der zuletzt geöffneten lokalen Ordner beim Start.
- Ungültige oder nicht mehr vorhandene gespeicherte Pfade fallen auf den jeweiligen Standardordner zurück.
- Pfade werden in ~/.config/lunacommander/settings.json gespeichert.

## 0.6.25
- Added a context-menu sorting submenu for name, date, size, and type.
- Each sort criterion supports ascending and descending order.
- Sorting labels are translated in German, English, French, Italian, and Dutch.
- Parent-folder entry remains at the top while sorting.
