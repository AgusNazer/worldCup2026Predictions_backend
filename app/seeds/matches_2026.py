"""
Seed data for World Cup 2026 matches - Official Schedule
All dates and times converted to UTC
"""

from datetime import datetime, timezone
from app.models import Match, MatchStatus
from app.database import SessionLocal


# World Cup 2026 - Group Stage Matches
# Times converted to UTC based on USA timezones during June
MATCHES_DATA = [
    # Jueves 11 de junio
    ("México", "Sudáfrica", datetime(2026, 6, 11, 17, 0, tzinfo=timezone.utc)),  # 12:00 CDT (UTC-5)
    ("Corea del Sur", "República Checa", datetime(2026, 6, 12, 0, 0, tzinfo=timezone.utc)),  # 19:00 CDT
    
    # Viernes 12 de junio
    ("Canadá", "Bosnia y Herzegovina", datetime(2026, 6, 12, 16, 0, tzinfo=timezone.utc)),  # 12:00 EDT (UTC-4)
    ("Estados Unidos", "Paraguay", datetime(2026, 6, 12, 22, 0, tzinfo=timezone.utc)),  # 18:00 PDT (UTC-7)
    
    # Sábado 13 de junio
    ("Qatar", "Suiza", datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Brasil", "Marruecos", datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Haití", "Escocia", datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)),  # 18:00 EDT
    ("Australia", "Turquía", datetime(2026, 6, 14, 1, 0, tzinfo=timezone.utc)),  # 21:00 PDT
    
    # Domingo 14 de junio
    ("Alemania", "Curazao", datetime(2026, 6, 14, 14, 0, tzinfo=timezone.utc)),  # 10:00 CDT
    ("Países Bajos", "Japón", datetime(2026, 6, 14, 17, 0, tzinfo=timezone.utc)),  # 13:00 CDT
    ("Costa de Marfil", "Ecuador", datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)),  # 16:00 EDT
    ("Suecia", "Túnez", datetime(2026, 6, 14, 23, 0, tzinfo=timezone.utc)),  # 19:00 CDT
    
    # Lunes 15 de junio
    ("España", "Cabo Verde", datetime(2026, 6, 15, 13, 0, tzinfo=timezone.utc)),  # 09:00 EDT
    ("Bélgica", "Egipto", datetime(2026, 6, 15, 17, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Arabia Saudita", "Uruguay", datetime(2026, 6, 15, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Irán", "Nueva Zelanda", datetime(2026, 6, 15, 23, 0, tzinfo=timezone.utc)),  # 18:00 PDT
    
    # Martes 16 de junio
    ("Francia", "Senegal", datetime(2026, 6, 16, 16, 0, tzinfo=timezone.utc)),  # 12:00 EDT
    ("Irak", "Noruega", datetime(2026, 6, 16, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Argentina", "Argelia", datetime(2026, 6, 16, 22, 0, tzinfo=timezone.utc)),  # 18:00 CDT
    ("Austria", "Jordania", datetime(2026, 6, 17, 1, 0, tzinfo=timezone.utc)),  # 21:00 PDT
    
    # Miércoles 17 de junio
    ("Portugal", "RD Congo", datetime(2026, 6, 17, 14, 0, tzinfo=timezone.utc)),  # 10:00 CDT
    ("Inglaterra", "Croacia", datetime(2026, 6, 17, 17, 0, tzinfo=timezone.utc)),  # 13:00 CDT
    ("Ghana", "Panamá", datetime(2026, 6, 17, 20, 0, tzinfo=timezone.utc)),  # 16:00 EDT
    ("Uzbekistán", "Colombia", datetime(2026, 6, 17, 23, 0, tzinfo=timezone.utc)),  # 19:00 CDT
    
    # Jueves 18 de junio
    ("República Checa", "Sudáfrica", datetime(2026, 6, 18, 13, 0, tzinfo=timezone.utc)),  # 09:00 EDT
    ("Suiza", "Bosnia y Herzegovina", datetime(2026, 6, 18, 19, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Canadá", "Qatar", datetime(2026, 6, 18, 22, 0, tzinfo=timezone.utc)),  # 15:00 PDT
    ("México", "Corea del Sur", datetime(2026, 6, 19, 0, 0, tzinfo=timezone.utc)),  # 18:00 CDT
    
    # Viernes 19 de junio
    ("Estados Unidos", "Australia", datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Escocia", "Marruecos", datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Brasil", "Haití", datetime(2026, 6, 19, 22, 0, tzinfo=timezone.utc)),  # 18:00 EDT
    ("Turquía", "Paraguay", datetime(2026, 6, 20, 1, 0, tzinfo=timezone.utc)),  # 21:00 PDT
    
    # Sábado 20 de junio
    ("Países Bajos", "Suecia", datetime(2026, 6, 20, 14, 0, tzinfo=timezone.utc)),  # 10:00 CDT
    ("Alemania", "Costa de Marfil", datetime(2026, 6, 20, 17, 0, tzinfo=timezone.utc)),  # 13:00 EDT
    ("Ecuador", "Curazao", datetime(2026, 6, 20, 21, 0, tzinfo=timezone.utc)),  # 17:00 CDT
    ("Túnez", "Japón", datetime(2026, 6, 21, 1, 0, tzinfo=timezone.utc)),  # 21:00 CDT
    
    # Domingo 21 de junio
    ("España", "Arabia Saudita", datetime(2026, 6, 21, 13, 0, tzinfo=timezone.utc)),  # 09:00 EDT
    ("Bélgica", "Irán", datetime(2026, 6, 21, 16, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Uruguay", "Cabo Verde", datetime(2026, 6, 21, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Nueva Zelanda", "Egipto", datetime(2026, 6, 21, 22, 0, tzinfo=timezone.utc)),  # 18:00 PDT
    
    # Lunes 22 de junio
    ("Argentina", "Austria", datetime(2026, 6, 22, 14, 0, tzinfo=timezone.utc)),  # 10:00 CDT
    ("Francia", "Irak", datetime(2026, 6, 22, 18, 0, tzinfo=timezone.utc)),  # 14:00 EDT
    ("Noruega", "Senegal", datetime(2026, 6, 22, 21, 0, tzinfo=timezone.utc)),  # 17:00 EDT
    ("Jordania", "Argelia", datetime(2026, 6, 23, 0, 0, tzinfo=timezone.utc)),  # 20:00 PDT
    
    # Martes 23 de junio
    ("Portugal", "Uzbekistán", datetime(2026, 6, 23, 14, 0, tzinfo=timezone.utc)),  # 10:00 CDT
    ("Inglaterra", "Ghana", datetime(2026, 6, 23, 17, 0, tzinfo=timezone.utc)),  # 13:00 EDT
    ("Panamá", "Croacia", datetime(2026, 6, 23, 20, 0, tzinfo=timezone.utc)),  # 16:00 EDT
    ("Colombia", "RD Congo", datetime(2026, 6, 23, 23, 0, tzinfo=timezone.utc)),  # 19:00 CDT
    
    # Miércoles 24 de junio
    ("Bosnia y Herzegovina", "Qatar", datetime(2026, 6, 24, 17, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Suiza", "Canadá", datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)),  # 12:00 PDT
    ("Marruecos", "Haití", datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("Escocia", "Brasil", datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)),  # 15:00 EDT
    ("República Checa", "México", datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)),  # 18:00 CDT
    ("Sudáfrica", "Corea del Sur", datetime(2026, 6, 24, 23, 0, tzinfo=timezone.utc)),  # 18:00 CDT
    
    # Jueves 25 de junio
    ("Curazao", "Costa de Marfil", datetime(2026, 6, 25, 17, 0, tzinfo=timezone.utc)),  # 13:00 EDT
    ("Ecuador", "Alemania", datetime(2026, 6, 25, 17, 0, tzinfo=timezone.utc)),  # 13:00 EDT
    ("Túnez", "Países Bajos", datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)),  # 16:00 CDT
    ("Japón", "Suecia", datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)),  # 16:00 CDT
    ("Paraguay", "Australia", datetime(2026, 6, 26, 0, 0, tzinfo=timezone.utc)),  # 19:00 PDT
    ("Turquía", "Estados Unidos", datetime(2026, 6, 26, 2, 0, tzinfo=timezone.utc)),  # 19:00 PDT
    
    # Viernes 26 de junio
    ("Senegal", "Irak", datetime(2026, 6, 26, 16, 0, tzinfo=timezone.utc)),  # 12:00 EDT
    ("Noruega", "Francia", datetime(2026, 6, 26, 16, 0, tzinfo=timezone.utc)),  # 12:00 EDT
    ("Cabo Verde", "Arabia Saudita", datetime(2026, 6, 26, 20, 0, tzinfo=timezone.utc)),  # 17:00 CDT
    ("Uruguay", "España", datetime(2026, 6, 26, 21, 0, tzinfo=timezone.utc)),  # 17:00 CDT
    ("Egipto", "Irán", datetime(2026, 6, 27, 0, 0, tzinfo=timezone.utc)),  # 20:00 PDT
    ("Nueva Zelanda", "Bélgica", datetime(2026, 6, 27, 0, 0, tzinfo=timezone.utc)),  # 20:00 PDT
    
    # Sábado 27 de junio
    ("Panamá", "Inglaterra", datetime(2026, 6, 27, 18, 0, tzinfo=timezone.utc)),  # 14:00 EDT
    ("Croacia", "Ghana", datetime(2026, 6, 27, 18, 0, tzinfo=timezone.utc)),  # 14:00 EDT
    ("RD Congo", "Uzbekistán", datetime(2026, 6, 27, 20, 30, tzinfo=timezone.utc)),  # 16:30 EDT
    ("Colombia", "Portugal", datetime(2026, 6, 27, 20, 30, tzinfo=timezone.utc)),  # 16:30 EDT
    ("Argelia", "Austria", datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)),  # 19:00 CDT
    ("Jordania", "Argentina", datetime(2026, 6, 28, 1, 0, tzinfo=timezone.utc)),  # 19:00 CDT
]


def seed_matches():
    """Insert all World Cup 2026 group stage matches into the database."""
    db = SessionLocal()
    try:
        # Check if matches already exist
        existing_count = db.query(Match).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} matches. Skipping seed.")
            return
        
        matches = []
        for team_a, team_b, match_date in MATCHES_DATA:
            match = Match(
                team_a=team_a,
                team_b=team_b,
                match_date=match_date,
                status=MatchStatus.scheduled,
            )
            matches.append(match)
        
        db.add_all(matches)
        db.commit()
        print(f"Successfully seeded {len(matches)} World Cup 2026 matches!")
    
    except Exception as e:
        db.rollback()
        print(f"Error seeding matches: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_matches()
