#!/usr/bin/python3
"""LunaCommander Qt6 edition."""
import os, sys, json, shutil, stat, ftplib, posixpath, threading, zipfile, tarfile, subprocess, mimetypes
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QSize, QObject, Signal, QRunnable, QThreadPool, QEvent, QPoint, QProcess, QMimeData, QUrl
from PySide6.QtGui import QAction, QKeySequence, QIcon, QCursor, QPixmap, QImage, QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QSplitter,QLineEdit,QPushButton,QTreeWidget,QTreeWidgetItem,QMenu,QInputDialog,QMessageBox,QFileDialog,QLabel,QProgressBar,QToolBar,QToolButton,QSizePolicy,QDialog,QFormLayout,QComboBox,QDialogButtonBox,QCheckBox,QStyle,QProgressBar,QHBoxLayout,QVBoxLayout,QAbstractItemView,QTextBrowser)




def archive_icon(filename):
    """Return a distinctive built-in icon for supported archive formats."""
    name=str(filename).lower()
    if name.endswith('.deb'):
        kind, color = 'DEB', QColor('#b83232')
    elif name.endswith('.zip'):
        kind, color = 'ZIP', QColor('#2878c8')
    elif name.endswith('.rar'):
        kind, color = 'RAR', QColor('#7852a9')
    elif name.endswith('.7z'):
        kind, color = '7z', QColor('#278b67')
    elif name.endswith(('.tar', '.tar.gz', '.tgz', '.tar.xz', '.txz',
                        '.tar.bz2', '.tbz2', '.tbz', '.tar.zst', '.tzst')):
        kind, color = 'TAR', QColor('#bd782c')
    else:
        return QIcon()

    pix = QPixmap(28, 28)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(QPen(QColor('#d9e5ef'), 1))
    if kind == 'RAR':
        # Three offset archive books with a visible binding strap.
        painter.setBrush(QColor('#563b83'))
        painter.drawRoundedRect(4, 4, 19, 7, 2, 2)
        painter.setBrush(QColor('#8b65b5'))
        painter.drawRoundedRect(3, 10, 21, 7, 2, 2)
        painter.setBrush(QColor('#b18ad2'))
        painter.drawRoundedRect(5, 16, 19, 7, 2, 2)
        painter.setPen(QPen(QColor('#f5e8c8'), 2))
        painter.drawLine(10, 4, 10, 23)
        painter.setPen(QPen(QColor('#38264f'), 1))
        painter.drawLine(10, 4, 10, 23)
    else:
        painter.setBrush(color)
        painter.drawRoundedRect(4, 2, 20, 24, 3, 3)
        painter.setPen(QPen(QColor('#ffffff'), 1))
        painter.drawLine(8, 7, 20, 7)
        painter.drawLine(8, 10, 20, 10)
        if kind == 'DEB':
            # Distinct Debian package: red package face with a clear DEB label.
            painter.setPen(QPen(QColor('#ffe7e7'), 1))
            painter.setFont(QFont('Sans', 6, QFont.Bold))
            painter.drawText(5, 21, 'DEB')
            painter.setPen(QPen(QColor('#ffd0d0'), 1))
            painter.drawLine(8, 13, 20, 13)
        elif kind == 'ZIP':
            painter.setPen(QPen(QColor('#f5d76e'), 2))
            painter.drawLine(14, 12, 14, 23)
            painter.setPen(QPen(QColor('#fff2b8'), 1))
            for y in (13, 17, 21):
                painter.drawPoint(14, y)
        elif kind == '7z':
            painter.setPen(QPen(QColor('#ffffff'), 1))
            painter.setFont(QFont('Sans', 7, QFont.Bold))
            painter.drawText(6, 21, '7z')
        else:
            painter.setPen(QPen(QColor('#fff1d7'), 1))
            painter.setFont(QFont('Sans', 6, QFont.Bold))
            painter.drawText(6, 21, 'TAR')
    painter.end()
    return QIcon(pix)


def filetype_icon(filename):
    """Draw a recognizable, compact icon for common non-image file types."""
    ext=Path(str(filename).lower()).suffix
    groups={
      'audio': {'.mp3','.wav','.flac','.ogg','.opus','.m4a','.aac','.wma','.aiff','.aif','.ape','.alac','.mid','.midi','.amr','.ac3','.dts','.dsf','.wv'},
      'video': {'.mp4','.mkv','.avi','.mov','.wmv','.webm','.mpeg','.mpg','.m4v','.ts','.mts','.m2ts','.flv','.vob','.ogv','.3gp'},
      'pdf': {'.pdf'},
      'document': {'.doc','.docx','.odt','.rtf','.txt','.md','.epub','.mobi'},
      'sheet': {'.xls','.xlsx','.ods','.csv'},
      'slide': {'.ppt','.pptx','.odp'},
      'disc': {'.iso','.img','.cue','.bin'},
      'code': {'.py','.sh','.desktop','.js','.html','.css','.json','.xml','.yml','.yaml'},
      'subtitle': {'.srt','.ass','.ssa','.sub','.idx'},
      'package': {'.rpm','.appimage','.exe'},
      'torrent': {'.torrent'},
    }
    kind=next((k for k,v in groups.items() if ext in v),None)
    if not kind: return QIcon()
    colors={'audio':'#2479bd','video':'#8b4bb5','pdf':'#c43b3b','document':'#3978b9','sheet':'#27845b','slide':'#c47732','disc':'#64748b','code':'#397f83','subtitle':'#6574a8','package':'#a45d32','torrent':'#558b45'}
    labels={'audio':'♪','video':'▶','pdf':'PDF','document':'DOC','sheet':'XLS','slide':'PPT','disc':'ISO','code':'</>','subtitle':'SUB','package':'PKG','torrent':'TOR'}
    pix=QPixmap(32,32); pix.fill(Qt.transparent)
    q=QPainter(pix); q.setRenderHint(QPainter.Antialiasing,True)
    q.setPen(QPen(QColor('#e8edf2'),1)); q.setBrush(QColor(colors[kind])); q.drawRoundedRect(3,2,26,28,4,4)
    q.setPen(QColor('white'))
    if kind=='audio':
        q.setPen(QPen(QColor('white'),2.5)); q.drawLine(18,7,18,22); q.drawLine(18,8,25,6); q.setBrush(QColor('white')); q.drawEllipse(10,19,9,7); q.drawEllipse(18,17,9,7)
    elif kind=='video':
        q.setBrush(QColor('white')); q.setPen(Qt.NoPen); q.drawPolygon([QPoint(11,8),QPoint(24,16),QPoint(11,24)])
    else:
        q.setFont(QFont('Sans',6 if len(labels[kind])>3 else 8,QFont.Bold)); q.drawText(pix.rect(),Qt.AlignCenter,labels[kind])
    q.end(); return QIcon(pix)


TRANSLATIONS = {
'de': {'open_with':'Öffnen mit','choose_application':'Andere Anwendung auswählen…','application_filter':'Programme','app_launch_error':'Die ausgewählte Anwendung konnte nicht gestartet werden.','rar_binary': 'RAR-Programm (rar)','rar_auto': 'Automatisch gefunden','rar_browse': 'RAR-Datei auswählen…','rar_missing': 'RAR-Programm nicht gefunden. Bitte in den Einstellungen den Pfad zu rar eintragen.','create_rar': 'RAR-Archiv erstellen','open':'Öffnen','back':'Zurück','up':'Eine Ebene höher','home':'Startordner','name':'Name','type':'Typ','size':'Größe','folder':'Ordner','file':'Datei','ready':'Bereit','queue':'Übertragungswarteschlange','new':'Neu','copy':'Kopieren','move':'Verschieben','delete':'Löschen','rename':'Umbenennen','properties':'Eigenschaften','refresh':'Aktualisieren','archive':'Archiv','ftp':'FTP','sftp':'SFTP','ftps':'FTPS','disconnect':'Trennen','search':'Suchen','settings':'Einstellungen','help':'Hilfe','menu':'Menü','view':'Anzeigen','edit':'Bearbeiten','new_folder':'Neuer Ordner','exit':'Beenden','file_menu':'Datei','connection':'Verbindung','view_menu':'Ansicht','theme':'Design wechseln','about':'Über LunaCommander','single':'Einfachklick zum Öffnen','double':'Doppelklick zum Öffnen','open_mode':'Dateien und Ordner öffnen','language':'Sprache','scheme':'Farbschema','dark':'Dunkel','light':'Hell','ok':'OK','cancel':'Abbrechen','connect':'Verbinden','server':'Server','port':'Port','user':'Benutzer','password':'Passwort','open_other':'In anderem Fenster öffnen','move_other':'In anderes Fenster verschieben','cut':'Ausschneiden','paste':'Einfügen','new_file':'Neue Datei','pack':'Packen','create_zip':'ZIP-Archiv erstellen','create_targz':'TAR.GZ-Archiv erstellen','create_tarxz':'TAR.XZ-Archiv erstellen','create_tarbz2':'TAR.BZ2-Archiv erstellen','create_7z':'7z-Archiv erstellen','remember_dirs':'Letzte Ordner beim Start wiederherstellen','default_left':'Standardordner links','default_right':'Standardordner rechts','browse':'Durchsuchen…','start_folders':'Startordner','show_hidden':'Versteckte Dateien und Ordner anzeigen','photo_preview':'Bild-Miniaturansichten in der Dateiliste anzeigen','no_photo_preview':'Kein Foto ausgewählt','sort':'Sortieren','sort_by':'Sortieren nach','sort_name':'Name','sort_date':'Datum','sort_size':'Größe','sort_type':'Typ','ascending':'Aufsteigend','descending':'Absteigend'},
'en': {'open_with':'Open with','choose_application':'Choose another application…','application_filter':'Applications','app_launch_error':'The selected application could not be started.','rar_binary': 'RAR executable','rar_auto': 'Automatically detected','rar_browse': 'Select RAR executable…','rar_missing': 'RAR executable not found. Set the path to rar in Settings.','create_rar': 'Create RAR archive','open':'Open','back':'Back','up':'Up one level','home':'Home folder','name':'Name','type':'Type','size':'Size','folder':'Folder','file':'File','ready':'Ready','queue':'Transfer queue','new':'New','copy':'Copy','move':'Move','delete':'Delete','rename':'Rename','properties':'Properties','refresh':'Refresh','archive':'Archive','ftp':'FTP','sftp':'SFTP','ftps':'FTPS','disconnect':'Disconnect','search':'Search','settings':'Settings','help':'Help','menu':'Menu','view':'View','edit':'Edit','new_folder':'New folder','exit':'Exit','file_menu':'File','connection':'Connection','view_menu':'View','theme':'Toggle theme','about':'About LunaCommander','single':'Single-click to open','double':'Double-click to open','open_mode':'Open files and folders','language':'Language','scheme':'Color scheme','dark':'Dark','light':'Light','ok':'OK','cancel':'Cancel','connect':'Connect','server':'Server','port':'Port','user':'User','password':'Password','open_other':'Open in other pane','move_other':'Move to other pane','cut':'Cut','paste':'Paste','new_file':'New file','pack':'Create archive','create_zip':'Create ZIP archive','create_targz':'Create TAR.GZ archive','create_tarxz':'Create TAR.XZ archive','create_tarbz2':'Create TAR.BZ2 archive','create_7z':'Create 7z archive','remember_dirs':'Restore last folders at startup','default_left':'Default folder (left)','default_right':'Default folder (right)','browse':'Browse…','start_folders':'Startup folders','show_hidden':'Show hidden files and folders','photo_preview':'Show image thumbnails in the file list','no_photo_preview':'No photo selected','sort':'Sort','sort_by':'Sort by','sort_name':'Name','sort_date':'Date','sort_size':'Size','sort_type':'Type','ascending':'Ascending','descending':'Descending'},
'fr': {'open_with':'Ouvrir avec','choose_application':'Choisir une autre application…','application_filter':'Applications','app_launch_error':'Impossible de démarrer l’application sélectionnée.','rar_binary': 'Exécutable RAR','rar_auto': 'Détecté automatiquement','rar_browse': 'Choisir l’exécutable RAR…','rar_missing': 'Exécutable RAR introuvable. Indiquez son chemin dans les paramètres.','create_rar': 'Créer une archive RAR','open':'Ouvrir','back':'Retour','up':'Niveau supérieur','home':'Dossier personnel','name':'Nom','type':'Type','size':'Taille','folder':'Dossier','file':'Fichier','ready':'Prêt','queue':'File de transferts','new':'Nouveau','copy':'Copier','move':'Déplacer','delete':'Supprimer','rename':'Renommer','properties':'Propriétés','refresh':'Actualiser','archive':'Archive','ftp':'FTP','sftp':'SFTP','ftps':'FTPS','disconnect':'Déconnecter','search':'Rechercher','settings':'Paramètres','help':'Aide','menu':'Menu','view':'Afficher','edit':'Modifier','new_folder':'Nouveau dossier','exit':'Quitter','file_menu':'Fichier','connection':'Connexion','view_menu':'Affichage','theme':'Changer le thème','about':'À propos de LunaCommander','single':'Clic simple pour ouvrir','double':'Double-clic pour ouvrir','open_mode':'Ouvrir fichiers et dossiers','language':'Langue','scheme':'Thème de couleurs','dark':'Sombre','light':'Clair','ok':'OK','cancel':'Annuler','connect':'Connecter','server':'Serveur','port':'Port','user':'Utilisateur','password':'Mot de passe','open_other':'Ouvrir dans l’autre panneau','move_other':'Déplacer vers l’autre panneau','cut':'Couper','paste':'Coller','new_file':'Nouveau fichier','pack':'Compresser','create_zip':'Créer une archive ZIP','create_targz':'Créer une archive TAR.GZ','create_tarxz':'Créer une archive TAR.XZ','create_tarbz2':'Créer une archive TAR.BZ2','create_7z':'Créer une archive 7z','remember_dirs':'Restaurer les derniers dossiers au démarrage','default_left':'Dossier par défaut (gauche)','default_right':'Dossier par défaut (droite)','browse':'Parcourir…','start_folders':'Dossiers de démarrage','show_hidden':'Afficher les fichiers et dossiers cachés','photo_preview':'Afficher les miniatures dans la liste des fichiers','no_photo_preview':'Aucune photo sélectionnée','sort':'Trier','sort_by':'Trier par','sort_name':'Nom','sort_date':'Date','sort_size':'Taille','sort_type':'Type','ascending':'Croissant','descending':'Décroissant'},
'it': {'open_with':'Apri con','choose_application':'Scegli un’altra applicazione…','application_filter':'Applicazioni','app_launch_error':'Impossibile avviare l’applicazione selezionata.','rar_binary': 'Eseguibile RAR','rar_auto': 'Rilevato automaticamente','rar_browse': 'Seleziona eseguibile RAR…','rar_missing': 'Eseguibile RAR non trovato. Imposta il percorso nelle impostazioni.','create_rar': 'Crea archivio RAR','open':'Apri','back':'Indietro','up':'Livello superiore','home':'Cartella iniziale','name':'Nome','type':'Tipo','size':'Dimensione','folder':'Cartella','file':'File','ready':'Pronto','queue':'Coda trasferimenti','new':'Nuovo','copy':'Copia','move':'Sposta','delete':'Elimina','rename':'Rinomina','properties':'Proprietà','refresh':'Aggiorna','archive':'Archivio','ftp':'FTP','sftp':'SFTP','ftps':'FTPS','disconnect':'Disconnetti','search':'Cerca','settings':'Impostazioni','help':'Aiuto','menu':'Menu','view':'Visualizza','edit':'Modifica','new_folder':'Nuova cartella','exit':'Esci','file_menu':'File','connection':'Connessione','view_menu':'Visualizza','theme':'Cambia tema','about':'Informazioni su LunaCommander','single':'Clic singolo per aprire','double':'Doppio clic per aprire','open_mode':'Apri file e cartelle','language':'Lingua','scheme':'Schema colori','dark':'Scuro','light':'Chiaro','ok':'OK','cancel':'Annulla','connect':'Connetti','server':'Server','port':'Porta','user':'Utente','password':'Password','open_other':'Apri nell’altro pannello','move_other':'Sposta nell’altro pannello','cut':'Taglia','paste':'Incolla','new_file':'Nuovo file','pack':'Crea archivio','create_zip':'Crea archivio ZIP','create_targz':'Crea archivio TAR.GZ','create_tarxz':'Crea archivio TAR.XZ','create_tarbz2':'Crea archivio TAR.BZ2','create_7z':'Crea archivio 7z','remember_dirs':'Ripristina le ultime cartelle all’avvio','default_left':'Cartella predefinita (sinistra)','default_right':'Cartella predefinita (destra)','browse':'Sfoglia…','start_folders':'Cartelle iniziali','show_hidden':'Mostra file e cartelle nascosti','photo_preview':'Mostra miniature delle immagini nell’elenco file','no_photo_preview':'Nessuna foto selezionata','sort':'Ordina','sort_by':'Ordina per','sort_name':'Nome','sort_date':'Data','sort_size':'Dimensione','sort_type':'Tipo','ascending':'Crescente','descending':'Decrescente'},
'nl': {'open_with':'Openen met','choose_application':'Andere toepassing kiezen…','application_filter':'Toepassingen','app_launch_error':'De geselecteerde toepassing kon niet worden gestart.','rar_binary': 'RAR-programma','rar_auto': 'Automatisch gevonden','rar_browse': 'RAR-programma selecteren…','rar_missing': 'RAR-programma niet gevonden. Stel het pad in bij Instellingen.','create_rar': 'RAR-archief maken','open':'Openen','back':'Terug','up':'Een niveau omhoog','home':'Thuismap','name':'Naam','type':'Type','size':'Grootte','folder':'Map','file':'Bestand','ready':'Gereed','queue':'Overdrachtwachtrij','new':'Nieuw','copy':'Kopiëren','move':'Verplaatsen','delete':'Verwijderen','rename':'Hernoemen','properties':'Eigenschappen','refresh':'Vernieuwen','archive':'Archief','ftp':'FTP','sftp':'SFTP','ftps':'FTPS','disconnect':'Verbinding verbreken','search':'Zoeken','settings':'Instellingen','help':'Help','menu':'Menu','view':'Weergeven','edit':'Bewerken','new_folder':'Nieuwe map','exit':'Afsluiten','file_menu':'Bestand','connection':'Verbinding','view_menu':'Beeld','theme':'Thema wisselen','about':'Over LunaCommander','single':'Enkele klik om te openen','double':'Dubbelklik om te openen','open_mode':'Bestanden en mappen openen','language':'Taal','scheme':'Kleurenschema','dark':'Donker','light':'Licht','ok':'OK','cancel':'Annuleren','connect':'Verbinden','server':'Server','port':'Poort','user':'Gebruiker','password':'Wachtwoord','open_other':'Openen in ander venster','move_other':'Verplaatsen naar ander venster','cut':'Knippen','paste':'Plakken','new_file':'Nieuw bestand','pack':'Archiveren','create_zip':'ZIP-archief maken','create_targz':'TAR.GZ-archief maken','create_tarxz':'TAR.XZ-archief maken','create_tarbz2':'TAR.BZ2-archief maken','create_7z':'7z-archief maken','remember_dirs':'Vorige mappen herstellen bij opstarten','default_left':'Standaardmap (links)','default_right':'Standaardmap (rechts)','browse':'Bladeren…','start_folders':'Startmappen','show_hidden':'Verborgen bestanden en mappen tonen','photo_preview':'Afbeeldingsminiaturen in de bestandslijst tonen','no_photo_preview':'Geen foto geselecteerd','sort':'Sorteren','sort_by':'Sorteren op','sort_name':'Naam','sort_date':'Datum','sort_size':'Grootte','sort_type':'Type','ascending':'Oplopend','descending':'Aflopend'}
}

# Extended translations for every visible dialog, prompt and archive action.
for _lang, _entries in {'de': {'extract_here': 'Hier entpacken', 'extract_to': 'In Ordner entpacken …', 'installed': 'Verwendete Programme und Dateiverwaltung', 'text_files': 'Textdateien', 'rar_support': 'RAR-Unterstützung', 'delete_title': 'Löschen', 'delete_confirm': '{name} wirklich löschen?', 'no': 'Nein', 'yes': 'Ja', 'deleting': 'Lösche: ', 'done': 'Fertig: ', 'error': 'Fehler: ', 'deleted': 'Gelöscht: ', 'delete_error': 'Löschfehler: ', 'size_bytes': 'Größe: {size:,} Bytes', 'path': 'Pfad: {path}', 'same_source': "'Quelle und Ziel sind identisch.'", 'server_copy_unavailable': "'Server-zu-Server-Kopieren ist nicht verfügbar.'", 'archive_local_only': 'Archivverwaltung ist derzeit nur für lokale Dateien verfügbar.', 'archive_exists': "'Archiv existiert'", 'archive_replace': "'Das Archiv existiert bereits. Ersetzen?'", 'pack_error': "'Packfehler'", 'extract_error': "'Entpackfehler'", 'open_archive_error': "'Datei im Archiv öffnen'", 'search_prompt': "'Dateiname enthält:'", 'remote_search_unavailable': "'Die Suche auf entfernten Servern ist noch nicht verfügbar.'", 'search_results': "'Suchergebnisse'", 'no_matches': "'Keine Treffer.'", 'search_error': "'Suchfehler'", 'connection_error': "'Verbindungsfehler'", 'generic_error': "'Fehler'", 'folder_name': "'Ordnername:'", 'file_name': "'Dateiname:'", 'new_name': "'Neuer Name:'", 'target_folder': "'Zielordner auswählen'", 'unsafe_archive': 'Unsicherer Archivpfad wurde blockiert.', 'unsupported_archive': 'Dieses Archivformat wird nicht unterstützt.', 'archive_missing_tool': 'Archivprogramm fehlt. Installiere unter Debian: sudo apt install 7zip unar unrar-free.', 'archive_created': 'Archiv erstellt: ', 'extracted': 'Entpackt: ', 'delete_archive_self': 'Das Archiv selbst kann hier nicht gelöscht werden.', 'delete_confirm_title': 'Löschen', 'source_target_same': "'Quelle und Ziel sind identisch.'", 'target_exists': "'Ziel existiert bereits'", 'target_exists_question': '„{name}“ ist im Ziel bereits vorhanden. Was soll passieren?', 'merge': "'Zusammenführen'", 'replace': "'Ersetzen'", 'skip': "'Überspringen'", 'cancel': 'Abbrechen', 'already_in_archive': 'Dieser Eintrag ist bereits im Archiv vorhanden. Bitte entferne ihn zuerst oder wähle einen anderen Namen.', 'remote_to_archive': 'Kopieren von FTP/SFTP direkt in ein Archiv wird derzeit nicht unterstützt.', 'archive_duplicate': 'Dieser Eintrag ist bereits im Archiv vorhanden. Bitte entferne ihn zuerst oder wähle einen anderen Namen.', 'select_entry': 'Bitte zuerst eine Datei oder einen Ordner im aktiven Fenster markieren.', 'moved': 'Verschoben: ', 'copied': 'Kopiert: ', 'transfer_error': "'Übertragungsfehler: '", 'about_version': 'LunaCommander 0.6.57 – Qt6', 'about_help': 'Hilfe'}, 'en': {'extract_here': 'Extract here', 'extract_to': 'Extract to folder…', 'installed': 'Installed programs and file handling', 'text_files': 'Text files', 'rar_support': 'RAR support', 'delete_title': 'Delete', 'delete_confirm': 'Really delete {name}?', 'no': 'No', 'yes': 'Yes', 'deleting': 'Deleting: ', 'done': 'Done: ', 'error': 'Error: ', 'deleted': 'Deleted: ', 'delete_error': 'Delete error: ', 'size_bytes': 'Size: {size:,} bytes', 'path': 'Path: {path}', 'same_source': 'Source and destination are identical.', 'server_copy_unavailable': 'Server-to-server copying is not available.', 'archive_local_only': 'Archive management is currently available for local files only.', 'archive_exists': 'Archive exists', 'archive_replace': 'The archive already exists. Replace it?', 'pack_error': 'Archive creation error', 'extract_error': 'Extraction error', 'open_archive_error': 'Open file in archive', 'search_prompt': 'Filename contains:', 'remote_search_unavailable': 'Searching remote servers is not available yet.', 'search_results': 'Search results', 'no_matches': 'No matches.', 'search_error': 'Search error', 'connection_error': 'Connection error', 'generic_error': 'Error', 'folder_name': 'Folder name:', 'file_name': 'File name:', 'new_name': 'New name:', 'target_folder': 'Select destination folder', 'unsafe_archive': 'Unsafe archive path was blocked.', 'unsupported_archive': 'This archive format is not supported.', 'archive_missing_tool': 'Archive utility missing. On Debian install: sudo apt install 7zip unar unrar-free.', 'archive_created': 'Archive created: ', 'extracted': 'Extracted: ', 'delete_archive_self': 'The archive itself cannot be deleted here.', 'delete_confirm_title': 'Delete', 'source_target_same': 'Source and destination are identical.', 'target_exists': 'Destination already exists', 'target_exists_question': '“{name}” already exists at the destination. What should happen?', 'merge': 'Merge', 'replace': 'Replace', 'skip': 'Skip', 'cancel': 'Cancel', 'already_in_archive': 'This entry already exists in the archive. Remove it first or choose another name.', 'remote_to_archive': 'Copying directly from FTP/SFTP into an archive is not supported yet.', 'archive_duplicate': 'This entry already exists in the archive. Choose another name or remove the existing entry first.', 'select_entry': 'Please select a file or folder in the active pane first.', 'moved': 'Moved: ', 'copied': 'Copied: ', 'transfer_error': 'Transfer error: ', 'about_version': 'LunaCommander 0.6.57 – Qt6', 'about_help': 'Help'}, 'fr': {'extract_here': 'Extraire ici', 'extract_to': 'Extraire dans un dossier…', 'installed': 'Programmes installés et gestion des fichiers', 'text_files': 'Fichiers texte', 'rar_support': 'Prise en charge RAR', 'delete_title': 'Supprimer', 'delete_confirm': 'Voulez-vous vraiment supprimer {name}\xa0?', 'no': 'Non', 'yes': 'Oui', 'deleting': 'Suppression\xa0: ', 'done': 'Terminé\xa0: ', 'error': 'Erreur\xa0: ', 'deleted': 'Supprimé\xa0: ', 'delete_error': 'Erreur de suppression\xa0: ', 'size_bytes': 'Taille\xa0: {size:,} octets', 'path': 'Chemin\xa0: {path}', 'same_source': 'La source et la destination sont identiques.', 'server_copy_unavailable': 'La copie de serveur à serveur n’est pas disponible.', 'archive_local_only': 'La gestion des archives est uniquement disponible pour les fichiers locaux.', 'archive_exists': 'L’archive existe', 'archive_replace': 'Cette archive existe déjà. La remplacer\xa0?', 'pack_error': 'Erreur de création d’archive', 'extract_error': 'Erreur d’extraction', 'open_archive_error': 'Ouvrir un fichier dans l’archive', 'search_prompt': 'Le nom contient\xa0:', 'remote_search_unavailable': 'La recherche sur les serveurs distants n’est pas encore disponible.', 'search_results': 'Résultats de recherche', 'no_matches': 'Aucun résultat.', 'search_error': 'Erreur de recherche', 'connection_error': 'Erreur de connexion', 'generic_error': 'Erreur', 'folder_name': 'Nom du dossier\xa0:', 'file_name': 'Nom du fichier\xa0:', 'new_name': 'Nouveau nom\xa0:', 'target_folder': 'Choisir le dossier de destination', 'unsafe_archive': 'Chemin d’archive non sûr bloqué.', 'unsupported_archive': 'Ce format d’archive n’est pas pris en charge.', 'archive_missing_tool': 'Utilitaire d’archive manquant. Sous Debian\xa0: sudo apt install 7zip unar unrar-free.', 'archive_created': 'Archive créée\xa0: ', 'extracted': 'Extrait\xa0: ', 'delete_archive_self': 'Impossible de supprimer l’archive elle-même ici.', 'delete_confirm_title': 'Supprimer', 'source_target_same': 'La source et la destination sont identiques.', 'target_exists': 'La destination existe déjà', 'target_exists_question': '«\xa0{name}\xa0» existe déjà à destination. Que faire\xa0?', 'merge': 'Fusionner', 'replace': 'Remplacer', 'skip': 'Ignorer', 'cancel': 'Annuler', 'already_in_archive': 'Cette entrée existe déjà dans l’archive. Supprimez-la ou choisissez un autre nom.', 'remote_to_archive': 'La copie directe de FTP/SFTP vers une archive n’est pas prise en charge.', 'archive_duplicate': 'Cette entrée existe déjà dans l’archive. Choisissez un autre nom ou supprimez l’entrée existante.', 'select_entry': 'Veuillez d’abord sélectionner un fichier ou un dossier dans le panneau actif.', 'moved': 'Déplacé\xa0: ', 'copied': 'Copié\xa0: ', 'transfer_error': 'Erreur de transfert\xa0: ', 'about_version': 'LunaCommander 0.6.57 – Qt6', 'about_help': 'Aide'}, 'it': {'extract_here': 'Estrai qui', 'extract_to': 'Estrai in una cartella…', 'installed': 'Programmi installati e gestione file', 'text_files': 'File di testo', 'rar_support': 'Supporto RAR', 'delete_title': 'Elimina', 'delete_confirm': 'Eliminare davvero {name}?', 'no': 'No', 'yes': 'Sì', 'deleting': 'Eliminazione: ', 'done': 'Completato: ', 'error': 'Errore: ', 'deleted': 'Eliminato: ', 'delete_error': 'Errore di eliminazione: ', 'size_bytes': 'Dimensione: {size:,} byte', 'path': 'Percorso: {path}', 'same_source': 'Origine e destinazione sono identiche.', 'server_copy_unavailable': 'La copia da server a server non è disponibile.', 'archive_local_only': 'La gestione degli archivi è disponibile solo per i file locali.', 'archive_exists': 'Archivio esistente', 'archive_replace': 'L’archivio esiste già. Sostituirlo?', 'pack_error': 'Errore di creazione archivio', 'extract_error': 'Errore di estrazione', 'open_archive_error': 'Apri file nell’archivio', 'search_prompt': 'Il nome contiene:', 'remote_search_unavailable': 'La ricerca sui server remoti non è ancora disponibile.', 'search_results': 'Risultati della ricerca', 'no_matches': 'Nessun risultato.', 'search_error': 'Errore di ricerca', 'connection_error': 'Errore di connessione', 'generic_error': 'Errore', 'folder_name': 'Nome cartella:', 'file_name': 'Nome file:', 'new_name': 'Nuovo nome:', 'target_folder': 'Seleziona cartella di destinazione', 'unsafe_archive': 'Percorso archivio non sicuro bloccato.', 'unsupported_archive': 'Questo formato di archivio non è supportato.', 'archive_missing_tool': 'Programma per archivi mancante. Su Debian: sudo apt install 7zip unar unrar-free.', 'archive_created': 'Archivio creato: ', 'extracted': 'Estratto: ', 'delete_archive_self': 'Non è possibile eliminare qui l’archivio stesso.', 'delete_confirm_title': 'Elimina', 'source_target_same': 'Origine e destinazione sono identiche.', 'target_exists': 'La destinazione esiste già', 'target_exists_question': '“{name}” esiste già nella destinazione. Cosa fare?', 'merge': 'Unisci', 'replace': 'Sostituisci', 'skip': 'Ignora', 'cancel': 'Annulla', 'already_in_archive': 'Questa voce è già presente nell’archivio. Rimuovila o scegli un altro nome.', 'remote_to_archive': 'La copia diretta da FTP/SFTP in un archivio non è supportata.', 'archive_duplicate': 'Questa voce è già presente nell’archivio. Scegli un altro nome o rimuovi quella esistente.', 'select_entry': 'Seleziona prima un file o una cartella nel pannello attivo.', 'moved': 'Spostato: ', 'copied': 'Copiato: ', 'transfer_error': 'Errore di trasferimento: ', 'about_version': 'LunaCommander 0.6.57 – Qt6', 'about_help': 'Aiuto'}, 'nl': {'extract_here': 'Hier uitpakken', 'extract_to': 'Uitpakken naar map…', 'installed': 'Geïnstalleerde programma’s en bestandsbeheer', 'text_files': 'Tekstbestanden', 'rar_support': 'RAR-ondersteuning', 'delete_title': 'Verwijderen', 'delete_confirm': '{name} echt verwijderen?', 'no': 'Nee', 'yes': 'Ja', 'deleting': 'Verwijderen: ', 'done': 'Voltooid: ', 'error': 'Fout: ', 'deleted': 'Verwijderd: ', 'delete_error': 'Verwijderfout: ', 'size_bytes': 'Grootte: {size:,} bytes', 'path': 'Pad: {path}', 'same_source': 'Bron en bestemming zijn hetzelfde.', 'server_copy_unavailable': 'Kopiëren van server naar server is niet beschikbaar.', 'archive_local_only': 'Archiefbeheer is alleen beschikbaar voor lokale bestanden.', 'archive_exists': 'Archief bestaat', 'archive_replace': 'Het archief bestaat al. Vervangen?', 'pack_error': 'Fout bij archief maken', 'extract_error': 'Uitpakfout', 'open_archive_error': 'Bestand in archief openen', 'search_prompt': 'Bestandsnaam bevat:', 'remote_search_unavailable': 'Zoeken op externe servers is nog niet beschikbaar.', 'search_results': 'Zoekresultaten', 'no_matches': 'Geen resultaten.', 'search_error': 'Zoekfout', 'connection_error': 'Verbindingsfout', 'generic_error': 'Fout', 'folder_name': 'Mapnaam:', 'file_name': 'Bestandsnaam:', 'new_name': 'Nieuwe naam:', 'target_folder': 'Doelmap selecteren', 'unsafe_archive': 'Onveilig archiefpad is geblokkeerd.', 'unsupported_archive': 'Dit archiefformaat wordt niet ondersteund.', 'archive_missing_tool': 'Archiefprogramma ontbreekt. Installeer op Debian: sudo apt install 7zip unar unrar-free.', 'archive_created': 'Archief gemaakt: ', 'extracted': 'Uitgepakt: ', 'delete_archive_self': 'Het archief zelf kan hier niet worden verwijderd.', 'delete_confirm_title': 'Verwijderen', 'source_target_same': 'Bron en bestemming zijn hetzelfde.', 'target_exists': 'Bestemming bestaat al', 'target_exists_question': '“{name}” bestaat al op de bestemming. Wat moet er gebeuren?', 'merge': 'Samenvoegen', 'replace': 'Vervangen', 'skip': 'Overslaan', 'cancel': 'Annuleren', 'already_in_archive': 'Dit item staat al in het archief. Verwijder het eerst of kies een andere naam.', 'remote_to_archive': 'Rechtstreeks kopiëren van FTP/SFTP naar een archief wordt niet ondersteund.', 'archive_duplicate': 'Dit item staat al in het archief. Kies een andere naam of verwijder het bestaande item.', 'select_entry': 'Selecteer eerst een bestand of map in het actieve deelvenster.', 'moved': 'Verplaatst: ', 'copied': 'Gekopieerd: ', 'transfer_error': 'Overdrachtsfout: ', 'about_version': 'LunaCommander 0.6.57 – Qt6', 'about_help': 'Help'}}.items():
    TRANSLATIONS[_lang].update(_entries)

for _lang, _entries in {'de': {'archive_label': 'Archiv', 'insert': 'Einfügen', 'archive_duplicate': 'Dieser Eintrag ist bereits im Archiv vorhanden. Bitte entferne ihn zuerst oder wähle einen anderen Namen.', 'remote_to_archive': 'Kopieren von FTP/SFTP direkt in ein Archiv wird derzeit nicht unterstützt.', 'select_entry': 'Bitte zuerst eine Datei oder einen Ordner im aktiven Fenster markieren.', 'archive_entries': 'Einträge', 'connected': 'verbunden', 'archive_created': 'Archiv erstellt: ', 'extracted': 'Entpackt: ', 'moved': 'Verschoben: ', 'copied': 'Kopiert: '}, 'en': {'archive_label': 'Archive', 'insert': 'Paste', 'archive_duplicate': 'This entry already exists in the archive. Remove it first or choose another name.', 'remote_to_archive': 'Copying directly from FTP/SFTP into an archive is not supported yet.', 'select_entry': 'Please select a file or folder in the active pane first.', 'archive_entries': 'entries', 'connected': 'connected', 'archive_created': 'Archive created: ', 'extracted': 'Extracted: ', 'moved': 'Moved: ', 'copied': 'Copied: '}, 'fr': {'archive_label': 'Archive', 'insert': 'Coller', 'archive_duplicate': 'Cette entrée existe déjà dans l’archive. Supprimez-la ou choisissez un autre nom.', 'remote_to_archive': 'La copie directe de FTP/SFTP vers une archive n’est pas prise en charge.', 'select_entry': 'Veuillez d’abord sélectionner un fichier ou un dossier dans le panneau actif.', 'archive_entries': 'entrées', 'connected': 'connecté', 'archive_created': 'Archive créée\xa0: ', 'extracted': 'Extrait\xa0: ', 'moved': 'Déplacé\xa0: ', 'copied': 'Copié\xa0: '}, 'it': {'archive_label': 'Archivio', 'insert': 'Incolla', 'archive_duplicate': 'Questa voce è già presente nell’archivio. Rimuovila o scegli un altro nome.', 'remote_to_archive': 'La copia diretta da FTP/SFTP in un archivio non è supportata.', 'select_entry': 'Seleziona prima un file o una cartella nel pannello attivo.', 'archive_entries': 'elementi', 'connected': 'connesso', 'archive_created': 'Archivio creato: ', 'extracted': 'Estratto: ', 'moved': 'Spostato: ', 'copied': 'Copiato: '}, 'nl': {'archive_label': 'Archief', 'insert': 'Plakken', 'archive_duplicate': 'Dit item staat al in het archief. Verwijder het eerst of kies een andere naam.', 'remote_to_archive': 'Rechtstreeks kopiëren van FTP/SFTP naar een archief wordt niet ondersteund.', 'select_entry': 'Selecteer eerst een bestand of map in het actieve deelvenster.', 'archive_entries': 'items', 'connected': 'verbonden', 'archive_created': 'Archief gemaakt: ', 'extracted': 'Uitgepakt: ', 'moved': 'Verplaatst: ', 'copied': 'Gekopieerd: '}}.items():
    TRANSLATIONS[_lang].update(_entries)

def folder_sort_key(row):
    n,d,_=row
    if n=='..': return (0,n.casefold())
    if d and not n.startswith('.'): return (1,n.casefold())
    if d: return (2,n.casefold())
    return (3,n.casefold())

class Remote:
    def __init__(self, proto, host, port, user, password):
        self.proto=proto
        if proto in ('FTP','FTPS'):
            cls=ftplib.FTP_TLS if proto=='FTPS' else ftplib.FTP
            self.client=cls(); self.client.connect(host,port,timeout=20); self.client.login(user,password)
            if proto=='FTPS': self.client.prot_p()
        else:
            import paramiko
            self.ssh=paramiko.SSHClient(); self.ssh.load_system_host_keys(); self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=host,port=port,username=user,password=password,timeout=20); self.client=self.ssh.open_sftp()
    def list(self,path):
        rows=[]
        if self.proto=='SFTP':
            for a in self.client.listdir_attr(path): rows.append((a.filename,stat.S_ISDIR(a.st_mode),a.st_size or 0))
        else:
            old=self.client.pwd()
            try:
                self.client.cwd(path)
                try:
                    for n,f in self.client.mlsd():
                        if n not in ('.','..'): rows.append((n,f.get('type')=='dir',int(f.get('size',0))))
                except Exception:
                    for n in self.client.nlst():
                        n=posixpath.basename(n.rstrip('/')) or n
                        if n in ('.','..'): continue
                        isdir=False; size=0
                        try: self.client.cwd(n); self.client.cwd('..'); isdir=True
                        except Exception:
                            try: size=self.client.size(n) or 0
                            except Exception: pass
                        rows.append((n,isdir,size))
            finally:
                try:self.client.cwd(old)
                except Exception:pass
        return sorted(rows,key=folder_sort_key)
    def mkdir(self,path):
        if self.proto=='SFTP':self.client.mkdir(path)
        else:self.client.mkd(path)
    def rmdir(self,path):
        if self.proto=='SFTP':self.client.rmdir(path)
        else:self.client.rmd(path)
    def close(self):
        try: self.client.close(); self.ssh.close() if self.proto=='SFTP' else self.client.quit()
        except Exception: pass


HELP_CONTENT = {'de': '<h1>LunaCommander – Hilfe</h1><p>Dieser Dateimanager zeigt zwei Verzeichnisse nebeneinander. So kannst du Dateien zwischen beiden Fenstern verwalten.</p>\n<h2>1. Die zwei Dateifenster</h2><ul><li>Links und rechts wird jeweils ein eigener Ordner angezeigt.</li><li>Klicke auf einen Ordner, um ihn zu öffnen. Mit „..“ gehst du eine Ebene zurück.</li><li>Über das Pfadfeld kannst du einen Pfad direkt eingeben. Die Schaltflächen daneben dienen zum Zurückgehen, eine Ebene nach oben und zum Home-Ordner.</li><li>Das aktive Fenster ist die Quelle für Dateiaktionen; das andere Fenster ist häufig das Ziel.</li></ul>\n<h2>2. Dateien und Ordner markieren</h2><ul><li>Einfacher Linksklick markiert einen Eintrag.</li><li><b>STRG + Linksklick</b>: einzelne Einträge zur Auswahl hinzufügen oder aus ihr entfernen.</li><li><b>SHIFT + Linksklick</b>: einen zusammenhängenden Bereich auswählen.</li><li>Mehrere markierte Einträge können gemeinsam über das Archiv-Menü gepackt werden. Beim Rechtsklick auf einen bereits markierten Eintrag bleibt die Auswahl erhalten.</li></ul>\n<h2>3. Dateien verwalten</h2><ul><li><b>Kopieren / Verschieben</b>: überträgt den ausgewählten Eintrag in das jeweils andere Dateifenster.</li><li><b>Ausschneiden, Kopieren, Einfügen</b>: verwendet die Zwischenablage innerhalb des Dateimanagers.</li><li><b>Neu</b>: erstellt eine Datei oder einen Ordner.</li><li><b>Umbenennen</b>: benennt den ausgewählten Eintrag um.</li><li><b>Löschen</b>: entfernt den ausgewählten Eintrag nach Rückfrage.</li><li><b>Eigenschaften</b>: zeigt Informationen zum ausgewählten Eintrag.</li><li><b>Suchen</b>: sucht im aktiven lokalen Ordner.</li></ul>\n<h2>4. Archive erstellen und entpacken</h2><ul><li>Über <b>Archiv → Packen</b> kannst du ZIP, RAR, 7z, TAR, TAR.GZ, TAR.XZ oder TAR.BZ2 erstellen.</li><li>Markiere vor dem Packen mehrere Dateien oder Ordner, um sie gemeinsam zu archivieren.</li><li>Zum Erstellen werden die externen Programme verwendet, deren Pfade unter <b>Einstellungen → Archivprogramme</b> hinterlegt sind.</li><li>TAR, TAR.GZ, TAR.XZ und TAR.BZ2 verwenden gemeinsam den Programmeintrag „TAR“.</li><li>Über „Hier entpacken“ oder „In Ordner entpacken“ kannst du unterstützte Archive extrahieren.</li><li>Ein unterstütztes Archiv kann durch Öffnen im Dateifenster durchsucht werden.</li></ul>\n<h2>5. FTP, FTPS und SFTP</h2><ul><li>Wähle FTP, FTPS oder SFTP in der oberen Leiste, um eine Serververbindung einzurichten.</li><li>Gib Serveradresse, Port und – falls erforderlich – Benutzername und Passwort ein.</li><li>Nach erfolgreicher Verbindung kannst du entfernte Dateien im aktiven Fenster durchsuchen und Dateien übertragen.</li><li>Mit „Trennen“ beendest du die Verbindung.</li></ul>\n<h2>6. Einstellungen</h2><ul><li><b>Sprache</b>: Deutsch, Englisch, Französisch, Italienisch oder Niederländisch.</li><li><b>Farbschema</b>: dunkles oder helles Design.</li><li><b>Öffnen</b>: Einfach- oder Doppelklick zum Öffnen von Dateien und Ordnern.</li><li><b>Startordner</b>: Standardordner für das linke und rechte Fenster festlegen und auf Wunsch die zuletzt verwendeten Ordner wiederherstellen.</li><li><b>Archivprogramme</b>: ausführbare Programme automatisch erkennen lassen oder den Programmpfad manuell auswählen. Der Status zeigt, ob die Datei ausführbar vorhanden ist.</li></ul>\n<h2>7. Funktionstasten</h2><ul><li><b>F1</b> Hilfe</li><li><b>F2</b> Menü</li><li><b>F3</b> Anzeigen / ausgewählten Eintrag öffnen</li><li><b>F4</b> Bearbeiten / ausgewählten Eintrag öffnen</li><li><b>F5</b> In das andere Fenster kopieren</li><li><b>F6</b> In das andere Fenster verschieben</li><li><b>F7</b> Neuen Ordner erstellen</li><li><b>F8</b> Löschen</li><li><b>F9</b> Einstellungen</li><li><b>F10</b> LunaCommander beenden</li></ul>\n<p><i>Tipp:</i> Wenn eine Aktion nicht verfügbar ist, prüfe zuerst, ob im aktiven Dateifenster ein passender Eintrag ausgewählt ist.</p>', 'en': "<h1>LunaCommander – Help</h1><p>This file manager displays two folders side by side, making it easy to manage and transfer files between them.</p>\n<h2>1. The two file panes</h2><ul><li>The left and right panes each display a separate folder.</li><li>Open a folder by clicking it. Select “..” to go up one level.</li><li>Type a path directly into the path field. The nearby buttons navigate back, up one level, or to the home folder.</li><li>The active pane is the source for file operations; the other pane is commonly the destination.</li></ul>\n<h2>2. Selecting files and folders</h2><ul><li>A normal left-click selects an item.</li><li><b>CTRL + left-click</b>: add an individual item to the selection or remove it.</li><li><b>SHIFT + left-click</b>: select a continuous range.</li><li>Multiple selected items can be archived together. Right-clicking an already selected item keeps the current selection.</li></ul>\n<h2>3. Managing files</h2><ul><li><b>Copy / Move</b>: transfer the selected item to the other file pane.</li><li><b>Cut, Copy, Paste</b>: use the file manager's clipboard.</li><li><b>New</b>: create a file or folder.</li><li><b>Rename</b>: rename the selected item.</li><li><b>Delete</b>: remove the selected item after confirmation.</li><li><b>Properties</b>: display information about the selected item.</li><li><b>Search</b>: search the active local folder.</li></ul>\n<h2>4. Creating and extracting archives</h2><ul><li>Use <b>Archive → Pack</b> to create ZIP, RAR, 7z, TAR, TAR.GZ, TAR.XZ, or TAR.BZ2 archives.</li><li>Select multiple files or folders first to put them into one archive.</li><li>Archive creation uses the external programs configured under <b>Settings → Archive programs</b>.</li><li>TAR, TAR.GZ, TAR.XZ, and TAR.BZ2 share one “TAR” program entry.</li><li>Use “Extract here” or “Extract to folder” to extract supported archives.</li><li>Open a supported archive in the file pane to browse its contents.</li></ul>\n<h2>5. FTP, FTPS, and SFTP</h2><ul><li>Choose FTP, FTPS, or SFTP in the top bar to configure a server connection.</li><li>Enter the server address, port, and username and password when required.</li><li>After connecting, browse remote files in the active pane and transfer files.</li><li>Choose “Disconnect” to close the connection.</li></ul>\n<h2>6. Settings</h2><ul><li><b>Language</b>: German, English, French, Italian, or Dutch.</li><li><b>Color scheme</b>: dark or light theme.</li><li><b>Open behavior</b>: single- or double-click to open files and folders.</li><li><b>Startup folders</b>: choose the default folder for each pane and optionally restore the last folders on startup.</li><li><b>Archive programs</b>: detect executables automatically or browse to a program path. The status indicates whether the selected file exists and is executable.</li></ul>\n<h2>7. Function keys</h2><ul><li><b>F1</b> Help</li><li><b>F2</b> Menu</li><li><b>F3</b> View / open selected item</li><li><b>F4</b> Edit / open selected item</li><li><b>F5</b> Copy to the other pane</li><li><b>F6</b> Move to the other pane</li><li><b>F7</b> Create a new folder</li><li><b>F8</b> Delete</li><li><b>F9</b> Settings</li><li><b>F10</b> Exit LunaCommander</li></ul>\n<p><i>Tip:</i> If an action is unavailable, first check that a suitable item is selected in the active file pane.</p>", 'fr': '<h1>LunaCommander – Aide</h1><p>Ce gestionnaire de fichiers affiche deux dossiers côte à côte pour faciliter la gestion et le transfert des fichiers.</p>\n<h2>1. Les deux panneaux</h2><ul><li>Les panneaux gauche et droit affichent chacun un dossier différent.</li><li>Cliquez sur un dossier pour l’ouvrir. Choisissez « .. » pour remonter d’un niveau.</li><li>Saisissez directement un chemin dans le champ correspondant. Les boutons voisins permettent de revenir en arrière, de monter d’un niveau ou d’ouvrir le dossier personnel.</li><li>Le panneau actif sert de source pour les opérations ; l’autre panneau sert généralement de destination.</li></ul>\n<h2>2. Sélectionner des fichiers et dossiers</h2><ul><li>Un clic gauche normal sélectionne un élément.</li><li><b>CTRL + clic gauche</b> : ajouter un élément à la sélection ou le désélectionner.</li><li><b>MAJ + clic gauche</b> : sélectionner une plage continue.</li><li>Plusieurs éléments sélectionnés peuvent être archivés ensemble. Un clic droit sur un élément déjà sélectionné conserve la sélection.</li></ul>\n<h2>3. Gérer les fichiers</h2><ul><li><b>Copier / Déplacer</b> : transférer l’élément sélectionné vers l’autre panneau.</li><li><b>Couper, Copier, Coller</b> : utiliser le presse-papiers du gestionnaire.</li><li><b>Nouveau</b> : créer un fichier ou un dossier.</li><li><b>Renommer</b> : renommer l’élément sélectionné.</li><li><b>Supprimer</b> : supprimer l’élément après confirmation.</li><li><b>Propriétés</b> : afficher les informations de l’élément sélectionné.</li><li><b>Rechercher</b> : rechercher dans le dossier local actif.</li></ul>\n<h2>4. Créer et extraire des archives</h2><ul><li>Utilisez <b>Archive → Compresser</b> pour créer des archives ZIP, RAR, 7z, TAR, TAR.GZ, TAR.XZ ou TAR.BZ2.</li><li>Sélectionnez plusieurs fichiers ou dossiers avant de les regrouper dans une archive.</li><li>La création utilise les programmes externes configurés dans <b>Paramètres → Programmes d’archivage</b>.</li><li>TAR, TAR.GZ, TAR.XZ et TAR.BZ2 partagent une seule entrée de programme « TAR ».</li><li>Utilisez « Extraire ici » ou « Extraire vers un dossier » pour extraire les archives prises en charge.</li><li>Ouvrez une archive prise en charge dans le panneau pour parcourir son contenu.</li></ul>\n<h2>5. FTP, FTPS et SFTP</h2><ul><li>Choisissez FTP, FTPS ou SFTP dans la barre supérieure pour configurer une connexion serveur.</li><li>Saisissez l’adresse du serveur, le port et, si nécessaire, le nom d’utilisateur et le mot de passe.</li><li>Après la connexion, parcourez les fichiers distants dans le panneau actif et transférez-les.</li><li>Choisissez « Déconnecter » pour fermer la connexion.</li></ul>\n<h2>6. Paramètres</h2><ul><li><b>Langue</b> : allemand, anglais, français, italien ou néerlandais.</li><li><b>Thème</b> : sombre ou clair.</li><li><b>Ouverture</b> : simple ou double clic pour ouvrir les fichiers et dossiers.</li><li><b>Dossiers de démarrage</b> : définir le dossier par défaut de chaque panneau et restaurer éventuellement les derniers dossiers utilisés.</li><li><b>Programmes d’archivage</b> : détecter automatiquement les exécutables ou choisir leur chemin. L’état indique si le fichier existe et est exécutable.</li></ul>\n<h2>7. Touches de fonction</h2><ul><li><b>F1</b> Aide</li><li><b>F2</b> Menu</li><li><b>F3</b> Afficher / ouvrir l’élément sélectionné</li><li><b>F4</b> Modifier / ouvrir l’élément sélectionné</li><li><b>F5</b> Copier vers l’autre panneau</li><li><b>F6</b> Déplacer vers l’autre panneau</li><li><b>F7</b> Créer un dossier</li><li><b>F8</b> Supprimer</li><li><b>F9</b> Paramètres</li><li><b>F10</b> Quitter LunaCommander</li></ul>\n<p><i>Conseil :</i> Si une action n’est pas disponible, vérifiez qu’un élément approprié est sélectionné dans le panneau actif.</p>', 'it': '<h1>LunaCommander – Guida</h1><p>Questo file manager mostra due cartelle affiancate e consente di gestire e trasferire facilmente i file tra i due pannelli.</p>\n<h2>1. I due pannelli</h2><ul><li>Il pannello sinistro e quello destro mostrano cartelle separate.</li><li>Fai clic su una cartella per aprirla. Seleziona « .. » per salire di un livello.</li><li>Puoi inserire direttamente un percorso nel campo del percorso. I pulsanti vicini consentono di tornare indietro, salire di un livello o aprire la cartella Home.</li><li>Il pannello attivo è la sorgente delle operazioni; l’altro pannello è normalmente la destinazione.</li></ul>\n<h2>2. Selezionare file e cartelle</h2><ul><li>Un normale clic sinistro seleziona un elemento.</li><li><b>CTRL + clic sinistro</b>: aggiunge un elemento alla selezione oppure lo deseleziona.</li><li><b>MAIUSC + clic sinistro</b>: seleziona un intervallo continuo.</li><li>Più elementi selezionati possono essere archiviati insieme. Il clic destro su un elemento già selezionato mantiene la selezione.</li></ul>\n<h2>3. Gestire i file</h2><ul><li><b>Copia / Sposta</b>: trasferisce l’elemento selezionato nell’altro pannello.</li><li><b>Taglia, Copia, Incolla</b>: usa gli appunti del file manager.</li><li><b>Nuovo</b>: crea un file o una cartella.</li><li><b>Rinomina</b>: rinomina l’elemento selezionato.</li><li><b>Elimina</b>: rimuove l’elemento dopo la conferma.</li><li><b>Proprietà</b>: mostra le informazioni sull’elemento selezionato.</li><li><b>Cerca</b>: cerca nella cartella locale attiva.</li></ul>\n<h2>4. Creare ed estrarre archivi</h2><ul><li>Usa <b>Archivio → Comprimi</b> per creare archivi ZIP, RAR, 7z, TAR, TAR.GZ, TAR.XZ o TAR.BZ2.</li><li>Seleziona prima più file o cartelle per inserirli nello stesso archivio.</li><li>La creazione usa i programmi esterni configurati in <b>Impostazioni → Programmi di archiviazione</b>.</li><li>TAR, TAR.GZ, TAR.XZ e TAR.BZ2 condividono un’unica voce di programma «TAR».</li><li>Usa «Estrai qui» o «Estrai in una cartella» per estrarre gli archivi supportati.</li><li>Apri un archivio supportato nel pannello per esplorarne il contenuto.</li></ul>\n<h2>5. FTP, FTPS e SFTP</h2><ul><li>Scegli FTP, FTPS o SFTP nella barra superiore per configurare una connessione al server.</li><li>Inserisci indirizzo del server, porta e, se richiesti, nome utente e password.</li><li>Dopo la connessione puoi esplorare i file remoti nel pannello attivo e trasferirli.</li><li>Seleziona «Disconnetti» per chiudere la connessione.</li></ul>\n<h2>6. Impostazioni</h2><ul><li><b>Lingua</b>: tedesco, inglese, francese, italiano o olandese.</li><li><b>Tema</b>: scuro o chiaro.</li><li><b>Apertura</b>: clic singolo o doppio per aprire file e cartelle.</li><li><b>Cartelle iniziali</b>: imposta la cartella predefinita per ciascun pannello e, se vuoi, ripristina all’avvio le ultime cartelle utilizzate.</li><li><b>Programmi di archiviazione</b>: rileva automaticamente gli eseguibili o seleziona manualmente il percorso. Lo stato indica se il file esiste ed è eseguibile.</li></ul>\n<h2>7. Tasti funzione</h2><ul><li><b>F1</b> Guida</li><li><b>F2</b> Menu</li><li><b>F3</b> Visualizza / apri elemento selezionato</li><li><b>F4</b> Modifica / apri elemento selezionato</li><li><b>F5</b> Copia nell’altro pannello</li><li><b>F6</b> Sposta nell’altro pannello</li><li><b>F7</b> Crea nuova cartella</li><li><b>F8</b> Elimina</li><li><b>F9</b> Impostazioni</li><li><b>F10</b> Esci da LunaCommander</li></ul>\n<p><i>Suggerimento:</i> Se un’azione non è disponibile, verifica prima che nel pannello attivo sia selezionato un elemento adatto.</p>', 'nl': '<h1>LunaCommander – Help</h1><p>Deze bestandsbeheerder toont twee mappen naast elkaar. Zo kun je bestanden tussen beide vensters beheren en overzetten.</p>\n<h2>1. De twee bestandspanelen</h2><ul><li>Het linker- en rechterpaneel tonen elk een eigen map.</li><li>Klik op een map om deze te openen. Kies „..” om één niveau omhoog te gaan.</li><li>Je kunt een pad rechtstreeks in het padveld invoeren. De knoppen ernaast gaan terug, één niveau omhoog of naar de thuismap.</li><li>Het actieve paneel is de bron voor bestandsacties; het andere paneel is meestal de bestemming.</li></ul>\n<h2>2. Bestanden en mappen selecteren</h2><ul><li>Een gewone linkermuisklik selecteert een item.</li><li><b>CTRL + linkermuisklik</b>: voeg afzonderlijke items toe aan de selectie of verwijder ze eruit.</li><li><b>SHIFT + linkermuisklik</b>: selecteer een aaneengesloten bereik.</li><li>Meerdere geselecteerde items kunnen samen worden gearchiveerd. Rechtsklikken op een al geselecteerd item behoudt de selectie.</li></ul>\n<h2>3. Bestanden beheren</h2><ul><li><b>Kopiëren / Verplaatsen</b>: zet het geselecteerde item over naar het andere paneel.</li><li><b>Knippen, Kopiëren, Plakken</b>: gebruik het klembord van de bestandsbeheerder.</li><li><b>Nieuw</b>: maak een bestand of map.</li><li><b>Hernoemen</b>: wijzig de naam van het geselecteerde item.</li><li><b>Verwijderen</b>: verwijder het geselecteerde item na bevestiging.</li><li><b>Eigenschappen</b>: toon informatie over het geselecteerde item.</li><li><b>Zoeken</b>: zoek in de actieve lokale map.</li></ul>\n<h2>4. Archieven maken en uitpakken</h2><ul><li>Gebruik <b>Archief → Inpakken</b> om ZIP-, RAR-, 7z-, TAR-, TAR.GZ-, TAR.XZ- of TAR.BZ2-archieven te maken.</li><li>Selecteer eerst meerdere bestanden of mappen om ze samen in één archief te plaatsen.</li><li>Voor het maken worden de externe programma’s gebruikt die zijn ingesteld onder <b>Instellingen → Archiveringsprogramma’s</b>.</li><li>TAR, TAR.GZ, TAR.XZ en TAR.BZ2 delen één programma-instelling „TAR”.</li><li>Gebruik „Hier uitpakken” of „Uitpakken naar map” om ondersteunde archieven uit te pakken.</li><li>Open een ondersteund archief in het bestandspaneel om de inhoud te bekijken.</li></ul>\n<h2>5. FTP, FTPS en SFTP</h2><ul><li>Kies FTP, FTPS of SFTP in de bovenste balk om een serververbinding in te stellen.</li><li>Voer het serveradres, de poort en indien nodig de gebruikersnaam en het wachtwoord in.</li><li>Na het verbinden kun je externe bestanden in het actieve paneel bekijken en overzetten.</li><li>Kies „Verbreken” om de verbinding te sluiten.</li></ul>\n<h2>6. Instellingen</h2><ul><li><b>Taal</b>: Duits, Engels, Frans, Italiaans of Nederlands.</li><li><b>Kleurenschema</b>: donker of licht.</li><li><b>Openen</b>: enkel- of dubbelklik om bestanden en mappen te openen.</li><li><b>Startmappen</b>: stel de standaardmap voor elk paneel in en herstel desgewenst de laatst gebruikte mappen bij het starten.</li><li><b>Archiveringsprogramma’s</b>: laat uitvoerbare programma’s automatisch detecteren of kies handmatig een programmapad. De status geeft aan of het bestand bestaat en uitvoerbaar is.</li></ul>\n<h2>7. Functietoetsen</h2><ul><li><b>F1</b> Help</li><li><b>F2</b> Menu</li><li><b>F3</b> Weergeven / geselecteerd item openen</li><li><b>F4</b> Bewerken / geselecteerd item openen</li><li><b>F5</b> Kopiëren naar het andere paneel</li><li><b>F6</b> Verplaatsen naar het andere paneel</li><li><b>F7</b> Nieuwe map maken</li><li><b>F8</b> Verwijderen</li><li><b>F9</b> Instellingen</li><li><b>F10</b> LunaCommander afsluiten</li></ul>\n<p><i>Tip:</i> Als een actie niet beschikbaar is, controleer dan eerst of in het actieve bestandspaneel een geschikt item is geselecteerd.</p>'}


class FileTreeWidget(QTreeWidget):
    """Tree view that exports selected local files as standard file URLs."""
    def __init__(self, pane=None, parent=None):
        super().__init__(parent)
        self.pane = pane

    def mimeData(self, items):
        mime = QMimeData()
        pane = self.pane
        urls = []
        if pane is not None and not pane.remote and pane.archive_file is None:
            seen = set()
            for item in items:
                row = item.data(0, Qt.UserRole)
                if not row:
                    continue
                name = row[0]
                if not name or name == '..':
                    continue
                path = Path(pane.path) / name
                try:
                    resolved = path.resolve(strict=True)
                except (OSError, RuntimeError):
                    continue
                key = str(resolved)
                if key in seen:
                    continue
                seen.add(key)
                urls.append(QUrl.fromLocalFile(key))
        mime.setUrls(urls)
        return mime


class Pane(QWidget):
    def __init__(self,app):
        super().__init__(); self.app=app; self.remote=None; self.path=str(Path.home()); self.rows=[]; self.history=[]; self.forward_history=[]; self.archive_file=None; self.archive_inner=''; self._thumbnail_generation=0; self.sort_field='name'; self.sort_descending=False 
        v=QVBoxLayout(self); v.setContentsMargins(3,3,3,3)
        nav=QHBoxLayout(); nav.setContentsMargins(0,0,0,0); nav.setSpacing(4)
        self.path_edit=QLineEdit(self.path); nav.addWidget(self.path_edit,1)
        self.nav_buttons=[]
        nav_defs=[('back','SP_ArrowBack',self.back),('up','SP_ArrowUp',self.up),('home','SP_DirHomeIcon',self.home)]
        for key,icon_name,fn in nav_defs:
            b=QPushButton(); b.setIcon(QApplication.style().standardIcon(getattr(QStyle,icon_name))); b.setIconSize(QSize(18,18)); b.setFixedSize(34,32); b.setToolTip(app.tr(key)); b.setAccessibleName(app.tr(key)); b.clicked.connect(fn); nav.addWidget(b); self.nav_buttons.append(b)
        b=QPushButton(app.tr('open')); b.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton)); b.setIconSize(QSize(16,16)); b.clicked.connect(self.go); nav.addWidget(b); self.nav_buttons.append(b)
        v.addLayout(nav)
        self.tree=FileTreeWidget(self); self.tree.setDragEnabled(True); self.tree.setDragDropMode(QAbstractItemView.DragOnly); self.tree.setDefaultDropAction(Qt.CopyAction); self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection); self.tree.setSelectionBehavior(QAbstractItemView.SelectRows); self._modifier_selection_click=False; self.tree.setColumnCount(3); self.tree.setHeaderLabels([self.app.tr('name'),self.app.tr('type'),self.app.tr('size')]); self.tree.setIconSize(QSize(72,72) if self.app.config.get('photo_preview', False) else QSize(28,28)); self.tree.setUniformRowHeights(not self.app.config.get('photo_preview', False)); self.tree.setContextMenuPolicy(Qt.CustomContextMenu); self.tree.customContextMenuRequested.connect(self.context_menu); self.tree.itemDoubleClicked.connect(self.activate); self.tree.itemClicked.connect(self.on_item_clicked); self.tree.currentItemChanged.connect(self.on_current_item_changed); self.tree.installEventFilter(self); self.tree.viewport().installEventFilter(self); self.path_edit.installEventFilter(self); self.tree.setExpandsOnDoubleClick(False); v.addWidget(self.tree,1)
        self.path_edit.returnPressed.connect(self.go); self.load(self.path)
    def on_current_item_changed(self, *_):
        self.app.active=self

    def set_thumbnail_mode(self, enabled):
        self.tree.setIconSize(QSize(72,72) if enabled else QSize(28,28))
        self.tree.setUniformRowHeights(not enabled)
        self.load(self.path, remember=False)

    def item_icon(self, name, is_dir, full_path=None):
        """Return a fast placeholder; image decoding happens in ThumbnailWorker."""
        base=(QApplication.style().standardIcon(QStyle.SP_DirIcon) if is_dir else
              (archive_icon(name) if not archive_icon(name).isNull() else
               (filetype_icon(name) if not filetype_icon(name).isNull() else
                QApplication.style().standardIcon(QStyle.SP_FileIcon))))
        if self.app.config.get('photo_preview', False):
            small=base.pixmap(QSize(28,28))
            canvas=QPixmap(76,76); canvas.fill(Qt.transparent)
            painter=QPainter(canvas)
            painter.drawPixmap((76-small.width())//2,(76-small.height())//2,small)
            painter.end()
            return QIcon(canvas)
        return base

    def queue_thumbnail(self, name, full_path):
        if not self.app.config.get('photo_preview', False) or not full_path:
            return
        if Path(name).suffix.lower() not in {'.jpg','.jpeg','.png','.gif','.bmp','.webp','.tif','.tiff','.jfif','.avif'}:
            return
        worker=ThumbnailWorker(self._thumbnail_generation,name,full_path)
        worker.signals.ready.connect(self.on_thumbnail_ready)
        QThreadPool.globalInstance().start(worker)

    def on_thumbnail_ready(self, generation, name, image):
        if generation != self._thumbnail_generation or not self.app.config.get('photo_preview', False):
            return
        for index in range(self.tree.topLevelItemCount()):
            item=self.tree.topLevelItem(index)
            data=item.data(0,Qt.UserRole)
            if data and data[0] == name and not data[1]:
                pix=QPixmap.fromImage(image)
                canvas=QPixmap(76,76); canvas.fill(Qt.transparent)
                painter=QPainter(canvas)
                painter.drawPixmap((76-pix.width())//2,(76-pix.height())//2,pix)
                painter.end()
                item.setIcon(0,QIcon(canvas))
                break

    def eventFilter(self,obj,event):
        # Keep the active pane in sync even when focus changes without a row click.
        if event.type() in (QEvent.FocusIn,QEvent.MouseButtonPress):
            self.app.active=self
        # Remember modifier state before QTreeWidget emits itemClicked.
        if event.type()==QEvent.MouseButtonPress and obj in (self.tree, self.tree.viewport(), self.path_edit):
            # Browser-style thumb buttons navigate the history of this pane only.
            if event.button() == Qt.BackButton:
                self.app.active=self
                self.back()
                return True
            if event.button() == Qt.ForwardButton:
                self.app.active=self
                self.forward()
                return True
            if obj in (self.tree, self.tree.viewport()):
                self._modifier_selection_click=bool(event.modifiers() & (Qt.ControlModifier|Qt.ShiftModifier))
        # QTreeWidget reserves F2 for inline rename and can swallow function keys.
        # Handle the file-manager bindings before the widget processes them.
        if event.type()==QEvent.KeyPress:
            key=event.key()
            if key in (Qt.Key_F2,Qt.Key_F5,Qt.Key_F6):
                self.app.active=self
                if key==Qt.Key_F2: self.app.show_menu()
                elif key==Qt.Key_F5: self.app.copy_other()
                elif key==Qt.Key_F6: self.app.move_other()
                return True
        return super().eventFilter(obj,event)
    def load(self,path,remember=True):
        self._thumbnail_generation += 1
        self.tree.setDragEnabled(not bool(self.remote))
        self.archive_file=None; self.archive_inner=''
        try:
            if remember and path!=self.path:
                self.history.append(self.path)
                self.forward_history.clear()
            if self.remote: path=posixpath.normpath(path or '/'); rows=self.remote.list(path)
            else:
                p=Path(path).expanduser().resolve(); path=str(p); rows=[('..',True,0)] if p.parent!=p else []
                mtime_by_name={}
                entries=[]
                with os.scandir(p) as scan:
                    for entry in scan:
                        try:
                            info=entry.stat(follow_symlinks=True)
                            is_dir=entry.is_dir(follow_symlinks=True)
                            entries.append((entry.name,is_dir,0 if is_dir else info.st_size))
                            mtime_by_name[entry.name]=info.st_mtime
                        except (OSError, PermissionError):
                            # Keep the name visible even if its target/metadata cannot be read.
                            try: is_dir=entry.is_dir(follow_symlinks=False)
                            except OSError: is_dir=False
                            entries.append((entry.name,is_dir,0))
                            mtime_by_name[entry.name]=0
                rows+=sorted(entries,key=folder_sort_key)
            if not self.app.config.get('show_hidden', False):
                rows=[row for row in rows if row[0]=='..' or not row[0].startswith('.')]
            self.path=path; self.path_edit.setText(path); self.rows=rows; self.tree.clear(); self.app.store_pane_path(self, path)
            for n,d,s in rows:
                it=QTreeWidgetItem([n,self.app.tr('folder') if d else self.app.tr('file'),'' if d else f'{s:,} B']); it.setData(0,Qt.UserRole,(n,d,s))
                it.setData(0,Qt.UserRole+1,mtime_by_name.get(n,0) if not self.remote else 0)
                full_path=(Path(path)/n) if not self.remote and n!='..' else None
                it.setIcon(0,self.item_icon(n,d,full_path)); self.tree.addTopLevelItem(it)
                if full_path and not d:
                    self.queue_thumbnail(n,full_path)
            self.tree.resizeColumnToContents(0)
            # Keep this pane's selected sort mode when refreshing or reopening a folder.
            self._apply_sort()
        except Exception as e:self.app.statusBar().showMessage(f'Fehler: {e}')
    def sort_entries(self, field, descending=False):
        # Remember the selected mode independently for each file pane.
        self.sort_field=field
        self.sort_descending=descending
        # Persist the sort mode for this pane so it survives an application restart.
        if hasattr(self.app, 'left') and hasattr(self.app, 'right'):
            side = 'left' if self is self.app.left else ('right' if self is self.app.right else None)
            if side:
                self.app.config[f'sort_{side}_field'] = self.sort_field
                self.app.config[f'sort_{side}_descending'] = self.sort_descending
                self.app.save_config()
        self._apply_sort()

    def _apply_sort(self):
        field=self.sort_field
        descending=self.sort_descending
        items=[self.tree.takeTopLevelItem(0) for _ in range(self.tree.topLevelItemCount())]
        def key(item):
            data=item.data(0,Qt.UserRole) or ('',False,0,0)
            name, is_dir, size = data[:3]
            mtime = item.data(0, Qt.UserRole + 1) or 0
            if name == '..': return (0, 0)
            if field == 'name': value=name.casefold()
            elif field == 'date': value=float(mtime)
            elif field == 'size': value=int(size or 0)
            elif field == 'type': value=('folder' if is_dir else Path(name).suffix.casefold(), name.casefold())
            else: value=name.casefold()
            return (1, value)
        if field == 'name':
            # Name sorting keeps directories grouped before files. Within the
            # directory group, visible folders come before dot-folders; dot-folders
            # remain ahead of files, matching the default pane order.
            parent = [x for x in items if (x.data(0, Qt.UserRole) or ('',))[0] == '..']
            rest = [x for x in items if (x.data(0, Qt.UserRole) or ('',))[0] != '..']
            def name_group(item):
                data = item.data(0, Qt.UserRole) or ('', False, 0)
                name, is_dir = data[0], bool(data[1])
                if is_dir and not name.startswith('.'):
                    return 0
                if is_dir:
                    return 1
                return 2
            groups = []
            for group_id in range(3):
                group = [x for x in rest if name_group(x) == group_id]
                group.sort(key=lambda x: (x.data(0, Qt.UserRole) or ('',))[0].casefold(), reverse=descending)
                groups.extend(group)
            ordered = parent + groups
        else:
            items.sort(key=key, reverse=descending)
            # Keep the parent entry at the top in either direction.
            parent=[x for x in items if (x.data(0,Qt.UserRole) or ('',))[0]=='..']
            rest=[x for x in items if (x.data(0,Qt.UserRole) or ('',))[0]!='..']
            ordered = parent + rest
        for item in ordered: self.tree.addTopLevelItem(item)

    def selected(self):
        it=self.tree.currentItem(); return it.data(0,Qt.UserRole) if it else None
    def on_item_clicked(self,it,col):
        self.app.active=self
        # Ctrl/Shift clicks are always selection gestures, even in single-click-open mode.
        modifiers=QApplication.keyboardModifiers()
        modifier_click=self._modifier_selection_click or bool(modifiers & (Qt.ControlModifier|Qt.ShiftModifier))
        self._modifier_selection_click=False
        if modifier_click:
            return
        if self.app.click_mode=='single':
            self.activate(it,col)
    def target(self,n): return posixpath.join(self.path,n) if self.remote else str(Path(self.path)/n)
    def load_archive(self, archive, inner='', remember=True):
        self.tree.setDragEnabled(False)
        archive=Path(archive).resolve()
        if remember and self.archive_file is None and str(archive)!=self.path:
            self.history.append(self.path)
        self.archive_file=archive; self.archive_inner=inner.strip('/')
        prefix=self.archive_inner+'/' if self.archive_inner else ''
        entries={}
        name=archive.name.lower()
        if name.endswith('.zip'):
            with zipfile.ZipFile(archive) as z:
                for info in z.infolist():
                    raw=info.filename.replace('\\','/').strip('/')
                    if not raw or not raw.startswith(prefix): continue
                    rest=raw[len(prefix):]
                    if not rest: continue
                    first=rest.split('/',1)[0]
                    if '/' in rest or info.is_dir(): entries[first]=[True,0]
                    else: entries[first]=[False,info.file_size]
        elif name.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            with tarfile.open(archive,'r:*') as t:
                for member in t.getmembers():
                    raw=member.name.strip('/')
                    if not raw or not raw.startswith(prefix): continue
                    rest=raw[len(prefix):]
                    if not rest: continue
                    first=rest.split('/',1)[0]
                    if '/' in rest or member.isdir(): entries[first]=[True,0]
                    elif member.isfile(): entries[first]=[False,member.size]
        else:
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Für die interne Archivansicht dieses Formats wird 7zip benötigt.')
            result=subprocess.run([tool,'l','-slt',str(archive)],capture_output=True,text=True)
            if result.returncode: raise RuntimeError(result.stderr or 'Archivinhalt konnte nicht gelesen werden.')
            current={}
            for line in result.stdout.splitlines()+['']:
                if not line.strip():
                    raw=current.get('Path','').replace('\\','/').strip('/')
                    if raw and raw.startswith(prefix):
                        rest=raw[len(prefix):]
                        if rest:
                            first=rest.split('/',1)[0]
                            isdir='/' in rest or current.get('Folder')=='+'
                            size=int(current.get('Size','0') or 0) if not isdir else 0
                            entries[first]=[isdir,size]
                    current={}
                elif ' = ' in line:
                    k,v=line.split(' = ',1); current[k]=v
        rows=[]
        if self.archive_inner: rows.append(('..',True,0))
        rows += [(n,v[0],v[1]) for n,v in entries.items()]
        self.path=str(archive)+'!/'+self.archive_inner
        self.path_edit.setText(self.path)
        self.rows=sorted(rows,key=folder_sort_key); self.tree.clear()
        for n,d,size in self.rows:
            it=QTreeWidgetItem([n,'Ordner' if d else 'Datei','' if d else f'{size:,} B'])
            it.setData(0,Qt.UserRole,(n,d,size)); it.setIcon(0,self.item_icon(n,d,None)); self.tree.addTopLevelItem(it)
        self.tree.resizeColumnToContents(0)
        self.app.statusBar().showMessage(f"{self.app.tr('archive_label')}: {archive.name}  |  {len(entries)} {self.app.tr('archive_entries')}")
    def activate(self,it,col=0):
        if not it:return
        r=it.data(0,Qt.UserRole); n,d,_=r
        if self.archive_file:
            if n=='..': self.load_archive(self.archive_file,self.archive_inner.rsplit('/',1)[0] if '/' in self.archive_inner else '',False); return
            inner='/'.join(x for x in (self.archive_inner,n) if x)
            if d: self.load_archive(self.archive_file,inner,False); return
            self.app.open_archive_member(self.archive_file,inner)
            return
        if d:self.load(posixpath.normpath(posixpath.join(self.path,n)) if self.remote else str(Path(self.path)/n))
        elif not self.remote:
            archive_suffixes=('.zip','.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.7z','.rar')
            target=Path(self.target(n))
            if target.name.lower().endswith(archive_suffixes):
                try:self.load_archive(target)
                except Exception as e:QMessageBox.warning(self,self.app.tr('archive_label'),str(e))
                return
            from PySide6.QtGui import QDesktopServices
            from PySide6.QtCore import QUrl
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(target)))
    def context_menu(self,pos):
        self.app.active=self; it=self.tree.itemAt(pos)
        if it and not it.isSelected():
            self.tree.clearSelection()
            self.tree.setCurrentItem(it)
        m=QMenu(self)
        actions=[(self.app.tr('open'),lambda:self.activate(self.tree.currentItem()) if self.tree.currentItem() else None)]
        if it and not self.remote and not self.archive_file:
            row=it.data(0,Qt.UserRole)
            if row and not row[1]:
                open_with=m.addMenu(self.app.tr('open_with'))
                target=Path(self.target(row[0]))
                suggestions=self.app.open_with_suggestions(target)
                for app_name, program, remembered in suggestions:
                    label=(app_name + ('  ★' if remembered else ''))
                    action=open_with.addAction(label)
                    action.setToolTip(program)
                    action.triggered.connect(lambda checked=False,item=it,exe=program:self.launch_with_application(item,exe,True))
                if suggestions:
                    open_with.addSeparator()
                choose=open_with.addAction(self.app.tr('choose_application'))
                choose.triggered.connect(lambda checked=False,item=it:self.open_with_application(item))
        actions += [(self.app.tr('copy')+' → '+self.app.tr('open_other'),self.app.copy_other),(self.app.tr('move')+' → '+self.app.tr('move_other'),self.app.move_other),(self.app.tr('rename'),self.app.rename),(self.app.tr('delete'),self.app.delete),(self.app.tr('properties'),self.app.properties),(self.app.tr('new_folder'),self.app.new_folder),(self.app.tr('new_file'),self.app.new_file),(self.app.tr('cut'),self.app.cut),(self.app.tr('copy'),self.app.copy),(self.app.tr('paste'),self.app.paste),(self.app.tr('refresh'),lambda:self.load(self.path))]
        for label,fn in actions:
            a=m.addAction(label); a.triggered.connect(fn)
        m.addSeparator()
        archive_menu=m.addMenu(self.app.tr('archive'))
        pack_menu=archive_menu.addMenu(self.app.tr('pack'))
        for label,fmt in [(self.app.tr('create_zip'),'zip'),('TAR-Archiv erstellen','tar'),(self.app.tr('create_targz'),'tar.gz'),(self.app.tr('create_tarxz'),'tar.xz'),(self.app.tr('create_tarbz2'),'tar.bz2'),(self.app.tr('create_7z'),'7z'),(self.app.tr('create_rar'),'rar')]:
            a=pack_menu.addAction(label); a.triggered.connect(lambda checked=False,f=fmt:self.app.pack_selected(f))
        extract=archive_menu.addAction(self.app.tr('extract_here'))
        extract.triggered.connect(self.app.extract_selected)
        extract_to=archive_menu.addAction(self.app.tr('extract_to'))
        extract_to.triggered.connect(self.app.extract_selected_to)
        m.addSeparator()
        sort_menu=m.addMenu(self.app.tr('sort_by'))
        for field,key in [('name','sort_name'),('date','sort_date'),('size','sort_size'),('type','sort_type')]:
            field_menu=sort_menu.addMenu(self.app.tr(key))
            asc=field_menu.addAction(self.app.tr('ascending'))
            asc.triggered.connect(lambda checked=False,f=field:self.sort_entries(f,False))
            desc=field_menu.addAction(self.app.tr('descending'))
            desc.triggered.connect(lambda checked=False,f=field:self.sort_entries(f,True))
        m.exec(self.tree.viewport().mapToGlobal(pos))
    def open_with_application(self, item):
        """Choose an executable, remember it for this extension and launch it."""
        if not item or self.remote or self.archive_file:
            return
        row=item.data(0,Qt.UserRole)
        if not row or row[1]:
            return
        target=Path(self.target(row[0]))
        program,_=QFileDialog.getOpenFileName(self, self.app.tr('open_with'), '/usr/bin', self.app.tr('application_filter')+' (*)')
        if program:
            self.launch_with_application(item,program,True)

    def launch_with_application(self, item, program, remember=True):
        if not item or self.remote or self.archive_file:
            return
        row=item.data(0,Qt.UserRole)
        if not row or row[1]:
            return
        target=Path(self.target(row[0]))
        if not os.path.isfile(program) or not os.access(program,os.X_OK):
            QMessageBox.warning(self,self.app.tr('open_with'),self.app.tr('app_launch_error'))
            return
        if not QProcess.startDetached(program, [str(target)]):
            QMessageBox.warning(self,self.app.tr('open_with'),self.app.tr('app_launch_error'))
            return
        if remember:
            self.app.remember_open_with(target,program)

    def back(self):
        if not self.history:
            return
        current = self.path
        previous = self.history.pop()
        self.forward_history.append(current)
        self.load(previous, False)

    def forward(self):
        if not self.forward_history:
            return
        current = self.path
        next_path = self.forward_history.pop()
        self.history.append(current)
        self.load(next_path, False)
    def up(self):
        if self.archive_file:
            if self.archive_inner:self.load_archive(self.archive_file,self.archive_inner.rsplit('/',1)[0] if '/' in self.archive_inner else '',False)
            else:self.back()
        else:self.load(posixpath.dirname(self.path.rstrip('/')) or '/' if self.remote else str(Path(self.path).parent))
    def home(self):self.archive_file=None; self.archive_inner=''; self.load('/' if self.remote else str(Path.home()))
    def go(self):self.load(self.path_edit.text())



class ThumbnailSignals(QObject):
    ready = Signal(int, str, QImage)

class ThumbnailWorker(QRunnable):
    """Decode and scale image thumbnails off the GUI thread."""
    def __init__(self, generation, name, path):
        super().__init__()
        self.generation=generation
        self.name=name
        self.path=str(path)
        self.signals=ThumbnailSignals()

    def run(self):
        try:
            image=QImage(self.path)
            if not image.isNull():
                image=image.scaled(72,72,Qt.KeepAspectRatio,Qt.SmoothTransformation)
                self.signals.ready.emit(self.generation,self.name,image)
        except Exception:
            pass


class TransferSignals(QObject):
    progress = Signal(int)
    finished = Signal(str, bool, str)
class DeleteWorker(QRunnable):
    def __init__(self, pane, name, is_dir):
        super().__init__(); self.pane=pane; self.name=name; self.is_dir=is_dir; self.signals=TransferSignals()
    def run(self):
        try:
            p=self.pane; path=p.target(self.name)
            if p.archive_file:
                member='/'.join(x for x in (p.archive_inner,self.name) if x)
                p.app.delete_archive_member(p.archive_file,member,self.is_dir)
            elif p.remote:
                if self.is_dir: raise RuntimeError('Das rekursive Löschen entfernter Ordner wird derzeit nicht unterstützt.')
                p.remote.client.remove(path) if p.remote.proto=='SFTP' else p.remote.client.delete(path)
            elif self.is_dir: shutil.rmtree(path)
            else: Path(path).unlink()
            self.signals.progress.emit(100); self.signals.finished.emit(self.name,True,'')
        except Exception as e: self.signals.finished.emit(self.name,False,str(e))

class DeleteBatchWorker(QRunnable):
    """Delete a captured selection in one worker, avoiding fragile per-item queue chaining."""
    def __init__(self, pane, rows):
        super().__init__()
        self.pane=pane
        self.rows=list(rows)
        self.signals=TransferSignals()
    def run(self):
        errors=[]
        total=len(self.rows)
        for index,(name,is_dir,_size) in enumerate(self.rows,1):
            try:
                pane=self.pane
                path=pane.target(name)
                if pane.archive_file:
                    member='/'.join(x for x in (pane.archive_inner,name) if x)
                    pane.app.delete_archive_member(pane.archive_file,member,is_dir)
                elif pane.remote:
                    if is_dir:
                        raise RuntimeError('Das rekursive Löschen entfernter Ordner wird derzeit nicht unterstützt.')
                    if pane.remote.proto=='SFTP':
                        pane.remote.client.remove(path)
                    else:
                        pane.remote.client.delete(path)
                elif is_dir:
                    shutil.rmtree(path)
                else:
                    Path(path).unlink()
            except Exception as exc:
                errors.append(f'{name}: {exc}')
            self.signals.progress.emit(int(index*100/total))
        summary=f'{total} Einträge'
        self.signals.finished.emit(summary,not errors,'; '.join(errors))

class TransferWorker(QRunnable):
    def __init__(self, src, dst, source_path, target_path, is_dir, move, conflict='merge'):
        super().__init__(); self.src=src; self.dst=dst; self.source_path=source_path; self.target_path=target_path; self.is_dir=is_dir; self.move=move; self.conflict=conflict; self.signals=TransferSignals(); self.total_bytes=0; self.done_bytes=0
        self.archive_file=src.archive_file if not src.remote else None
        self.archive_member='/'.join(x for x in (src.archive_inner, Path(source_path.split('!/')[-1]).name) if x) if self.archive_file else ''
    def run(self):
        name=posixpath.basename(self.source_path.rstrip('/')) or Path(self.source_path).name
        try:
            if self.src.remote and self.dst.remote: raise RuntimeError(self.tr('server_copy_unavailable'))
            self.total_bytes = self.measure_total()
            exists = self.target_exists()
            if exists and self.conflict == 'skip':
                self.signals.finished.emit(name, True, 'Übersprungen – Ziel existiert bereits.'); return
            if exists and self.conflict == 'replace':
                self.remove_target()
            if self.dst.archive_file and self.archive_file:
                self.copy_archive_to_archive()
                if self.move: self.src.app.delete_archive_member(self.archive_file,self.archive_member,self.is_dir)
            elif self.dst.archive_file:
                if self.move and self.src.remote: raise RuntimeError('Verschieben von einem entfernten Server in ein Archiv wird nicht unterstützt.')
                self.copy_into_archive()
                if self.move:
                    if self.src.archive_file:
                        self.src.app.delete_archive_member(self.archive_file,self.archive_member,self.is_dir)
                    else:
                        shutil.rmtree(self.source_path) if self.is_dir else os.unlink(self.source_path)
            elif self.archive_file:
                self.copy_from_archive()
                if self.move: self.src.app.delete_archive_member(self.archive_file,self.archive_member,self.is_dir)
            elif self.src.remote: self.remote_to_local(self.source_path,self.target_path,self.is_dir)
            elif self.dst.remote: self.local_to_remote(self.source_path,self.target_path,self.is_dir)
            elif self.is_dir:
                if exists and self.conflict == 'merge':
                    self.copy_local_tree(Path(self.source_path),Path(self.target_path),merge=True)
                else: self.copy_local_tree(Path(self.source_path),Path(self.target_path),merge=False)
            else:
                Path(self.target_path).parent.mkdir(parents=True,exist_ok=True); self.copy_local_file(Path(self.source_path),Path(self.target_path))
            if self.move and not self.archive_file and not self.dst.archive_file:
                if self.src.remote: self.remove_remote(self.source_path,self.is_dir)
                else: shutil.rmtree(self.source_path) if self.is_dir else os.unlink(self.source_path)
            self.signals.progress.emit(100)
            self.signals.finished.emit(name,True,'')
        except Exception as e: self.signals.finished.emit(name,False,str(e))
    def archive_entries(self):
        """Return (name, is_dir, size) entries relative to the selected archive folder."""
        archive=self.archive_file; base=self.archive_member.strip('/')
        prefix=base+'/' if base else ''
        name=archive.name.lower(); found={}
        if name.endswith('.zip'):
            with zipfile.ZipFile(archive) as z:
                for info in z.infolist():
                    raw=info.filename.replace('\\','/').strip('/')
                    if not raw.startswith(prefix): continue
                    rel=raw[len(prefix):]
                    if not rel: continue
                    first=rel.split('/',1)[0]
                    isdir='/' in rel or info.is_dir()
                    found[first]=(isdir,0 if isdir else info.file_size)
        elif name.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            with tarfile.open(archive,'r:*') as t:
                for m in t.getmembers():
                    raw=m.name.replace('\\','/').strip('/')
                    if not raw.startswith(prefix): continue
                    rel=raw[len(prefix):]
                    if not rel: continue
                    first=rel.split('/',1)[0]; isdir='/' in rel or m.isdir()
                    if isdir or m.isfile(): found[first]=(isdir,0 if isdir else m.size)
        else:
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Für dieses Archiv wird 7zip benötigt.')
            r=subprocess.run([tool,'l','-slt',str(archive)],capture_output=True,text=True)
            if r.returncode: raise RuntimeError(r.stderr or 'Archiv kann nicht gelesen werden.')
            current={}
            for line in r.stdout.splitlines()+['']:
                if not line.strip():
                    raw=current.get('Path','').replace('\\','/').strip('/')
                    if raw.startswith(prefix):
                        rel=raw[len(prefix):]
                        if rel:
                            first=rel.split('/',1)[0]; d='/' in rel or current.get('Folder')=='+'
                            found[first]=(d,0 if d else int(current.get('Size','0') or 0))
                    current={}
                elif ' = ' in line:
                    k,v=line.split(' = ',1); current[k]=v
        return [(n,d,z) for n,(d,z) in found.items()]

    def archive_stream(self, member):
        """Yield a member's bytes without creating a bogus filesystem archive path."""
        low=self.archive_file.name.lower()
        if low.endswith('.zip'):
            with zipfile.ZipFile(self.archive_file) as z, z.open(member,'r') as f:
                while True:
                    b=f.read(1024*1024)
                    if not b: break
                    yield b
        elif low.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            with tarfile.open(self.archive_file,'r:*') as t:
                f=t.extractfile(member)
                if f is None: raise RuntimeError('Archivdatei kann nicht gelesen werden: '+member)
                with f:
                    while True:
                        b=f.read(1024*1024)
                        if not b: break
                        yield b
        else:
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Für dieses Archiv wird 7zip benötigt.')
            proc=subprocess.Popen([tool,'x','-so',str(self.archive_file),member],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                while True:
                    b=proc.stdout.read(1024*1024)
                    if not b: break
                    yield b
                err=proc.stderr.read().decode(errors='replace')
                if proc.wait()!=0: raise RuntimeError(err or 'Datei konnte nicht aus dem Archiv gelesen werden.')
            finally:
                if proc.poll() is None: proc.kill()

    def write_archive_member(self, member, target):
        if self.dst.remote:
            if self.dst.remote.proto=='SFTP':
                target.parent if isinstance(target,Path) else None
                parent=posixpath.dirname(str(target))
                try: self.dst.remote.client.makedirs(parent,exist_ok=True)
                except Exception: pass
                with self.dst.remote.client.open(str(target),'wb') as out:
                    for block in self.archive_stream(member): out.write(block); self.report_bytes(len(block))
            else:
                parent,name=posixpath.split(str(target)); old=self.dst.remote.client.pwd()
                try:
                    self.dst.remote.client.cwd(parent or '/')
                    import io
                    data=b''.join(self.archive_stream(member))
                    self.dst.remote.client.storbinary('STOR '+name,io.BytesIO(data),1024*1024)
                    self.report_bytes(len(data))
                finally: self.dst.remote.client.cwd(old)
        else:
            target=Path(target); target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('wb') as out:
                for block in self.archive_stream(member): out.write(block); self.report_bytes(len(block))

    def copy_into_archive(self):
        """Add a local file/folder to the currently opened destination archive."""
        archive=self.dst.archive_file
        low=archive.name.lower()
        source=Path(self.source_path)
        member=self.target_path.replace('\\','/').strip('/')
        if not source.exists(): raise FileNotFoundError(str(source))
        if low.endswith('.zip'):
            with zipfile.ZipFile(archive,'a',compression=zipfile.ZIP_DEFLATED,allowZip64=True) as z:
                if source.is_dir():
                    for root,dirs,files in os.walk(source):
                        rel=Path(root).relative_to(source).as_posix()
                        arc_root=member.rstrip('/')
                        folder_name=arc_root if rel=='.' else arc_root+'/'+rel
                        if not dirs and not files: z.writestr(folder_name.rstrip('/')+'/', '')
                        for d in dirs:
                            dp=folder_name+'/'+d
                            z.writestr(dp.rstrip('/')+'/', '')
                        for f in files:
                            fp=Path(root)/f; z.write(fp,folder_name+'/'+f)
                else: z.write(source,member)
        elif low.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            import tempfile
            suffix=''.join(archive.suffixes) or '.tar'
            fd,tmp=tempfile.mkstemp(prefix='lunacommander-archive-',suffix=suffix,dir=str(archive.parent)); os.close(fd)
            try:
                mode='w:gz' if low.endswith(('.tar.gz','.tgz')) else 'w:xz' if low.endswith(('.tar.xz','.txz')) else 'w:bz2' if low.endswith(('.tar.bz2','.tbz2')) else 'w' if low.endswith('.tar') else None
                if mode is None: raise RuntimeError('Das Hinzufügen zu diesem TAR-Kompressionsformat wird nicht unterstützt.')
                with tarfile.open(archive,'r:*') as old, tarfile.open(tmp,mode) as new:
                    for info in old.getmembers():
                        if info.isdir(): new.addfile(info)
                        elif info.isfile():
                            stream=old.extractfile(info)
                            if stream is not None:
                                with stream: new.addfile(info,stream)
                    new.add(source,arcname=member,recursive=True)
                os.replace(tmp,archive)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        elif low.endswith(('.7z','.rar')):
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Zum Schreiben dieses Archivs wird 7-Zip benötigt.')
            if low.endswith('.rar'): raise RuntimeError('RAR-Archive können mit den freien Debian-Werkzeugen nicht zuverlässig erweitert werden. Bitte ZIP, 7z oder TAR verwenden.')
            r=subprocess.run([tool,'a','-y',str(archive),str(source)],cwd=str(source.parent),capture_output=True,text=True)
            if r.returncode not in (0,1): raise RuntimeError(r.stderr or r.stdout or 'Datei konnte nicht ins Archiv übernommen werden.')
        else: raise RuntimeError('Dieses Archivformat unterstützt das Hinzufügen hier nicht.')
        self.signals.progress.emit(100)

    def copy_archive_to_archive(self):
        # Stage through a temporary folder; all archive I/O stays in this worker thread.
        import tempfile
        original_source=self.source_path; original_target=self.target_path
        with tempfile.TemporaryDirectory(prefix='lunacommander-archive-transfer-') as temp:
            staged=Path(temp)/Path(self.archive_member).name
            self.target_path=str(staged)
            self.copy_from_archive()
            self.source_path=str(staged)
            self.target_path=original_target
            self.copy_into_archive()
        self.source_path=original_source; self.target_path=original_target

    def copy_from_archive(self):
        base=self.archive_member.strip('/')
        if not self.is_dir:
            self.write_archive_member(base,self.target_path); return
        # Enumerate all descendants and recreate the selected folder tree at destination.
        low=self.archive_file.name.lower(); files=[]; dirs=set()
        if low.endswith('.zip'):
            with zipfile.ZipFile(self.archive_file) as z:
                items=[(i.filename.replace('\\','/').strip('/'),i.is_dir(),i.file_size) for i in z.infolist()]
        elif low.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            with tarfile.open(self.archive_file,'r:*') as t:
                items=[(m.name.replace('\\','/').strip('/'),m.isdir(),m.size) for m in t.getmembers() if m.isdir() or m.isfile()]
        else:
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Für dieses Archiv wird 7zip benötigt.')
            r=subprocess.run([tool,'l','-slt',str(self.archive_file)],capture_output=True,text=True)
            if r.returncode: raise RuntimeError(r.stderr or 'Archiv kann nicht gelesen werden.')
            items=[]; cur={}
            for line in r.stdout.splitlines()+['']:
                if not line.strip():
                    n=cur.get('Path','').replace('\\','/').strip('/')
                    if n: items.append((n,cur.get('Folder')=='+',int(cur.get('Size','0') or 0)))
                    cur={}
                elif ' = ' in line:
                    k,v=line.split(' = ',1); cur[k]=v
        prefix=base+'/'
        for n,isdir,size in items:
            if n==base and isdir: continue
            if not n.startswith(prefix): continue
            rel=n[len(prefix):]
            if not rel: continue
            parts=rel.split('/')
            for i in range(1,len(parts)):
                dirs.add('/'.join(parts[:i]))
            if isdir: dirs.add(rel)
            else: files.append((n,rel,size))
        if self.dst.remote:
            root=str(self.target_path).rstrip('/')
            if self.dst.remote.proto=='SFTP':
                try:self.dst.remote.client.makedirs(root,exist_ok=True)
                except Exception:pass
            else:
                old=self.dst.remote.client.pwd()
                try:self.dst.remote.client.cwd(root)
                except Exception:self.dst.remote.client.mkd(root)
                finally:self.dst.remote.client.cwd(old)
            for rel in sorted(dirs,key=lambda x:x.count('/')):
                dest=posixpath.join(root,rel)
                if self.dst.remote.proto=='SFTP':
                    try:self.dst.remote.client.makedirs(dest,exist_ok=True)
                    except Exception:pass
                else:
                    old=self.dst.remote.client.pwd()
                    try:self.dst.remote.client.cwd(dest)
                    except Exception:
                        parent,name=posixpath.split(dest); self.dst.remote.client.cwd(parent or '/'); self.dst.remote.client.mkd(name)
                    finally:self.dst.remote.client.cwd(old)
            for full,rel,size in files:self.write_archive_member(full,posixpath.join(root,rel))
        else:
            root=Path(self.target_path); root.mkdir(parents=True,exist_ok=True)
            for rel in dirs:(root/rel).mkdir(parents=True,exist_ok=True)
            for full,rel,size in files:self.write_archive_member(full,root/rel)

    def copy_local_file(self,source,target):
        target.parent.mkdir(parents=True,exist_ok=True)
        with open(source,'rb') as inp, open(target,'wb') as out:
            while True:
                block=inp.read(1024*1024)
                if not block: break
                out.write(block); self.report_bytes(len(block))
        shutil.copystat(source,target,follow_symlinks=False)
    def copy_local_tree(self,source,target,merge=False):
        target.mkdir(parents=True,exist_ok=True)
        for child in source.iterdir():
            dest=target/child.name
            if child.is_dir() and not child.is_symlink():
                if dest.exists() and not dest.is_dir(): raise FileExistsError(str(dest))
                self.copy_local_tree(child,dest,merge=True)
            else:
                if dest.exists() and not merge: raise FileExistsError(str(dest))
                self.copy_local_file(child,dest)
    def measure_total(self):
        try:
            if self.src.remote:
                if not self.is_dir:
                    if self.src.remote.proto == 'SFTP': return int(self.src.remote.client.stat(self.source_path).st_size or 0)
                    return int(self.src.remote.client.size(self.source_path) or 0)
                total=0
                for name,is_dir,size in self.src.remote.list(self.source_path):
                    if name!='..':
                        child=posixpath.join(self.source_path,name)
                        total += self.measure_remote(child,is_dir)
                return total
            root=Path(self.source_path)
            if root.is_file(): return root.stat().st_size
            return sum(f.stat().st_size for f in root.rglob('*') if f.is_file() and not f.is_symlink())
        except Exception: return 0
    def measure_remote(self,path,is_dir):
        remote=self.src.remote
        if not is_dir:
            try: return int(remote.client.stat(path).st_size or 0) if remote.proto=='SFTP' else int(remote.client.size(path) or 0)
            except Exception: return 0
        total=0
        for name,d,size in remote.list(path):
            if name!='..': total += self.measure_remote(posixpath.join(path,name),d)
        return total
    def report_bytes(self,count):
        if self.total_bytes<=0: return
        self.done_bytes += max(0,int(count))
        self.signals.progress.emit(min(99,int(self.done_bytes*100/self.total_bytes)))
    def target_exists(self):
        if self.dst.remote:
            try:
                if self.dst.remote.proto == 'SFTP': self.dst.remote.client.stat(self.target_path)
                else:
                    parent,name=posixpath.split(self.target_path.rstrip('/'))
                    try:
                        old=self.dst.remote.client.pwd(); self.dst.remote.client.cwd(parent or '/')
                        try: self.dst.remote.client.sendcmd('MLST '+name)
                        finally: self.dst.remote.client.cwd(old)
                    except Exception:
                        return any(row[0] == name for row in self.dst.remote.list(parent or '/'))
            except Exception: return False
            return True
        if self.dst.archive_file:
            return self.archive_destination_exists()
        return Path(self.target_path).exists()
    def archive_destination_exists(self):
        archive=self.dst.archive_file; wanted=self.target_path.strip('/')
        low=archive.name.lower()
        if low.endswith('.zip'):
            with zipfile.ZipFile(archive) as z: return any(i.filename.rstrip('/')==wanted or i.filename.rstrip('/').startswith(wanted+'/') for i in z.infolist())
        if low.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
            with tarfile.open(archive,'r:*') as t: return any(m.name.rstrip('/')==wanted or m.name.rstrip('/').startswith(wanted+'/') for m in t.getmembers())
        tool=shutil.which('7zz') or shutil.which('7z')
        if tool:
            r=subprocess.run([tool,'l','-slt',str(archive)],capture_output=True,text=True)
            return any(line.startswith('Path = ') and line[7:].strip('/')==wanted for line in r.stdout.splitlines())
        return False
    def remove_target(self):
        if self.dst.archive_file:
            raise RuntimeError('Einträge in Archiven werden nicht automatisch überschrieben. Bitte zuerst den vorhandenen Eintrag entfernen oder umbenennen.')
        if self.dst.remote:
            remote=self.dst.remote
            try:
                if remote.proto=='SFTP': mode=remote.client.stat(self.target_path).st_mode
                else:
                    parent,name=posixpath.split(self.target_path.rstrip('/')); old=remote.client.pwd(); remote.client.cwd(parent or '/')
                    try: isdir=False; remote.client.cwd(name); remote.client.cwd('..'); isdir=True
                    except Exception: pass
                    finally: remote.client.cwd(old)
                    mode=None
                if remote.proto=='SFTP':
                    import stat as statmod
                    if statmod.S_ISDIR(mode):
                        for item in remote.client.listdir_attr(self.target_path): self._remove_remote_path(posixpath.join(self.target_path,item.filename),statmod.S_ISDIR(item.st_mode))
                        remote.client.rmdir(self.target_path)
                    else: remote.client.remove(self.target_path)
                elif isdir:
                    for name2,d,_ in remote.list(self.target_path):
                        if name2!='..': self._remove_remote_path(posixpath.join(self.target_path,name2),d)
                    remote.rmdir(self.target_path)
                else: remote.client.delete(self.target_path)
            except Exception as exc: raise RuntimeError('Vorhandenes Ziel konnte nicht ersetzt werden: '+str(exc))
        else:
            target=Path(self.target_path)
            if target.is_dir() and not target.is_symlink(): shutil.rmtree(target)
            else: target.unlink()
    def _remove_remote_path(self,path,is_dir):
        remote=self.dst.remote
        if is_dir:
            for item in remote.client.listdir_attr(path):
                import stat as statmod
                self._remove_remote_path(posixpath.join(path,item.filename),statmod.S_ISDIR(item.st_mode))
            remote.client.rmdir(path)
        else: remote.client.remove(path)
    def remote_to_local(self,rpath,lpath,is_dir):
        remote=self.src.remote
        if is_dir:
            Path(lpath).mkdir(parents=True,exist_ok=True)
            for name,d,size in remote.list(rpath):
                if name!='..': self.remote_to_local(posixpath.join(rpath,name),str(Path(lpath)/name),d)
        else:
            Path(lpath).parent.mkdir(parents=True,exist_ok=True)
            if remote.proto=='SFTP':
                size=int(remote.client.stat(rpath).st_size or 0); remote.client.get(rpath,lpath,callback=lambda done,total:self.signals.progress.emit(min(99,int((self.done_bytes+done)*100/self.total_bytes))) if self.total_bytes else None); self.done_bytes+=size
            else:
                with open(lpath,'wb') as f:
                    def cb(block):
                        f.write(block); self.report_bytes(len(block))
                    remote.client.retrbinary('RETR '+rpath,cb,blocksize=65536)
    def local_to_remote(self,lpath,rpath,is_dir):
        remote=self.dst.remote
        if is_dir:
            try: remote.mkdir(rpath)
            except Exception: remote.list(rpath)
            for child in Path(lpath).iterdir(): self.local_to_remote(str(child),posixpath.join(rpath,child.name),child.is_dir() and not child.is_symlink())
        elif remote.proto=='SFTP':
            size=Path(lpath).stat().st_size; remote.client.put(lpath,rpath,callback=lambda done,total:self.signals.progress.emit(min(99,int((self.done_bytes+done)*100/self.total_bytes))) if self.total_bytes else None); self.done_bytes+=size
        else:
            with open(lpath,'rb') as f:
                def cb(block): self.report_bytes(len(block))
                remote.client.storbinary('STOR '+rpath,f,blocksize=65536,callback=cb)
    def remove_remote(self,rpath,is_dir):
        remote=self.src.remote
        if is_dir:
            for name,d,size in remote.list(rpath):
                if name!='..': self.remove_remote(posixpath.join(rpath,name),d)
            remote.rmdir(rpath)
        elif remote.proto=='SFTP': remote.client.remove(rpath)
        else: remote.client.delete(rpath)

class Main(QMainWindow):
    def __init__(self):
        super().__init__(); self.language='de'; self.setWindowTitle(self.tr('about_version')); self.resize(1500,900); self.setMinimumSize(1050,680); self.active=None; self.clip=None; self.dark=True; self.click_mode='double'; self.config_path=Path.home()/'.config/lunacommander/settings.json'; self.config={}; self.load_config(); self.language=self.config.get('language','de')
        self.left=Pane(self); self.right=Pane(self); self.active=self.left
        # Restore each pane's sort mode before loading the startup folders.
        for pane, side in ((self.left, 'left'), (self.right, 'right')):
            pane.sort_field = self.config.get(f'sort_{side}_field', 'name')
            pane.sort_descending = bool(self.config.get(f'sort_{side}_descending', False))
        self.restore_start_folders(); self.thread_pool=QThreadPool.globalInstance(); self.transfer_busy=False; self.transfer_queue=[]; self.queue_labels=[]
        split=QSplitter(); split.addWidget(self.left); split.addWidget(self.right); split.setSizes([620,620])
        central=QWidget(); lay=QVBoxLayout(central); lay.setContentsMargins(8,8,8,8)
        # The top actions are placed in a normal horizontal layout instead of
        # QToolBar's size-hint based layout. Equal stretch factors make every
        # button share the full available width, with no unused strip at right.
        top_bar=QWidget(); top_bar.setObjectName('topActionBar')
        top_layout=QHBoxLayout(top_bar); top_layout.setContentsMargins(0,0,0,0); top_layout.setSpacing(2)
        toolbar_actions=[
            ('new','SP_FileDialogNewFolder',self.new_file),('copy','SP_FileIcon',self.copy),('move','SP_ArrowForward',self.move_other),('delete','SP_TrashIcon',self.delete),('rename','SP_FileDialogDetailedView',self.rename),('properties','SP_MessageBoxInformation',self.properties),('refresh','SP_BrowserReload',self.refresh),('archive','SP_DirOpenIcon',self.show_menu),('ftp','SP_DriveNetIcon',lambda:self.connect_remote('FTP')),('sftp','SP_DriveNetIcon',lambda:self.connect_remote('SFTP')),('ftps','SP_DriveNetIcon',lambda:self.connect_remote('FTPS')),('disconnect','SP_DialogCancelButton',self.disconnect),('search','SP_FileDialogContentsView',self.search_files),('settings','SP_FileDialogInfoView',self.settings_dialog)
        ]
        self.toolbar_actions=[]; self.toolbar_buttons=[]
        for key,icon_name,fn in toolbar_actions:
            a=QAction(self.style().standardIcon(getattr(QStyle,icon_name)),self.tr(key),self); a.triggered.connect(fn)
            b=QToolButton(); b.setDefaultAction(a); b.setToolButtonStyle(Qt.ToolButtonTextUnderIcon); b.setIconSize(QSize(24,24))
            b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred); b.setMinimumWidth(0); b.setMinimumHeight(52)
            b.setObjectName('topActionButton'); top_layout.addWidget(b,1); self.toolbar_actions.append((a,key)); self.toolbar_buttons.append(b)
        lay.addWidget(top_bar)
        lay.addWidget(split,1)
        split.setMinimumHeight(300)
        self.function_bar=QWidget(); self.function_layout=QHBoxLayout(self.function_bar)
        self.function_layout.setContentsMargins(0,5,0,5); self.function_layout.setSpacing(5)
        function_defs=[
            ('help','SP_DialogHelpButton',self.show_help),('menu','SP_FileDialogListView',self.show_menu),('view','SP_FileDialogContentsView',self.view_selected),('edit','SP_FileDialogDetailedView',self.edit_selected),('copy','SP_FileIcon',self.copy_other),('move','SP_ArrowForward',self.move_other),('new_folder','SP_FileDialogNewFolder',self.new_folder),('delete','SP_TrashIcon',self.delete),('settings','SP_FileDialogInfoView',self.settings_dialog),('exit','SP_DialogCloseButton',self.close)
        ]
        self.function_buttons=[]
        for i,(key,icon_name,fn) in enumerate(function_defs,1):
            label=f'F{i} {self.tr(key)}'; b=QPushButton(label); b.setIcon(self.style().standardIcon(getattr(QStyle,icon_name))); b.setIconSize(QSize(20,20)); b.setObjectName('functionKey'); b.setMinimumHeight(44); b.setMinimumWidth(100); b.setToolTip(label)
            b.clicked.connect(fn); self.function_layout.addWidget(b,1); self.function_buttons.append(b)
            shortcut=QAction(self); shortcut.setShortcut(QKeySequence(f'F{i}')); shortcut.setShortcutContext(Qt.ApplicationShortcut)
            shortcut.triggered.connect(fn); self.addAction(shortcut)
        lay.addWidget(self.function_bar)
        self.queue_label=QLabel('📦  '+self.tr('queue')); lay.addWidget(self.queue_label)
        self.queue_area=QWidget(); self.queue_layout=QVBoxLayout(self.queue_area)
        self.queue_layout.setContentsMargins(0,0,0,0); self.queue_layout.setSpacing(3)
        self.queue_labels=[]; self.queue_next_index=0
        for slot in range(3):
            row=QWidget(); row.setFixedHeight(25); box=QHBoxLayout(row); box.setContentsMargins(4,0,4,0); box.setSpacing(8)
            title=QLabel(self.tr('ready')); title.setMinimumWidth(220); title.setMaximumWidth(420)
            progress=QProgressBar(); progress.setRange(0,100); progress.setValue(0); progress.setTextVisible(True); progress.setFormat('%p%'); progress.setFixedHeight(18)
            box.addWidget(title); box.addWidget(progress,1)
            self.queue_layout.addWidget(row); self.queue_labels.append((row,title,progress))
        self.queue_area.setMinimumHeight(87); self.queue_area.setMaximumHeight(87); lay.addWidget(self.queue_area)
        self.setCentralWidget(central); self.statusBar().showMessage('Bereit')
        self.make_menu(); self.setStyleSheet(self.stylesheet())
        self.click_mode=self.config.get('click_mode','double'); self.apply_language()
    def configured_folder(self, key):
        raw = self.config.get(key) or str(Path.home())
        path = Path(raw).expanduser()
        return str(path.resolve()) if path.is_dir() else str(Path.home())
    def restore_start_folders(self):
        defaults = {'default_left': str(Path.home()), 'default_right': str(Path.home())}
        use_last = bool(self.config.get('remember_last_dirs', True))
        for pane, side in ((self.left, 'left'), (self.right, 'right')):
            fallback = self.config.get('default_' + side, defaults['default_' + side])
            fallback_path = Path(fallback).expanduser()
            if not fallback_path.is_dir(): fallback_path = Path.home()
            candidate = self.config.get('last_' + side) if use_last else None
            candidate_path = Path(candidate).expanduser() if candidate else fallback_path
            if not candidate_path.is_dir(): candidate_path = fallback_path
            pane.load(str(candidate_path), remember=False)
    def store_pane_path(self, pane, path):
        if not hasattr(self, 'left') or not hasattr(self, 'right'): return
        if getattr(pane, 'remote', None) or getattr(pane, 'archive_file', None): return
        key = 'last_left' if pane is self.left else 'last_right'
        self.config[key] = str(path)
        self.save_config()
    def tr(self,key):
        return TRANSLATIONS.get(self.language,TRANSLATIONS['de']).get(key,TRANSLATIONS['de'].get(key,key))
    def apply_language(self):
        self.setWindowTitle(self.tr('about_version'))
        for action,key in getattr(self,'toolbar_actions',[]): action.setText(self.tr(key)); action.setToolTip(self.tr(key))
        keys=['help','menu','view','edit','copy','move','new_folder','delete','settings','exit']
        for i,(button,key) in enumerate(zip(getattr(self,'function_buttons',[]),keys),1):
            button.setText(f'F{i} {self.tr(key)}'); button.setToolTip(f'F{i} {self.tr(key)}')
        if hasattr(self,'queue_label'): self.queue_label.setText('📦  '+self.tr('queue'))
        for pane in (getattr(self,'left',None),getattr(self,'right',None)):
            if pane:
                pane.tree.setHeaderLabels([self.tr('name'),self.tr('type'),self.tr('size')])
                if pane.nav_buttons:
                    for button,key in zip(pane.nav_buttons[:3],('back','up','home')):
                        button.setToolTip(self.tr(key)); button.setAccessibleName(self.tr(key))
                    pane.nav_buttons[-1].setText(self.tr('open'))
                for row in range(pane.tree.topLevelItemCount()):
                    item=pane.tree.topLevelItem(row); data=item.data(0,Qt.UserRole)
                    if data: item.setText(1,self.tr('folder') if data[1] else self.tr('file'))
        self.menuBar().clear(); self.make_menu()
        self.statusBar().showMessage(self.tr('ready'))
    def make_menu(self):
        menus=[
            (self.tr('file_menu'),[(self.tr('new')+'…',self.new_file),(self.tr('new_folder'),self.new_folder),(self.tr('exit'),self.close)]),
            (self.tr('connection'),[(self.tr('ftp')+' '+self.tr('connect').lower(),lambda:self.connect_remote('FTP')),(self.tr('ftps')+' '+self.tr('connect').lower(),lambda:self.connect_remote('FTPS')),(self.tr('sftp')+' '+self.tr('connect').lower(),lambda:self.connect_remote('SFTP')),(self.tr('disconnect'),self.disconnect)]),
            (self.tr('view_menu'),[(self.tr('refresh'),self.refresh),(self.tr('theme'),self.toggle_theme)]),
            (self.tr('settings'),[(self.tr('settings'),self.settings_dialog)]),
            (self.tr('help'),[(self.tr('help'),self.show_help),(self.tr('about'),self.show_about)])
        ]
        for title,items in menus:
            m=self.menuBar().addMenu(title)
            for label,fn in items:
                a=m.addAction(label); a.triggered.connect(fn)
    def stylesheet(self):return 'QMainWindow,QWidget{background:#091827;color:#e7f2ff} QTreeWidget{background:#102235;alternate-background-color:#132a40;selection-background-color:#0864b5;border:1px solid #245b8d} QHeaderView::section{background:#123454;color:white;padding:6px;border:0} QLineEdit{background:#102b43;color:white;padding:6px;border:1px solid #245b8d} QPushButton,QToolButton{background:#104574;color:white;padding:6px;border:1px solid #2677ad;border-radius:4px} QMenu{background:#102b43;color:white} QMenu::item:selected{background:#0864b5} QMenuBar{background:#0b1d2d;color:#e7f2ff} QMenuBar::item:selected{background:#0864b5} QPushButton#functionKey{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1264ae,stop:1 #073b78);color:white;border:1px solid #1686e6;border-radius:6px;padding:8px 4px;font-weight:bold;font-size:13px} QPushButton#functionKey:hover{background:#0874d1;border:1px solid #63c5ff} QWidget#topActionBar{background:#0b2034;border:0} QToolButton#topActionButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #17496f,stop:1 #0c2c49);border:1px solid #286b99;border-radius:6px;padding:6px 6px;margin:1px;font-weight:bold} QProgressBar{background:#102b40;color:#f4f8fc;border:1px solid #315c7b;border-radius:5px;text-align:center;height:18px} QProgressBar::chunk{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1596e8,stop:1 #49c0ff);border-radius:4px} QToolButton#topActionButton:hover{background:#075ba2} QStatusBar{background:#071522;color:#cfe6ff} QTreeWidget::item{height:32px;padding:2px} QTreeWidget{font-size:14px} QHeaderView::section{font-size:14px;padding:7px}'
    def show_menu(self):
        # F2 must open a menu, not merely move focus to the menu bar.
        self.menuBar().setVisible(True)
        actions=self.menuBar().actions()
        if actions and actions[0].menu():
            actions[0].menu().popup(QCursor.pos())
    def show_help(self):
        dialog=QDialog(self)
        dialog.setWindowTitle('LunaCommander – '+self.tr('help'))
        dialog.resize(820,700)
        layout=QVBoxLayout(dialog)
        browser=QTextBrowser(dialog)
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
        browser.setHtml('<html><head><meta charset="utf-8"><style>'
                        'body{font-family:sans-serif;font-size:10.5pt;line-height:1.45;padding:8px;}'
                        'h1{color:#238bd1;font-size:20pt;} h2{color:#238bd1;font-size:13pt;margin-top:22px;}'
                        'li{margin:5px 0;} p{margin:8px 0;}'
                        '</style></head><body>'+HELP_CONTENT.get(self.language,HELP_CONTENT['en'])+'</body></html>')
        layout.addWidget(browser,1)
        buttons=QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        close_button=buttons.button(QDialogButtonBox.Close)
        if close_button:
            close_button.setText({'de':'Schließen','en':'Close','fr':'Fermer','it':'Chiudi','nl':'Sluiten'}.get(self.language,'Close'))
        layout.addWidget(buttons)
        dialog.exec()
    def show_about(self):
        about_text=(f"<div style='text-align:center;'>"
                    f"<p><b>{self.tr('about_version')}</b></p>"
                    f"<p>Goldisoft 2026</p>"
                    f"</div>")
        QMessageBox.about(self,self.tr('about'),about_text)
    def view_selected(self):
        p=self.active or self.left; r=p.selected()
        if r and not r[1]: p.activate(p.tree.currentItem(),0)
    def edit_selected(self):
        self.view_selected()
    def settings_dialog(self):
        d=QDialog(self); d.setWindowTitle(self.tr('settings')); f=QFormLayout(d)
        lang=QComboBox(); lang.addItem('Deutsch','de'); lang.addItem('English','en'); lang.addItem('Français','fr'); lang.addItem('Italiano','it'); lang.addItem('Nederlands','nl'); lang.setCurrentIndex(max(0,lang.findData(self.language))); f.addRow(self.tr('language'),lang)
        theme=QComboBox(); theme.addItems([self.tr('dark'),self.tr('light')]); theme.setCurrentIndex(0 if self.dark else 1)
        f.addRow(self.tr('scheme'),theme)
        click=QComboBox(); click.addItem(self.tr('double'),'double'); click.addItem(self.tr('single'),'single'); click.setCurrentIndex(0 if self.click_mode=='double' else 1)
        f.addRow(self.tr('open_mode'),click)
        f.addRow(QLabel('<b>'+self.tr('start_folders')+'</b>'))
        remember=QCheckBox(self.tr('remember_dirs')); remember.setChecked(bool(self.config.get('remember_last_dirs', True)))
        f.addRow(remember)
        show_hidden=QCheckBox(self.tr('show_hidden'))
        show_hidden.setChecked(bool(self.config.get('show_hidden', False)))
        f.addRow(show_hidden)
        photo_preview=QCheckBox(self.tr('photo_preview'))
        photo_preview.setChecked(bool(self.config.get('photo_preview', False)))
        f.addRow(photo_preview)
        left_row=QWidget(); left_layout=QHBoxLayout(left_row); left_layout.setContentsMargins(0,0,0,0)
        left_path=QLineEdit(str(self.config.get('default_left', str(Path.home())))); left_browse=QPushButton(self.tr('browse'))
        left_browse.clicked.connect(lambda: (lambda chosen: left_path.setText(chosen) if chosen else None)(QFileDialog.getExistingDirectory(d,self.tr('default_left'),left_path.text() or str(Path.home()))))
        left_layout.addWidget(left_path,1); left_layout.addWidget(left_browse); f.addRow(self.tr('default_left'),left_row)
        right_row=QWidget(); right_layout=QHBoxLayout(right_row); right_layout.setContentsMargins(0,0,0,0)
        right_path=QLineEdit(str(self.config.get('default_right', str(Path.home())))); right_browse=QPushButton(self.tr('browse'))
        right_browse.clicked.connect(lambda: (lambda chosen: right_path.setText(chosen) if chosen else None)(QFileDialog.getExistingDirectory(d,self.tr('default_right'),right_path.text() or str(Path.home()))))
        right_layout.addWidget(right_path,1); right_layout.addWidget(right_browse); f.addRow(self.tr('default_right'),right_row)
        f.addRow(QLabel('<b>Archivprogramme – externe Programme</b>'))
        archive_fields={}
        archive_defaults={
            'zip': ('zip', 'zip'),
            'rar': ('rar', 'rar'),
            '7z': ('7zz', '7z'),
            'tar': ('tar', 'tar'),
        }
        archive_labels={'zip':'ZIP','rar':'RAR','7z':'7-Zip','tar':'TAR','tar.gz':'TAR.GZ','tar.xz':'TAR.XZ','tar.bz2':'TAR.BZ2'}
        for fmt,(command,display) in archive_defaults.items():
            configured=(self.config.get('archive_binaries',{}).get(fmt,'') or '').strip()
            detected=configured or shutil.which(command) or (shutil.which('7z') if fmt=='7z' else '')
            row=QWidget(); row_layout=QHBoxLayout(row); row_layout.setContentsMargins(0,0,0,0)
            field=QLineEdit(detected or '')
            browse=QPushButton(self.tr('browse'))
            browse.clicked.connect(lambda checked=False, w=field: (lambda chosen: w.setText(chosen) if chosen else None)(QFileDialog.getOpenFileName(d,'Programm auswählen',w.text() or '/usr/bin')[0]))
            status=QLabel('Installiert' if detected and Path(detected).is_file() and os.access(detected,os.X_OK) else 'Nicht gefunden')
            field.textChanged.connect(lambda value, label=status: label.setText('Installiert' if value and Path(value).is_file() and os.access(value,os.X_OK) else 'Nicht gefunden'))
            row_layout.addWidget(field,1); row_layout.addWidget(browse); row_layout.addWidget(status)
            f.addRow(archive_labels[fmt],row); archive_fields[fmt]=field
        f.addRow(QLabel('<b>'+self.tr('installed')+'</b>'))
        editor_info=self.default_app_for('text/plain')
        f.addRow(self.tr('text_files'),QLabel(editor_info))
        buttons=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        # Set captions ourselves: Qt's standard labels can remain English on a German desktop.
        button_texts = {
            'de': ('OK', self.tr('cancel')), 'en': ('OK', 'Cancel'),
            'fr': ('Valider', 'Annuler'), 'it': ('OK', 'Annulla'),
            'nl': ('OK', 'Annuleren'),
        }
        ok_text, cancel_text = button_texts.get(self.language, button_texts['en'])
        buttons.button(QDialogButtonBox.Ok).setText(ok_text)
        buttons.button(QDialogButtonBox.Cancel).setText(cancel_text)
        f.addRow(buttons)
        buttons.accepted.connect(d.accept); buttons.rejected.connect(d.reject)
        if d.exec()==QDialog.Accepted:
            self.dark=(theme.currentIndex()==0); self.click_mode=click.currentData(); self.language=lang.currentData()
            self.config['click_mode']=self.click_mode; self.config['language']=self.language
            self.config['remember_last_dirs']=remember.isChecked()
            hidden_changed=bool(self.config.get('show_hidden', False)) != show_hidden.isChecked()
            self.config['show_hidden']=show_hidden.isChecked()
            self.config['photo_preview']=photo_preview.isChecked()
            self.config['archive_binaries']={fmt: field.text().strip() for fmt,field in archive_fields.items()}
            self.config['rar_binary']=self.config['archive_binaries'].get('rar','')
            for key, field in (('default_left', left_path), ('default_right', right_path)):
                candidate=Path(field.text()).expanduser()
                self.config[key]=str(candidate.resolve()) if candidate.is_dir() else str(Path.home())
            self.save_config()
            self.left.set_thumbnail_mode(photo_preview.isChecked())
            self.right.set_thumbnail_mode(photo_preview.isChecked())
            if hidden_changed:
                self.left.load(self.left.path, remember=False)
                self.right.load(self.right.path, remember=False)
            if not remember.isChecked():
                self.left.load(self.config['default_left'], remember=False)
                self.right.load(self.config['default_right'], remember=False)
            self.apply_language()
            self.setStyleSheet(self.stylesheet() if self.dark else 'QWidget{background:#edf3f8;color:#172b3d} QTreeWidget{background:white;color:#172b3d} QLineEdit{background:white;color:#172b3d}')
    def default_app_for(self,mime):
        try:
            result=subprocess.run(['xdg-mime','query','default',mime],capture_output=True,text=True,timeout=3)
            desktop=result.stdout.strip()
            if desktop:
                return desktop
        except Exception: pass
        return 'System-Standardprogramm (QDesktopServices)'
    def detect_rar_binary(self):
        configured=(self.config.get('rar_binary') or '').strip()
        candidates=[configured, shutil.which('rar'), '/usr/local/bin/rar', '/usr/bin/rar', str(Path.home()/'.local/bin/rar')]
        for candidate in candidates:
            if candidate and Path(candidate).is_file() and os.access(candidate,os.X_OK): return str(Path(candidate).resolve())
        return ''
    def archive_tool(self, fmt):
        configured=(self.config.get('archive_binaries',{}).get(fmt,'') or '').strip()
        defaults={'zip':['zip'],'rar':['rar'],'7z':['7zz','7z'],'tar':['tar'],'tar.gz':['tar'],'tar.xz':['tar'],'tar.bz2':['tar']}
        candidates=[configured] if configured else []
        candidates += [shutil.which(x) for x in defaults.get(fmt,[])]
        for candidate in candidates:
            if candidate and Path(candidate).is_file() and os.access(candidate,os.X_OK):
                return str(Path(candidate).resolve())
        return ''

    def archive_backend_info(self):
        path=self.detect_rar_binary()
        if path:return f'RAR ({path})'
        for command in ('unar','unrar','7zz','7z'):
            found=shutil.which(command)
            if found:return f'{command} ({found}) – nur zum Entpacken/Lesen'
        return 'Kein RAR-Programm gefunden.'
    def archive_path(self):
        p=self.active; row=p.selected()
        if not row or row[0]=='..':return None
        if p.remote:
            QMessageBox.information(self,self.tr('archive_label'),self.tr('archive_local_only')); return None
        return Path(p.target(row[0]))
    def pack_selected(self,fmt):
        pane=self.active
        selected=[]
        if pane and not pane.remote and not pane.archive_file:
            for item in pane.tree.selectedItems():
                row=item.data(0,Qt.UserRole)
                if row and row[0]!='..':
                    selected.append(Path(pane.target(row[0])))
        if not selected:
            source=self.archive_path()
            if source is None:return
            selected=[source]
        parent=selected[0].parent
        if any(item.parent != parent for item in selected):
            QMessageBox.information(self,self.tr('archive_label'),'Bitte nur Dateien und Ordner aus demselben Verzeichnis markieren.')
            return
        suffix={'zip':'.zip','tar':'.tar','tar.gz':'.tar.gz','tar.xz':'.tar.xz','tar.bz2':'.tar.bz2','7z':'.7z','rar':'.rar'}[fmt]
        base_name=selected[0].name if len(selected)==1 else selected[0].stem+'_Auswahl'
        target=parent/(base_name+suffix)
        tool=self.archive_tool(fmt)
        if not tool:
            QMessageBox.warning(self,self.tr('pack_error'),f'Für {fmt.upper()} ist kein Programm eingerichtet. Bitte den Programmpfad in den Einstellungen eintragen.')
            return
        if target.exists():
            choice=QMessageBox.question(self,self.tr('archive_exists'),self.tr('archive_replace'),QMessageBox.Yes|QMessageBox.No)
            if choice!=QMessageBox.Yes:return
            target.unlink()
        try:
            names=[item.name for item in selected]
            if fmt=='zip':
                cmd=[tool,'-r','-q',str(target)]+names
            elif fmt=='rar':
                cmd=[tool,'a','-r','-y',target.name]+names
            elif fmt=='7z':
                cmd=[tool,'a','-t7z',str(target)]+names
            elif fmt=='tar':
                cmd=[tool,'-cf',str(target)]+names
            else:
                flag={'tar.gz':'-czf','tar.xz':'-cJf','tar.bz2':'-cjf'}[fmt]
                cmd=[tool,flag,str(target)]+names
            result=subprocess.run(cmd,cwd=str(parent),capture_output=True,text=True)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f'{fmt.upper()}-Erstellung fehlgeschlagen.')
            pane.load(pane.path)
            self.statusBar().showMessage(self.tr('archive_created')+target.name)
        except Exception as e:
            try: target.unlink(missing_ok=True)
            except Exception: pass
            QMessageBox.warning(self,self.tr('pack_error'),str(e))
    def extract_selected(self):
        source=self.archive_path()
        if source is None:return
        self.extract_archive(source,source.parent)
    def extract_selected_to(self):
        source=self.archive_path()
        if source is None:return
        dest=QFileDialog.getExistingDirectory(self,self.tr('target_folder'),str(source.parent))
        if dest:self.extract_archive(source,Path(dest))
    def extract_archive(self,source,destination):
        name=source.name.lower()
        try:
            if name.endswith('.zip'):
                with zipfile.ZipFile(source) as z:
                    root=destination.resolve()
                    for member in z.infolist():
                        out=(destination/member.filename).resolve()
                        if root not in out.parents and out!=root:raise RuntimeError('Unsicherer Archivpfad wurde blockiert.')
                    z.extractall(destination)
            elif name.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
                with tarfile.open(source,'r:*') as t:
                    root=destination.resolve()
                    for member in t.getmembers():
                        out=(destination/member.name).resolve()
                        if root not in out.parents and out!=root:raise RuntimeError('Unsicherer Archivpfad wurde blockiert.')
                        if member.issym() or member.islnk():raise RuntimeError('Archive mit symbolischen/harten Links werden aus Sicherheitsgründen nicht entpackt.')
                    t.extractall(destination,filter='data')
            elif name.endswith(('.rar','.7z')):
                if name.endswith('.rar'):
                    # Prefer unar/unrar for RAR: Debian's free 7zip build omits the proprietary RAR decoder.
                    tool=shutil.which('unar') or shutil.which('unrar') or shutil.which('7zz') or shutil.which('7z')
                else:
                    tool=shutil.which('7zz') or shutil.which('7z') or shutil.which('unar')
                if not tool:raise RuntimeError('Archivprogramm fehlt. Installiere unter Debian: sudo apt install 7zip unar unrar-free.')
                if Path(tool).name in ('7z','7zz'):cmd=[tool,'x','-y',f'-o{destination}',str(source)]
                elif Path(tool).name=='unar':cmd=[tool,'-o',str(destination),str(source)]
                else:cmd=[tool,'x','-o+',str(source),str(destination)]
                result=subprocess.run(cmd,capture_output=True,text=True)
                if result.returncode:raise RuntimeError(result.stderr or result.stdout or 'Entpacken fehlgeschlagen.')
            else:raise RuntimeError('Dieses Archivformat wird nicht unterstützt.')
            self.active.load(self.active.path); self.statusBar().showMessage(self.tr('extracted')+source.name)
        except Exception as e:QMessageBox.warning(self,self.tr('extract_error'),str(e))
    def open_archive_member(self, archive, member):
        try:
            import tempfile
            suffix=Path(member).suffix
            cache=Path.home()/'.cache/lunacommander/archive-open'
            cache.mkdir(parents=True,exist_ok=True)
            target=cache/(Path(member).name)
            if archive.name.lower().endswith('.zip'):
                with zipfile.ZipFile(archive) as z:
                    info=z.getinfo(member)
                    if info.file_size > 512*1024*1024: raise RuntimeError('Datei ist für das direkte Öffnen zu groß (über 512 MB).')
                    target.write_bytes(z.read(info))
            elif archive.name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2','.tar.zst')):
                with tarfile.open(archive,'r:*') as t:
                    info=t.getmember(member)
                    if not info.isfile() or info.size > 512*1024*1024: raise RuntimeError('Datei kann nicht direkt geöffnet werden oder ist zu groß.')
                    stream=t.extractfile(info)
                    if stream is None: raise RuntimeError('Datei konnte nicht gelesen werden.')
                    target.write_bytes(stream.read())
            else:
                tool=shutil.which('7zz') or shutil.which('7z')
                if not tool: raise RuntimeError('7zip wird zum Öffnen dieser Archivdatei benötigt.')
                result=subprocess.run([tool,'e','-y',f'-o{cache}',str(archive),member],capture_output=True,text=True)
                if result.returncode: raise RuntimeError(result.stderr or result.stdout or 'Datei konnte nicht extrahiert werden.')
                target=cache/Path(member).name
            from PySide6.QtGui import QDesktopServices
            from PySide6.QtCore import QUrl
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(target)))
        except Exception as e: QMessageBox.warning(self,self.tr('open_archive_error'),str(e))
    def search_files(self):
        p=self.active or self.left
        term,ok=QInputDialog.getText(self,self.tr('search'),self.tr('search_prompt'))
        if not ok or not term:return
        if p.remote:
            QMessageBox.information(self,self.tr('search'),self.tr('remote_search_unavailable')); return
        matches=[]
        try:
            for root,dirs,files in os.walk(p.path):
                for name in dirs+files:
                    if term.casefold() in name.casefold(): matches.append(str(Path(root)/name))
                    if len(matches)>=500: break
                if len(matches)>=500: break
            QMessageBox.information(self,self.tr('search_results'), '\\n'.join(matches[:80]) if matches else self.tr('no_matches'))
        except Exception as e: QMessageBox.warning(self,self.tr('search_error'),str(e))
    def load_config(self):
        try:self.config=json.loads(self.config_path.read_text())
        except Exception:self.config={}
    def save_config(self):
        self.config_path.parent.mkdir(parents=True,exist_ok=True); self.config_path.write_text(json.dumps(self.config,indent=2)); os.chmod(self.config_path,0o600)
    def remember_open_with(self, target, program):
        name=target.name.lower()
        ext=next((x for x in ('.tar.gz','.tar.xz','.tar.bz2') if name.endswith(x)),target.suffix.lower()) or '[no-extension]'
        apps=self.config.setdefault('open_with_apps',{})
        apps[ext]={'program':str(Path(program).resolve()),'name':Path(program).name}
        self.save_config()

    def open_with_suggestions(self, target):
        """Return installed, sensible applications for a file type; remembered choice first."""
        name=target.name.lower()
        ext=next((x for x in ('.tar.gz','.tar.xz','.tar.bz2') if name.endswith(x)),target.suffix.lower())
        groups={
            'video': ('.mp4','.mkv','.avi','.mov','.wmv','.webm','.mpeg','.mpg','.m4v','.ts','.mts','.m2ts','.flv','.vob','.ogv','.3gp'),
            'audio': ('.mp3','.wav','.flac','.ogg','.opus','.m4a','.aac','.wma','.aiff','.aif','.ape','.alac','.mid','.midi','.amr','.ac3','.dts','.dsf','.wv'),
            'image': ('.jpg','.jpeg','.png','.gif','.bmp','.webp','.tif','.tiff','.avif','.svg'),
            'pdf': ('.pdf',),
            'text': ('.txt','.md','.log','.csv','.json','.xml','.yaml','.yml','.ini','.conf','.py','.sh','.html','.css','.js','.desktop'),
            'office': ('.doc','.docx','.odt','.rtf','.xls','.xlsx','.ods','.ppt','.pptx','.odp'),
            'archive': ('.zip','.rar','.7z','.tar','.gz','.tgz','.xz','.bz2','.tar.gz','.tar.xz','.tar.bz2'),
            'ebook': ('.epub','.mobi'),
        }
        candidates={
            'video': [('VLC','vlc'),('MPV','mpv')],
            'audio': [('VLC','vlc'),('MPV','mpv'),('Audacious','audacious')],
            'image': [('Bildbetrachter','loupe'),('Ristretto','ristretto'),('Eye of GNOME','eog'),('Gwenview','gwenview'),('Feh','feh')],
            'pdf': [('Document Viewer','evince'),('Atril','atril'),('Okular','okular'),('Xreader','xreader')],
            'text': [('Mousepad','mousepad'),('Geany','geany'),('Kate','kate'),('Gedit','gedit'),('Xed','xed')],
            'office': [('LibreOffice','libreoffice'),('OnlyOffice','onlyoffice-desktopeditors')],
            'archive': [('Engrampa','engrampa'),('File Roller','file-roller'),('Ark','ark'),('Xarchiver','xarchiver')],
            'ebook': [('Calibre','ebook-viewer'),('Foliate','foliate'),('Okular','okular')],
        }
        kind=next((k for k,extensions in groups.items() if ext in extensions),None)
        result=[]; seen=set()
        remembered=self.config.get('open_with_apps',{}).get(ext,{})
        if remembered:
            program=remembered.get('program','')
            if program and Path(program).is_file() and os.access(program,os.X_OK):
                result.append((remembered.get('name') or Path(program).name,program,True)); seen.add(os.path.realpath(program))
        for name,command in candidates.get(kind,[]):
            program=shutil.which(command)
            if program and os.path.realpath(program) not in seen:
                result.append((name,program,False)); seen.add(os.path.realpath(program))
        return result
    def connect_remote(self,proto):
        d=QDialog(self);d.setWindowTitle(proto+' '+self.tr('connect').lower());f=QFormLayout(d);last=self.config.get('last_connection',{}); host=QLineEdit(last.get('host',''));port=QLineEdit(str(last.get('port',{'FTP':21,'FTPS':21,'SFTP':22}[proto])));user=QLineEdit(last.get('user',''));pw=QLineEdit(last.get('password',''));pw.setEchoMode(QLineEdit.Password)
        for label,w in [('Server',host),('Port',port),('Benutzer',user),('Passwort',pw)]:f.addRow(label,w)
        buttons=QDialogButtonBox(); connect_btn=buttons.addButton('Verbinden',QDialogButtonBox.AcceptRole); cancel_btn=buttons.addButton(self.tr('cancel'),QDialogButtonBox.RejectRole); f.addRow(buttons); connect_btn.clicked.connect(d.accept); cancel_btn.clicked.connect(d.reject)
        if d.exec()!=QDialog.Accepted:return
        try:
            r=Remote(proto,host.text(),int(port.text()),user.text(),pw.text()); pane=self.active or self.left
            if pane.remote:pane.remote.close()
            pane.remote=r;pane.load('/');self.config['last_connection']={'host':host.text(),'port':int(port.text()),'user':user.text(),'password':pw.text(),'proto':proto};self.save_config();self.statusBar().showMessage(proto+' '+self.tr('connected'))
        except Exception as e:QMessageBox.critical(self,self.tr('connection_error'),str(e))
    def disconnect(self):
        p=self.active or self.left
        if p.remote:p.remote.close();p.remote=None;p.load(str(Path.home()))
    def refresh(self):self.left.load(self.left.path);self.right.load(self.right.path)
    def other(self,p):return self.right if p is self.left else self.left
    def ask_name(self,title,label,default=''):
        n,ok=QInputDialog.getText(self,title,label,text=default);return n.strip() if ok else None
    def new_folder(self):
        p=self.active;n=self.ask_name('Neuer Ordner',self.tr('folder_name'))
        if n:
            try:p.remote.mkdir(posixpath.join(p.path,n)) if p.remote else Path(p.path,n).mkdir();p.load(p.path)
            except Exception as e:QMessageBox.warning(self,self.tr('generic_error'),str(e))
    def new_file(self):
        p=self.active;n=self.ask_name('Neue Datei',self.tr('file_name'))
        if n:
            try:
                if p.remote:
                    path=posixpath.join(p.path,n)
                    if p.remote.proto=='SFTP':p.remote.client.open(path,'wb').close()
                    else:
                        import io;p.remote.client.storbinary('STOR '+path,io.BytesIO(b''))
                else:Path(p.path,n).touch(exist_ok=False)
                p.load(p.path)
            except Exception as e:QMessageBox.warning(self,self.tr('generic_error'),str(e))
    def rename(self):
        p=self.active;r=p.selected()
        if not r or r[0]=='..':return
        n=self.ask_name('Umbenennen',self.tr('new_name'),r[0])
        if n:
            try:
                if p.remote:p.remote.client.rename(p.target(r[0]),p.target(n))
                else:Path(p.target(r[0])).rename(p.target(n))
                p.load(p.path)
            except Exception as e:QMessageBox.warning(self,self.tr('generic_error'),str(e))
    def delete_archive_member(self, archive, member, is_dir):
        """Remove one member or a complete directory subtree from an archive."""
        import tempfile
        archive=Path(archive); low=archive.name.lower(); member=member.strip('/')
        if not member: raise RuntimeError('Das Archiv selbst kann hier nicht gelöscht werden.')
        def selected(name):
            name=name.replace('\\','/').strip('/')
            return name==member or (is_dir and name.startswith(member+'/'))
        if low.endswith('.zip'):
            fd,tmp=tempfile.mkstemp(prefix='lunacommander-delete-',suffix='.zip',dir=str(archive.parent)); os.close(fd)
            try:
                with zipfile.ZipFile(archive,'r') as src, zipfile.ZipFile(tmp,'w') as dst:
                    for info in src.infolist():
                        if selected(info.filename): continue
                        dst.writestr(info,src.read(info.filename) if not info.is_dir() else b'')
                os.replace(tmp,archive)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        elif low.endswith(('.tar','.tar.gz','.tgz','.tar.xz','.txz','.tar.bz2','.tbz2')):
            fd,tmp=tempfile.mkstemp(prefix='lunacommander-delete-',suffix=''.join(archive.suffixes) or '.tar',dir=str(archive.parent)); os.close(fd)
            try:
                mode='w:gz' if low.endswith(('.tar.gz','.tgz')) else 'w:xz' if low.endswith(('.tar.xz','.txz')) else 'w:bz2' if low.endswith(('.tar.bz2','.tbz2')) else 'w'
                with tarfile.open(archive,'r:*') as src, tarfile.open(tmp,mode) as dst:
                    for info in src.getmembers():
                        if selected(info.name): continue
                        stream=src.extractfile(info) if info.isfile() else None
                        if stream is None: dst.addfile(info)
                        else:
                            with stream: dst.addfile(info,stream)
                os.replace(tmp,archive)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        elif low.endswith(('.7z','.rar')):
            tool=shutil.which('7zz') or shutil.which('7z')
            if not tool: raise RuntimeError('Zum Bearbeiten dieses Archivs wird 7-Zip benötigt.')
            if low.endswith('.rar'):
                raise RuntimeError('RAR-Archive können mit den freien Debian-Werkzeugen nicht zuverlässig bearbeitet werden.')
            cmd=[tool,'d',str(archive),member]
            if is_dir: cmd.append('-r')
            result=subprocess.run(cmd,capture_output=True,text=True)
            if result.returncode: raise RuntimeError(result.stderr or result.stdout or 'Eintrag konnte nicht aus dem Archiv gelöscht werden.')
        else: raise RuntimeError('Das Löschen wird für dieses Archivformat nicht unterstützt.')

    def delete(self):
        p=self.active
        if p is None:return
        rows=[]
        for item in p.tree.selectedItems():
            row=item.data(0,Qt.UserRole)
            if row and row[0] != '..':
                rows.append((row[0],bool(row[1]),row[2]))
        if not rows:
            row=p.selected()
            if row and row[0] != '..':
                rows=[(row[0],bool(row[1]),row[2])]
        if not rows:return
        # Avoid separately deleting children already covered by a selected directory.
        filtered=[]
        for name,is_dir,size in rows:
            if any(parent_is_dir and name.startswith(parent.rstrip('/')+'/')
                   for parent,parent_is_dir,_ in rows if parent != name):
                continue
            filtered.append((name,is_dir,size))
        rows=filtered
        if not rows:return
        if len(rows)==1:
            prompt=self.tr('delete_confirm').format(name=rows[0][0])
        else:
            count=len(rows)
            prompt={
                'de':f'{count} markierte Dateien und Ordner wirklich löschen?',
                'en':f'Really delete {count} selected files and folders?',
                'fr':f'Supprimer les {count} fichiers et dossiers sélectionnés ({count}) ?',
                'it':f'Eliminare i {count} file e cartelle selezionati?',
                'nl':f'{count} geselecteerde bestanden en mappen echt verwijderen?'
            }.get(self.language,f'Really delete {count} selected files and folders?')
        box=QMessageBox(self)
        box.setWindowTitle(self.tr('delete_title'))
        box.setText(prompt)
        no_btn=box.addButton(self.tr('no'),QMessageBox.RejectRole)
        yes_btn=box.addButton(self.tr('yes'),QMessageBox.DestructiveRole)
        box.setDefaultButton(no_btn)
        box.exec()
        if box.clickedButton() is not yes_btn:return
        worker=DeleteBatchWorker(p,rows)
        label=QLabel(self.tr('deleting')+f'{len(rows)} Einträge')
        progress=self.add_queue_label(label)
        if progress is not None:
            worker.signals.progress.connect(progress.setValue)
        worker.signals.finished.connect(
            lambda n,ok,error,w=worker,l=label,pane=p:self.delete_finished(n,ok,error,w,l,pane))
        self.transfer_queue.append(worker)
        self.statusBar().showMessage(self.tr('deleting')+f' ({len(rows)})')
        self.start_next_transfer()
    def delete_finished(self,name,ok,error,worker,label,pane):
        label.setText((self.tr('done') if ok else self.tr('error'))+name+((' – '+error) if error else ''))
        if ok:
            if pane.archive_file: pane.load_archive(pane.archive_file,pane.archive_inner,False)
            else: pane.load(pane.path)
            self.statusBar().showMessage(self.tr('deleted')+name)
        else:self.statusBar().showMessage(self.tr('delete_error')+error)
        self.transfer_busy=False; QTimer.singleShot(0,self.start_next_transfer)

    def properties(self):
        p=self.active;r=p.selected()
        if r:QMessageBox.information(self,self.tr('properties'),f"{r[0]}\n{self.tr('size_bytes').format(size=r[2])}\n{self.tr('path').format(path=p.path)}")
    def copy(self):
        r=self.active.selected()
        if r and r[0]!='..':self.clip=(self.active,r[0],False)
    def cut(self):
        r=self.active.selected()
        if r and r[0]!='..':self.clip=(self.active,r[0],True)
    def paste(self):
        if not self.clip:return
        src,n,cut=self.clip;dst=self.active
        a=src.target(n);b='/'.join(x for x in (dst.archive_inner,n) if x) if dst.archive_file else dst.target(n)
        if src is dst and os.path.abspath(a)==os.path.abspath(b):
            QMessageBox.information(self,self.tr('insert'),self.tr('same_source')); return
        if src.remote and dst.remote:
            QMessageBox.information(self,self.tr('help'),self.tr('server_copy_unavailable')); return
        row=src.selected(); is_dir=row[1] if row and row[0]==n else (Path(a).is_dir() if not src.remote else False)
        conflict='merge'
        if dst.archive_file:
            probe=TransferWorker(src,dst,a,b,is_dir,cut,conflict)
            exists=probe.archive_destination_exists()
        else: exists=self.target_exists_for_pane(dst,b)
        if exists:
            if dst.archive_file:
                QMessageBox.information(self,self.tr('archive_label'),self.tr('archive_duplicate')); return
            conflict=self.ask_conflict(n)
            if conflict is None:return
        worker=TransferWorker(src,dst,a,b,is_dir,cut,conflict)
        label=QLabel((self.tr('moved') if cut else self.tr('copied'))+n); progress=self.add_queue_label(label)
        worker.signals.progress.connect(progress.setValue)
        worker.signals.finished.connect(lambda name,ok,error,w=worker,l=label,s=src,d=dst:self.transfer_finished(name,ok,error,w,l,s,d))
        self.transfer_queue.append(worker); self.start_next_transfer()
        if cut:self.clip=None
    def target_exists_for_pane(self,pane,target):
        if pane.remote:
            try:
                if pane.remote.proto=='SFTP': pane.remote.client.stat(target)
                else:
                    parent,name=posixpath.split(target.rstrip('/'))
                    try:
                        old=pane.remote.client.pwd(); pane.remote.client.cwd(parent or '/')
                        try: pane.remote.client.sendcmd('MLST '+name)
                        finally: pane.remote.client.cwd(old)
                    except Exception:
                        return any(row[0] == name for row in pane.remote.list(parent or '/'))
                return True
            except Exception:return False
        return Path(target).exists()
    def copy_other(self):self.copy_transfer(False)
    def move_other(self):self.copy_transfer(True)
    def ask_conflict(self,name):
        box=QMessageBox(self); box.setWindowTitle(self.tr('target_exists')); box.setText(self.tr('target_exists_question').format(name=name))
        merge_btn=box.addButton(self.tr('merge'),QMessageBox.AcceptRole)
        replace_btn=box.addButton(self.tr('replace'),QMessageBox.DestructiveRole)
        skip_btn=box.addButton(self.tr('skip'),QMessageBox.ActionRole)
        box.addButton(self.tr('cancel'),QMessageBox.RejectRole); box.exec(); clicked=box.clickedButton()
        if clicked is merge_btn:return 'merge'
        if clicked is replace_btn:return 'replace'
        if clicked is skip_btn:return 'skip'
        return None
    def add_queue_label(self,label):
        # The three queue rows are permanent; a new task reuses them in rotation.
        if not self.queue_labels:
            return None
        index=self.queue_next_index % len(self.queue_labels)
        self.queue_next_index=(index+1) % len(self.queue_labels)
        row,old_title,progress=self.queue_labels[index]
        layout=row.layout()
        layout.removeWidget(old_title); old_title.deleteLater()
        label.setMinimumWidth(220); label.setMaximumWidth(420)
        layout.insertWidget(0,label)
        self.queue_labels[index]=(row,label,progress)
        progress.setValue(0); progress.setVisible(True)
        return progress
    def copy_transfer(self,move):
        src=self.active or self.left; dst=self.other(src); r=src.selected()
        if not r or r[0]=='..':
            self.statusBar().showMessage(self.tr('select_entry'))
            return
        name,is_dir,_=r
        target='/'.join(x for x in (dst.archive_inner,name) if x) if dst.archive_file else dst.target(name)
        conflict='merge'
        exists=False
        if dst.archive_file:
            if src.remote:
                QMessageBox.information(self,self.tr('archive_label'),self.tr('remote_to_archive')); return
            probe=TransferWorker(src,dst,src.target(name),target,is_dir,move,conflict)
            try: exists=probe.archive_destination_exists()
            except Exception as e: QMessageBox.warning(self,self.tr('archive_label'),str(e)); return
        else: exists=self.target_exists_for_pane(dst,target)
        if exists:
            if dst.archive_file:
                QMessageBox.information(self,self.tr('archive_label'),self.tr('archive_duplicate')); return
            conflict=self.ask_conflict(name)
            if conflict is None:return
        worker=TransferWorker(src,dst,src.target(name),target,is_dir,move,conflict)
        label=QLabel((self.tr('moved') if move else self.tr('copied'))+name); progress=self.add_queue_label(label)
        worker.signals.progress.connect(progress.setValue)
        worker.signals.finished.connect(lambda n,ok,error,w=worker,l=label,s=src,d=dst:self.transfer_finished(n,ok,error,w,l,s,d))
        self.transfer_queue.append(worker); self.statusBar().showMessage((self.tr('moved') if move else self.tr('copied'))+name); self.start_next_transfer()
    def start_next_transfer(self):
        if self.transfer_busy or not self.transfer_queue:return
        self.transfer_busy=True; self.current_transfer=self.transfer_queue.pop(0); self.thread_pool.start(self.current_transfer)
    def transfer_finished(self,name,ok,error,worker,label,src,dst):
        label.setText((self.tr('done') if ok else self.tr('error'))+name+((' – '+error) if error else ''))
        if ok:
            if src.archive_file: src.load_archive(src.archive_file,src.archive_inner,False)
            else: src.load(src.path)
            if dst.archive_file: dst.load_archive(dst.archive_file,dst.archive_inner,False)
            else: dst.load(dst.path)
            self.statusBar().showMessage((self.tr('moved') if worker.move else self.tr('copied'))+name)
        else:self.statusBar().showMessage(self.tr('transfer_error')+error)
        self.transfer_busy=False; QTimer.singleShot(0,self.start_next_transfer)
    def ftp_download(self,p,src,dst):
        with open(dst,'wb') as f:p.remote.client.retrbinary('RETR '+src,f.write)
    def toggle_theme(self):
        self.dark=not self.dark;self.setStyleSheet(self.stylesheet() if self.dark else 'QWidget{background:#edf3f8;color:#172b3d} QTreeWidget{background:white;color:#172b3d} QLineEdit{background:white;color:#172b3d}')
    def closeEvent(self,e):
        for pane, side in ((self.left, 'left'), (self.right, 'right')):
            if not pane.remote and not pane.archive_file and Path(pane.path).is_dir(): self.config['last_'+side]=pane.path
        self.save_config()
        for p in (self.left,self.right):
            if p.remote:p.remote.close()
        e.accept()

if __name__=='__main__':
    app=QApplication(sys.argv);app.setApplicationName('LunaCommander');w=Main();w.show();sys.exit(app.exec())
