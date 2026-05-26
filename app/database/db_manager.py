import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Resolve local SQLite path relative to this script's directory
DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DB_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DB_DIR, "study_buddy.db")

# Read database URL from environment
database_url = os.getenv("DATABASE_URL")

# Resolve PostgreSQL vs. SQLite fallback
if database_url:
    # Heroku / other hostings sometimes use postgres:// instead of postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    db_url = database_url
    connect_args = {}
else:
    db_url = f"sqlite:///{SQLITE_PATH}"
    connect_args = {"check_same_thread": False}

# Initialize engine and session
try:
    engine = create_engine(db_url, connect_args=connect_args)
    # Quick connectivity check
    with engine.connect() as conn:
        pass
except Exception as e:
    print(f"⚠️ Failed to connect to database at {db_url}. Falling back to SQLite local. Error: {e}")
    db_url = f"sqlite:///{SQLITE_PATH}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ====================== SCHEMAS ======================

class UserStats(Base):
    __tablename__ = 'user_stats'
    username = Column(String(50), primary_key=True, default='You')
    points = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    last_study_date = Column(String(20), nullable=True)
    study_sessions_today = Column(Integer, default=0)
    flashcards_reviewed = Column(Integer, default=0)
    perfect_days = Column(Integer, default=0)

class UserBadge(Base):
    __tablename__ = 'user_badges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), default='You', index=True)
    badge_id = Column(String(50), nullable=False)
    earned_at = Column(String(30), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

class Leaderboard(Base):
    __tablename__ = 'leaderboard'
    name = Column(String(50), primary_key=True)
    points = Column(Integer, default=0)

class StudyMaterial(Base):
    __tablename__ = 'study_materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), default='You', index=True)
    material_type = Column(String(50))
    topic = Column(String(100))
    content = Column(Text)
    timestamp = Column(String(30))

class PracticeTest(Base):
    __tablename__ = 'practice_tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), default='You', index=True)
    topic = Column(String(100))
    num_questions = Column(Integer, default=5)
    difficulty = Column(String(30), default='Intermediate')
    content = Column(Text)
    user_answers = Column(Text, default='{}')  # JSON string
    submitted = Column(Boolean, default=False)
    extra_data = Column(Text, default='{}')  # JSON string for dynamic keys like corrects, explanations
    timestamp = Column(String(30))

class Flashcard(Base):
    __tablename__ = 'flashcards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), default='You', index=True)
    count = Column(Integer, default=10)
    focus = Column(String(50), default='Mixed')
    content = Column(Text)
    extra_data = Column(Text, default='{}')  # JSON string for SRS
    timestamp = Column(String(30))


# ====================== INITIALIZER ======================

def init_db():
    """Initializes tables and seeds default leaderboard values"""
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        # Check user stats for 'You'
        you_stats = session.query(UserStats).filter_by(username='You').first()
        if not you_stats:
            session.add(UserStats(
                username='You',
                points=0,
                streak=0,
                last_study_date=None,
                study_sessions_today=0,
                flashcards_reviewed=0,
                perfect_days=0
            ))
            
        # Seed default leaderboard scores if empty
        if session.query(Leaderboard).count() == 0:
            defaults = [
                Leaderboard(name="Alex", points=1250),
                Leaderboard(name="Sam", points=980),
                Leaderboard(name="Jordan", points=750),
                Leaderboard(name="Taylor", points=620),
                Leaderboard(name="You", points=0)
            ]
            session.add_all(defaults)
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error seeding DB: {e}")
    finally:
        session.close()


# ====================== DATA ACCESS FUNCTIONS ======================

def get_gamification_state(username='You'):
    """Loads gamification stats, badges, and leaderboard from DB"""
    session = SessionLocal()
    try:
        stats = session.query(UserStats).filter_by(username=username).first()
        if not stats:
            stats = UserStats(username=username)
            session.add(stats)
            session.commit()
            
        badges = [b.badge_id for b in session.query(UserBadge).filter_by(username=username).all()]
        
        # Load and sync leaderboard
        leaderboard_rows = session.query(Leaderboard).order_by(Leaderboard.points.desc()).all()
        you_in_leaderboard = False
        leaderboard = []
        for row in leaderboard_rows:
            points = stats.points if row.name == username else row.points
            leaderboard.append({"name": row.name, "points": points})
            if row.name == username:
                you_in_leaderboard = True
                
        if not you_in_leaderboard:
            leaderboard.append({"name": username, "points": stats.points})
            
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        
        # Parse last_study_date string to date object
        last_date = None
        if stats.last_study_date:
            try:
                last_date = datetime.strptime(stats.last_study_date, "%Y-%m-%d").date()
            except ValueError:
                pass

        return {
            "points": stats.points,
            "badges": badges,
            "streak": stats.streak,
            "last_study_date": last_date,
            "study_sessions_today": stats.study_sessions_today,
            "flashcards_reviewed": stats.flashcards_reviewed,
            "perfect_days": stats.perfect_days,
            "leaderboard": leaderboard
        }
    finally:
        session.close()

def save_gamification_state(gamification, username='You'):
    """Saves gamification stats, badges, and leaderboard values to DB"""
    session = SessionLocal()
    try:
        stats = session.query(UserStats).filter_by(username=username).first()
        if not stats:
            stats = UserStats(username=username)
            session.add(stats)
            
        stats.points = gamification["points"]
        stats.streak = gamification["streak"]
        stats.last_study_date = gamification["last_study_date"].strftime("%Y-%m-%d") if gamification["last_study_date"] else None
        stats.study_sessions_today = gamification["study_sessions_today"]
        stats.flashcards_reviewed = gamification["flashcards_reviewed"]
        stats.perfect_days = gamification["perfect_days"]
        
        # Save new badges
        existing_badges = {b.badge_id for b in session.query(UserBadge).filter_by(username=username).all()}
        for badge_id in gamification["badges"]:
            if badge_id not in existing_badges:
                session.add(UserBadge(username=username, badge_id=badge_id))
                
        # Sync leaderboard 'You' score
        you_row = session.query(Leaderboard).filter_by(name=username).first()
        if you_row:
            you_row.points = gamification["points"]
        else:
            session.add(Leaderboard(name=username, points=gamification["points"]))
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving gamification state: {e}")
    finally:
        session.close()

def reset_stats(username='You'):
    """Resets user stats and leaderboard 'You' points back to zero in the database"""
    session = SessionLocal()
    try:
        stats = session.query(UserStats).filter_by(username=username).first()
        if stats:
            stats.points = 0
            stats.streak = 0
            stats.last_study_date = None
            stats.study_sessions_today = 0
            stats.flashcards_reviewed = 0
            stats.perfect_days = 0
            
        # Delete user's badges
        session.query(UserBadge).filter_by(username=username).delete()
        
        # Reset user's points on leaderboard
        you_row = session.query(Leaderboard).filter_by(name=username).first()
        if you_row:
            you_row.points = 0
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error resetting stats: {e}")
    finally:
        session.close()

# --- STUDY MATERIALS ---

def get_study_materials(username='You'):
    """Retrieves all generated study materials for a user"""
    session = SessionLocal()
    try:
        rows = session.query(StudyMaterial).filter_by(username=username).order_by(StudyMaterial.id.asc()).all()
        return [{
            "timestamp": r.timestamp,
            "type": r.material_type,
            "content": r.content
        } for r in rows]
    finally:
        session.close()

def save_study_material(username, material_type, topic, content):
    """Saves a new study material set to the database"""
    session = SessionLocal()
    try:
        mat = StudyMaterial(
            username=username,
            material_type=material_type,
            topic=topic,
            content=content,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        session.add(mat)
        session.commit()
    finally:
        session.close()

# --- PRACTICE TESTS ---

def get_practice_tests(username='You'):
    """Retrieves all generated practice tests for a user"""
    session = SessionLocal()
    try:
        rows = session.query(PracticeTest).filter_by(username=username).order_by(PracticeTest.id.asc()).all()
        tests = []
        for r in rows:
            # Reconstruct the structure used in Streamlit session state
            test_dict = {
                "timestamp": r.timestamp,
                "num_questions": r.num_questions,
                "difficulty": r.difficulty,
                "content": r.content,
                "submitted": r.submitted,
                "user_answers": json.loads(r.user_answers),
            }
            # Unpack dynamic items stored in extra_data
            extra = json.loads(r.extra_data)
            test_dict.update(extra)
            tests.append(test_dict)
        return tests
    finally:
        session.close()

def save_practice_test(username, topic, test_data):
    """Saves or updates a practice test in the database"""
    session = SessionLocal()
    try:
        # Check if this test already exists by timestamp
        existing = session.query(PracticeTest).filter_by(
            username=username, 
            timestamp=test_data["timestamp"]
        ).first()
        
        # Prepare dynamic fields for extra_data (avoiding duplicate standard columns)
        extra_keys = {}
        for k, v in test_data.items():
            if k not in ["timestamp", "num_questions", "difficulty", "content", "submitted", "user_answers"]:
                extra_keys[k] = v
                
        user_answers_str = json.dumps(test_data.get("user_answers", {}))
        extra_data_str = json.dumps(extra_keys)
        
        if existing:
            existing.submitted = test_data.get("submitted", False)
            existing.user_answers = user_answers_str
            existing.extra_data = extra_data_str
        else:
            new_test = PracticeTest(
                username=username,
                topic=topic,
                num_questions=test_data.get("num_questions", 5),
                difficulty=test_data.get("difficulty", "Intermediate"),
                content=test_data["content"],
                user_answers=user_answers_str,
                submitted=test_data.get("submitted", False),
                extra_data=extra_data_str,
                timestamp=test_data["timestamp"]
            )
            session.add(new_test)
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving practice test: {e}")
    finally:
        session.close()

# --- FLASHCARDS ---

def get_flashcards(username='You'):
    """Retrieves all generated flashcards for a user"""
    session = SessionLocal()
    try:
        rows = session.query(Flashcard).filter_by(username=username).order_by(Flashcard.id.asc()).all()
        return [{
            "timestamp": r.timestamp,
            "count": r.count,
            "focus": r.focus,
            "content": r.content,
            "srs_data": json.loads(r.extra_data)
        } for r in rows]
    finally:
        session.close()

def save_flashcard(username, topic, card_set_data):
    """Saves or updates a set of generated flashcards in the database"""
    session = SessionLocal()
    try:
        # Check if already exists by timestamp
        existing = session.query(Flashcard).filter_by(
            username=username, 
            timestamp=card_set_data["timestamp"]
        ).first()
        
        extra_data_str = json.dumps(card_set_data.get("srs_data", {}))
        
        if existing:
            existing.extra_data = extra_data_str
        else:
            new_set = Flashcard(
                username=username,
                count=card_set_data.get("count", 10),
                focus=card_set_data.get("focus", "Mixed"),
                content=card_set_data["content"],
                extra_data=extra_data_str,
                timestamp=card_set_data["timestamp"]
            )
            session.add(new_set)
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving flashcards: {e}")
    finally:
        session.close()

# --- CLEANUP ---

def clear_generated_content(username='You'):
    """Deletes all generated materials, quizzes, and flashcards for a user"""
    session = SessionLocal()
    try:
        session.query(StudyMaterial).filter_by(username=username).delete()
        session.query(PracticeTest).filter_by(username=username).delete()
        session.query(Flashcard).filter_by(username=username).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error clearing generated content: {e}")
    finally:
        session.close()
