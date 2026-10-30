# LunaCommander 0.6.43

LunaCommander ist ein zweispaltiger Dateimanager für Debian 13 (Trixie) und Raspberry Pi OS auf ARM64.

## Funktionen

- Zwei Dateifenster mit unabhängiger Navigation.
- Dateien und Ordner markieren: **STRG + Linksklick** für einzelne Einträge, **SHIFT + Linksklick** für einen zusammenhängenden Bereich.
- Dateien und Ordner erstellen, kopieren, verschieben, löschen (auch mehrere markierte Einträge gemeinsam), umbenennen und Eigenschaften anzeigen.
- FTP-, FTPS- und SFTP-Verbindungen.
- Archive erstellen: ZIP, RAR, 7z, TAR, TAR.GZ, TAR.XZ und TAR.BZ2.
- Archive entpacken und unterstützte Archive im Dateifenster durchsuchen.
- Externe Archivprogramme unter **Einstellungen → Archivprogramme** konfigurieren. TAR, TAR.GZ, TAR.XZ und TAR.BZ2 verwenden gemeinsam den Programmeintrag **TAR**.
- Dunkles/helles Farbschema, Deutsch, Englisch, Französisch, Italienisch und Niederländisch.
- Einzel- oder Doppelklick zum Öffnen sowie getrennte Startordner.
- F1–F10 für Hilfe, Menü, Anzeigen, Bearbeiten, Kopieren, Verschieben, Neuer Ordner, Löschen, Einstellungen und Beenden.

## Optionale RAR-Unterstützung

Für das Erstellen von RAR-Archiven wird das externe RARLAB-Programm `rar` benötigt. Es ist keine freie Standardabhängigkeit von Debian und wird deshalb nicht automatisch installiert. Wenn `rar` vorhanden ist, erkennt LunaCommander es automatisch. Andernfalls kann der vollständige Programmpfad unter **Einstellungen → Archivprogramme → RAR** eingetragen werden.

## Speicherort der Einstellungen

Persönliche Einstellungen wie Sprache, Farbschema, Klickverhalten und Startordner werden hier gespeichert:

```text
~/.config/lunacommander/settings.json

---

# Installation mit DEB-Paket

Wenn du stattdessen das Debian-Paket verwenden möchtest, lade `lunacommander_0.6.43_all.deb` herunter. Öffne ein Terminal im Download-Ordner und führe aus:

```bash
sudo apt update
sudo apt install ./lunacommander_0.6.43_all.deb
```

APT installiert die im DEB-Paket angegebenen Abhängigkeiten automatisch.

## LunaCommander nach der DEB-Installation starten

Über den Eintrag **LunaCommander** im Anwendungsmenü oder im Terminal:

```bash
lunacommander
```

# Installation ohne DEB (ZIP-Version)

Diese Anleitung installiert die benötigten Systempakete und startet LunaCommander direkt aus dem entpackten ZIP-Ordner. **Dafür wird kein DEB-Paket und kein pip benötigt.**

## 1. Abhängigkeiten installieren

Terminal öffnen und diesen Befehl vollständig kopieren:

```bash
sudo apt update
sudo apt install -y python3 python3-pyside6.qtwidgets python3-paramiko xdg-utils zip tar gzip xz-utils bzip2 7zip unar unrar-free
```

## 2. ZIP herunterladen und entpacken

Wenn die ZIP-Datei im Ordner `Downloads` liegt:

```bash
mkdir -p ~/Programme
unzip ~/Downloads/LunaCommander_0.6.43_GITHUB.zip -d ~/Programme
```

## 3. In den Programmordner wechseln

```bash
cd ~/Programme/lunacommander
```

Falls du das ZIP in einen anderen Ordner entpackt hast, passe den Pfad entsprechend an. In diesem Ordner muss die Datei `main.py` liegen.

## 4. LunaCommander starten

```bash
python3 main.py
```

Zum späteren erneuten Starten genügt wieder:

```bash
cd ~/Programme/lunacommander
python3 main.py
```

## Technische Hinweise

- Das DEB-Paket installiert LunaCommander unter `/usr/share/lunacommander`.
- Der Startbefehl des DEB-Pakets lautet `lunacommander`.
- Debian-Paketarchitektur: `all`.
- Es wird keine virtuelle Python-Umgebung angelegt.
- Bei der ZIP-Version startet `python3 main.py` die Anwendung direkt aus dem Quellverzeichnis.
- Während der Installation wird kein `pip` ausgeführt.

## Integrierte Hilfe

Mit **F1** oder über das Menü **Hilfe** öffnest du die Bedienungsanleitung. Sie ist in Deutsch, Englisch, Französisch, Italienisch und Niederländisch verfügbar.

73 de DO2QG Andreas
