import json
import sqlite3
import os
from datetime import datetime, time, timedelta
import logging

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, 'planner.db')

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            # Log the full path of the database file
            self.logger.info(
                f"Attempting to connect to database at: {self.db_path}")

            # Initialize the connection
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            # Initialize the database structure
            self.initialize_db()

            self.logger.info(
                "Successfully connected to the database and initialized structure.")
        except sqlite3.OperationalError as e:
            self.logger.error(f"Failed to open database: {e}")
            self.logger.info(f"Current working directory: {os.getcwd()}")
            self.logger.info(f"Directory contents: {os.listdir(os.path.dirname(self.db_path))}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def initialize_db(self):
        self.cursor.executescript('''
            -- Projects table
            CREATE TABLE IF NOT EXISTS Projects (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              description TEXT,
              status TEXT,
              priority INTEGER,
              due_date DATE,
              estimated_time INTEGER,
              xp_reward INTEGER
            );

            -- Tasks table
            CREATE TABLE IF NOT EXISTS Tasks (
              id INTEGER PRIMARY KEY,
              project_id INTEGER,
              name TEXT NOT NULL,
              description TEXT,
              status TEXT,
              priority INTEGER,
              estimated_time INTEGER,
              xp_reward INTEGER,
              FOREIGN KEY (project_id) REFERENCES Projects (id)
            );

            -- ProjectSkills table
            CREATE TABLE IF NOT EXISTS ProjectSkills (
              project_id INTEGER,
              skill_name TEXT,
              xp_multiplier FLOAT,
              FOREIGN KEY (project_id) REFERENCES Projects (id)
            );

            -- DailySchedule table
            CREATE TABLE IF NOT EXISTS DailySchedule (
              id INTEGER PRIMARY KEY,
              date DATE UNIQUE,
              wake_time TIME,
              sleep_time TIME
            );

            -- ScheduleItems table
            CREATE TABLE IF NOT EXISTS ScheduleItems (
              id INTEGER PRIMARY KEY,
              schedule_id INTEGER,
              name TEXT,
              start_time TIME,
              end_time TIME,
              type TEXT,
              project_id INTEGER NULL,
              task_id INTEGER NULL,
              completed BOOLEAN DEFAULT FALSE,
              xp_gained INTEGER DEFAULT 0,
              FOREIGN KEY (schedule_id) REFERENCES DailySchedule(id),
              FOREIGN KEY (project_id) REFERENCES Projects(id),
              FOREIGN KEY (task_id) REFERENCES Tasks(id)
            );

            -- XPLog table
            CREATE TABLE IF NOT EXISTS XPLog (
              id INTEGER PRIMARY KEY,
              date DATE,
              player_name TEXT,
              skill_name TEXT,
              xp_gained INTEGER,
              source TEXT
            );

            -- Goals table
            CREATE TABLE IF NOT EXISTS Goals (
              id INTEGER PRIMARY KEY,
              description TEXT NOT NULL,
              start_date DATE,
              end_date DATE,
              status TEXT
            );
        ''')
        self.conn.commit()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def load_player_data(self):
        with open(os.path.join(self.data_dir, 'player_data.json'), 'r') as f:
            return json.load(f)

    def save_player_data(self, player_data):
        with open(os.path.join(self.data_dir, 'player_data.json'), 'w') as f:
            json.dump(player_data, f, indent=2)

    def load_schedule_config(self):
        with open(os.path.join(self.data_dir, 'schedule_config.json'), 'r') as f:
            return json.load(f)

    def add_project(self, name, description, priority, due_date, estimated_time, xp_reward):
        self.cursor.execute('''
            INSERT INTO Projects (name, description, status, priority, due_date, estimated_time, xp_reward)
            VALUES (?, ?, 'Not Started', ?, ?, ?, ?)
        ''', (name, description, priority, due_date, estimated_time, xp_reward))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_task(self, project_id, name, description, priority, estimated_time, xp_reward):
        self.cursor.execute('''
            INSERT INTO Tasks (project_id, name, description, status, priority, estimated_time, xp_reward)
            VALUES (?, ?, ?, 'Not Started', ?, ?, ?)
        ''', (project_id, name, description, priority, estimated_time, xp_reward))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_projects_and_tasks(self):
        self.cursor.execute('''
            SELECT p.id, p.name, p.description, p.status, p.priority, p.due_date, p.estimated_time, p.xp_reward,
                   t.id, t.name, t.description, t.status, t.priority, t.estimated_time, t.xp_reward
            FROM Projects p
            LEFT JOIN Tasks t ON p.id = t.project_id
            ORDER BY p.priority DESC, p.due_date, t.priority DESC
        ''')
        return self.cursor.fetchall()

    def generate_daily_schedule(self, date):
        config = self.load_schedule_config()
        wake_time = datetime.strptime(config['wake_time'], '%H:%M').time()
        sleep_time = datetime.strptime(config['sleep_time'], '%H:%M').time()

        self.cursor.execute('''
            INSERT OR REPLACE INTO DailySchedule (date, wake_time, sleep_time)
            VALUES (?, ?, ?)
        ''', (date, wake_time, sleep_time))
        schedule_id = self.cursor.lastrowid

        wake_datetime = datetime.combine(date, wake_time)
        for block in config['time_blocks']:
            if block['start'].startswith('+'):
                start = wake_datetime + timedelta(hours=int(block['start'][1:].split(':')[0]),
                                                  minutes=int(block['start'][1:].split(':')[1]))
            elif block['start'].startswith('-'):
                sleep_datetime = datetime.combine(date, sleep_time)
                start = sleep_datetime - timedelta(hours=int(block['start'][1:].split(':')[0]),
                                                   minutes=int(block['start'][1:].split(':')[1]))
            else:
                start = datetime.combine(date, datetime.strptime(
                    block['start'], '%H:%M').time())

            duration = timedelta(hours=int(block['duration'].split(':')[0]),
                                 minutes=int(block['duration'].split(':')[1]))
            end = start + duration

            self.cursor.execute('''
                INSERT INTO ScheduleItems (schedule_id, name, start_time, end_time, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (schedule_id, block['name'], start.time(), end.time(), block['type']))

        self.conn.commit()

    def get_daily_schedule(self, date):
        self.cursor.execute('''
            SELECT s.id, s.wake_time, s.sleep_time, 
                   i.name, i.start_time, i.end_time, i.type, i.completed, i.project_id, i.task_id
            FROM DailySchedule s
            LEFT JOIN ScheduleItems i ON s.id = i.schedule_id
            WHERE s.date = ?
            ORDER BY i.start_time
        ''', (date,))
        return self.cursor.fetchall()

    def update_schedule_item(self, item_id, completed, xp_gained=0):
        self.cursor.execute('''
            UPDATE ScheduleItems
            SET completed = ?, xp_gained = ?
            WHERE id = ?
        ''', (completed, xp_gained, item_id))
        self.conn.commit()

    def log_xp_gain(self, player_name, skill_name, xp_gained, source):
        self.cursor.execute('''
            INSERT INTO XPLog (date, player_name, skill_name, xp_gained, source)
            VALUES (DATE('now'), ?, ?, ?, ?)
        ''', (player_name, skill_name, xp_gained, source))
        self.conn.commit()

    def add_goal(self, description, start_date, end_date):
        self.cursor.execute('''
            INSERT INTO Goals (description, start_date, end_date, status)
            VALUES (?, ?, ?, 'In Progress')
        ''', (description, start_date, end_date))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_goals(self, status=None):
        if status:
            self.cursor.execute(
                'SELECT * FROM Goals WHERE status = ?', (status,))
        else:
            self.cursor.execute('SELECT * FROM Goals')
        return self.cursor.fetchall()

    def update_goal_status(self, goal_id, status):
        self.cursor.execute(
            'UPDATE Goals SET status = ? WHERE id = ?', (status, goal_id))
        self.conn.commit()

    def get_routine(self, routine_name):
        routine_path = os.path.join(
            self.data_dir, 'routines', f'{routine_name}.md')
        if os.path.exists(routine_path):
            with open(routine_path, 'r') as f:
                return f.read()
        else:
            return None

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            self.logger.info("Database connection closedd.")