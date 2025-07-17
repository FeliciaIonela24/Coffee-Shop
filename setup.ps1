# Calea către baza de date
$dbPath = "cafe_app\app.db"

# Ștergere dacă există
if (Test-Path $dbPath) {
    Remove-Item $dbPath
    Write-Host " Baza de date a fost ștearsă."
} else {
    Write-Host "Baza de date nu a fost găsită."
}

# Creare și populare
Write-Host "Rulez init_db.py..."
python cafe_app\init_db.py

# Pornire server
Write-Host "Pornesc serverul Flask..."
python run.py
